from .queue import Queue
from .job import Job
from .utils import executionCode
from typing import Dict, Type, Union, Tuple, Callable
from time import sleep
import importlib
import subprocess
import sys, json, os
from bson import json_util

def run_with_executable(function_name, executable=None, args=[], kwargs={}, stdout=None, modulePaths=[]):
  if executable is None:
    executable = sys.executable

  if modulePaths is None:
    modulePaths = []

  data = {"function_name": function_name, "args": args, "kwargs": kwargs, "stdout": stdout, "modules": modulePaths + [os.getcwd(),]}
  result = subprocess.run([executable, "-c", executionCode], stdout=subprocess.PIPE, input=str.encode(json.dumps(data, default=json_util.default)))
  out = result.stdout.decode().split("\n")
  if len(out) > 0:
    output = json.loads(out[-1], object_hook=json_util.object_hook)
    return output

class Worker:

  def __init__(self, queues: Union[Tuple[Queue,...], Type[Queue]], channel: Union[Tuple[str,...], str]=None, heart_beat: int = 1, verbosity: str = "error", logger: Union[str, Callable] = None, executables: Dict = None, logFile: str = None, modulePaths=[]) -> None:
    
    if isinstance(queues, tuple) or isinstance(queues, list):
      self.queues = queues
    elif isinstance(queues, Queue):
      self.queues = tuple([queues])

    if isinstance(channel, tuple) or isinstance(channel, list):
      self._channels = channel
    elif isinstance(channel, str):
      self._channels = [channel]
    else:
      self._channels = None

    self._working = False
    self._heart_beat = heart_beat
    self._running = False

    self._verbosity = verbosity
    self.setLogger(logger)

    self.logFile = None
    if not logFile is None:
      self.logFile = logFile

    self.modulePaths = modulePaths

    if not executables is None and isinstance(executables, dict):
      self.executables = executables
    else:
      self.executables = {}
    
  def setLogger(self, logger: Union[str, Callable]):
    if callable(logger):
      self._logger = logger
    elif isinstance(logger, str):
      callback = str(logger)
      if str(callback).__contains__("."):
        mod_name, func_name = callback.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        self._logger = func
      elif callback in globals():
        func = globals()[callback]
        self._logger = func
    else:
      self._logger = None

  def setVerbosity(self, verbosity: str):
    self.verbosity = verbosity

  def start(self):
    self._running = True
    self._run()

  def stop(self):
    self._running = False

  def _work(self):
    self._working = True
    job: Type[Job] = None

    for queue in self.queues:
      if self._channels is None:
        job = queue.dequeue()
        if not job is None:
          break
      else:
        for channel in self._channels:
          job = queue.dequeue(channel)
          if not job is None:
            break
        if not job is None:
          break

    if not job is None:
      self._run_job(job)
      self._working = False
    else:
      self._working = False

  def _run_job(self, job: Type[Job]):
    payload = job.payload
    job.setVerbosity(self._verbosity)
    job.setLogger(self._logger)
    try:
      if not payload is None:
        callback = payload.get("function_name")

        if not callback is None:
          args = payload.get("args", [])
          kwargs = payload.get("kwargs", {})
          executable = None
          channel = job.channel

          if not channel is None:
            if channel in self.executables:
              executable = self.executables[channel]

          output = run_with_executable(callback, args=args, kwargs=kwargs, executable=executable, stdout=self.logFile, modulePaths=self.modulePaths)

          if not output is None:
            if "result" in output:
              job.complete(output["result"])
            if "error" in output:
              print(output["error"])
              job.error(output["error"])
        else:
          job.error(f"Error: no callback funtion specified for job!")
          print(f"Error: no callback funtion specified for job!")

    except Exception as ex:
      job.error(f"Error: {ex}")
      print(f"Error: {ex}")

  def _run(self):
    while True:
      if not self._running:
        break

      if not self._working:
        self._work()

      sleep(self._heart_beat)