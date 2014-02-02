from game import Game

def main():
    game = Game()
    game.eventLoop()
    game.cleanUp()

    return 0

if __name__ == '__main__':
    main()
