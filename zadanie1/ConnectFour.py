# Author: Adrian Paczewski
# Author: Kamil Kornatowski
# game description: https://en.wikipedia.org/wiki/Connect_Four


# pip install easyAI
# pip install numpy
import numpy as np
from easyAI import TwoPlayerGame, Human_Player


class ConnectFour(TwoPlayerGame):

    def __init__(self, players):
        """
        Define board, players
        Parameters:
            players (list): List of players which will play the game
        Returns:
            Self object.
        """
        self.players = players
        self.board = np.array([[0 for _ in range(7)] for _ in range(6)])  # initialize 6x7 board
        self.current_player = 1  # player 1 starts

    def possible_moves(self):
        """
        Returns:
            List of possible moves.
        """
        return [i for i in range(7) if (self.board[:, i].min() == 0)]  # return column indexes where minimum value is 0

    def make_move(self, column):
        """
        Define how to make a move
        Parameters:
            column (list): selected column
        """
        line = np.argmin(self.board[:, column] != 0)  # return first occurrence of a non-zero element in given column
        self.board[line, column] = self.current_player  # set player move in the game board

    def show(self):
        """
        Print game board in console
        """
        print('\n' + '\n'.join(
            ['0 1 2 3 4 5 6', 13 * '-'] +
            [' '.join([['.', 'O', 'X'][self.board[5 - j][i]]
                       for i in range(7)]) for j in range(6)]))

    def win(self):
        """
        Check win condition
        Returns:
            Bool: True or False
        """
        return find_four(self.board, self.opponent_index)  # return true if four in the row

    def is_over(self):
        """
        Check if the game is over
        Returns:
            Bool: True or False
        """
        return (self.board.min() > 0) or self.win()  # return true if board is full or win() is true

    def scoring(self):
        """
        Define score for win and lose
        Returns:
            int: Score
        """
        return 100 if self.win() else 0  # return 100 if win and 0 if lose


def find_four(board, current_player):
    """
    The code is evaluating the game board for a winning condition by checking
    for a sequence of four identical tokens in a row, column, or diagonal.

    POS_DIR is a list of starting positions and corresponding directions.
    Each POS_DIR entry is a pair [position, direction], where 'position' is a starting position and 'direction'
    is a movement direction.

    Parameters:
        board (array): game board
        current_player (int): Index of the opponent player
    Returns:
        Bool: True or False
    """
    for position, direction in POS_DIR:
        streak = 0
        while (0 <= position[0] <= 5) and (
                0 <= position[1] <= 6):  # check if the position is within the bounds of the game board
            if board[position[0], position[
                1]] == current_player:  # check if the token at the current position is equal to current_player
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
            position = position + direction  # each iteration position is updated by adding direction
    return False


# define starting positions with direction
POS_DIR = (
    np.array([[[i, 0], [0, 1]] for i in range(6)] +  # rows [0, 0] to [5, 0] in direction [0, 1]
             [[[0, i], [1, 0]] for i in range(7)] +  # columns [0, 0] to [0, 6] in direction [1, 0]
             [[[i, 0], [1, 1]] for i in range(1, 3)] +  # diagonals from top-left to bottom-right for the first two rows
             [[[0, i], [1, 1]] for i in range(4)] + # diagonals from top-left to bottom-right for the first four columns
             [[[i, 6], [1, -1]] for i in range(1, 3)] + # diagonals from top-right to bottom-left for the first two rows
             [[[0, i], [1, -1]] for i in range(3, 7)]))  # diagonals from top-right to bottom-left for the last four columns

if __name__ == '__main__':

    from easyAI import AI_Player, Negamax

    ai = Negamax(5)
    ai2 = Negamax(5)
    game = ConnectFour([AI_Player(ai), Human_Player()])
    game.play()
    if game.win():
        print("Player %d wins." % game.opponent_index)
    else:
        print("It's a draw.")
