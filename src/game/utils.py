from dataclasses import dataclass
from enum import Enum

class State(Enum):
    IN_WORD = 1
    CORRECT_LOCATION = 2
    UNSEEN = 0

@dataclass
class DisplaySpecification:
    """Holding display specifications for WordyPy:
        - block_width: the width of each character in pixels
        - block_height: the height of each character in pixels
        - correct_location_color: the hex code to color the block when it is correct
        - incorrect_location_color: the hex code to color the block when it is in the wrong location but exists in the string
        - incorrect_color: the hex code to color the block when it is not in the string
        - space_between_letters: the amount of padding to put between characters, in pixels
        - word_color: the hex code of the background color of the string
    """
    block_width: int = 60
    block_height: int = 60
    correct_location_color: str = "#00274C"
    incorrect_location_color: str = "#FFCB05"
    incorrect_color: str = "#D3D3D3"
    space_between_letters: int = 5
    word_color: str = "#FFFFFF"