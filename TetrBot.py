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
        ay_end = min(area_size[1], round(block_size[1] * (y+1)))
        rlt.append([])

        for x in range(board_size[0]):
            ax_start = round(block_size[0] * x)
            ax_end = min(area_size[0], round(block_size[0] * (x+1)))
            
            rlt[-1].append(average_area(board_sum_rgb, ax_start, ax_end, ay_start, ay_end) > 10)



board_size = [10, 20]
area_size = {'top': 298, 'left': 789, 'width': 343, 'height': 683}
block_size = [area_size['width'] / board_size[0], area_size['height'] / board_size[1]]
area = scs.get_screen(area_size)

