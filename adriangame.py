import tkinter as tk
import random

# Ukuran layar dan blok
GAME_WIDTH = 600
GAME_HEIGHT = 400
SPACE_SIZE = 20
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BG_COLOR = "#000000"

# Kecepatan (dalam ms)
SPEED = 100

class Snake:
    def __init__(self):
        self.body = [[100, 100], [80, 100], [60, 100]]
        self.direction = "right"

class Food:
    def __init__(self, canvas, snake):
        x = random.randint(0, (GAME_WIDTH - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
        while [x, y] in snake.body:
            x = random.randint(0, (GAME_WIDTH - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
        self.coordinates = [x, y]
        self.food = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        self.snake = Snake()
        self.food = Food(self.canvas, self.snake)
        self.score = 0
        self.running = True

        self.root.bind("<Left>", lambda event: self.change_direction("left"))
        self.root.bind("<Right>", lambda event: self.change_direction("right"))
        self.root.bind("<Up>", lambda event: self.change_direction("up"))
        self.root.bind("<Down>", lambda event: self.change_direction("down"))

        self.snake_squares = []
        for x, y in self.snake.body:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
            self.snake_squares.append(square)

        self.next_turn()

    def next_turn(self):
        if not self.running:
            return

        x, y = self.snake.body[0]

        if self.snake.direction == "up":
            y -= SPACE_SIZE
        elif self.snake.direction == "down":
            y += SPACE_SIZE
        elif self.snake.direction == "left":
            x -= SPACE_SIZE
        elif self.snake.direction == "right":
            x += SPACE_SIZE

        new_head = [x, y]

        if self.check_collision(new_head):
            self.game_over()
            return

        self.snake.body.insert(0, new_head)
        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.snake_squares.insert(0, square)

        if new_head == self.food.coordinates:
            self.canvas.delete("food")
            self.food = Food(self.canvas, self.snake)
            self.score += 1
        else:
            self.snake.body.pop()
            self.canvas.delete(self.snake_squares.pop())

        self.root.after(SPEED, self.next_turn)

    def change_direction(self, new_direction):
        if new_direction == "left" and not self.snake.direction == "right":
            self.snake.direction = "left"
        elif new_direction == "right" and not self.snake.direction == "left":
            self.snake.direction = "right"
        elif new_direction == "up" and not self.snake.direction == "down":
            self.snake.direction = "up"
        elif new_direction == "down" and not self.snake.direction == "up":
            self.snake.direction = "down"

    def check_collision(self, head):
        x, y = head
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        if head in self.snake.body[1:]:
            return True
        return False

    def game_over(self):
        self.running = False
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="GAME OVER", fill="red", font=("Arial", 30, "bold"))

# Jalankan game
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game Cacing Tkinter")
    game = SnakeGame(root)
    root.mainloop()
