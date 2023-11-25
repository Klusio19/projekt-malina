from setup import init
from polling_loop import loop


if __name__ == '__main__':
    try:
        init()
        loop()
    except KeyboardInterrupt:
        quit()
