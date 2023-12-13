# This file contains implementations of various schedulers
from abc import ABC, abstractmethod

class Scheduler(ABC):
  @abstractmethod
  def forward(machines, sched_queue):
    pass

class NaiveScheduler(Scheduler):
  def forward(machines, sched_queue):
    # Naive scheduler just picks the first feasible machine
    while len(sched_queue) > 0:
      # Looking at job at front of scheduler queue
      job = sched_queue[0]
      for i, machine in enumerate(machines):
        # If machine can take the job, do it
        if machine.can_do_job(job):
          machine.add_job(job)
          # remove job from queue
          sched_queue.pop(0)
          break
      else:
        return # blocked

