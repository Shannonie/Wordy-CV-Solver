from PIL import Image, ImageFont, ImageDraw

from game.utils import State, DisplaySpecification

class WordyRenderer:
    def __init__(self, display_spec: DisplaySpecification = None):
        self.ds = display_spec
    
    def _render_letter(self, letter: str, state: int) -> Image:
        if state == State.CORRECT_LOCATION:
            color = self.ds.correct_location_color
        elif state == State.IN_WORD:
            color = self.ds.incorrect_location_color
        else:
            color = self.ds.incorrect_color
            
        block_img = Image.new("RGB", (self.ds.block_width, self.ds.block_height), color)

        try:
            font = ImageFont.truetype("data/Roboto-Bold.ttf", 50)
        except:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(block_img)
        draw.text((self.ds.block_width // 2, self.ds.block_height // 2), letter,
                  anchor="mm", font=font)

        return block_img
    
    def render(self, guesses: list[str], feedback_history: list[list[int]]) -> Image:
        word_len = len(guesses[0])
        width = word_len * self.ds.block_width + (word_len - 1) * self.ds.space_between_letters
        height = len(guesses) * self.ds.block_height

        image = Image.new("RGB", (width, height), color=self.ds.word_color)

        for row, guess in enumerate(guesses):
            for col, letter in enumerate(guess):
                block_img = self._render_letter(letter, feedback_history[row][col])
                x = col * (self.ds.block_width + self.ds.space_between_letters)
                y = row * self.ds.block_height
                image.paste(block_img, (x, y))

        return image