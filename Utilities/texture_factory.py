from typing import List
from PIL import Image, ImageFont, ImageDraw
from texture_colors import COLORS
from game_board import GameBoard


class TextureFactory:
    def __init__(self, boards: List[GameBoard]):
        self.boards = boards

    def generate_textures(self):
        for file_num, board in enumerate(self.boards):
            image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            cell_size = 1024 // board.cols
            font = ImageFont.truetype("arial", cell_size)
            offset = (1024 - (cell_size * board.cols)) // 2 - 1
            w, h = draw.textsize('8', font=font)
            h += int(h * 0.21)

            for row_num, row in enumerate(board.solution):
                for col_num, symbol in enumerate(row):
                    color = COLORS[int(symbol) % (len(COLORS) - 1)]
                    curr_x = int(col_num * cell_size) + offset
                    curr_y = int(row_num * cell_size) + offset

                    if board.board[row_num][col_num] == -1:
                        draw.rectangle(
                            [(curr_x, curr_y),
                             (curr_x + cell_size, curr_y + cell_size)],
                            fill=color,
                            outline='black',
                            width=2
                            )
                    else:
                        draw.rectangle(
                            [(curr_x, curr_y),
                             (curr_x + cell_size, curr_y + cell_size)],
                            fill=color,
                            outline='black',
                            width=2
                            )
                        text = str(board.board[row_num][col_num])
                        draw.text(
                            (curr_x + (cell_size - w) / 2,
                             curr_y + (cell_size - h) / 2),
                            text=text, fill='black', font=font)
                    curr_x += cell_size
                    curr_y += cell_size
            image.save('textures/' + str(file_num) + '.png', 'PNG')