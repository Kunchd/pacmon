import math

# Job class
# Machine class
# Cell class - applies a scheduler, keeps a scheduler queue

class Job:
  def __init__(self, id:int, mem:float, cores:int, compute:float):
    self.id = id
    self.mem = mem
    self.cores = cores
    self.compute = compute # amount of compute left to do

  def __repr__(self):
    return f"Job {self.id}: compute left={self.compute}"

class Machine:
  def __init__(self, mem, cores):
     self.jobs = [] # list of jobs currently running on the machine
     self.mem = mem
     self.mem_free = mem
     self.cores = cores
     self.cores_free = cores

  def add_job(self, job):
    self.jobs.append(job)
    self.mem_free -= job.mem
    self.cores_free -= job.cores

  def forward(self): # forward pass
    decr = self.cores / (self.cores - self.cores_free)

    for i in reversed(range(len(self.jobs))):
      # decrement job compute by decr
      # if job compute <= 0, take it out of the jobs list
      self.jobs[i].compute -= decr
      if self.jobs[i].compute <= 0:
        self.cores_free += self.jobs[i].cores
        self.mem_free += self.jobs[i].mem
        self.jobs.pop(i)
        # print("deleted job")

class Cell:
  """dump wrapper of scheduler"""
  def __init__(self, sched):
    self.sched = sched # scheduler type
    self.sched_queue = [] # list of jobs that haven't been assigned to machine
    self.machines = []

  def add_machine(self, machine):
    self.machines.append(machine)

  def add_job(self, job):
    self.sched_queue.append(job)

  def forward(self):
    # run scheduler - assign things to machines
    self.sched.forward(self.machines, self.sched_queue)





