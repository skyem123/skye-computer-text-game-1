import gameio
import saveload

VER_NUM = int(0)
VERSION = str(VER_NUM) + " experimental."


def main():
    saveload.Menu().shell()
    gameio.write("\nGoodbye, Player.\n")

if __name__ == "__main__":
    main()
