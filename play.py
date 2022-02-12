import pygame
import sys
import model
import ai

pygame.init()
BOARD_SIZE = 4
NANO_TO_SEC = 1000000000

# UI
size = width, height = 480, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption('{} Puzzle'.format(BOARD_SIZE**2-1))
FPS = 30

# Fonts
tileFont = pygame.font.SysFont("", 72)

# Colors
black = (0,0,0)
borderColor = (92, 90, 86)
tileColor = (242, 197, 133)
fontColor = black

# ai
ai.init(BOARD_SIZE)
aiMoveIndex = 0
aiMoves = []

def gameLoop():
    clock = pygame.time.Clock()

    puzzle = model.Puzzle(boardSize=BOARD_SIZE)

    while True:
        for event in pygame.event.get():
            handleInput(event, puzzle)

        drawPuzzle(puzzle)
        pygame.display.flip()
        clock.tick(FPS)

def handleInput(event, puzzle):
    global aiMoveIndex
    global aiMoves

    if event.type == pygame.QUIT: sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            puzzle.shuffle()
            aiMoveIndex = 0
            aiMoves = []
        elif event.key == pygame.K_h:
            if len(aiMoves) == 0:
                aiMoves = ai.idaStar(puzzle)
                aiMoveIndex = 0

            if len(aiMoves) != 0:
                puzzle.move(aiMoves[aiMoveIndex])
                if puzzle.checkWin():
                    aiMoveIndex = 0
                    aiMoves = []
                else:
                    aiMoveIndex += 1

    elif event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        puzzleCoord = (pos[1]*puzzle.boardSize//height,
                        pos[0]*puzzle.boardSize//width)
        dir = (puzzleCoord[0] - puzzle.blankPos[0],
                puzzleCoord[1] - puzzle.blankPos[1])

        if dir == puzzle.RIGHT:
            puzzle.move(puzzle.RIGHT)
        elif dir == puzzle.LEFT:
            puzzle.move(puzzle.LEFT)
        elif dir == puzzle.DOWN:
            puzzle.move(puzzle.DOWN)
        elif dir == puzzle.UP:
            puzzle.move(puzzle.UP)


def drawPuzzle(puzzle):
    screen.fill(black)

    for i in range(puzzle.boardSize):
        for j in range(puzzle.boardSize):
            currentTileColor = tileColor
            numberText = str(puzzle[i][j])

            if puzzle[i][j] == 0:
                currentTileColor = borderColor
                numberText = ''

            rect = pygame.Rect(j*width/puzzle.boardSize,
                                i*height/puzzle.boardSize,
                                width/puzzle.boardSize,
                                height/puzzle.boardSize)

            pygame.draw.rect(screen, currentTileColor, rect)
            pygame.draw.rect(screen, borderColor, rect, 1)

            fontImg = tileFont.render(numberText, 1, fontColor)
            screen.blit(fontImg,
                        (j*width/puzzle.boardSize + (width/puzzle.boardSize - fontImg.get_width())/2,
                        i*height/puzzle.boardSize + (height/puzzle.boardSize - fontImg.get_height())/2))


if __name__ =="__main__":
    gameLoop()
