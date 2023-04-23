import numpy as np
from colorama import Fore, Style
from AI_bot import AIBot
from constants import *


class Coordinates:
    def __init__(self, i, j):
        self.x = i
        self.y = j


class Connect4:
    def __init__(self):
        self.SINGLE_PLAYER = 1
        self.MULTI_PLAYER = 2

        self._board = np.zeros((NO_ROWS, NO_COLUMNS), dtype=int)
        self.stack_next_cells = [0 for _ in range(NO_COLUMNS)]
        self._AI_bot = AIBot()

        self.game_over = False
        self.no_moves = 0

    def __print_board(self):
        for i in range(NO_ROWS - 1, -1, -1):
            num = str(i)
            if i < 10:
                num = "0" + num
            print(Fore.CYAN + num, end=" ")
            for j in range(NO_COLUMNS):
                if self._board[i][j] == EMPTY:
                    print(Fore.WHITE + " .", end=" ")
                elif self._board[i][j] == PLAYER:
                    print(Fore.GREEN + " P", end=" ")
                else:
                    print(Fore.RED + " B", end=" ")
            print()

        print("   ", end="")
        for i in range(NO_COLUMNS):
            num = str(i)
            if i < 10:
                num = "0" + num
            print(Fore.CYAN + num, end=" ")
        print()

        print(Style.RESET_ALL)

    def __print_separate_line(self):
        print(Fore.GREEN + "---------------------------------------------------", end="")
        print()
        print(Style.RESET_ALL)

    def __print_input_error_msg(self):
        print(Fore.RED + "Your move is not valid", end="")
        print()
        print(Style.RESET_ALL)

    def __print_AIbot_error_msg(self):
        print(Fore.RED + "AI bot failed to deliver the next move", end="")
        print()
        print(Style.RESET_ALL)

    def __print_winning_msg(self, player, player_mode):
        if player == PLAYER or player_mode == self.MULTI_PLAYER:
            print(Fore.GREEN + f"Player {player} Won", end="")
        else:
            print(Fore.RED + f"AI Bot Won", end="")
        print()
        print(Style.RESET_ALL)

    def __update_stack_next_cell(self, column):
        self.stack_next_cells[column] += 1

    def __set_move(self, player, column):
        if column < 0 or column >= NO_COLUMNS:
            return False

        i = self.stack_next_cells[column]
        if i >= NO_ROWS:
            return False

        if self._board[i, column] != EMPTY:
            return False

        self._board[i, column] = player
        self.__update_stack_next_cell(column)
        self.no_moves += 1
        if player == PLAYER:
            self._AI_bot.update_player_values_for_player(self._board, Coordinates(i, column))
            self._AI_bot.update_bot_values_for_player(self._board, Coordinates(i, column))
        else:
            self._AI_bot.update_bot_values_for_bot(self._board, Coordinates(i, column))
            self._AI_bot.update_player_values_for_bot(self._board, Coordinates(i, column))
        return True

    def __check_winning(self, last_column, player):
        last_row = self.stack_next_cells[last_column]-1
        # Check column
        if last_row > 2 and np.all(self._board[last_row - 3:last_row + 1, last_column] == player):
            return True
        else:
            # Check rows
            for y in range(max(0, last_column-3), min(NO_COLUMNS, last_column + 4) - 3):
                if np.all(self._board[last_row, y:y + 4] == player):
                    return True

            # Check diagonals
            k_min_diff1 = max(max(0, last_row-3)-last_row, max(0, last_column-3)-last_column)
            k_max_diff1 = min(min(NO_ROWS, last_row + 4) - last_row - 3,
                              min(NO_COLUMNS, last_column + 4) - last_column - 3)
            for z in range(k_min_diff1, k_max_diff1):
                if np.all(np.diag(self._board[last_row + z:last_row + z + 4, last_column + z:last_column + z + 4]) == player):
                    return True

            k_min_diff2 = max(max(0, last_row-3) - last_row, last_column - min(NO_COLUMNS - 1, last_column + 3))
            k_max_diff2 = min(min(NO_ROWS, last_row + 4) - last_row - 3, last_column - 3 - max(-1, last_column - 4))
            for z in range(k_min_diff2, k_max_diff2):
                if np.all(np.diag(
                        np.rot90(self._board[last_row + z:last_row + z + 4, last_column - z - 3:last_column - z + 1])) == player):
                    return True

        return False

    def play_without_GUI(self, player_mode):
        player = 1
        while not self.game_over and self.no_moves < 42:
            if player == PLAYER:
                self.__print_board()
                print("PLAYER 1's Move...")
                try:
                    next_column = int(input("Enter your next move (column number): ").strip())
                    status = self.__set_move(player, next_column)
                    if not status:
                        self.__print_input_error_msg()
                        self.__print_separate_line()
                        continue
                except ValueError:
                    self.__print_input_error_msg()
                    self.__print_separate_line()
                    continue

            else:
                if player_mode == self.SINGLE_PLAYER:
                    next_column = self._AI_bot.get_next_move(self._board, self.stack_next_cells)
                    print("AI's Move: column " + str(next_column))
                    if next_column >= 0:
                        status = self.__set_move(player, next_column)
                        if not status:
                            self.__print_input_error_msg()
                            self.__print_separate_line()
                            continue
                    else:
                        self.__print_AIbot_error_msg()
                        self.__print_separate_line()
                        continue
                else:
                    self.__print_board()
                    print("PLAYER 2's Move...")
                    try:
                        next_column = int(input("Enter your next move (column number): ").strip())
                        status = self.__set_move(player, next_column)
                        if not status:
                            self.__print_input_error_msg()
                            self.__print_separate_line()
                            continue
                    except ValueError:
                        self.__print_input_error_msg()
                        self.__print_separate_line()
                        continue

            self.__print_separate_line()

            is_winning = self.__check_winning(next_column, player)
            if is_winning:
                self.__print_board()
                self.__print_winning_msg(player, player_mode)
                self.game_over = True

            player = 3 - player

    def update_on_player_move(self, next_column):
        try:
            status = self.__set_move(PLAYER, next_column)
            if not status:
                self.__print_input_error_msg()
                self.__print_separate_line()
                return False
            self.no_moves += 1
            is_winning = self.__check_winning(next_column, PLAYER)
            if is_winning:
                self.__print_board()
                self.__print_winning_msg(PLAYER, self.SINGLE_PLAYER)
                self.game_over = True
        except ValueError:
            self.__print_input_error_msg()
            self.__print_separate_line()
            return False

        return True

    def make_AI_bot_move(self):
        next_column = self._AI_bot.get_next_move(self._board, self.stack_next_cells)
        print("AI's Move: column " + str(next_column))
        if next_column >= 0:
            status = self.__set_move(BOT, next_column)
            if not status:
                self.__print_input_error_msg()
                self.__print_separate_line()
                return False
            self.no_moves += 1
            is_winning = self.__check_winning(next_column, BOT)
            if is_winning:
                self.__print_board()
                self.__print_winning_msg(BOT, self.SINGLE_PLAYER)
                self.game_over = True
        else:
            self.__print_AIbot_error_msg()
            self.__print_separate_line()
            return False

        return next_column

    def on_start_new_game(self):
        self._board = np.zeros((NO_ROWS, NO_COLUMNS), dtype=int)
        self.stack_next_cells = [0 for _ in range(NO_COLUMNS)]
        self._AI_bot = AIBot()

        self.game_over = False
        self.no_moves = 0
