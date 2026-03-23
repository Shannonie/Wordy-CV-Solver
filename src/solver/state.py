from dataclasses import dataclass, field
from typing import List

@dataclass
class Letter:
    letter: str
    index: int
    in_correct_place: bool = False
    in_word: bool = False

    def is_in_correct_place(self) -> bool:
        return self.in_correct_place

    def is_in_word(self) -> bool:
        return self.in_word
    
    def __init__(self, letter, index=None):
        self.letter = letter
        self.index = index
        self.in_correct_place = False
        self.in_word = False

NUM_LETTER = 5

@dataclass
class SolverState:
    word_length: int = NUM_LETTER
    record_word: List[str] = field(default_factory=lambda: ["-"] * NUM_LETTER)
    letters_in_word: List[str] = field(default_factory=list)
    letters_out_of_word: List[str] = field(default_factory=list)

    def set_letter_state(self, pixel: tuple, letter: Letter, spec):
        """
        Determine letter state from pixel color
        """
        pixel_value = '#{:02X}{:02X}{:02X}'.format(*pixel)
    
        if pixel_value == spec.correct_location_color:
            letter.in_correct_place = True
            letter.in_word = True
        elif pixel_value == spec.incorrect_location_color:
            letter.in_word = True

    def update_statet(self, letter:Letter):
        """
        Update internal state based on feedback from a letter.
        """

        idx = letter.index
        char = letter.letter

        if letter.in_correct_place:
           self.record_word[idx] = char
        elif letter.in_word :
            if char not in self.letters_in_word:
                self.letters_in_word.append(char)
        else:
            if char not in self.letters_out_of_word:
                self.letters_out_of_word.append(char)

    def __str__(self):
        return (
            f"Pattern: {''.join(self.record_word)} | "
            f"In word: {self.letters_in_word} | "
            f"Not in word: {self.letters_out_of_word}"
        )