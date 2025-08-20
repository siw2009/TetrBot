from time import sleep
import keyboard
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


def fit_location(board_column_top: list[int], mino_bottom: list[list[int]], mino_height: list[int]) -> list[int]:
    rlt = []
    for mino in range(len(mino_bottom)):
        for i in range(len(board_column_top) - len(mino_bottom[mino]) +1):
            required = max([board_column_top[i+j] - mino_bottom[mino][j] for j in range(len(mino_bottom[mino]))])
            gaps = sum([required + mino_bottom[mino][j] - board_column_top[i+j] for j in range(len(mino_bottom[mino]))])
            total_height = required + mino_height[mino]
            rlt.append([i, mino, gaps * 4 + total_height])
    
    return min(rlt, key = lambda x: x[2])


def press(target_column: int, current_column: int, spin: int):
    global cantHold
    cantHold = False

    for i in range(spin):
        keyboard.press_and_release('x')
        # sleep(0.01)

    movement = 'right'  if target_column > current_column else  'left'
    for i in range(abs(target_column - current_column)):
        keyboard.press_and_release(movement)
        # sleep(0.01)
    
    keyboard.press_and_release('space')



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
mino_bottom = [[[0, 0]],
               [[0, 0, 0, 0], [0]],
               [[0, 0, 0], [0, 2], [1, 1, 0], [0, 0]],
               [[0, 0, 0], [0, 0], [0, 1, 1], [2, 0]],
               [[0, 0, 1], [1, 0]],
               [[0, 0, 0], [0, 1], [1, 0, 1], [1, 0]],
               [[1, 0, 0], [0, 1]]]
mino_height = [[2],
               [1, 4],
               [2, 3, 2, 3],
               [2, 3, 2, 3],
               [2, 3],
               [2, 3, 2, 3],
               [2, 3]]
mino_column = [[4],
               [3, 5],
               [3, 4, 3, 3],
               [3, 4, 3, 3],
               [3, 4],
               [3, 4, 3, 3],
               [3, 4]]
mino_name = ['O', 'I', 'J', 'L', 'S', 'T', 'Z']

held = -1
cantHold = False



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
    if held == -1:
        keyboard.press_and_release('shift')
        held = new_mino
        cantHold = True
        continue

    if new_mino > -1:
        action = fit_location(find_column_top(board, board_size), mino_bottom[new_mino], mino_height[new_mino])
        
        if not cantHold:
            holdAction = fit_location(find_column_top(board, board_size), mino_bottom[held], mino_height[held])

            if holdAction[2] < action[2]:
                keyboard.press_and_release('shift')
                press(holdAction[0], mino_column[held][holdAction[1]], holdAction[1])

                held = new_mino
                cantHold = True
            else:
                press(action[0], mino_column[new_mino][action[1]], action[1])    

        else:
            press(action[0], mino_column[new_mino][action[1]], action[1])

    print('--' * 50)

    # sleep(1)