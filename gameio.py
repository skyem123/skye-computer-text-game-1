import os


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


class RealFS():
    def _sanitize(self, path):
        """Converts a Unix fake path into something that can be added onto the real path without issues."""
        # Remove the slash...
        if path[0] == "/":
            path = path[1:]
        # Join the paths...
        path = os.path.join(self._get_real_base(), path)
        # Get the absolute path
        path = os.path.abspath(path)
        # Make sure it does not go outside of the base path!
        if os.path.commonprefix([self._get_real_base(), path]) != self._get_real_base():
            raise Exception("Not Allowed to Escape Base Path!")
        return path
    
    def _get_real_base(self):
        raise NotImplementedError()

    def ls(self, sub):
       return os.listdir(self._sanitize(sub))

class SaveFS(RealFS):
    def _get_real_base(self):
        return os.getcwd()
    
