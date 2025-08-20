import pygame



def draw(win: pygame.Surface, src: bytes, win_size: list[int] | None = None):
    if win_size == None:  win_size = list(win.get_size())
    pxarray = pygame.PixelArray(win)

    idx = 0
    for y in range(win_size[1]):
        for x in range(win_size[0]):
            pxarray[x][y] = (src[idx], src[idx+1], src[idx+2])
            idx += 3



win = pygame.display.set_mode(size, pygame.DOUBLEBUF)
clock = pygame.time.Clock()

pygame.event.set_blocked(None)
pygame.event.set_allowed([pygame.QUIT])



draw(win, rlt)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



    pygame.display.flip()
    clock.tick()