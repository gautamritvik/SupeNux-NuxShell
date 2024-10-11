import os
import subprocess
import time
import readline
import cmd
import psutil
import platform
from datetime import datetime


# Exit
def exit_terminal():
    exit()
# System information
def system_info():
    print(f"\nSystem Information:\n")
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}\n")
# Memory information
def memory_info():
    print(f"\nMemory Information:\n")
    svmem = psutil.virtual_memory()
    print(f"Total: {svmem.total}")
    print(f"Available: {svmem.available}")
    print(f"Used: {svmem.used}")
    print(f"Percentage: {svmem.percent}\n")



# Command workflow
commands = {
    "exit": exit_terminal,
    "system -info": system_info,
    "memory -info": memory_info
}

while True:
    user_cmd = input("SupeNux NuxShell @ /SupeNuxPC/DRV1/TerminalCalls/NuxShell --- $ >>> ")
    if user_cmd in commands:
        commands[user_cmd]()
    else:
        os.system(user_cmd)