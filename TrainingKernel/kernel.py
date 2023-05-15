import ast
import debugpy
import inspect
from ipykernel.kernelbase import Kernel
import wpilib

debugMe=True
if(debugMe):
    # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
    debugpy.listen(5678) # ensure that this port is the same as the one in your launch.json
    print("Waiting for debugger attach")
    debugpy.wait_for_client()
    debugpy.breakpoint()
    print("Attached!")

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

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        
        
        if not silent:
            response = ""
            errors = False

            # Clear the incoming function names
            try:
                self.robotInit = None
            except NameError:
                pass

            try:
                self.robotPeriodic = None
            except NameError:
                pass

            # evaluate the incoming code
            initBodyFound = False
            periodicBodyFound = False

            tree = ast.parse(code)
            exec_exprs = []
            for module in tree.body:
                exec_exprs.append(module)
                if(module.name == "robotInit"):
                    initBodyFound = True
                if(module.name == "robotPeriodic"):
                    periodicBodyFound = True
            exec_expr = ast.Module(exec_exprs, type_ignores=[])
            exec(compile(exec_expr, 'file', 'exec'), self.__dict__)

            # read back the code contents and report it to the user.
            try:
                if(self.robotInit is not None):
                    initCodeStr = inspect.getsource(self.robotInit)
                else:
                    response += "You not provide a robotInit Function!\n"
                    initCodeStr = "pass"
            except Exception as e:
                response += "Couldn't evaluate the robotInit code: \n"
                response += str(e)
                response += "\n"
                errors = True

            try:
                if(self.robotPeriodic is not None):
                    periodicCodeStr = inspect.getsource(self.robotPeriodic)
                else:
                    response += "You not provide a robotPeriodic Function!\n"
                    periodicCodeStr = "pass"
            except Exception as e:
                response += "Couldn't evaluate the robotPeriodic code: \n"
                response += str(e)
                response += "\n"
                errors = True
            
            if(not errors):
                response += "Running robot with the following code:\n\n"
                response += "def robotInit():\n"
                response += initCodeStr
                response += "\n"
                response += "def robotPeriodic():\n"
                response += periodicCodeStr
            else:
                response += "Errors present, not launching robot."


            stream_content = {'name': 'stdout', 'text': response}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
