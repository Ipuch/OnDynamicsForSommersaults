import os, shutil

# from Comparison import ComparisonAnalysis, ComparisonParameters
import pickle
import numpy as np
from multiprocessing import Pool, cpu_count
from datetime import date
import smtplib, ssl
import miller_run
from bioptim import OdeSolver

Date = date.today()
Date = Date.strftime("%d-%m-%y")

out_path_raw = "../OnDynamicsForSommersaults_results/raw_" + Date
os.mkdir(out_path_raw)
out_path_secondary_variables = "../OnDynamicsForSommersaults_results/secondary_variables"

cpu_number = cpu_count()

# dynamics_types = ["explicit", "root_explicit", "implicit", "root_implicit"]
# ode_solver = [OdeSolver.RK4, OdeSolver.RK4, OdeSolver.RK2, OdeSolver.RK2]

model_str = "Model_JeCh_15DoFs.bioMod"
n_shooting = (125, 25)
duration = 1.545
nstep = 5

n_threads = 4  # Should be 8
ode_solver = [OdeSolver.RK4, OdeSolver.RK4]
dynamics_types = ["explicit", "root_explicit"]


def generate_calls(
    n,
    Date,
    n_shooting: tuple,
    duration: float,
    dynamics_types: list,
    ode_solver: list,
    nstep: int,
    n_threads: int,
    out_path_raw: str,
    model_str: str,
):
    calls = []
    for i, dynamics_type in enumerate(dynamics_types):
        for i_rand in range(n):  # Should be 100
            calls.append(
                [
                    Date,
                    i_rand,
                    n_shooting,
                    duration,
                    dynamics_type,
                    ode_solver[i],
                    nstep,
                    n_threads,
                    out_path_raw,
                    model_str,
                ]
            )
    return calls


calls = generate_calls(
    100, Date, n_shooting, duration, dynamics_types, ode_solver, nstep, n_threads, out_path_raw, model_str
)

pool_number = int(cpu_number / n_threads)
with Pool(pool_number) as p:  # should be 4
    p.map(miller_run.main, calls)

# Second call
n_threads = 1  # Should be 8
ode_solver = [OdeSolver.RK2, OdeSolver.RK2]
dynamics_types = ["implicit", "root_implicit"]

calls = generate_calls(
    100, Date, n_shooting, duration, dynamics_types, ode_solver, nstep, n_threads, out_path_raw, model_str
)
pool_number = int(cpu_number / n_threads)
with Pool(pool_number) as p:  # should be 4
    p.map(miller_run.main, calls)
