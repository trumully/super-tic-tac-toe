from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(slots=True)
class Grid:
    """A grid data structure.

    Parameters:
        rows (int): The number of rows in the grid.
        columns (int): The number of columns in the grid.
        empty_value (Any, optional): Represents empty space in the grid.
                                     Defaults to None.
    """

    rows: int
    columns: int
    empty_value: Optional[Any] = None
    _grid: list[list[Any]] = field(init=False)

    def __post_init__(self) -> None:
        if self.rows <= 0:
            raise ValueError("Rows must be greater than 0")
        if self.columns <= 0:
            raise ValueError("Columns must be greater than 0")
        self._grid = self.make_grid()

    def check_index(self, x: int, y: int) -> None:
        """Check if the given index is within the grid bounds.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.

        Raises:
            IndexError: If the index is out of bounds for x or y.
        """
        if not (0 <= x < self.rows):
            raise IndexError(f"X coordinate out of range: {x}")
        if not (0 <= y < self.columns):
            raise IndexError(f"Y coordinate out of range: {y}")

    def make_grid(self) -> list[list[Any]]:
        """Generate a 2D grid with the specified number of rows, columns, and empty
        value.

        Returns:
            list[list[Any]]: A 2D grid.
        """
        return [
            [self.empty_value for _ in range(self.columns)] for _ in range(self.rows)
        ]

    def set_at(self, value: Any, *, x: int, y: int) -> None:
        """Set the value at the given x, y coordinates.

        Args:
            value (Any): The value to set.
            x (int): The x coordinate.
            y (int): The y coordinate.
        """
        self.check_index(x, y)
        self._grid[y][x] = value

    def get_at(self, x: int, y: int) -> Any:
        """Get the value at the given x, y coordinates.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.

        Returns:
            Any: The value at the given x, y coordinates.
        """
        self.check_index(x, y)
        return self._grid[y][x]

    def __str__(self) -> str:
        return "\n".join(
            [
                " ".join([str(self._grid[y][x]) for x in range(self.columns)])
                for y in range(self.rows)
            ]
        )
