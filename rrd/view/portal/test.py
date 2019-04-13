import os

active_proc = os.popen('top -bi -n 1 -d 0.1').read().encode().decode().split('\n\n')[1].split('\n')
active_proc_header = active_proc[0]
active_proc_list = active_proc[1:-1]
active_proc_num = len(active_proc_list)

for single_proc in active_proc_list:
    single_proc_prop = single_proc.split()
    Pid = single_proc_prop[0]
    User = single_proc_prop[1]
    cpu_usage = single_proc_prop[8]
    mem_usage = single_proc_prop[9]
    name = single_proc_prop[11]
    print(single_proc_prop)
    print(Pid, User, cpu_usage, mem_usage, name)