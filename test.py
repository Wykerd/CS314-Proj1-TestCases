import sys
import difflib
import subprocess
import os

def compare_files(file_path_1, file_path_2):
    with open(file_path_1, 'r') as file_1, open(file_path_2, 'r') as file_2:
        file_1_contents = file_1.read()
        file_2_contents = file_2.read()
        if file_1_contents == file_2_contents:
            return True
        else:
            return False
        

def display_file_diff(file_path_1, file_path_2):
    with open(file_path_1, 'r') as file_1, open(file_path_2, 'r') as file_2:
        file_1_contents = file_1.readlines()
        file_2_contents = file_2.readlines()

    diff = difflib.unified_diff(file_1_contents, file_2_contents)

    print(''.join(diff))

def execute_command_in_directory(command, directory):
    print(f'$ {command}')
    output = subprocess.run(command, shell=True, cwd=directory, capture_output=True, text=True)
    return output

if __name__ == '__main__':
    root_dir_raw = sys.argv[1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(root_dir_raw)

    print(f'Running tests in project root: {root_dir}')

    arr = {chr(i): chr(i) for i in range(ord('A'), ord('I')+1)}
    arr['A'] = "Priority Scheduler 1 - Given Test Case"
    arr['B'] = "Priority Scheduler 2 - Multiple Processes Same Priority"
    arr['C'] = "Priority Scheduler 3 - Duplicate Resource Names"
    arr['D'] = "Priority Scheduler 4 - Long Boy"
    arr['E'] = "FCFS 1 - Given Test Case"
    arr['F'] = "FCFS 2 - Long Test Case"
    arr['G'] = 'Deadlock 1 (Priority Scheduler) - Multiple Deadlocks'
    arr['H'] = "Priority Scheduler 5 - Longer Boy"
    arr['I'] = "FCFS 3 - Longer Test Case"
    arr['J'] = 'Deadlock 2 (Priority Scheduler) - Two Proccesses Locked'

    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

    execute_command_in_directory('make clean', root_dir)
    execute_command_in_directory('make', root_dir)

    passed = 0
    total = 0

    for i in arr:
        is_priority = arr[i].startswith("Priority") or arr[i].startswith("Deadlock")
        process1_path = os.path.abspath(f'{script_dir}/TestIn/process{i}1.list')
        process2_path = os.path.abspath(f'{script_dir}/TestIn/process{i}2.list')
        arg_3 = '0' if is_priority else '2'

        execute_command_in_directory(f'./schedule_processes {process1_path} {process2_path} {arg_3} 2', root_dir)

        log_file_path = os.path.abspath(f'{root_dir}/scheduler.log')
        expected_log_file_path = os.path.abspath(f'{script_dir}/TestOut/{i}.log')

        if compare_files(log_file_path, expected_log_file_path): 
            print(f'{GREEN}[PASSED]{END} {arr[i]}')    
            passed += 1
        else: 
            print(f'{RED}[FAILED]{END} {arr[i]}')
            print(f'{RED}Differences:{END} \n')
            display_file_diff(log_file_path, expected_log_file_path)
        
        if os.path.exists(log_file_path):
            os.remove(log_file_path)

        total += 1
    
    print(f'{GREEN}{passed}/{total} tests passed{END}')
