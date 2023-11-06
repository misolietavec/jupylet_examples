from jupylet.app import App
from jupylet.sprite import Sprite
from jupylet.label import Label
from random import randint, choice

WIDTH = 800
HEIGHT = 450
b_colors = ("red", "blue", "yellow", "green", "magenta")


app = App(WIDTH, HEIGHT, resource_dir='images')
app.window.cursor = False
app.window.clear(red=0.8, green=0.8, blue=0.8)


global bricks

def make_bricks():
    global bricks
    bricks = []
    x_pos, x_step, y_step = 60, 2 * 340 / 9, 30
    for row in range(10):
        y_pos = 225 + 180
        for col in range(4):
            brick = Sprite(f"{choice(b_colors)}.png", x = x_pos, y = y_pos, scale = 0.15)
            bricks.append(brick)
            y_pos -= y_step
        x_pos += x_step
        

def draw_bricks():
    global bricks
    for brick in bricks:
        brick.draw()        


# setup
ball = Sprite('ball.png', scale=0.1)
paddle = Sprite('paddle.png', scale=0.2)
message = Label(text='Game is running!', color='#000000', font_size=18, anchor_x='center')


def setup():
    ball.x, ball.y = WIDTH / 2, 35
    ball.dx, ball.dy = 2.5, 4 + randint (-1, 2)
    ball.active = True
    message.text = 'Game is running!'
    message.x, message.y = WIDTH - 80, 50
    paddle.x, paddle.y = WIDTH / 2, 10
    make_bricks()
    paddle.draw()
    ball.draw()
    draw_bricks()
    message.draw()


# update
def ball_collide_bricks():
    for brick in bricks:
        if len(ball.collisions_with(brick)) > 0:
            return brick
    return []


@app.run_me_every(1 / 60)
def update_ball(ct, dt):
    if not ball.active: 
        return
    ball.x += ball.dx
    ball.y += ball.dy
    if ball.left < 0 or ball.right > WIDTH: 
        ball.dx = -ball.dx
    if ball.top > HEIGHT:
        ball.dy = -ball.dy
        
    hit_brick = ball_collide_bricks()
    if hit_brick:
        bricks.remove(hit_brick)
        ball.dy = -ball.dy
    if ball.collisions_with(paddle).size > 0:
        ball.dy = -ball.dy
    ball.active = not ((ball.bottom < 0) or (len(bricks) == 0))
    if not ball.active:
        result = "You WON" if len(bricks) == 0 else "You LOST"
        message.text = f'{result}\nPress P - new game\nPress Q - quit'
        message.x, message.y = WIDTH / 2, HEIGHT / 2
        message.align = 'center'


@app.event
def mouse_position_event(x, y, dx, dy):
    px = max(40, x) if x < WIDTH - 40 else WIDTH - 40
    paddle.x = px


@app.event
def render(ct, dt):
    app.window.clear(red=0.8, green=0.8, blue=0.8)
    message.draw()
    if ball.active:
        ball.draw()
        paddle.draw()
        draw_bricks()


@app.event
def key_event(key, action, modifiers):
    keys = app.window.keys
    if action  == keys.ACTION_PRESS:
        if key == keys.P:
            setup()
        if key == keys.Q:
            app.close()


setup()
app.run()
