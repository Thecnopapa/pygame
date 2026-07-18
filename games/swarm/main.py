import pygame, sys, os


from engines import Engine
from screens import Screen
from games import Game

ART_FOLDER = os.path.join("..", "..", "Jueguito", "assets")
DEBUG = "--debug" in sys.argv

def main():
    engine = Engine()
    screen = Screen(engine, background="black")

    game = Game(screen)


    while engine.running:

        engine.start_frame()

        screen.clear()

        game.update()

        screen.tick()

        engine.end_frame()
        #print()

    engine.quit()



if __name__ == "__main__":
    main()
