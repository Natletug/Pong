import random
import tkinter as tk
from pathlib import Path

BEST_SCORE_FILE = Path(__file__).resolve().parent / "meilleur_score.txt"

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 16
PADDLE_HEIGHT = 120
PADDLE_SPEED = 9
BALL_SIZE = 14
BALL_SPEED = 5
n = 0
nn = [WINDOW_WIDTH/4,WINDOW_WIDTH/4*3,WINDOW_WIDTH/4,WINDOW_WIDTH/4*3]
nnn = [WINDOW_HEIGHT/4,WINDOW_HEIGHT/4,WINDOW_HEIGHT/4*3,WINDOW_HEIGHT/4*3]
def load_best_score():
    try:
        with BEST_SCORE_FILE.open("r", encoding="utf-8") as file:
            value = file.read().strip()
            return int(value) if value else 0
    except FileNotFoundError:
        return 0


class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.score = 0
        self.best_score = load_best_score()
        self.game_over = False
        self.up_pressed = False
        self.down_pressed = False

        self.player_y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.ai_y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.player_x = 20
        self.ai_x = WINDOW_WIDTH - 20 - PADDLE_WIDTH

        self.reset_ball()

        self.root.bind("<KeyPress-Up>", self.on_up_press)
        self.root.bind("<KeyRelease-Up>", self.on_up_release)
        self.root.bind("<KeyPress-Down>", self.on_down_press)
        self.root.bind("<KeyRelease-Down>", self.on_down_release)
        self.root.bind("<KeyPress-r>", lambda event: self.restart_game())
        self.root.bind("<KeyPress-R>", lambda event: self.restart_game())

        self.tick()

    def on_up_press(self, event):
        self.up_pressed = True

    def on_up_release(self, event):
        self.up_pressed = False

    def on_down_press(self, event):
        self.down_pressed = True

    def on_down_release(self, event):
        self.down_pressed = False

    def save_best_score(self):
        if self.score > self.best_score:
            self.best_score = self.score
            with BEST_SCORE_FILE.open("w", encoding="utf-8") as file:
                file.write(str(self.best_score))

    def reset_ball(self):
        self.ball_x = WINDOW_WIDTH // 2 - BALL_SIZE // 2
        self.ball_y = WINDOW_HEIGHT // 2 - BALL_SIZE // 2
        self.ball_dx = random.choice((-1, 1)) * BALL_SPEED
        self.ball_dy = random.choice((-1, 1)) * random.randint(2, 5)

    def restart_game(self):
        self.score = 0
        self.game_over = False
        self.player_y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.ai_y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.reset_ball()

    def move_player(self):
        if self.up_pressed:
            self.player_y -= PADDLE_SPEED
        if self.down_pressed:
            self.player_y += PADDLE_SPEED
        self.player_y = max(0, min(WINDOW_HEIGHT - PADDLE_HEIGHT, self.player_y))

    def move_ai(self):
        target_center = self.ball_y + BALL_SIZE / 2
        ai_center = self.ai_y + PADDLE_HEIGHT / 2
        if target_center > ai_center:
            self.ai_y += 6
        elif target_center < ai_center:
            self.ai_y -= 6
        self.ai_y = max(0, min(WINDOW_HEIGHT - PADDLE_HEIGHT, self.ai_y))

    def update_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_y <= 0 or self.ball_y + BALL_SIZE >= WINDOW_HEIGHT:
            self.ball_dy *= -1

        player_rect = (self.player_x, self.player_y, self.player_x + PADDLE_WIDTH, self.player_y + PADDLE_HEIGHT)
        if (
            player_rect[0] <= self.ball_x + BALL_SIZE <= player_rect[2]
            and player_rect[1] <= self.ball_y <= player_rect[3]
            and self.ball_dx < 0
        ):
            self.ball_x = self.player_x + PADDLE_WIDTH
            self.ball_dx = abs(self.ball_dx) + 0.2
            self.ball_dy = (self.ball_y + BALL_SIZE / 2 - (self.player_y + PADDLE_HEIGHT / 2)) * 0.18
            self.score += 1
            self.save_best_score()

        ai_rect = (self.ai_x, self.ai_y, self.ai_x + PADDLE_WIDTH, self.ai_y + PADDLE_HEIGHT)
        if (
            ai_rect[0] <= self.ball_x <= ai_rect[2]
            and ai_rect[1] <= self.ball_y + BALL_SIZE <= ai_rect[3]
            and self.ball_dx > 0
        ):
            self.ball_x = self.ai_x - BALL_SIZE
            self.ball_dx = -(abs(self.ball_dx) + 0.2)
            self.ball_dy = (self.ball_y + BALL_SIZE / 2 - (self.ai_y + PADDLE_HEIGHT / 2)) * 0.18

        if self.ball_x < 0:
            self.game_over = True
            self.save_best_score()

        if self.ball_x > WINDOW_WIDTH:
            self.reset_ball()

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_line(WINDOW_WIDTH // 2, 0, WINDOW_WIDTH // 2, WINDOW_HEIGHT, fill="white", dash=(8, 8))
        self.canvas.create_rectangle(
            self.player_x,
            self.player_y,
            self.player_x + PADDLE_WIDTH,
            self.player_y + PADDLE_HEIGHT,
            fill="white",
        )
        self.canvas.create_rectangle(
            self.ai_x,
            self.ai_y,
            self.ai_x + PADDLE_WIDTH,
            self.ai_y + PADDLE_HEIGHT,
            fill="white",
        )
        self.canvas.create_oval(
            self.ball_x,
            self.ball_y,
            self.ball_x + BALL_SIZE,
            self.ball_y + BALL_SIZE,
            fill="white",
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            20,
            text=f"Score: {self.score}   Best: {self.best_score}",
            fill="white",
            font=("Arial", 14),
        )

        if self.game_over:
            self.cats()
            self.canvas.create_text(
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
                text="Game Over",
                fill="white",
                font=("Arial", 36, "bold"),
            )
            self.canvas.create_text(
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 + 35,
                text="Press R to restart",
                fill="white",
                font=("Arial", 16),
            )
    
    def cats(self):
        for i in range(len(nn)):
            self.canvas.create_text(
                nn[i],
                nnn[i],
                text=""" /\___/\ """,
                fill="white",
                font=("Arial", 16),
            )
            self.canvas.create_text(
                nn[i],
                nnn[i] +21,
                text=""" (=^ . ^=) """,
                fill="white",
                font=("Arial", 16),
            )
            self.canvas.create_text(
                nn[i]+20,
                nnn[i] + 42,
                text=""" (") (")___/ """,
                fill="white",
                font=("Arial", 16),
            )
  

    def tick(self):
        if not self.game_over:
            self.move_player()
            self.move_ai()
            self.update_ball()
        self.draw()
        self.root.after(16, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()
