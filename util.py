import soundfile as sf
import sounddevice as sd
import subprocess

def play_sound(filename, block=False):
    sd.play(*sf.read(filename, dtype='int16'))
    if block: sd.wait()

import subprocess
import os

def profile_filename(profile):
    filename = f'profiles/{profile}.gamecontroller.amgp'
    if os.path.exists(filename):
        return filename
    else:
        raise FileNotFoundError(f"Profile file '{filename}' does not exist.")

class AntimicroX():
    """
    A class representing AntimicroX, a utility for mapping gamepad input to keyboard and mouse events.
    """

    def __init__(self, default_profile=None):
        self.default_profile = default_profile
        pass

    def start(self):
        """
        Starts the AntimicroX process in the system tray.
        """
        command = ['antimicrox', '--tray']

        if self.default_profile is not None:
            command += ['--profile', profile_filename(self.default_profile)]

        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def stop(self):
        """
        Stops the AntimicroX process.
        """
        self.process.terminate()
        self.process.wait()
    
    def change_profile(self, profile):
        """
        Changes the active profile in AntimicroX.

        Args:
            profile (str): The name of the profile to switch to.
        """
        subprocess.run(['antimicrox', '--profile', profile_filename(profile)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
