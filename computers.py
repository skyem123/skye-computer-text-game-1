import gameio


# Assumes that the path to join onto is a directory
def path_push(path, joins, sep="/"):
    if not path.endswith("/"):
        path += "/"
    # ...and join!
    return path + joins


def path_split(path, sep="/"):
    return path.split(sep=sep)


def path_join(chunks, sep="/"):
    return sep.join(chunks)


def path_clean(path, sep="/"):
    # Solve the absolute paths!
    i = len(path)
    while i > 0:
        i -= 1
        if i >= 1:
            if path[i-1:i+1] == "//":
                path = path[i:]

    path = path_split(path, sep)
    chunks = []
    for chunk in path:
        if chunk == "..":
            if len(chunks) > 1:
                chunks.pop()
        elif chunk == ".":
            pass
        else: chunks.append(chunk)

    return sep + (path_join(chunks, sep)).lstrip(sep)


class Computer:
    def motd(self):
        return ""

    def file_is_dir(self, location):
        if location == "/":
            return True

    def run_program(self, location, command, args):
        return False

    def _prompt(self, location):
        raise NotImplementedError("Please Implement Prompt!")

    def _cd(self, location, args):
        if len(args) > 1:
            args = args[1:]
            relative = " ".join(args)
            absolute = path_push(location, relative)
            absolute = path_clean(absolute)
            # Error checking
            if self.file_is_dir(absolute):
                location = absolute
            else:
                gameio.error("Path `" + absolute + "` is not a directory!\n")

        return location

    def shell(self, show_motd=True, initial_location="~"):
        if show_motd:
            gameio.write(self.motd())

        ended = False
        location = initial_location
        while not ended:
            gameio.write(self._prompt(location))
            args = gameio.read_line().split()

            if len(args) > 0:
                command = args[0]

            # Internal Commands
            if command == "exit":
                ended = True
            elif command == "pwd":
                gameio.write(location + "\n")
            elif command == "cd":
                location = self._cd(location, args)
            else:  # External Commands
                if not self.run_program(location, command, args):
                    gameio.error("Command `" + command + "` not found!\n")
