import numpy as np
import sys

from infra import *

# input to run a test:
# - distribution of machines (small, medium, large)
# - distribution of jobs (small, large)
# - type of workload (uniform, bursty)
# - scheduler type

MACHINE_DISTR = {
  "small": 50,
  "medium": 30,
  "large": 20
}

JOB_DISTR = {
  "small": 80,
  "large": 20
}

TOTAL_STEPS = 100_000

def run_test(
  load=100_000, # number of total jobs
  machine_distr=MACHINE_DISTR,
  job_distr=JOB_DISTR,
  workload_type="uniform", # uniform, bursty
  scheduler=None,
  total_steps=TOTAL_STEPS,
  num_machines=100
):
  cell = Cell(scheduler)
  # Initialize machines
  for i in range(num_machines):
    probab = np.random.uniform(0, 100)
    if probab <= machine_distr["small"]:
      cell.add_machine(Machine(mem=6, cores=4))
    elif probab <= machine_distr["small"] + machine_distr["medium"]:
      cell.add_machine(Machine(mem=64, cores=10))
    elif probab <= 100:
      cell.add_machine(Machine(mem=1000, cores=32))
    else:
      raise Exception("Invalid machine type")


  num_jobs = np.zeros(total_steps, dtype=int)
  if workload_type == "uniform":
    if load <= total_steps:
      # give out a job every total_steps
      intv = total_steps // load
      num_jobs[::intv] = 1
    else:
      num_jobs[:] = load // total_steps
  # TODO: bursty case

  for i in range(total_steps):
    # Classify each job at current timestep
    for j in range(num_jobs[i]):
      prob = np.random.uniform(0, 100)
      if prob <= job_distr["small"]:
        cell.queue_job(Job(f"{i}-{j}", mem=2, cores=1, compute=np.random.randint(1, 11), start=i))
      elif prob <= 100:
        cell.queue_job(Job(f"{i}-{j}", mem=64, cores=10, compute=np.random.randint(20, 41), start=i))
      else:
        raise Exception("Invalid job type")

    # Run scheduler to actually assign jobs to machines
    cell.forward(i)

  # check if we have unfinished jobs at the end - if so, keep running to finish them
  print("Unfinished jobs, keep running", file=sys.stderr)
  while cell.is_inactive():
    cell.forward(i)
    i += 1

