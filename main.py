"""This module starts the application.

PySnake a simple snake game with GUI and the feature of saving results.

"""

from tkinter import Tk

from game import Game
from gui import GuiApp


__author__ = 'Artem Kustov'
__email__ = 'artem.kustov@artcom-net.ru'
__version__ = '1.0'


if __name__ == '__main__':
    root = Tk()
    gui = GuiApp(root)
    game = Game(gui)
    game.start()
    root.mainloop()
