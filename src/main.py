from game.wordy import Wordy
from solver.solver import WordySolver

def main():
    NUM_GUESS_MAX = 5
    wordy = Wordy(debug=False)
    spec = wordy.get_display_spec()
    word_list = wordy.get_word_list()
    solver = WordySolver(word_list)

    for i in range(NUM_GUESS_MAX):
        try:
            # Get an image of the current board state from wordy.
            # Note that the image contains some number of random guesses (always less than 5 guesses).
            board = wordy.get_board_state()
            board.show()

            # Create a new *good* guess based on the image and rules of wordy
            new_guess = solver.solve(board,spec)
            if wordy.check_guess(new_guess):
                print("Solved!")
                break
        except Exception as e:
            raise e

if __name__ == "__main__":
    main()