"""Wrapper Game class for PySnake game.

This class is essentially a wrapper, which manages all the components
of the game:
    - Snake;
    - Apple;
    - ScoreDb;
    - GuiApp.

"""


import os
import re
import time
import random

from tkinter import DISABLED, StringVar

from gui import *
from score_db import ScoreDb


__author__ = 'Artem Kustov'
__email__ = 'artem.kustov@artcom-net.ru'
__version__ = '1.0'


class Game(object):
    """Wrapper class."""

    _SCORE_DB_PATH = os.path.join(os.path.expanduser('~'), GuiApp.TITLE)

    def __init__(self, gui_app):
        """Initialize an instance.

        Argument gui_app is instance of the GuiApp class.

        """
        self._gui = gui_app
        self._snake = Snake(self._gui.c_game_main)
        self._apple = self._create_apple()
        self._player = None
        self._score = 0
        self._score_db = Game._load_score_db()
        self._top_score = self._score_db.get_top_score()

    def start(self):
        """Starts application."""

        self._gui.master.protocol('WM_DELETE_WINDOW', self._close_root)
        self._gui.btn_start['command'] = self._pre_start
        self._gui.btn_score['command'] = self._show_top_scores
        self._gui.show_menu()

    def _pre_start(self):
        """Actions before start the game."""

        self._gui.c_game_main.bind('<KeyPress>', self._snake.change_direction)
        self._update_top_score()
        self._update_score()
        self._gui.show_game()
        self._start_game()

    def _start_game(self):
        """Starting the game."""

        self._snake.move()
        if self._snake_crush():
            self._game_over()
        else:
            if self._snake.segments[0].coord == self._apple.coord:
                self._apple.__del__()
                self._score += 1
                self._update_score()
                self._snake.add_segment()
                self._apple = self._create_apple()
            self._gui.master.after(self._snake.speed, self._start_game)

    def _create_apple(self):
        """Creating new apple."""

        apple_coord = self._random_coord()
        while apple_coord in \
                [coord.coord[0:2] for coord in self._snake.segments]:
            apple_coord = self._random_coord()
        else:
            return Apple(self._gui.c_game_main, apple_coord)

    @staticmethod
    def _random_coord():
        """Random generation of apple coordinates"""

        return list(
            (random.randrange(0, GuiApp.GAME_AREA_SIZE['width'] - 19, 20),
             random.randrange(0, GuiApp.GAME_AREA_SIZE['height'] - 19, 20))
        )

    def _snake_crush(self):
        """Checks snake crush."""

        crush = False
        head_coord, *body_coord = self._snake.segments
        if head_coord.coord in [body.coord for body in body_coord]:
            crush = True
        elif [neg_coord for neg_coord in head_coord.coord if neg_coord < 0]:
            crush = True
        elif [over_coord for over_coord in head_coord.coord \
              if over_coord > GuiApp.GAME_AREA_SIZE['width']]:
            crush = True
        return crush

    def _update_top_score(self):
        """Updates a top score on a label widget."""

        self._gui.l_game_top['text'] = re.sub(
            r'\d{1,2}$', str(self._top_score), self._gui.l_game_top['text']
        )

    def _update_score(self):
        """Updates a score on a label widget."""

        self._gui.l_game_top['text'] = re.sub(
            r'\d{1,2}', str(self._score), self._gui.l_game_top['text'], count=1
        )

    def _show_top_scores(self):
        """Opens the child of window with top players."""

        self._gui.show_top_scores(self._score_db.get_scores())
        if not self._score_db:
            self._gui.btn_result_clear['state'] = DISABLED
        else:
            self._gui.btn_result_clear['command'] = self._clear_score_db

    def _show_entry_player(self):
        """Opens the child of window at the end of the game.
        Shows score and entry for input a player name.

        """

        if self._score != 0:
            self._gui.show_entry_player(self._score)
            self._gui.btn_ok['command'] = self._check_player_name
            self._gui.w_entry_player.protocol(
                'WM_DELETE_WINDOW', self._close_entry_win
            )
        else:
            self._renew_game()

    def _close_entry_win(self):
        """Closes the child window and initialize the new game."""

        self._gui.w_entry_player.destroy()
        self._renew_game()

    def _game_over(self):
        """Shows game over text on a label widget,
        removes elements from the playing area.

        """
        self._gui.show_game_over()
        time.sleep(3)
        for snake_segment in self._snake.segments[::-1]:
            snake_segment.__del__()
            time.sleep(0.1)
        self._apple.__del__()
        time.sleep(1)
        self._show_entry_player()

    def _save_score(self):
        """It saves the scores of the player in a database."""

        self._player = self._player.capitalize()
        if self._player in self._score_db:
            old_score = self._score_db[self._player]
            self._score_db[self._player] = \
                self._score if self._score > old_score else old_score
        else:
            self._score_db[self._player] = self._score
        self._gui.w_entry_player.destroy()
        self._renew_game()

    def _get_player_name(self):
        """Getting the player name."""

        self._player = self._gui.player.get().strip()

    def _check_player_name(self):
        """Checks player name."""

        self._get_player_name()
        if self._player.isdigit() or len(self._player) > 15:
            self._gui.show_player_error()
            self._show_entry_player()
        else:
            self._save_score()

    def _renew_game(self):
        """Initialize a new game."""

        self.__init__(self._gui)
        self._gui.l_game_top['text'] = 'Score: 0\t\tTopScore: 0'
        self._update_top_score()
        self._update_score()
        self._gui.player = StringVar()
        self._gui.show_menu()

    def _close_root(self):
        """Actions at the closing of the root window."""

        self._score_db.close()
        self._gui.master.destroy()

    def _clear_score_db(self):
        """Deletes all entries from the database."""

        self._score_db.clear_db()
        self._score_db.close()
        self._score_db = Game._load_score_db()
        self._top_score = self._score_db.get_top_score()
        self._gui.w_top_scores.destroy()

    @classmethod
    def _load_score_db(cls):
        """Load the database with the results."""

        if not os.path.exists(cls._SCORE_DB_PATH):
            os.makedirs(cls._SCORE_DB_PATH)
        return ScoreDb(os.path.join(cls._SCORE_DB_PATH, GuiApp.TITLE))
