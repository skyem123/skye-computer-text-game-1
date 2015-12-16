import computers
import gameio
import os


class SaveFS(gameio.RealFS):
    __base = os.path.abspath(os.path.join(os.getcwd(), "saves/"))

    def __init__(self):
        if "saves" not in os.listdir(os.getcwd()):
            os.mkdir(self.__base)

    def _get_real_base(self):
        return self.__base

save_fs = SaveFS()


def new_game(name):
    if not save_fs.path_exists(name):
        save_fs.make_dir(name)
        return True
    else: return False


def load_game(name):
    # Is there actually a game there?
    if not save_fs.path_is_dir(name):
        return False
    # If so, load it and play!
    return True


def rm_game(name):
    # Is there actually a game there?
    if not save_fs.path_is_dir(name):
        gameio.error("Path does not exist!")
    # If so, delete the game!
    save_fs.rm_dir(name, recursive=True)
    return True


class Menu(computers.Computer):
    __filesystem = save_fs

    def get_FS(self):
        return self.__filesystem

    def shell(self, show_motd=True, initial_location="/"):
        computers.Computer.shell(self, show_motd, initial_location)

    def _prompt(self, location):
        return "> "

    def run_program(self, location, command, args):
        if command == "ls":
            for file in self.get_FS().ls("/"):
                if self.get_FS().path_is_dir(computers.path_push(location, file)):
                    gameio.write(file + "\t")
            gameio.write("\n")
        elif command == "load":
            if len(args) <= 1:
                gameio.error("Command `load` requires a name as it's argument.\n")
                return True

            if not load_game(computers.path_push(location, args[1])):
                gameio.error("Could not load game, `" + args[1] + "`.\n")
            else:
                gameio.write("\nGame `" + args[1] + "` quit.\n")
            return True

        elif command == "new":
            if len(args) <= 1:
                gameio.error("Command `new` requires a name as it's argument.\n")
                return True

            if new_game(computers.path_push(location, args[1])):
                gameio.write("Created new game, `" + args[1] + "`.\nRun the command `load " + args[1] + "` to play!\n")
            else:
                gameio.error("Could not create new game `" + args[1] + "`.\n")
            return True
        elif command == "rm":
            if len(args) <= 1:
                gameio.error("Command `rm` requires a name as it's argument.\n")
                return True

            if rm_game(computers.path_push(location, args[1])):
                gameio.write("Deleted game, `" + args[1] + "`.\n")
            else:
                gameio.error("Could not delete game, `" + args[1] + "`.\n")
        else:
            return False
        return True

    def motd(self):
        return """
Run the command `new`, followed by a name, to start a new game.
Run the command `ls` to list saves.
Run the command `load`, followed by a name, to load a saved game.
Run the command `rm`, followed by a name, to delete a saved game.

Remember, to save the game, you run the command `save` on your starting computer!
"""