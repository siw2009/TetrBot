from mss import mss



def get_screen(area: tuple[int]) -> bytes:
    with mss() as sct:
        # monitor = sct.monitors[1]
        sct_img = sct.grab(area)
        size = sct_img.size
        rlt = sct_img.rgb