import os
import subprocess
import debugpy
from ipykernel.kernelbase import Kernel

rootDir = "TrainingKernel/tmpRobot"


debugMe=False
if(debugMe):
    # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
    debugpy.listen(5678) # ensure that this port is the same as the one in your launch.json
    print("Waiting for debugger attach")
    debugpy.wait_for_client()
    debugpy.breakpoint()
    print("Attached!")
    

def adjust_indentation(code):
    lines = code.split('\n')
    first_line_indentation = len(lines[0]) - len(lines[0].lstrip())

    adjusted_lines = [' ' * 4 + line[first_line_indentation:] for line in lines]

    return '\n'.join(adjusted_lines)

class UserRobotRunner:
    def __init__(self):
        self.process = None

    def start(self):
        if self.is_running():
            # Process is already running
            self.stop()

        self.process = subprocess.Popen(
            "start cmd /C \"python robot.py sim || pause\"",  
            universal_newlines=True,
            shell=True,
            cwd = rootDir,
            #creationflags = subprocess.CREATE_NEW_CONSOLE
        )

    def stop(self):
        if self.is_running():
            self.process.terminate()
            self.process.wait()

    def is_running(self):
        return self.process and self.process.poll() is None

class TrainingKernel(Kernel):
    implementation = 'RobotPy Training'
    implementation_version = '1.0'
    language = 'py'
    language_version = '3.11'
    language_info = {
        'name': 'echo',
        'mimetype': 'text/py',
        'file_extension': '.py',
    }
    banner = "RobotPy Training Kernel Client"
    
    userCode = UserRobotRunner()

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        
        if not silent:
            
            code = adjust_indentation(code)
            
            with open("TrainingKernel/robot.py_tmplt", "r") as robotPyTmplt:
                
                if(not os.path.isdir(rootDir)):
                    os.makedirs(rootDir)
                    
                with open(os.path.join(rootDir, "robot.py"), "w") as outFile:
                    for line in robotPyTmplt:
                        outFile.write(line.replace("${USER_CODE}", code))
                        
                    self.userCode.start()
                
            response = "Running robot with the following code:\n\n"
            response += code

            stream_content = {'name': 'stdout', 'text': response}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
