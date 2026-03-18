import subprocess
import os
from consts import *

process = None
output_path_check = None

def run_meshroom_basic(meshroom_path, input_path, output_path, cache_directory, config_path=None, forceCompute=True):
    global process
    global output_path_check
    print(input_path)
    os.makedirs(output_path, exist_ok=True)
    output_path_check = output_path
    # meshroom_cmd = [
    #     meshroom_path, 
    #     '--input', input_path,
    #     '--output', output_path,
    #     '--cache', cache_directory
    # ]
    
    # # Add params option if a config file is specified
    # if config_path:
    #     meshroom_cmd.extend(['--overrides', config_path])
    # if forceCompute:
    #     meshroom_cmd.append('--forceCompute')
    meshroom_cmd = [f'{meshroom_path} --input {input_path} --output {output_path} --cache {cache_directory} --overrides {config_path} --forceCompute']
    try:
        # Run Meshroom command
        process = subprocess.Popen(meshroom_cmd, shell=True)
        # print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running Meshroom: {e}")
        return False
    return True

def run_meshroom(input_directory, output_directory, cache_directory):
    return(run_meshroom_basic(meshroom_batch_path, input_directory, output_directory, cache_directory, config_file))


def is_meshroom_done():
    global process
    if process is None:
        return True
    return process.poll() is not None

def is_meshroom_success():
    global process
    global output_path_check
    if process is None:
        return False
    if os.path.exists(os.path.join(output_path_check, texture_name)):
        return True
    return False

def terminate_meshroom():
    global process
    if process is not None:
        process.terminate()
    process = None
