from mss import mss



def get_screen(area: dict) -> bytes:
    '''
    area parameter must be a dictionary
    **top, left, width, height, mon**
    where mon specifies which monitor to capture from
    '''

    with mss() as sct:
        # monitor = sct.monitors[1]
        sct_img = sct.grab(area)
        # size = sct_img.size
    return sct_img.rgb