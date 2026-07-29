from utils import *
from engine import Engine


def main():
    engine = Engine()


    while engine.running:

        engine.start_frame()
        if not engine.running:
            continue
        if engine.game is None:
            engine.show_menu()
        else:
            engine.tick()
        engine.end_frame()

    engine.quit()



if __name__ == "__main__":
    main()
