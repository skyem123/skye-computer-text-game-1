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
            gameio.write("TODO\n")
        elif command == "new":
            if len(args) <= 1:
                gameio.error("Command `new` requires a name as it's argument.")
                return True
            if new_game(args[1]):
                gameio.write("New game, `" + args[1] + "` created.\nRun the command `load " + args[1] + "` to play!\n")
            else:
                gameio.error("New game, `" + args[1] + "` could not be created.\n")
            return True
        else:
            return False
        return True

    def motd(self):
        return """
Run the command `new`, followed by a name, to start a new game.
Run the command `load`, followed by a name, to load a saved game from a file.
Run the command `ls` to list saves.

Remember, to save the game, you run the command `save` on your starting computer!
"""