""" GUI classes for PySnake game.

This module provides classes which allow the display, positioning
and control of game objects.
Classes: GuiApp, Segment, Apple, SnakeSegment, Snake.

"""


import tkinter.messagebox as msg_box

from tkinter import *


__all__ = ['GuiApp', 'Snake', 'Apple']
__author__ = 'Artem Kustov'
__email__ = 'artem.kustov@artcom-net.ru'
__version__ = '1.0'


class GuiApp(object):
    """Main GUI of game. This class provides methods for
    manage windows, frames and other widgets.
    The object of this class is controlled instance of the Game.

    """
    TITLE = 'PySnake'
    GAME_AREA_SIZE = {'width': 500, 'height': 500}
    _BG = '#013106'
    _FG = '#56C12F'
    _ACT_BG = '#56A32F'
    _FONT = 'Times 14 bold'
    _BUTTON_CONF = {'width': 12, 'bd': 4, 'bg': '#56C12F', 'fg': '#013106'}

    def __init__(self, master):
        """Initialize an instance.

        Argument master is instance of the Tk().

        """
        # Configuring the main window.
        self.master = master
        self.master.title(GuiApp.TITLE)
        self.master.resizable(0, 0)
        self.master.option_add('*Font', GuiApp._FONT)
        self.master.option_add('*Background', GuiApp._BG)
        self.master.option_add('*Activebackground', GuiApp._ACT_BG)
        self.master.option_add('*Foreground', GuiApp._FG)
        # Load app images.
        self.master.iconbitmap('images/icon.ico')
        self._img_game_area = PhotoImage(file='images/game_area.gif')
        self._img_menu_title = PhotoImage(file='images/menu_title.png')
        self._img_menu_snake = PhotoImage(file='images/menu_snake.png')
        # Configuring menu frame.
        self.f_menu = Frame(self.master, bd=50)
        self.l_img_menu_title = Label(
            self.f_menu, image=self._img_menu_title, bd=0
        )
        self.l_img_menu_snake = Label(
            self.f_menu, image=self._img_menu_snake, bd=0
        )
        self.btn_start = Button(
            self.f_menu, text='START GAME',
            **GuiApp._BUTTON_CONF
        )
        self.btn_score = Button(
            self.f_menu, text='HIGH SCORE',
            **GuiApp._BUTTON_CONF
        )
        # Configuring game frames.
        self.f_game_top = Frame(self.master, bd=10, relief=RIDGE)
        self.l_game_top = Label(
            self.f_game_top, text='Score: 0\t\tTopScore: 0'
        )
        self.f_game_main = Frame(
            self.master,
            bd=18,
            bg='#013106',
            relief=RIDGE
        )
        self.c_game_main = Canvas(
            self.f_game_main,
            width=GuiApp.GAME_AREA_SIZE['width'],
            height=GuiApp.GAME_AREA_SIZE['height']
        )
        self.c_game_main.create_image(
            GuiApp.GAME_AREA_SIZE['width'] / 2,
            GuiApp.GAME_AREA_SIZE['height'] / 2,
            image=self._img_game_area
        )
        # Initialize child window with top of scores.
        self.w_top_scores = None
        self.f_top_scores = None
        self.l_top_player = None
        self.l_top_score = None
        self.btn_result_close = None
        self.btn_result_clear = None
        # Initialize child window for getting player name.
        self.w_entry_player = None
        self.f_entry_player = None
        self.l_entry_score = None
        self.l_entry_text = None
        self.e_entry_player = None
        self.btn_ok = None
        self.player = StringVar()
        # Placing widgets.
        self.l_img_menu_title.grid(row=0, column=0, columnspan=2)
        self.l_img_menu_snake.grid(row=1, column=0, columnspan=2, pady=50)
        self.btn_start.grid(row=2, column=0, sticky=E, padx=(0, 30))
        self.btn_score.grid(row=2, column=1, sticky=W)
        self.l_game_top.pack()
        self.c_game_main.pack()
        # Configuring widgets.
        self._align_window(self.master)

    def show_menu(self):
        """Shows main menu."""

        self.f_game_top.pack_forget()
        self.f_game_main.pack_forget()
        self.f_menu.pack()

    def show_game(self):
        """Shows game area."""

        self.f_menu.pack_forget()
        self.f_game_top.pack(fill=X)
        self.f_game_main.pack()
        self.c_game_main.focus_set()

    def show_top_scores(self, scores):
        """Opens the child of window with top players."""

        self.w_top_scores = Toplevel(self.master)
        self.w_top_scores.resizable(0, 0)
        self.w_top_scores.transient(self.master)
        self.f_top_scores = Frame(self.w_top_scores, bd=60)
        self.l_top_player = Label(self.f_top_scores, text='Player')
        self.l_top_score = Label(self.f_top_scores, text='Score')
        self.btn_result_close = Button(
            self.f_top_scores,
            text='CLOSE',
            command=self._close_top_scores,
            **GuiApp._BUTTON_CONF
        )
        self.btn_result_clear = Button(
            self.f_top_scores,
            text='CLEAR',
            **GuiApp._BUTTON_CONF
        )
        self.f_top_scores.pack()
        self.l_top_player.grid(row=0, column=0, pady=(0, 20))
        self.l_top_score.grid(row=0, column=1, pady=(0, 20))
        row = 1
        for score in scores:
            Label(
                self.f_top_scores,
                text=score[0],
                fg='#ABF54E').grid(row=row, column=0)
            Label(
                self.f_top_scores,
                text=score[1],
                fg='#ABF54E').grid(row=row, column=1)
            row += 1
        row += 1
        self.btn_result_close.grid(
            row=row,
            column=0,
            pady=(50, 0),
            padx=(0, 10)
        )
        self.btn_result_clear.grid(row=row, column=1, pady=(50, 0))
        self.f_top_scores.focus_set()
        self._align_window(self.w_top_scores)

    def show_entry_player(self, score):
        """Opens the child of window at the end of the game.
        Shows score and entry for input a player name.

        """
        self.w_entry_player = Toplevel(self.master)
        self.w_entry_player.resizable(0, 0)
        self.w_entry_player.transient(self.master)
        self.f_entry_player = Frame(self.w_entry_player, bg='#013106', bd=50)
        self.l_entry_score = Label(
            self.f_entry_player,
            text='Score: %s' % score
        )
        self.l_entry_text = Label(self.f_entry_player, text='Enter your name')
        self.e_entry_player = Entry(
            self.f_entry_player,
            width=16,
            bd=3, bg='white',
            fg='#013106',
            textvariable=self.player
        )
        self.btn_ok = Button(
            self.f_entry_player,
            text='OK',
            state=DISABLED,
            **GuiApp._BUTTON_CONF
        )
        self.f_entry_player.pack()
        self.l_entry_score.pack()
        self.l_entry_text.pack()
        self.e_entry_player.pack(pady=(20, 0))
        self.btn_ok.pack(pady=(50, 0))
        self.e_entry_player.focus_set()
        self._align_window(self.w_entry_player)
        self.player.trace('w', lambda *event: self._switch_btn_ok())

    def show_game_over(self):
        """Change top label text."""

        self.l_game_top['text'] = 'Game Over'
        self.f_game_top.update()

    def _close_top_scores(self):
        """Destroys a child window."""

        self.w_top_scores.destroy()

    def _switch_btn_ok(self):
        """Change state of the button."""

        if self.player.get().strip():
            self.btn_ok['state'] = NORMAL
        else:
            self.btn_ok['state'] = DISABLED

    @staticmethod
    def show_player_error():
        """Shows a message with error."""

        msg_box.showerror('Error', 'Player name must contain letter(s) \
                                   and not exceed 15 characters!')

    @staticmethod
    def _align_window(win):
        """Aligns window center."""

        w_screen = win.winfo_screenwidth()
        h_screen = win.winfo_screenheight()
        w_win, h_win, x_win, y_win = re.findall(r'\d{1,4}', win.geometry())
        if w_win == '1' and h_win == '1':
            w_win = GuiApp.GAME_AREA_SIZE['width']
            h_win = GuiApp.GAME_AREA_SIZE['height']
        x = (w_screen / 2) - (int(w_win) / 2)
        y = (h_screen / 2) - (int(h_win) / 2)
        win.geometry('+{0:.0f}+{1:.0f}'.format(x, y))


class Segment(object):
    """The base class inherits Apple and SnakeSegment."""

    SIZE = 20

    def __init__(self, canvas_obj, coord, color=''):
        """Initialize an instance.

        Argument canvas_obj is instance of the Canvas class,
        coord is coordinates of the view: (x, y, x2, y2),
        color determined in classes successors.

        """
        self.canvas_obj = canvas_obj
        self.segment = self.canvas_obj.create_rectangle(
            coord[0],
            coord[1],
            coord[0] + Segment.SIZE,
            coord[1] + Segment.SIZE, fill=color
        )

    @property
    def coord(self):
        """Getter coordinates of the segment."""

        return self.canvas_obj.coords(self.segment)

    @coord.setter
    def coord(self, coord):
        """Setter coordinates of the segment."""

        self.canvas_obj.coords(self.segment, coord)

    def __del__(self):
        """Removes segment from the canvas object."""

        try:
            self.canvas_obj.delete(self.segment)
            self.canvas_obj.update()
        except TclError:
            pass


class Apple(Segment):
    """Subclass of the Segment."""

    COLOR = 'red'

    def __init__(self, canvas_obj, coord):
        super().__init__(canvas_obj, coord, color=Apple.COLOR)


class SnakeSegment(Segment):
    """Subclass of the Segment."""

    COLOR = '#56C12F'

    def __init__(self, canvas_obj, coord):
        super().__init__(canvas_obj, coord, color=SnakeSegment.COLOR)


class Snake(object):
    """This class defines the properties and methods of the snake.
    An object of class snake consists of the SnakeSegment instances.
    The object of this class is controlled instance of the Game.

    """

    _SNAKE_LEN = 3
    _HEAD_POSITION = (60, 60)
    _DIRECTIONS = {
        'Left': (-1, 0),
        'Right': (1, 0),
        'Up': (0, -1),
        'Down': (0, 1)
    }
    _SPEED = 400

    def __init__(self, canvas_obj):
        """Initialize an instance.

        Argument canvas_obj is instance of the Canvas class.

        """
        self.canvas_obj = canvas_obj
        segments_coord = [Snake._HEAD_POSITION, ]
        for segment in range(Snake._SNAKE_LEN - 1):
            segments_coord.append(
                (Snake._HEAD_POSITION[0] - SnakeSegment.SIZE * (segment + 1),
                 Snake._HEAD_POSITION[1])
            )
        self.segments = [
            SnakeSegment(self.canvas_obj, coord) for coord in segments_coord
        ]
        self.direction = Snake._DIRECTIONS['Right']
        self.speed = Snake._SPEED

    def move(self):
        """Moves the snake."""

        prev_coord = [segment.coord for segment in self.segments]
        for segment in self.segments[1:]:
            index = self.segments.index(segment)
            coord = prev_coord[index - 1]
            segment.coord = coord
        head_coord = self.segments[0].coord
        self.segments[0].coord = (
            head_coord[0] + self.direction[0] * SnakeSegment.SIZE,
            head_coord[1] + self.direction[1] * SnakeSegment.SIZE,
            head_coord[2] + self.direction[0] * SnakeSegment.SIZE,
            head_coord[3] + self.direction[1] * SnakeSegment.SIZE
        )

    def change_direction(self, event):
        """Changes the direction of the snake."""

        if event.keysym in Snake._DIRECTIONS:
            self.direction = Snake._DIRECTIONS[event.keysym]

    def change_speed(self):
        """Changes the speed of the snake."""

        if self.speed > 150:
            self.speed -= 10
        elif 80 < self.speed <= 150:
            self.speed -= 5
        elif 20 < self.speed <= 80:
            self.speed -= 2
        else:
            self.speed -= 1

    def add_segment(self):
        """Adds to the tail segment of a snake."""

        tail_coord = self.segments[-1].coord
        segment_coord = (
            tail_coord[2] - SnakeSegment.SIZE,
            tail_coord[3] - SnakeSegment.SIZE
        )
        self.segments.append(SnakeSegment(self.canvas_obj, segment_coord))
        self.change_speed()
