from infra import *
from eval import *
from scheds import *

from contextlib import redirect_stdout

def get_tot_lat(fname):
  with open(fname, "r") as f:
    tot_lat = 0
    for row in f:
      row = row.split(" ")
      if len(row) != 3 or not row[0].startswith("Latency"):
        print("error line", row)
        continue
      tot_lat += int(row[-1])

  return tot_lat


# NAMING CONVENTION:
# {workload type}-load-{load}-{total_steps}

loads = [250000]
for load in loads:
    print("\nLoad", load)
    for _ in range(10):
        workload_type = "unif"
        sched = "naive"
        # note: these are strings just so naming is easier
        load = str(load)
        total_steps = "1000"
        mach_config = "./config/mach-100.txt"

        fname = f"{workload_type}-load-{load}-{total_steps}-{sched}"
        full_fname = f"./data/{fname}.txt"

        with open(full_fname, "w+") as f:
            with redirect_stdout(f):
                run_test(
                    scheduler=NaiveScheduler,
                    load=int(float(load)),
                    machine_config=mach_config,
                    total_steps=int(float(total_steps))
                )

        # print(full_fname)
        print(get_tot_lat(full_fname), end=" ")