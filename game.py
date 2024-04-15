from dataclasses import dataclass, field
from typing import Any, Optional

from grid import Grid

DRAW = "DRAW"


@dataclass
class TicTacToe(Grid):
    """A class to represent a Tic-tac-toe game.

    Attributes
        grid (Grid): The grid of the game.
        circle (Any): The symbol for the circle player.
        cross (Any): The symbol for the cross player.
    """

    empty_value: Optional[Any] = "-"

    circle: Any = "o"
    cross: Any = "x"

    @property
    def winning_combinations(self) -> list[list[tuple[int, int]]]:
        return (
            # Rows
            [[(i, j) for j in range(self.columns)] for i in range(self.rows)]
            +
            # Columns
            [[(i, j) for i in range(self.rows)] for j in range(self.columns)]
            +
            # Main diagonal
            [[(i, i) for i in range(min(self.rows, self.columns))]]
            +
            # Secondary diagonal
            [[(i, self.columns - i - 1) for i in range(min(self.rows, self.columns))]]
        )

    @property
    def players(self) -> tuple[Any, Any]:
        return self.circle, self.cross

    def get_winner(self) -> Optional[Any]:
        """Get the winner of the game.

        Returns:
            Optional[Any]: The winner of the game, None if there is no winner, or DRAW
            if the game is a draw.
        """
        for player in self.players:
            for combination in self.winning_combinations:
                if all(self.get_at(x, y) == player for x, y in combination):
                    return player
        return DRAW if self.check_for_draw() else None

    def check_for_draw(self) -> bool:
        for i in range(self.rows):
            for j in range(self.columns):
                if self.is_legal_move(i, j):
                    return False
        return True

    def is_legal_move(self, x: int, y: int) -> bool:
        """Check if a move is legal.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        try:
            self.check_index(x, y)
        except IndexError:
            return False
        return self.get_at(x, y) is self.empty_value

    def make_move(self, player: Any, *, x: int, y: int) -> bool:
        """Make a move in the game.

        Args:
            player (Any): The player making the move.
            x (int): The x coordinate.
            y (int): The y coordinate.
        """
        if is_valid := self.is_legal_move(x, y):
            self.set_at(player, x=x, y=y)
        return is_valid


def make_tictactoe(rows: int = 3, columns: int = 3) -> TicTacToe:
    return TicTacToe(rows, columns)


@dataclass
class SuperTicTacToe(TicTacToe):
    """A class to represent a Super Tic-tac-toe game. Unlike regular Tic-tac-toe,
    separate tic-tac-toe games fill up each square in the grid. The player making the
    first move can start in any of the games like they would in a regular game. The
    next player must move in the game corresponding to the square of the previous move.

    i.e: If the first move was the top-right square in the middle game, the next player
    must make a move in the top-right game.

    Once a grid game is won, that square is considered "earned" by the player who
    won it.

    Special Cases:
        - If a grid game draws, it remains un-earned.
        - If the entire game draws, the winner is the player with the most earned
          squares.
    """

    inner_rows: int = 3
    inner_columns: int = 3
    moves: dict[Any, list[tuple[int, int]]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._grid = [
            [
                make_tictactoe(self.inner_rows, self.inner_columns)
                for _ in range(self.columns)
            ]
            for _ in range(self.rows)
        ]
        # [(co-ords in grid), (co-ords of grid)]
        self.moves = {player: [] for player in self.players}
        self.current_player = self.cross
        self.previous_player = self.circle

    @property
    def inner_height(self) -> int:
        return self.get_at(0, 0).rows

    @property
    def inner_width(self) -> int:
        return self.get_at(0, 0).columns

    def cycle_players(self) -> Any:
        self.current_player, self.previous_player = (
            self.previous_player,
            self.current_player,
        )

    def play(self) -> None:
        print(self)
        while self.get_winner() is None:
            player = self.current_player
            self.make_move(player, self.get_move(player))
            print(self)
            self.cycle_players()

    def input_move(self, msg: str) -> tuple[int, int]:
        x, y = map(int, input(msg + " ").split(","))
        try:
            self.check_index(x, y)
        except IndexError:
            print("Invalid coordinates. Try again.")
            return self.input_move()
        return x, y

    def get_move(self, player: Any) -> list[tuple[int, int]]:

        if (forced_move := self.get_forced_move()) is None:
            while not self.is_legal_move(
                *(
                    grid_chosen := self.input_move(
                        f"{player} | choose a grid to play in (x, y):"
                    )
                )
            ):
                print("Invalid grid. Try again.")
        else:
            grid_chosen = forced_move
        grid = self.get_at(*grid_chosen)
        while not grid.is_legal_move(
            *(
                square_chosen := self.input_move(
                    f"{player} | choose a square to play in (x, y):"
                )
            )
        ):
            print("Invalid square. Try again.")

        return [square_chosen, grid_chosen]

    def make_move(self, player: Any, move: list[tuple[int, int]]) -> None:
        grid_x, grid_y = move[1]
        square_x, square_y = move[0]
        grid_game = self.get_at(grid_x, grid_y)
        if grid_game.make_move(player, x=square_x, y=square_y):
            self.moves[player].append(move)

    def is_legal_move(self, x: int, y: int) -> bool:
        try:
            self.check_index(x, y)
        except IndexError:
            return False

        is_draw = self.get_at(x, y).get_winner() == DRAW
        forced = self.get_forced_move()
        if forced is None:
            return not is_draw
        return not is_draw and (x, y) == forced

    def get_forced_move(self) -> Optional[tuple[int, int]]:
        if all(len(m) == 0 for m in self.moves.values()):
            return None
        return self.moves[self.previous_player][-1][0]

    def set_at(self, value: Any, *, x1: int, y1: int, x2: int, y2: int) -> None:
        """Set the value at the given x, y coordinates.

        Args:
            value (Any): The value to set.
            x1 (int): The x coordinate of the grid game.
            y1 (int): The y coordinate of the grid game.
            x2 (int): The x coordinate of the square in the grid game.
            y2 (int): The y coordinate of the square in the grid game.
        """
        grid_game: TicTacToe = self.get_at(x1, y1)
        grid_game.set_at(value, x=x2, y=y2)

    def get_at(
        self, x1: int, y1: int, *, x2: Optional[int] = None, y2: Optional[int] = None
    ) -> TicTacToe | Any:
        """Get the value at the given x, y coordinates.

        Args:
            x1 (int): The x coordinate of the grid game.
            y1 (int): The y coordinate of the grid game.
            x2 (int, optional): The x coordinate of the square in the grid game.
            y2 (int, optional): The y coordinate of the square in the grid game.

        Returns:
            TicTacToe | Any: Either the grid at x1, y1 or the value at x2, y2 within the
            grid at x1, y1.
        """
        grid = self._grid[y1][x1]
        if x2 is None and y2 is None:
            return grid
        return grid.get_at(x=x2, y=y2)

    def get_winner(self) -> Any:
        """Get the winner of the game.

        Returns:
            Any: The winner of the game.
        """
        for player in self.players:
            for combination in self.winning_combinations:
                if all(
                    self.get_at(x, y).get_winner() == player for x, y in combination
                ):
                    return player
        if self.check_for_draw():
            return max(self.get_wins(player) for player in self.players)

    def get_wins(self, player: Any) -> int:
        return len(
            [grid.get_winner() for grid in self._grid if grid.get_winner() == player]
        )

    def check_for_draw(self) -> bool:
        for game in self._grid:
            for grid in game:
                if grid.get_winner() is None:
                    return False
        return True

    def __str__(self) -> str:
        result = ""

        for i in range(self.rows):
            rows = [str(self._grid[i][j]).split("\n") for j in range(self.columns)]

            for k in range(self.inner_width):
                row_str = " | ".join(rows[j][k] for j in range(self.columns))
                result += row_str + "\n"

            if i < self.rows - 1:
                result += ("-" * len(row_str)) + "\n"

        return result[:-1]


def make_super_tictactoe(
    rows: int = 3, columns: int = 3, *, inner_rows: int = 3, inner_columns: int = 3
) -> SuperTicTacToe:
    return SuperTicTacToe(
        rows, columns, inner_rows=inner_rows, inner_columns=inner_columns
    )


def main():
    # Initialize the game
    game = make_super_tictactoe()

    game.play()


if __name__ == "__main__":
    main()
