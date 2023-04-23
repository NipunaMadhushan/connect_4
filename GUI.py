# import tkinter module
import tkinter as tk
from PIL import Image, ImageTk
from connect_4 import Connect4
from constants import *


class GUI:
    def __init__(self):
        self._connect_4 = Connect4()
        self._game_over = False

        self._window = tk.Tk()
        self._window.geometry("500x750")
        self._window.minsize(500, 750)
        self._window.maxsize(500, 750)
        self._window.title("Connect 4")

        self._starting_frame = tk.Frame(self._window)
        self._column_button_frame = tk.Frame(self._window)
        self._board_frame = tk.Frame(self._window)

        self.GREEN_BUTTON_IMG = self.__get_image(r"images\green_button.png", 20, 20)
        self.EMPTY_CELL_IMG = self.__get_image(r"images\empty_cell.png", 50, 50)
        self.GREY_CELL_IMG = self.__get_image(r"images\grey_cell.png", 50, 50)
        self.BLACK_CELL_IMG = self.__get_image(r"images\black_cell.png", 50, 50)

        self.info_text = tk.Label(self._starting_frame, text="", font=("Arial", 15), foreground="green", width=100)
        self.cell_UIs = []

        self.__include_initial_UI()

        self._starting_frame.pack(padx=1, pady=20)
        self._column_button_frame.pack(padx=20, pady=10)
        self._board_frame.pack(padx=40, pady=10)
        self._window.mainloop()

    def __include_initial_UI(self):
        heading = tk.Label(self._starting_frame, text="Connect 4",
                           font=("Arial", 20),
                           foreground="blue",
                           width=20)
        heading.pack(padx=20, pady=10)

        new_game_button = tk.Button(self._starting_frame, text="New Game", font=("Arial", 13),
                                    width=20, foreground="purple", background="yellow",
                                    command=self.on_new_game_button_clicked)
        new_game_button.pack(padx=20, pady=10)

        exit_button = tk.Button(self._starting_frame, text="Exit", font=("Arial", 13),
                                width=20, foreground="white", background="brown",
                                command=self.on_exit_button_clicked)
        exit_button.pack(padx=20, pady=20)

        self.info_text.pack(padx=20, pady=20)

    def __get_image(self, file_path, width, height):
        img = Image.open(file_path)
        img = img.resize((width, height))
        img = ImageTk.PhotoImage(img)

        return img

    def __include_column_select_buttons(self):
        for j in range(NO_COLUMNS):
            ct1 = tk.Label(self._column_button_frame, text="Column\n" + str(j + 1),
                           font=("Arial", 6),
                           foreground="black",
                           width=5)

            c1 = tk.Button(self._column_button_frame, image=self.GREEN_BUTTON_IMG, borderwidth=0,
                           command=self.__get_column_function(j))
            ct1.grid(row=0, column=j, padx=12.5, pady=0)
            c1.grid(row=1, column=j, padx=12.5, pady=0)

    def __get_column_function(self, column):
        if column == 0:
            return self.on_column_1_button_clicked
        elif column == 1:
            return self.on_column_2_button_clicked
        elif column == 2:
            return self.on_column_3_button_clicked
        elif column == 3:
            return self.on_column_4_button_clicked
        elif column == 4:
            return self.on_column_5_button_clicked
        elif column == 5:
            return self.on_column_6_button_clicked
        else:
            return self.on_column_7_button_clicked

    def __include_initial_grid(self):
        for i in range(NO_ROWS):
            cell_UI_row = []
            for j in range(NO_COLUMNS):
                cell = tk.Label(self._board_frame, image=self.EMPTY_CELL_IMG, width=50, height=50)
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell_UI_row.append(cell)
            self.cell_UIs.append(cell_UI_row)

    def __make_move(self, column):
        if not self._game_over:
            status = self._connect_4.update_on_player_move(column)
            if status:
                self.update_cell_UI(self._connect_4.stack_next_cells[column] - 1, column, GREY_CELL_TYPE)
                if self._connect_4.game_over:
                    self.update_info_text("Player won the game!", "green")
                    self._game_over = True
                else:
                    next_column = self._connect_4.make_AI_bot_move()
                    if next_column >= 0:
                        self.update_cell_UI(self._connect_4.stack_next_cells[next_column] - 1, next_column,
                                            BLACK_CELL_TYPE)
                        if self._connect_4.game_over:
                            self.update_info_text("Computer won the game!", "red")
                            self._game_over = True
                if not self._game_over and self._connect_4.no_moves >= 42:
                    self._game_over = True
                    self.update_info_text("Game was drawn!", "brown")
            else:
                self.update_info_text(f"Column {column + 1} is completely filled.\nPlease make another valid move",
                                      "red")

    def on_new_game_button_clicked(self):
        self._game_over = False
        self.cell_UIs = []
        self.update_info_text("", "green")
        self.__include_column_select_buttons()
        self.__include_initial_grid()
        self._connect_4.on_start_new_game()

    def on_exit_button_clicked(self):
        self._window.destroy()

    def on_column_1_button_clicked(self):
        self.__make_move(0)

    def on_column_2_button_clicked(self):
        self.__make_move(1)

    def on_column_3_button_clicked(self):
        self.__make_move(2)

    def on_column_4_button_clicked(self):
        self.__make_move(3)

    def on_column_5_button_clicked(self):
        self.__make_move(4)

    def on_column_6_button_clicked(self):
        self.__make_move(5)

    def on_column_7_button_clicked(self):
        self.__make_move(6)

    def update_info_text(self, text, color):
        self.info_text.config(text=text, foreground=color)

    def update_cell_UI(self, row, column, cell_type):
        if cell_type == GREY_CELL_TYPE:
            self.cell_UIs[row][column].config(image=self.GREY_CELL_IMG)
        else:
            self.cell_UIs[row][column].config(image=self.BLACK_CELL_IMG)


gui = GUI()
