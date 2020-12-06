import subprocess

numberOfProcesses = []
count_of_thermometers = int(input('Write down the current amount of thermometers:'))

for i in range(count_of_thermometers):
    p = subprocess.Popen(['/home/user/workspace/SuitHome/01/bin/python', 'thermometers.py'])
    numberOfProcesses.append(p)

door_p = subprocess.Popen(['/home/user/workspace/SuitHome/01/bin/python', 'door.py'])
numberOfProcesses.append(door_p)

common_subscriber_p = subprocess.Popen(['/home/user/workspace/SuitHome/01/bin/python', 'common_subscriber.py',
                                        str(count_of_thermometers)])
numberOfProcesses.append(common_subscriber_p)

for j in numberOfProcesses:
    j.wait()