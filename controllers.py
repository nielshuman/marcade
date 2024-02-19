import subprocess

def input_remapper_control(deamon_command, device=None, preset=None):
    command = ['input-remapper-control']
    
    command += ['--command', deamon_command]

    if device is not None:
        command += ['--device', device]
    if preset is not None:
        command += ['--preset', preset]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return True
    else:
        raise ValueError(f'input-remapper-control returned non-zero exit code: {result.returncode}\n{result.stderr}')
    
def stop_all():
    input_remapper_control('stop-all')

class Controller:
    def __init__(self, name) -> None:
        self.name = name
    
    def start(self, preset):
        input_remapper_control('start', device=self.name, preset=preset)
    
    def stop(self):
        input_remapper_control('stop', device=self.name)

P1 = Controller('DragonRise Inc.   Generic   USB  Joystick  ')
P2 = Controller('DragonRise Inc.   Generic   USB  Joystick  2')