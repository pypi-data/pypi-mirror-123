from subprocess import run

from cli.config.config import config

"""
    Execute the local server launch script
    The script path is fetched from the configuration files
"""
def create():
    
    launch_script_path = None
    try:
        launch_script_path = config['command']['workshop']['create']['script_path'].get(str)
    except:
        pass

    if launch_script_path == None:
        print("Could not execute local server launch script : Could not read script path from configuration file")
    else:
        completedProcess = run([launch_script_path], shell=True)