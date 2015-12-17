import computers
import gameio
import os
import game


class Save:
    name = ""
    save_info = {}
    history = []

    def __init__(self, name, save_info, history):
        self.name = name
        self.save_info = save_info.copy()
        self.history = history.copy()

    def store(self, info_file, history_file, close=True):
        for key, value in self.save_info.items():
            info_file.write(key + ":" + str(value) + "\n")

        for entry in self.history:
            history_file.write(entry + "\n")

        if close:
            info_file.close()
            history_file.close()

    def load(self, info_file, history_file, close=True):
        for i, line in enumerate(info_file):
            if line == "":
                continue
            key, value = line.split(':', 1)
            self.save_info[key] = value[:-1]

        for i, line in enumerate(history_file):
            self.history.append(line)

        if close:
            info_file.close()
            history_file.close()


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
    else:
        return False
    
    save = Save(save_info={
        "version": game.VER_NUM,
        "pretty_version": game.VERSION,
        "created_as": name
    }, history=[], name=name)
    save.store(close=True,
               info_file=save_fs.file_open(computers.path_push(name, "saveinfo.txt"), 'w'),
               history_file=save_fs.file_open(computers.path_push(name, "history.txt"), 'w'))
    
    return True


def load_game(name):
    # Is there actually a game there?
    if not save_fs.path_is_dir(name):
        return False
    # Firstly, we need to actually load the stuff into memory
    game.now_playing = Save(save_info={}, history=[], name=name)
    game.now_playing.load(close=True,
                          info_file=save_fs.file_open(computers.path_push(name, "saveinfo.txt"), 'r'),
                          history_file=save_fs.file_open(computers.path_push(name, "history.txt"), 'r'))

    # Then we need to make a new game...
    start = computers.FirstComputer()
    # ...start logging...
    gameio.set_input_logging(True)
    # ...then set the replay up...
    gameio.set_replay(game.now_playing.history.copy())
    # ...and start playing!
    start.shell()
    # Before we exit, make sure there is no replay!
    gameio.clear_replay()
    # Also stop logging!
    gameio.set_input_logging(False)
    return True


def save_game(save_obj, input_log):
    save_obj.history = input_log
    save_obj.store(close=True,
                   info_file=save_fs.file_open(computers.path_push(save_obj.name, "saveinfo.txt"), 'w'),
                   history_file=save_fs.file_open(computers.path_push(save_obj.name, "history.txt"), 'w'))
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
            if len(args) > 1:
                location = computers.path_push(location, args[1])
            # To avoid crashes...
            if not self.get_FS().path_is_dir(location):
                gameio.error("The path `"+ location +"` is not a directory or does not exist.\n")
                return True
            for file in self.get_FS().ls(location):
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

            location = computers.path_clean(computers.path_push(location, args[1]))
            if location == "/":
                gameio.error("Cannot delete whole saves directory (the root directory) `/`.\n")
                return True

            if rm_game(location):
                gameio.write("Deleted game, `" + args[1] + "`.\n")
            else:
                gameio.error("Could not delete game, `" + args[1] + "`.\n")
        elif command == "mkdir":
            if len(args) <= 1:
                gameio.error("Command `mkdir` requires a folder name as it's argument.\n")
                return True
            location = computers.path_clean(computers.path_push(location, args[1]))
            if self.get_FS().path_exists(location):
                gameio.error("Cannot create new directory, path `" + location + "` already exists.\n")
            else:
                self.get_FS().make_dir(location)
        else:
            return False
        return True

    def motd(self):
        return """
To exit, run the command `exit`.

Run the command `new`, followed by a name, to start a new game.
Run the command `ls` to list saves.
Run the command `load`, followed by a name, to load a saved game.
Run the command `rm`, followed by a name, to delete a saved game.

Remember, to save the game, you run the command `save` on your starting computer!
"""
