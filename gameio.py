import os
import shutil


def write(text):
    if len(text) >= 1 and text[-1] != '\n':
        print(text, end='', flush=True)
    else:
        print(text, end='', flush=False)


def error(text):
    write(text)


__replay_input = []


def clear_replay():
    global __replay_input
    __replay_input = []


def set_replay(replay):
    global __replay_input
    __replay_input = replay


def is_replaying():
    return len(__replay_input) > 0


__input_log = []
__input_logging = False


def set_input_logging(status=None):
    global __input_logging
    if status is None:
        __input_logging = not __input_logging
    else:
        __input_logging = not not status


def get_input_logging():
    return __input_logging


def get_input_log():
    return __input_log


def clear_input_log(amount=-1):
    global __input_log
    if amount == -1:
        __input_log = []
    else:
        __input_log = __input_log[:-amount]



def read_line():
    line = ""

    if len(__replay_input) != 0:
        line = __replay_input.pop(0)
        write(line)
        return line
    else:
        line = input()

    if __input_logging:
        __input_log.append(line)

    return line


class FS():
    def ls(self, sub):
        raise NotImplementedError()

    def path_is_dir(self, path):
        raise NotImplementedError()

    def path_exists(self, path):
        raise NotImplementedError()

    def make_dir(self, path):
        raise NotImplementedError()

    def rm_dir(self, path, recursive=False):
        raise NotImplementedError()

    def _file_open_write(self, path):
        return NotImplementedError()

    def _file_open_read(self, path):
        return NotImplementedError()

    def _file_open_append(self, path):
        return NotImplementedError()

    def file_open(self, path, mode='r'):
        if mode == 'r':
            return self._file_open_read(path)
        elif mode == 'w':
            return self._file_open_write(path)
        elif mode == 'a':
            return self._file_open_append(path)


class RealFS(FS):
    def _sanitize(self, path):
        """Converts a Unix fake path into something that can be added onto the real path without issues."""
        # Remove the slash...
        while len(path) > 0 and path[0] == "/":
            path = path[1:]
        # Join the paths...
        path = os.path.join(self._get_real_base(), path)
        # Get the absolute path
        path = os.path.abspath(path)
        # Make sure it does not go outside of the base path!
        #print([self._get_real_base(), path])
        if os.path.commonprefix([self._get_real_base(), path]) != self._get_real_base():
            raise Exception("Not Allowed to Escape Base Path!")
        return path
    
    def _get_real_base(self):
        raise NotImplementedError()

    def ls(self, path):
        return os.listdir(self._sanitize(path))

    def path_is_dir(self, path):
        return os.path.isdir(self._sanitize(path))

    def path_exists(self, path):
        return os.path.exists(self._sanitize(path))

    def make_dir(self, path):
        return os.mkdir(self._sanitize(path))

    def rm_dir(self, path, recursive=False):
        path = self._sanitize(path)
        if not recursive:
            return os.rmdir(path)
        else:
            return shutil.rmtree(path)

    def _file_open_write(self, path):
        return open(self._sanitize(path), 'w')

    def _file_open_read(self, path):
        return open(self._sanitize(path), 'r')

    def _file_open_append(self, path):
        return open(self._sanitize(path), 'a')


