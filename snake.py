import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False,False)
canvas = tkinter.Canvas(window, bg = 'black', width = WINDOW_WIDTH,height = WINDOW_HEIGHT,borderwidth=0,highlightthickness=0)
canvas.pack()
canvas.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

windowX = int((screen_width/2) - (window_width/2))
windowY = int((screen_height/2) - (window_height/2))

window.geometry(f'{window_width}x{window_height}+{windowX}+{windowY}')

snake = Tile(5*TILE_SIZE,5*TILE_SIZE)#snake head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)#food
snakeBody = []
velocityX = 0
velocityY = 0
gameOver = False
score = 0


def change_direction(e):
    global velocityX,velocityY,gameOver,score
    if gameOver:
        return

    if e.keysym == 'Up' and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == 'Down' and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == 'Left' and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == 'Right' and velocityX != -1:
        velocityX = 1
        velocityY = 0
def move():
    global snake,food,snakeBody,gameOver,score
    if gameOver:
        return
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        gameOver = True
        return

    for tile in snakeBody:
        if snake.x == tile.x and snake.y == tile.y:
            gameOver = True
            return

    #collision
    if (snake.x == food.x and snake.y == food.y):
        snakeBody.append(Tile(food.x,food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    for i in range(len(snakeBody)-1,-1,-1):
        tile = snakeBody[i]
        if(i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prevTile = snakeBody[i -1]
            tile.x = prevTile.x
            tile.y = prevTile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def restart_game(event):
    global snake, food, snakeBody, velocityX, velocityY, gameOver, score
    if gameOver:
        snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
        food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
        snakeBody = []
        velocityX = 0
        velocityY = 0
        score = 0
        gameOver = False

def draw():
    global snake,food, snakeBody,gameOver,score
    move()

    canvas.delete("all")

    # food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

    #snake
    canvas.create_rectangle(snake.x,snake.y,snake.x+TILE_SIZE,snake.y+TILE_SIZE, fill = 'lime green')

    #body
    for tile in snakeBody:
        canvas.create_rectangle(tile.x,tile.y,tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'lime green')

    if gameOver:
        canvas.create_text(WINDOW_WIDTH/2,WINDOW_HEIGHT/2, font = 'Ariel 20', text = f"Game Over: {score}", fill = 'white')
    else:
        canvas.create_text(30,20,font = 'Ariel 10', text = f"Score: {score}", fill = 'white')
    window.after(100, draw)

draw()

window.bind('<KeyRelease>', change_direction)
window.bind("<space>", restart_game)
window.mainloop()

