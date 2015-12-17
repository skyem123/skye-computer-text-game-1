import os
import shutil


def write(text):
    if text[-1] != '\n':
        print(text, end='', flush=True)
    else:
        print(text, end='', flush=False)


def error(text):
    write(text)


def read_line():
    return input()


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

    def file_open(self, path, mode='r'):
        if mode == 'r':
            return self._file_open_read(path)
        elif mode == 'w':
            return self._file_open_write(path)


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


