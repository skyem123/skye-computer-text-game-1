import computers
import gameio
import os


class Menu(computers.Computer):
    def shell(self, show_motd=True, initial_location="/"):
        computers.Computer.shell(self, show_motd, initial_location)

    def _prompt(self, location):
        return "> "

    def motd(self):
        return """
Run the command `new` to start a new game.
Run the command `load` to load a saved game from a file.
Run the command `ls` to list saves.

Remember, to save the game, you run the command `save` on your starting computer!
"""


def main():
    Menu().shell()
    gameio.write("\nGoodbye, Player.\n")

if __name__ == "__main__":
    main()
