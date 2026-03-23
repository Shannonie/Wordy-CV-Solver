import random
from typing import List
from PIL import Image

from vision.ocr import extract_letter
from vision.segmentation import split_board
from solver.state import SolverState, Letter

class WordySolver:
    def __init__(self, word_list:List[str]):
        self.word_list = word_list.copy()
        self.solve_state = SolverState()

    def _make_guess(self) -> str:
        candidates = self.word_list.copy()

        # Filter by known correct positions
        for idx, letter in enumerate(self.solve_state.record_word):
            if letter != "-":
                candidates = [word for word in candidates if word[idx] == letter]
        
        # Filter words that must contain certain letters
        candidates = [word for word in candidates
                      if all(letter in word for letter in self.solve_state.letters_in_word)]
        
        # Remove words with excluded letters
        for letter in self.solve_state.letters_out_of_word:
            candidates = [word for word in candidates if letter not in word]

        if not candidates:
            raise ValueError("No candidates left to guess.")

        return random.choice(candidates)

    def _process_board(self, board:Image, spec):
        """
        Extract letters from board and update solver state
        """

        segments = split_board(board, spec)
        for row_segments in segments:
            for col, segment in enumerate(row_segments):
                letter_char = extract_letter(segment)

                if not letter_char:
                    continue
                
                letter = Letter(letter_char[0], col)
                pixel = segment.getpixel((0, 0))
                self.solve_state.set_letter_state(pixel, letter, spec)
                self.solve_state.update_statet(letter)

    def solve(self, board:Image, spec) -> str:
        """
        Query the wordy module and make a guess for the word.

        Args:
        board: An image representing the current state of the board from wordy.
        Returns: A guessed word based on the game board state.
        """
        
        self._process_board(board, spec)
        new_guess = self._make_guess()

        # remove guessed word to avoid repetition
        if new_guess in self.word_list:
            self.word_list.remove(new_guess)

        return new_guess