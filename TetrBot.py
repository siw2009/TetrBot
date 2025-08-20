import ScreenShot as scs



def convert_to_rgbsum(source: bytes, area_size: list[int]) -> list[list[int]]:
    rlt = []
    idx = 0
    for y in range(area_size[1]):
        rlt.append([])
        for x in range(area_size[0]):
            rlt[-1].append(source[idx] + source[idx+1] + source[idx+2])
            idx += 3
    
    return rlt


def average_area(source_sum_rgb: list[list[int]], startx: int, endx: int, starty: int, endy: int) -> float:
    rlt = 0
    for y in range(starty, endy+1):
        for x in range(startx, endx+1):
            rlt += source_sum_rgb[y][x]

    return rlt / (endx - startx) / (endy - starty)


def scan_board(board_sum_rgb: list[list[int]], board_size: list[int], area_size: list[int]) -> list[list[int]]:
    '''
    board_sum_rgb must contain summed values of rgb
    for example, (255, 127, 63) will be stored as 445
    '''

    block_size = [area_size[i] / board_size[i] for i in range(2)]
    rlt = []

    for y in range(board_size[1]):
        ay_start = round(block_size[1] * y)
        ay_end = min(area_size[1], round(block_size[1] * (y+1))) -1
        rlt.append([])

        for x in range(board_size[0]):
            ax_start = round(block_size[0] * x)
            ax_end = min(area_size[0], round(block_size[0] * (x+1))) -1
            
            rlt[-1].append(int(average_area(board_sum_rgb, ax_start, ax_end, ay_start, ay_end) > 100))

    return rlt


def detect_new(current: list[list[int]], board_size: list[int], mino_table: list[list[list[int]]]) -> int:
    found = False
    found_coords = [-1,-1]
    for y in range(board_size[1]):
        for x in range(board_size[0]):
            if current[y][x]:
                found = True
                found_coords = [x,y]
                break

        if found:  break

    if found:
        for i,mino in enumerate(mino_table):
            b = True
            for coord in mino:
                nx = found_coords[0] + coord[0]
                ny = found_coords[1] + coord[1]

                if nx < 0 or nx >= board_size[0] or ny < 0 or ny >= board_size[1] or not(current[ny][nx]):
                    b = False
                    break

            if b:  return i

    return -1


def find_column_top(board: list[list[int]], board_size: list[int]) -> list[int]:
    rlt = []
    for column in range(board_size[0]):
        unfound = True
        for y in range(board_size[1]):
            if board[y][column]:
                unfound = False
                rlt.append(board_size[1] - y)
                break
        
        if unfound:  rlt.append(0)

    return rlt



def fit_location(board_column_top: list[int], mino_bottom: list[int]) -> tuple[int, int]:
    rlt_height = -1
    rlt = -1
    for x in range(len(board_column_top) - len(mino_bottom)):
        fitable = True
        h = board_column_top[x] - mino_bottom[0]
        for i in range(1, len(mino_bottom)):
            if board_column_top[x+i] - mino_bottom[i] != h:
                fitable = False
                break
        
        if fitable and (rlt_height == -1 or rlt_height > board_column_top[x]):
            rlt = x
            rlt_height = board_column_top[x]
    
    return rlt, rlt_height



board_size = [10, 20]
area_size = {'top': 298, 'left': 789, 'width': 343, 'height': 683}

block_size = [area_size['width'] / board_size[0], area_size['height'] / board_size[1]]
top_board_size = [10, 4]
top_size = {'top': round(area_size['top'] - block_size[1] * top_board_size[1]), 'left': area_size['left'], 'width': area_size['width'], 'height': round(block_size[1] * top_board_size[1])}

mino_table = [[[1, 0], [0, 1], [1, 1]],
              [[1, 0], [2, 0], [3, 0]],
              [[0, 1], [1, 1], [2, 1]],
              [[0, 1], [-1, 1], [-2, 1]],
              [[1, 0], [0, 1], [-1, 1]],
              [[-1, 1], [0, 1], [1, 1]],
              [[1, 0], [1, 1], [2, 1]]]
mino_bottom = [[[1, 1]],
               [[1, 1, 1, 1], [1]],
               [[1, 1, 1], [1, 3], [2, 2, 1], [1, 1]],
               [[1, 1, 1], [1, 1], [1, 2, 2], [3, 1]],
               [[1, 1, 2], [2, 1]],
               [[1, 1, 1], [1, 2], [2, 1, 2], [2, 1]],
               [[2, 1, 1], [1, 2]]]
mino_name = ['O', 'I', 'J', 'L', 'S', 'T', 'Z']


from time import sleep
import keyboard


while True:
    top_area = scs.get_screen(top_size)
    top_board = scan_board(convert_to_rgbsum(top_area, [top_size['width'], top_size['height']]), top_board_size, [top_size['width'], top_size['height']])

    area = scs.get_screen(area_size)
    board = scan_board(convert_to_rgbsum(area, [area_size['width'], area_size['height']]), board_size, [area_size['width'], area_size['height']])

    for y in range(len(top_board)):
        for x in range(len(top_board[0])):
            print('██' if top_board[y][x] else '  ', end = '')
        print()

    for y in range(len(board)):
        for x in range(len(board[0])):
            print('██' if board[y][x] else '  ', end = '')
        print()
    
    new_mino = detect_new(top_board, top_board_size, mino_table)
    if new_mino > -1:
        print(mino_name[new_mino])

    # print(find_column_top(board, board_size))
        print(min([(fit_location(find_column_top(board, board_size), shape), i) for i, shape in enumerate(mino_bottom[new_mino])], key = lambda x: x[0][1] if x[0][1]>-1 else 200))

    print('--' * 50)

    keyboard.wait('space')
    sleep(0.05)