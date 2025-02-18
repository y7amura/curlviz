from dataclasses import dataclass, field
from enum import IntEnum

from . import consts


class Team(IntEnum):
    """Team label

    Each stone on the sheet is basically owned by one of two teams: `Team.Team0` or `Team.Team1`.

    Items:
        Team0 (int): the label for team0
        Team1 (int): the label for team1
        Dummy (int): the label for non-existing team, defined to distinguish non-existing stones
    """

    Team0 = 0
    Team1 = 1
    Dummy = 2

    def is_entity(self) -> bool:
        """Returns `True` if self is either `Team.Team0` or `Team.Team1`

        This method checks whether self is an entity or a dummy.
        It returns `True` iff self is equal to either `Team.Team0` or `Team.Team1`, otherwise returns `False`.
        """
        return self == Team.Team0 or self == Team.Team1


@dataclass
class Stone:
    """A Stone on the sheet

    Attributes:
        x (float): x-coordinate of the stone
        y (float): y-coordinate of the stone
        team (Team): stone holder
    """

    x: float
    y: float
    team: Team = field(default=Team.Dummy)

    def __post_init__(self) -> None:
        self.team = Team(self.team)


@dataclass
class Sheet:
    """Curling sheet

    Attributes:
        config (Config): configuration of the sheet
        stones (List[Stone]): stones on the sheet
    """

    stones: list[Stone] = field(default_factory=lambda: [])

    def put(self, stone: Stone) -> None:
        """Puts a stone on the sheet

        Arguments:
            x (float): x-coordinate of the stone
            y (float): y-coordinate of the stone
            team (Team): stone holder

        Exceptions:
            This method raises a runtime error when too many stones are added.
            Currently, a sheet does not accept more than 16 stones.
        """
        if len(self.stones) > consts.MAX_NUM_OF_STONES:
            raise RuntimeError("Too many stones on a sheet.")
        self.stones.append(stone)

    def count_stones(self) -> int:
        """Returns the number of stones on the sheet

        This function counts the stones the sheet holds.
        This function will never return values greater than 16 or negative values.
        """
        return len(self.stones)
