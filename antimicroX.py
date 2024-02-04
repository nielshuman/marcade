import subprocess
import os


class AntimicroX():
    """
    A class representing AntimicroX, a utility for mapping gamepad input to keyboard and mouse events.
    """

    def __init__(self, profiles_directory='.', default_profile=None):
        self.default_profile = default_profile
        self.profiles_directory = profiles_directory
        pass

    def start(self, profile=None):
        """
        Starts the AntimicroX process in the system tray.
        """
        command = ['antimicrox', '--tray']
        if profile is not None:
            command += ['--profile', self.profile_filename(profile)]
        elif self.default_profile is not None:
            command += ['--profile', self.profile_filename(self.default_profile)]

        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def stop(self):
        """
        Stops the AntimicroX process.
        """
        self.process.terminate()
        self.process.wait()
    
    def change_profile(self, profile_name):
        """
        Changes the active profile in AntimicroX.

        Args:
            profile (str): The name of the profile to switch to.
        """
        subprocess.run(['antimicrox', '--profile', self.profile_filename(profile_name)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f'Antimicrox changed to profile {profile_name}')

    def change_to_default(self):
        """
        Changes the active profile in AntimicroX to the default profile.
        """     
        if self.default_profile is not None:
            self.change_profile(self.default_profile)
        else:
            raise ValueError('No default profile set.')
    
    def profile_filename(self, profile_name):
        """
        Returns the filename of a profile (relative to the current working directory).
        """
        if profile_name.endswith('.gamecontroller.amgp'):
            filename = os.path.join(self.profiles_directory, profile_name)
        else:
            filename = os.path.join(self.profiles_directory, f'{profile_name}.gamecontroller.amgp')
        if os.path.exists(filename):
            return filename
        else:
            raise FileNotFoundError(f"Profile file '{filename}' does not exist.")