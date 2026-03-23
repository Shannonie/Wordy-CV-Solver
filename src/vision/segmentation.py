from typing import List
from PIL import Image

from game.utils import DisplaySpecification

def split_board(board:Image.Image, spec:DisplaySpecification) -> List[List[Image.Image]]:
    """
    Split the board image into a 2D list of letter image segments.

    Args:
        board: Full board image
        spec: DisplaySpecification (block size, spacing)
    Returns:
        List of rows, each row is a list of letter images
    """

    NUM_COLUMN = 5
    rows = board.height // spec.block_height    
    segments = []

    for row in range(rows):
        row_segments = []

        for col in range(NUM_COLUMN):
            left = col * (spec.block_width + spec.space_between_letters)
            top = row * spec.block_height
            right = left + spec.block_width
            bottom = top + spec.block_height

            segment = board.crop((left, top, right, bottom))
            row_segments.append(segment)

        segments.append(row_segments)

    return segments