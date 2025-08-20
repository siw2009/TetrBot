import ScreenShot as scs



board_config = [10, 20]
area_config = {'top': 298, 'left': 789, 'width': 343, 'height': 683}
block_size = [area_config['width'] / board_config[0], area_config['height'] / board_config[1]]
area = scs.get_screen(area_config)

