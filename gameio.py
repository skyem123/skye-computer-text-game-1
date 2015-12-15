def write(text):
    if text[-1] != '\n':
        print(text, end='', flush=True)
    else:
        print(text, end='', flush=False)


def error(text):
    write(text)

def read_line():
    return input()
