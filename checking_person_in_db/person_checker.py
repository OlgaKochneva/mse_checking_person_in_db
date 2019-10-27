import sys

from app import App, msg

if __name__ == '__main__':
    if len(sys.argv) < 2:
        msg('err', 'Nо video source to process', print)
        sys.exit(1)

    App(sys.argv[1]).run()
