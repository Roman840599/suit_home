import subprocess
import sys
import argparse


python_interpreter = sys.executable
numberOfProcesses = []


parser = argparse.ArgumentParser()
parser.add_argument('count_of_thermometers', type=int, help='Input desired count of thermometers you want to run')
args = parser.parse_args()
count_of_thermometers = args.count_of_thermometers
if count_of_thermometers <= 0:
    parser.error("count of thermometers must be a positive argument")


for i in range(count_of_thermometers):
    p = subprocess.Popen([python_interpreter, 'thermometers.py'])
    numberOfProcesses.append(p)


for j in numberOfProcesses:
    j.wait()