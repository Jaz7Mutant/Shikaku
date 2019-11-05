import glob
from board import Board
from rectangle import Rectangle
from point import Point
import colorama


def main():
    colorama.init()
    filenames = sorted(glob.glob("puzzles/*.txt"))
    for filename in filenames:
        board = Board()
        board.read_board(filename)
        print(filename)
        _update_blocks_factors(board)
        count = [0] * len(board.blocks)
        board.solution = [[-1 for c in range(board.cols)] for r in
                          range(board.rows)]
        for i in range(len(board.blocks)):
            board.solution[board.blocks[i].row][
                board.blocks[i].col] = i  # todo

        for z in range(len(board.blocks)):
            irow = board.blocks[z].row
            icol = board.blocks[z].col
            ivalue = board.blocks[z].value
            faclist = board.blocks[z].factors
            for fac in faclist:
                for i in range(ivalue // fac):
                    for j in range(fac):
                        top_left = Point(icol + i - ivalue // fac + 1,
                                         irow - j)
                        bottom_right = Point(icol + i, irow + fac - 1 - j)
                        try:
                            # rect = Rectangle(board, top_left, bottom_right, Color(z))
                            rect = Rectangle(board, top_left, bottom_right, z)
                            rect.draw_rectangle()
                        except AssertionError:
                            continue

        last_cells = [[] for i in range(len(board.blocks))]
        for row in range(board.rows):
            for col in range(board.cols):
                # value = Color(board.solution[row][col]).value
                value = board.solution[row][col]
                last_cells[value].append([row, col])

        board.solution = [[-1 for c in range(board.cols)] for r in
                          range(board.rows)]
        for i in range(len(board.blocks)):
            board.solution[board.blocks[i].row][board.blocks[i].col] = i

        backtrack(0, board, count, last_cells)
        board.print_solution()


def backtrack(nexti: int, board: Board, count: list, last_cells: list):
    # stop backtracking when it has looped through all the anchors,
    # which means a solution is found
    if nexti > len(board.blocks) - 1:
        return True

    # set row, column, and value of the current anchor
    irow = board.blocks[nexti].row
    icol = board.blocks[nexti].col
    ivalue = board.blocks[nexti].value

    # while the counter for the current nexti hasn't reached the end of the factor
    # list for the current nexti
    while count[nexti] < len(board.blocks[nexti].factors):
        # a list of all the factors of the value of current nexti
        faclist = board.blocks[nexti].factors
        # the current factor being processed
        fac = faclist[count[nexti]]
        # loop through all the valid rectangles of size fac by ivalue/fac
        for i in range(ivalue // fac):
            for j in range(fac):
                # if the rectangle in the current position is vaild and it only has values -1 and
                # the index of the current anchor, set values in that rectangle to the index of the
                # current anchor, and then call recursion to the next anchor
                top_left = Point(icol + i - ivalue // fac + 1, irow - j)
                bottom_right = Point(icol + i, irow + fac - 1 - j)
                try:
                    # rect = Rectangle(board, top_left, bottom_right, Color(nexti))
                    rect = Rectangle(board, top_left, bottom_right, nexti)
                    if not rect.check_conflicts():
                        rect.draw_rectangle()
                        notCover = False
                        for z in range(len(last_cells[nexti])):
                            r = last_cells[nexti][z][0]
                            c = last_cells[nexti][z][1]
                            if board.solution[r][c] == -1:
                                notCover = True
                                break
                        if notCover == False:
                            # if the recursion returns True, which means a solution is found,
                            # keep returning true until the very first level of recursion
                            if backtrack(nexti + 1, board, count,
                                         last_cells) == True:
                                return True
                        # if recursion doesn't return True or some last cells are not covered,
                        # set the values in that rectangle back to -1

                        # rect = Rectangle(board, top_left, bottom_right, Color(-1))

                        rect = Rectangle(board, top_left, bottom_right, -1)
                        rect.draw_rectangle()

                        # assign anchor value to its position
                        board.solution[board.blocks[nexti].row][
                            board.blocks[nexti].col] = nexti
                except AssertionError:
                    pass
                    # todo:
        # increase counter by 1, so go to the next factor in the list
        count[nexti] += 1

    # if no valid rectangles are found, set counter for the current anchor back to 0
    if nexti > 0:
        count[nexti] = 0


def _update_blocks_factors(board: 'Board'):
    for block in board.blocks:
        block.calculate_factors()


if __name__ == '__main__':
    main()
