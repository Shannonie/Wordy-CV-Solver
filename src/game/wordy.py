from PIL import Image
from pathlib import Path
import random

from game.utils import DisplaySpecification, State
from game.renderer import WordyRenderer

class Wordy:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.display_spec = DisplaySpecification()
        self.word_list = self._load_words("data/words.txt")
        self.guess_list = []
        self.target_word = None
        self.known_pattern = [State.UNSEEN] * 5
        self.discovered_in_word = set()

        if self.debug:
            print(f"[DEBUG] Target Word: {self.target_word}")
    
    @staticmethod
    def _load_words(path: str) -> list[str]:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Word file not found: {path}")
        with open(p, "r", encoding="utf-8") as f:
            return list({line.strip().upper() for line in f})

    def _verify_guess(self, guess: str):
        """
        Raises ValueError if the guess violates previously revealed information.
        
        """
        # Enforce correct positions
        for idx, letter in enumerate(guess):
            if self.known_pattern[idx] == State.CORRECT_LOCATION and letter != self.target_word[idx]:
                raise ValueError(f"Letter '{letter}' at position {idx} must be '{self.target_word[idx]}'")

        # Enforce presence of known letters
        for letter in self.discovered_in_word:
            if letter not in guess:
                raise ValueError(f"Letter '{letter}' must appear in guess")

    def _evaluate_feedback(self, guess: str) -> list[State]:
        feedback = []

        for idx, letter in enumerate(guess):
            if letter == self.target_word[idx]:
                feedback.append(State.CORRECT_LOCATION)
            elif letter in self.target_word:
                feedback.append(State.IN_WORD)
                self.discovered_in_word.add(letter)
            else:
                feedback.append(State.UNSEEN)
        
        return feedback

    def _apply_guess(self, guess: str):
        feedback = self._evaluate_feedback(guess)

        # update known pattern (same logic as original)
        for i, code in enumerate(feedback):
            if code == State.CORRECT_LOCATION:
                self.known_pattern[i] = State.CORRECT_LOCATION
            elif code == State.IN_WORD and self.known_pattern[i] != State.CORRECT_LOCATION:
                self.known_pattern[i] = State.IN_WORD

        self.guess_list.append(guess)
        return feedback

    def get_display_spec(self) -> DisplaySpecification:
        if self.debug:
            print(self.display_spec)
        return self.display_spec

    def get_word_list(self) -> list[str]:
        return self.word_list
    
    def get_board_state(self, target_word_debug: str = None, guess_words_debug: list[str] = None) -> Image:
        """
        A WordPy board is a single PIL Image that uses the DisplaySpecification returned by get_display_spec().
        The image will have at least one row in it, and at most 5 rows (e.g. there is at least one guess left to be made).
        The board state will follow the rules of WordyPy.

        Args:
            target_word_debug: Optional, a string representing the target word which is only for testing a specific target word.
            guess_words_debug: Optional, a list of strings representing the guess words which is only for testing specific word guess combinations.
        Returns:
            An image representing the current state of the board
        """
        
        if self.target_word == None:
            self.target_word = random.choice(self.word_list)
            self.word_list.remove(self.target_word)
        
        original_target = self.target_word
        if target_word_debug:
            self.target_word = target_word_debug
        
        num_guesses = (random.randint(1, 5) if guess_words_debug is None else len(guess_words_debug))
        guesses: list[str] = []
        if guess_words_debug == None:
            for _ in range(num_guesses):
                guess = random.choice(self.word_list)
                self.word_list.remove(guess)
                guesses.append(guess)
        else:
            guesses = guess_words_debug
        
        if self.debug:
            print(f"Target Word: {self.target_word}\nNumber of Guesses: {num_guesses}\nGuesses: {guesses}")
        
        feedback_history = []
        for guess in guesses:
            feedback = self._apply_guess(guess)
            feedback_history.append(feedback)
        
        self.target_word = original_target

        renderer = WordyRenderer(self.display_spec)
        return renderer.render(guesses, feedback_history)

    def check_guess(self, guess: str) -> bool:
        """
        Process a guess and return True if it matches the target word, False otherwise.
        Updates internal guesses and feedback history for rendering.
        
        Args:
            guess: A string representing the user's guess for the target word.
        Returns:
            A boolean value indicating if the guess was correct or not.
        """
        if self.debug:
            print(f"New guess: {guess}")
            print(f"Last Target Word: {self.target_word}")
            print(f"Last Guesses: {self.guess_list}")
        
        if not isinstance(guess, str) or len(guess) != len(self.target_word):
            raise ValueError("Guess must match target word length")

        if guess in self.guess_list:
            raise ValueError("Duplicate guess.")
        
        self.guess_list.append(guess)

        if guess == self.target_word:
            return True
        
        self._verify_guess(guess)

        return False