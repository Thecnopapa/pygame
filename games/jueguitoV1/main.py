import pygame, sys, os


from engine import Engine

ART_FOLDER = os.path.join("..", "..", "Jueguito", "assets")
DEBUG = "--debug" in sys.argv

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
