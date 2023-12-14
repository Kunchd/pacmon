# This file contains implementations of various schedulers
import random

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


class EPVMScheduler(Scheduler):
  def forward(machines, sched_queue):
    # E-Mosix implementation based on https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=877834

    def cost(num_machines, pos_util, neg_util):
      return num_machines ** pos_util - num_machines ** neg_util
    
    # Assignment logic
    while len(sched_queue) > 0:
      min_cost = float('inf')
      machine_pick = -1
      job = sched_queue[0]

      for i, machine in enumerate(machines):
        if machine.can_do_job(job):
          existing_util = (machine.cores - machine.cores_free) / machine.cores
          job_util = job.cores / machine.cores
          marginal_cost = cost(len(machines), existing_util + job_util, existing_util)
          if marginal_cost < min_cost:
            machine_pick = i
            min_cost = marginal_cost
      
      if machine_pick < 0:
        break # block on jobs that can't be fit

      machines[machine_pick].add_job(job)
      sched_queue.pop(0)

    # Reassignment logic
    for machine in machines:
      for i, job in enumerate(machine.jobs):
        existing_util = (machine.cores - machine.cores_free) / machine.cores
        job_util = job.cores / machine.cores
        current_cost = cost(len(machines), existing_util, existing_util - job_util)

        # pick from a random subset of machines
        samples = random.sample(machines, int(0.25 * len(machines)))
        min_cost = current_cost
        machine_pick = -1
        for j, machine2 in enumerate(samples):
          if machine2.can_do_job(job):
            m2_existing_util = (machine2.cores - machine2.cores_free) / machine2.cores
            marginal_cost = cost(len(machines), m2_existing_util + job_util, m2_existing_util)
            
            if marginal_cost < min_cost:
              machine_pick = j
              min_cost = marginal_cost
        
        # transfer if necessary
        if machine_pick >= 0:
          machine.remove_job(i)
          machines[machine_pick].add_job(job)
