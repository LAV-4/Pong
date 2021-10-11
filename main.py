import pygame as p
import sys
import random


class Ball:
    def __init__(self, screen, color, posX, posY, radius):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dX = 0
        self.dY = 0
        self.show()

    def show(self):
        p.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    def start_moving(self):
        self.dX = -15
        self.dY = random.randint(2, 5)

    def move(self):
        self.posX += self.dX
        self.posY += self.dY

    def paddle_collision(self):
        self.dX = -self.dX

    def wall_collision(self):
        self.dY = -self.dY

    def restart_pos(self):
        self.posX = WIDTH//2
        self.posY = HEIGHT//2
        self.dX = 0
        self.dY = 0
        self.show()


class Paddle:
    def __init__(self, screen, color, posX, posY, width, height):
        self.screen = screen
        self.color = color
        self.width = width
        self.height = height
        self.posX = posX
        self.posY = posY
        self.state = "stopped"
        self.show()

    def show(self):
        p.draw.rect(self.screen, self.color, (self.posX-self.width//2, self.posY-self.height//2, self.width, self.height))

    def move(self):
        if self.state == "up":
            self.posY -= 12
        elif self.state == "down":
            self.posY += 12

    def clamp(self):
        if self.posY-self.height//2 <= 0:
            self.posY = self.height//2
        elif self.posY+self.height//2 >= HEIGHT:
            self.posY = HEIGHT-self.height//2

    def restart_pos(self):
        self.posY = HEIGHT//2
        self.state = "stopped"
        self.show()


class CollisionManager:
    def collision_ball_paddle1(self, ball, paddle):
        ballX = ball.posX
        ballY = ball.posY
        paddle_rightX = paddle.posX - paddle.width//2
        paddleY = paddle.posY - paddle.height//2

        if ballY + ball.radius > paddleY and ballY - ball.radius < paddleY + paddle.height:
            if ballX - ball.radius <= paddle_rightX + paddle.width:
                return True

    def collision_ball_paddle2(self, ball, paddle):
        ballX = ball.posX
        ballY = ball.posY
        paddle_leftX = paddle.posX - paddle.width // 2
        paddleY = paddle.posY - paddle.height // 2

        if ballY + ball.radius > paddleY and ballY - ball.radius < paddleY + paddle.height:
            if ballX + ball.radius >= paddle_leftX:
                return True

    def collision_ball_wall(self, ball):
        if ball.posY - ball.radius <= 0:
            return True
        if ball.posY + ball.radius >= HEIGHT:
            return True
        return False

    def collision_ball_goal1(self, ball):
        return ball.posX - ball.radius <= 15

    def collision_ball_goal2(self, ball):
        return ball.posX + ball.radius >= WIDTH - 15


class PlayerScore:
    def __init__(self, screen, points, posX, posY):
        self.screen = screen
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = p.font.SysFont("monospace", 80, bold=True)
        self.label = self.font.render(self.points, False, WHITE)
        self.show()

    def show(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

    def increase_score(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, False, WHITE)

    def restart(self):
        self.points = "0"
        self.label = self.font.render(self.points, False, WHITE)

p.init()

WIDTH = 900
HEIGHT = 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen = p.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)
p.display.set_caption("Pong")
icon = p.image.load("Images/pong_icon.jpg")
p.display.set_icon(icon)
screen.blit(icon, ((WIDTH-icon.get_width())//2, (HEIGHT-icon.get_height())//2))
p.display.update()
p.time.wait(3000)


def paint_back():
    screen.fill(BLACK)
    p.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5)


def restart(score1, score2, paddle1, paddle2):
    paint_back()
    score1.restart()
    score2.restart()
    paddle1.restart_pos()
    paddle2.restart_pos()


def main():
    paint_back()
    ball = Ball(screen, WHITE, WIDTH // 2, HEIGHT // 2, 15)
    paddle1 = Paddle(screen, WHITE, 30, HEIGHT // 2, 20, 120)
    paddle2 = Paddle(screen, WHITE, WIDTH - 30, HEIGHT // 2, 20, 120)
    collision = CollisionManager()
    score1 = PlayerScore(screen, "0", WIDTH//4, 15)
    score2 = PlayerScore(screen, "0", WIDTH*3//4, 15)
    run = True
    game_over = True
    clock = p.time.Clock()

    while run:
        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()

            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE and game_over:
                    game_over = False
                    ball.start_moving()
                if event.key == p.K_r and game_over:
                    restart(score1, score2, paddle1, paddle2)
                    ball.start_moving()
                if event.key == p.K_w:
                    paddle1.state = "up"
                if event.key == p.K_s:
                    paddle1.state = "down"
                if event.key == p.K_UP:
                    paddle2.state = "up"
                if event.key == p.K_DOWN:
                    paddle2.state = "down"

            if event.type == p.KEYUP:
                if not p.key.get_pressed()[p.K_w] and not p.key.get_pressed()[p.K_s]:
                    paddle1.state = "stopped"
                if not p.key.get_pressed()[p.K_UP] and not p.key.get_pressed()[p.K_DOWN]:
                    paddle2.state = "stopped"

        if not game_over:
            paint_back()
            ball.move()
            ball.show()

            paddle1.move()
            paddle1.clamp()
            paddle1.show()

            paddle2.show()
            paddle2.clamp()
            paddle2.move()

            if collision.collision_ball_paddle1(ball, paddle1):
                ball.paddle_collision()
            elif collision.collision_ball_paddle2(ball, paddle2):
                ball.paddle_collision()
            if collision.collision_ball_wall(ball):
                ball.wall_collision()
            if collision.collision_ball_goal1(ball):
                paint_back()
                score2.increase_score()
                ball.restart_pos()
                paddle1.restart_pos()
                paddle2.restart_pos()
                game_over = True
            if collision.collision_ball_goal2(ball):
                paint_back()
                score1.increase_score()
                ball.restart_pos()
                paddle1.restart_pos()
                paddle2.restart_pos()
                game_over = True

        score1.show()
        score2.show()

        p.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()