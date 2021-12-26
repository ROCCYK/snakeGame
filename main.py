from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SNAKE_COLOUR = '#E7090D'
BODY_PARTS = 3
SPEED = 100
SPACE_SIZE = 50
FOOD_COLOUR = '#DBDBDB'
BACKGROUND_COLOUR = '#181C27'



class Snake:
    def __init__(self):
        self.bodySize = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag='snake')
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag='food')



def nextTurn(snake, food):
    x, y = snake.coordinates[0]
    match direction:
        case 'up':
            y -= SPACE_SIZE
        case 'down':
            y += SPACE_SIZE
        case 'left':
            x -= SPACE_SIZE
        case 'right':
            x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f'Score: {score}')
        canvas.delete('food')
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if checkCollisions(snake):
        gameOver()
    else:
        window.after(SPEED, nextTurn, snake, food)

def changeDirection(newDirection):
    global direction
    match newDirection:
        case 'left':
            if direction != 'right':
                direction = newDirection
        case 'right':
            if direction != 'left':
                direction = newDirection
        case 'up':
            if direction != 'down':
                direction = newDirection
        case 'down':
            if direction != 'up':
                direction = newDirection

def checkCollisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for bodyPart in snake.coordinates[1:]:
        if x == bodyPart[0] and y == bodyPart[1]:
            return True
    return False

def gameOver():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('arial', 70), text='Game Over', fill='red', tag='gameover')

window = Tk()
window.title('snake game')
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text=f'Score: {score}', font=('arial',40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.bind('<Left>', lambda event: changeDirection('left'))
window.bind('<Right>', lambda event: changeDirection('right'))
window.bind('<Up>', lambda event: changeDirection('up'))
window.bind('<Down>', lambda event: changeDirection('down'))


snake = Snake()
food = Food()
nextTurn(snake, food)
window.mainloop()