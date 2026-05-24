import subprocess
import threading

class CommandHandler:
    """Execute and manage system commands safely"""
    
    def __init__(self):
        self.processes = []
    
    def execute(self, cmd, timeout=None, capture_output=True):
        """Execute a command"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                shell=isinstance(cmd, str)
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return None, "Command timed out", -1
        except Exception as e:
            return None, str(e), -1
    
    def execute_async(self, cmd, callback=None):
        """Execute command asynchronously"""
        def run():
            stdout, stderr, code = self.execute(cmd)
            if callback:
                callback(stdout, stderr, code)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return thread
