import numpy as np
import sys

from infra import *

def dprint(msg):
  print(msg, file=sys.stderr)

# input to run a test:
# - distribution of machines (small, medium, large)
# - distribution of jobs (small, large)
# - type of workload (uniform, bursty)
# - scheduler type

JOB_DISTR = {
  "small": 90,
  "large": 10
}

TOTAL_STEPS = 100_000

def run_test(
  load:int =100_000, # number of total jobs
  machine_config=None,
  job_distr=JOB_DISTR,
  workload_type:str ="uniform", # uniform, bursty
  scheduler=None,
  total_steps:int =TOTAL_STEPS,
  num_machines:int =100
):
  # dprint(f"Total steps {total_steps}")
  # dprint(f"Load {load}")
  # dprint(f"Machines {num_machines}")

  cell = Cell(scheduler)
  # Initialize machines
  with open(machine_config, "r") as f:
    for row in f:
      row = row.strip()
      if row == "small":
        cell.add_machine(Machine(mem=6, cores=4))
      elif row == "medium":
        cell.add_machine(Machine(mem=64, cores=16))
      elif row == "large":
        cell.add_machine(Machine(mem=1000, cores=32))
      else:
        raise Exception(f"invalid machine type: '{row}'")

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
        cell.queue_job(Job(f"{i}-{j}", mem=1, cores=1, compute=np.random.randint(1, 11), start=i))
      else:
        cell.queue_job(Job(f"{i}-{j}", mem=64, cores=10, compute=np.random.randint(20, 41), start=i))

    # Run scheduler to actually assign jobs to machines
    cell.forward(i)

  # check if we have unfinished jobs at the end - if so, keep running to finish them
  # print("Unfinished jobs, keep running", file=sys.stderr)
  while cell.is_inactive():
    cell.forward(i)
    i += 1

