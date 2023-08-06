import warnings
from time import sleep
from utils.os_helper import paths, command
from utils.thread_helpers import thread
from playerFramework.exceptions import *
import subprocess


class player:
    """The base class initialising the player.
    This will cause any other instances of this player to exit"""

    def __init__(self, executable: str, info: dict, warning=True):
        """
        :param warning:
        boolean to spit out warnings
        default set to True

        :param executable:
        path to the executable file

        :param info:
        a dictionary containing the IO file path and commands to pause or play the player
        i.e.
        {
            'io file': '/Users/*/.ioFile',
            'play' : ['player', '**path**'],
            'pause': 'pause',
            'resume': 'resume',
            'exit': 'stop',
            'Volume': 'volume:{}'
        }

        if the player does not conform to the standard arg[0] == executable_path and arg[1] == track_path
        the 'play' value must be a list which defines how the player will ba called via subprocesses/utils
        with the keyword '**path**' which defines where the framework will replace it with the path to the track
        otherwise leave 'play' to the value of None
        """
        self.internalKill = False
        self.warning = warning
        self.exec = paths.Path(executable)
        self.info = info
        self.thread = None
        if not self.exec.isPath():
            raise PlayerPathNotValid('Player not found')

    def changeValue(self, key_name, Format=False):
        """
        :param key_name:
        Will be used to find the value against info dictionary
        :param Format:
        Value to format the string via {}
        :return:
        """
        try:
            if Format is False:
                with open(self.info['io file'], 'w+') as file:
                    file.write(self.info[key_name])
            else:
                writeINFO = self.info[key_name].format(Format)
                with open(self.info['io file'], 'w+') as file:
                    file.write(writeINFO)

        except FileNotFoundError or PermissionError as exception:
            raise UnableToWriteToIOFile(exception)

        except KeyError as exception:
            raise UndefinedKeyName(exception)

    def play_track(self, track_path):
        """
        The player will not be run on the main thread
        to wait till the player is completed on the main thread use .wait_for_player()

        :param track_path:
        path to the file that will be played
        :return:
        """

        def internal_player(playerClass, track):
            arguments = [playerClass.exec.path]
            playINFO = playerClass.info['play']
            if playINFO is None:
                arguments.append(track_path)
            else:
                for a in playINFO:
                    if a == '**path**':
                        a = track

                    arguments.append(a)

            try:
                process = subprocess.Popen(args=arguments, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)


                process.communicate()[0].decode('utf8')
                process.wait()
                process.poll()
                returnCode = int(process.returncode)

                if returnCode == 1 or -1:
                    pass

                elif returnCode == -15 or -9:
                    if self.internalKill is not True:
                        raise ProcessTerminatedExternally

            except KeyboardInterrupt:
                if playerClass.warning:
                    warnings.warn('Player was stopped with KeyBoardInterrupt')

            self.thread = None
            self.process = None

        self._kill_player()
        self.thread = thread(func=internal_player, args=[self, track_path])

    def wait_for_player(self):
        if self.thread is not None:
            self.thread.join()

    def is_playing(self):
        if self.thread is None:
            return False
        elif self.thread is not None:
            return True

    def _kill_player(self):
        self.internalKill = True
        command(['killall', self.exec.last_component()], quite=True)
        sleep(0.1)
        self.internalKill = False

    def exit(self):
        self._kill_player()


