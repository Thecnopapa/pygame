import pygame


from Engine import Engine
from Screen import Screen
from Game import Game

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

    engine.quit()



if __name__ == "__main__":
    main()
