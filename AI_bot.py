import numpy as np
from constants import *


class Coordinates:
    def __init__(self, i, j):
        self.x = i
        self.y = j


class AIBot:
    def __init__(self):
        self._player_values = np.zeros((NO_ROWS, NO_COLUMNS), dtype=int)
        self._bot_values = np.zeros((NO_ROWS, NO_COLUMNS), dtype=int)
        self.__calculate_initial_values()

    def __calculate_initial_values(self):
        for i in range(NO_ROWS):
            for j in range(NO_COLUMNS):
                score = 0
                if i > 0:
                    for x in range(i-1, max(-1, i-4), -1):
                        score += EMPTY_CELL_VALUE
                # if i+1 < self.NO_ROWS:
                #     for x in range(i+1, min(self.NO_ROWS, i+4)):
                #         score += self.EMPTY_CELL_VALUE
                if j > 0:
                    for y in range(j-1, max(-1, j-4), -1):
                        score += EMPTY_CELL_VALUE
                if j < NO_COLUMNS - 1:
                    for x in range(j+1, min(NO_COLUMNS, j + 4)):
                        score += EMPTY_CELL_VALUE
                if i > 0 and j > 0:
                    k_min = min(i - max(-1, i - 4), j - max(-1, j - 4))
                    for k in range(1, k_min):
                        score += EMPTY_CELL_VALUE
                if i + 1 < NO_ROWS and j + 1 < NO_COLUMNS:
                    k_max = min(min(NO_ROWS, i + 4) - i, min(NO_COLUMNS, j + 4) - j)
                    for k in range(1, k_max):
                        score += EMPTY_CELL_VALUE
                if i > 0 and j + 1 < NO_COLUMNS:
                    k_min = min(i - max(-1, i - 4), min(NO_COLUMNS, j + 4) - j)
                    for k in range(1, k_min):
                        score += EMPTY_CELL_VALUE
                if i + 1 < NO_ROWS and j > 0:
                    k_max = min(min(NO_ROWS, i + 4) - i, j - max(-1, j - 4))
                    for k in range(1, k_max):
                        score += EMPTY_CELL_VALUE

                self._player_values[i, j] = score
                self._bot_values[i, j] = score

    def __update_column_values_of_own(self, board, cell: Coordinates, player):
        opponent = 3 - player
        values = self._player_values if player == PLAYER else self._bot_values

        # if cell.x > 0:
        #     for i in range(cell.x - 1, max(-1, cell.x - 4), -1):
        #         if board[i, cell.y] != opponent:
        #             if board[i, cell.y] == self.EMPTY:
        #                 values[i, cell.y] += self.SAME_CELL_VALUE
        #         else:
        #             break
        if cell.x + 1 < NO_ROWS:
            for i in range(cell.x + 1, min(NO_ROWS, cell.x + 4)):
                if board[i, cell.y] != opponent:
                    if board[i, cell.y] == EMPTY:
                        values[i, cell.y] += SAME_CELL_VALUE
                else:
                    break

    def __update_row_values_of_own(self, board, cell: Coordinates, player):
        opponent = 3 - player
        values = self._player_values if player == PLAYER else self._bot_values

        if cell.y > 0:
            for j in range(cell.y - 1, max(-1, cell.y - 4), -1):
                if board[cell.x, j] != opponent:
                    if board[cell.x, j] == EMPTY:
                        values[cell.x, j] += SAME_CELL_VALUE
                else:
                    break
        if cell.y + 1 < NO_COLUMNS:
            for j in range(cell.y + 1, min(NO_COLUMNS, cell.y + 4)):
                if board[cell.x, j] != opponent:
                    if board[cell.x, j] == EMPTY:
                        values[cell.x, j] += SAME_CELL_VALUE
                else:
                    break

    def __update_diagonal_values_of_own(self, board, cell: Coordinates, player):
        opponent = 3 - player
        values = self._player_values if player == PLAYER else self._bot_values

        if cell.x > 0 and cell.y > 0:
            k_min = min(cell.x - max(-1, cell.x - 4), cell.y - max(-1, cell.y - 4))
            for k in range(1, k_min):
                if board[cell.x - k, cell.y - k] != opponent:
                    if board[cell.x - k, cell.y - k] == EMPTY:
                        values[cell.x - k, cell.y - k] += SAME_CELL_VALUE
                else:
                    break
        if cell.x + 1 < NO_ROWS and cell.y + 1 < NO_COLUMNS:
            k_max = min(min(NO_ROWS, cell.x + 4) - cell.x, min(NO_COLUMNS, cell.y + 4) - cell.y)
            for k in range(1, k_max):
                if board[cell.x + k, cell.y + k] != opponent:
                    if board[cell.x + k, cell.y + k] == EMPTY:
                        values[cell.x + k, cell.y + k] += SAME_CELL_VALUE
                else:
                    break
        if cell.x > 0 and cell.y + 1 < NO_COLUMNS:
            k_min = min(cell.x - max(-1, cell.x - 4), min(NO_COLUMNS, cell.y + 4) - cell.y)
            for k in range(1, k_min):
                if board[cell.x - k, cell.y + k] != opponent:
                    if board[cell.x - k, cell.y + k] == EMPTY:
                        values[cell.x - k, cell.y + k] += SAME_CELL_VALUE
                else:
                    break
        if cell.x + 1 < NO_ROWS and cell.y > 0:
            k_max = min(min(NO_ROWS, cell.x + 4) - cell.x, cell.y - max(-1, cell.y - 4))
            for k in range(1, k_max):
                if board[cell.x + k, cell.y - k] != opponent:
                    if board[cell.x + k, cell.y - k] == EMPTY:
                        values[cell.x + k, cell.y - k] += SAME_CELL_VALUE
                else:
                    break

    def __update_column_values_of_opponent(self, board, cell: Coordinates, player):
        values = self._bot_values if player == PLAYER else self._player_values

        if cell.x > 0:
            for i in range(cell.x - 1, max(-1, cell.x - 4), -1):
                if board[i, cell.y] != player:
                    reduce_value = EMPTY_CELL_VALUE + SAME_CELL_VALUE
                    if board[i, cell.y] == EMPTY:
                        reduce_value = EMPTY_CELL_VALUE
                        values[i, cell.y] -= EMPTY_CELL_VALUE
                    for x in range(cell.x + 1, min(NO_ROWS, i + 4)):
                        if board[x, cell.y] != player:
                            if board[x, cell.y] == EMPTY:
                                values[x, cell.y] -= reduce_value
                        else:
                            break
                else:
                    break
        # if cell.x + 1 < self.NO_ROWS:
        #     for i in range(cell.x + 1, min(self.NO_ROWS, cell.x + 4)):
        #         if board[i, cell.y] != player:
        #             reduce_value = self.EMPTY_CELL_VALUE + self.SAME_CELL_VALUE
        #             if board[i, cell.y] == self.EMPTY:
        #                 reduce_value = self.EMPTY_CELL_VALUE
        #                 values[i, cell.y] -= self.EMPTY_CELL_VALUE
        #             for x in range(cell.x - 1, max(-1, i - 4), -1):
        #                 if board[x, cell.y] != player:
        #                     if board[x, cell.y] == self.EMPTY:
        #                         values[x, cell.y] -= reduce_value
        #                 else:
        #                     break
        #         else:
        #             break

    def __update_row_values_of_opponent(self, board, cell: Coordinates, player):
        values = self._bot_values if player == PLAYER else self._player_values

        if cell.y > 0:
            for j in range(cell.y - 1, max(0, cell.y - 4), -1):
                if board[cell.x, j] != player:
                    reduce_value = EMPTY_CELL_VALUE + SAME_CELL_VALUE
                    if board[cell.x, j] == EMPTY:
                        reduce_value = EMPTY_CELL_VALUE
                        values[cell.x, j] -= EMPTY_CELL_VALUE
                    for y in range(cell.y + 1, min(NO_COLUMNS, j + 4)):
                        if board[cell.x, y] != player:
                            if board[cell.x, y] == EMPTY:
                                values[cell.x, y] -= reduce_value
                        else:
                            break
                else:
                    break
        if cell.y + 1 < NO_COLUMNS:
            for j in range(cell.y + 1, min(NO_COLUMNS, cell.y + 4)):
                if board[cell.x, j] != player:
                    reduce_value = EMPTY_CELL_VALUE + SAME_CELL_VALUE
                    if board[cell.x, j] == EMPTY:
                        reduce_value = EMPTY_CELL_VALUE
                        values[cell.x, j] -= EMPTY_CELL_VALUE
                    for y in range(cell.y - 1, max(-1, j - 4), -1):
                        if board[cell.x, y] != player:
                            if board[cell.x, y] == EMPTY:
                                values[cell.x, y] -= reduce_value
                        else:
                            break
                else:
                    break

    def __update_diagonal_values_of_opponent(self, board, cell: Coordinates, player):
        values = self._bot_values if player == PLAYER else self._player_values

        if cell.x > 0 and cell.y > 0:
            k_min = min(cell.x - max(0, cell.x - 4), cell.y - max(0, cell.y - 4))
            for k in range(1, k_min):
                if board[cell.x - k, cell.y - k] != player:
                    reduce_value = EMPTY_CELL_VALUE + SAME_CELL_VALUE
                    if board[cell.x - k, cell.y - k] == EMPTY:
                        reduce_value = EMPTY_CELL_VALUE
                        values[cell.x - k, cell.y - k] -= EMPTY_CELL_VALUE
                    z_max = min(min(NO_ROWS, cell.x - k + 4) - cell.x,
                                min(NO_COLUMNS, cell.y - k + 4) - cell.y)
                    for z in range(0, z_max):
                        if board[cell.x + z, cell.y + z] != player:
                            if board[cell.x + z, cell.y + z] == EMPTY:
                                values[cell.x + z, cell.y + z] -= reduce_value
                        else:
                            break
                else:
                    break
        if cell.x + 1 < NO_ROWS and cell.y + 1 < NO_COLUMNS:
            k_max = min(min(NO_ROWS, cell.x + 4) - cell.x, min(NO_COLUMNS, cell.y + 4) - cell.y)
            for k in range(1, k_max):
                if board[cell.x + k, cell.y + k] != player:
                    reduce_value = EMPTY_CELL_VALUE + SAME_CELL_VALUE
                    if board[cell.x + k, cell.y + k] == EMPTY:
                        reduce_value = EMPTY_CELL_VALUE
                        values[cell.x + k, cell.y + k] -= EMPTY_CELL_VALUE
                    z_min = min(cell.x - max(-1, cell.x + k - 4), cell.y - max(-1, cell.y + k - 4))
                    for z in range(0, z_min):
                        if board[cell.x - z, cell.y - z] != player:
                            if board[cell.x - z, cell.y - z] == EMPTY:
                                values[cell.x - z, cell.y - z] -= reduce_value
                        else:
                            break
                else:
                    break
        if cell.x > 0 and cell.y + 1 < NO_COLUMNS:
            k_min = min(cell.x - max(0, cell.x - 4), min(NO_COLUMNS, cell.y + 4) - cell.y)
            for k in range(1, k_min):
                if board[cell.x - k, cell.y + k] != player:
                    reduce_value = EMPTY_CELL_VALUE + SAME_CELL_VALUE
                    if board[cell.x - k, cell.y + k] == EMPTY:
                        reduce_value = EMPTY_CELL_VALUE
                        values[cell.x - k, cell.y + k] -= EMPTY_CELL_VALUE
                    z_min = min(min(NO_ROWS, cell.x - k + 4) - cell.x, cell.y - max(-1, cell.y + k - 4))
                    for z in range(0, z_min):
                        if board[cell.x + z, cell.y - z] != player:
                            if board[cell.x + z, cell.y - z] == EMPTY:
                                values[cell.x + z, cell.y - z] -= reduce_value
                        else:
                            break
                else:
                    break
        if cell.x + 1 < NO_ROWS and cell.y > 0:
            k_max = min(min(NO_ROWS, cell.x + 4) - cell.x, cell.y - max(0, cell.y - 4))
            for k in range(1, k_max):
                if board[cell.x + k, cell.y - k] != player:
                    reduce_value = EMPTY_CELL_VALUE + SAME_CELL_VALUE
                    if board[cell.x + k, cell.y - k] == EMPTY:
                        reduce_value = EMPTY_CELL_VALUE
                        values[cell.x + k, cell.y - k] -= EMPTY_CELL_VALUE
                    z_max = min(cell.x - max(-1, cell.x + k - 4), min(NO_COLUMNS, cell.y - k + 4) - cell.y)
                    for z in range(0, z_max):
                        if board[cell.x - z, cell.y + z] != player:
                            if board[cell.x - z, cell.y + z] == EMPTY:
                                values[cell.x - z, cell.y + z] -= reduce_value
                        else:
                            break
                else:
                    break

    def update_player_values_for_player(self, board, cell: Coordinates):
        self._player_values[cell.x, cell.y] = 0
        self.__update_row_values_of_own(board, cell, PLAYER)
        self.__update_column_values_of_own(board, cell, PLAYER)
        self.__update_diagonal_values_of_own(board, cell, PLAYER)

    def update_bot_values_for_bot(self, board, cell: Coordinates):
        self._bot_values[cell.x, cell.y] = 0
        self.__update_row_values_of_own(board, cell, BOT)
        self.__update_column_values_of_own(board, cell, BOT)
        self.__update_diagonal_values_of_own(board, cell, BOT)

    def update_bot_values_for_player(self, board, cell: Coordinates):
        self._bot_values[cell.x, cell.y] = 0
        self.__update_row_values_of_opponent(board, cell, PLAYER)
        self.__update_column_values_of_opponent(board, cell, PLAYER)
        self.__update_diagonal_values_of_opponent(board, cell, PLAYER)

    def update_player_values_for_bot(self, board, cell: Coordinates):
        self._player_values[cell.x, cell.y] = 0
        self.__update_row_values_of_opponent(board, cell, BOT)
        self.__update_column_values_of_opponent(board, cell, BOT)
        self.__update_diagonal_values_of_opponent(board, cell, BOT)

    def __check_winning_move(self, board, cell: Coordinates):
        # Check column
        if cell.x > 2 and np.all(board[cell.x-3:cell.x, cell.y] == BOT):
            return True
        else:
            # Check rows
            for y in range(max(0, cell.y-3), min(NO_COLUMNS, cell.y + 4) - 3):
                if np.count_nonzero(board[cell.x, y:y+4] == BOT) >= 3:
                    return True

            # Check diagonals
            k_min_diff1 = max(max(0, cell.x-3)-cell.x, max(0, cell.y-3)-cell.y)
            k_max_diff1 = min(min(NO_ROWS, cell.x + 4) - cell.x - 3, min(NO_COLUMNS, cell.y + 4) - cell.y - 3)
            for z in range(k_min_diff1, k_max_diff1):
                if np.count_nonzero(np.diag(board[cell.x+z:cell.x+z+4, cell.y+z:cell.y+z+4]) == BOT) >= 3:
                    return True

            k_min_diff2 = max(max(0, cell.x-3) - cell.x, cell.y - min(NO_COLUMNS - 1, cell.y + 3))
            k_max_diff2 = min(min(NO_ROWS, cell.x + 4) - cell.x - 3, cell.y - 3 - max(-1, cell.y - 4))
            for z in range(k_min_diff2, k_max_diff2):
                if np.count_nonzero(np.diag(np.rot90(board[cell.x+z:cell.x+z+4, cell.y-z-3:cell.y-z+1])) == BOT) >= 3:
                    return True

        return False

    def __check_blocking_move(self, board, cell: Coordinates):
        # Check column
        if cell.x > 2 and np.all(board[cell.x-3:cell.x, cell.y] == PLAYER):
            return True
        else:
            # Check rows
            for y in range(max(0, cell.y - 3), min(NO_COLUMNS, cell.y + 4) - 3):
                if np.count_nonzero(board[cell.x, y:y + 4] == PLAYER) >= 3:
                    return True

            # Check diagonals
            k_min_diff1 = max(max(0, cell.x - 3) - cell.x, max(0, cell.y - 3) - cell.y)
            k_max_diff1 = min(min(NO_ROWS, cell.x + 4) - 3, min(NO_COLUMNS, cell.y + 4) - 3)
            for z in range(k_min_diff1, k_max_diff1):
                if np.count_nonzero(np.diag(board[cell.x+z:cell.x+z+4, cell.y+z:cell.y+z+4]) == PLAYER) >= 3:
                    return True

            k_min_diff2 = max(max(0, cell.x-3) - cell.x, cell.y - min(NO_COLUMNS - 1, cell.y + 3))
            k_max_diff2 = min(min(NO_ROWS, cell.x + 4) - cell.x - 3, cell.y - 3 - max(-1, cell.y - 4))
            for z in range(k_min_diff2, k_max_diff2):
                if np.count_nonzero(np.diag(np.rot90(board[cell.x+z:cell.x+z+4, cell.y-z-3:cell.y-z+1])) == PLAYER) >= 3:
                    return True

        return False

    def __check_double_blocking_move(self, board, cell: Coordinates):
        # Check rows
        for y in range(max(0, cell.y-4), min(NO_COLUMNS, cell.y + 5) - 4):
            if np.count_nonzero(board[cell.x, y:y+5] == PLAYER) == 2 and \
                    np.count_nonzero(board[cell.x, y:y+5] == EMPTY) == 3:
                if (cell.y > 0 and board[cell.x, cell.y-1] == PLAYER) or \
                        (cell.y + 1 < NO_COLUMNS and board[cell.x, cell.y + 1] == PLAYER):
                    return True

        # Check diagonals
        k_min_diff1 = max(max(0, cell.x-4)-cell.x, max(0, cell.y-4)-cell.y)
        k_max_diff1 = min(min(NO_ROWS, cell.x + 5) - 4, min(NO_COLUMNS, cell.y + 5) - 4)
        for z in range(k_min_diff1, k_max_diff1):
            if np.count_nonzero(np.diag(board[cell.x+z:cell.x+z+5, cell.y+z:cell.y+z+5]) == PLAYER) == 2 and \
                    np.count_nonzero(np.diag(board[cell.x+z:cell.x+z+5, cell.y+z:cell.y+z+5]) == EMPTY) == 3:
                if (cell.x > 0 and cell.y > 0 and board[cell.x-1, cell.y-1] == PLAYER) or \
                        (cell.x + 1 < NO_COLUMNS and cell.y + 1 < NO_COLUMNS and board[cell.x+1, cell.y+1] == PLAYER):
                    return True

        k_min_diff2 = max(max(0, cell.x-4) - cell.x, cell.y - min(NO_COLUMNS - 1, cell.y + 4))
        k_max_diff2 = min(min(NO_ROWS, cell.x + 5) - cell.x - 4, cell.y - 3 - max(-1, cell.y - 4))
        for z in range(k_min_diff2, k_max_diff2):
            if np.count_nonzero(np.diag(
                    np.rot90(board[cell.x+z:cell.x+z+5, cell.y-z-4:cell.y-z+1])) == PLAYER) == 2 and \
                    np.count_nonzero(np.diag(
                        np.rot90(board[cell.x+z:cell.x+z+5, cell.y-z-4:cell.y-z+1])) == EMPTY) == 3:
                if (cell.x > 0 and cell.y + 1 < NO_COLUMNS and board[cell.x - 1, cell.y + 1] == PLAYER) or \
                        (cell.x + 1 < NO_COLUMNS and cell.y > 0 and board[cell.x+1, cell.y-1] == PLAYER):
                    return True

        return False

    def get_next_move(self, board, stack_next_cells):
        # Check winning move
        for j in range(NO_COLUMNS):
            next_cell_row = stack_next_cells[j]
            if next_cell_row < NO_ROWS:
                is_bot_winning = self.__check_winning_move(board, Coordinates(next_cell_row, j))
                if is_bot_winning:
                    return j

        # Check blocking move
        for j in range(NO_COLUMNS):
            next_cell_row = stack_next_cells[j]
            if next_cell_row < NO_ROWS:
                is_player_winning = self.__check_blocking_move(board, Coordinates(next_cell_row, j))
                if is_player_winning:
                    return j

        # Check double blocking moves (player has possibility to win with two moves)
        double_blocking_moves = []
        for j in range(NO_COLUMNS):
            next_cell_row = stack_next_cells[j]
            if next_cell_row < NO_ROWS:
                is_player_winning_double_move = self.__check_double_blocking_move(board, Coordinates(next_cell_row, j))
                if is_player_winning_double_move:
                    double_blocking_moves.append(j)

        maximum_cell_value = 0
        next_column = -1

        # Evaluate double blocking move with maximum cell value
        if len(double_blocking_moves) > 0:
            for j in double_blocking_moves:
                next_cell_row = stack_next_cells[j]
                if next_cell_row < NO_ROWS:
                    value = max(self._player_values[next_cell_row, j], self._bot_values[next_cell_row, j])
                    if value > maximum_cell_value:
                        maximum_cell_value = value
                        next_column = j

        if next_column >= 0:
            return next_column

        # Evaluate random move with maximum cell value
        for j in range(NO_COLUMNS):
            next_cell_row = stack_next_cells[j]
            if next_cell_row < NO_ROWS:
                value = max(self._player_values[next_cell_row, j], self._bot_values[next_cell_row, j])
                if value > maximum_cell_value:
                    maximum_cell_value = value
                    next_column = j

        if next_column >= 0:
            return next_column

        return False

