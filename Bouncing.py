from jupylet.sprite import Sprite
from jupylet.app import App

WIDTH = 640
HEIGHT = 480

app = App(WIDTH, HEIGHT)
app.window.cursor = False


class Ball(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__('ball.png',  *args, **kwargs)
        self.vx = 5
        self.vy = 6
        self.stopped = False

ball = Ball(x=WIDTH / 3, y=HEIGHT / 4, scale=0.15)


@app.run_me_every(1 / 60)
def update_ball(ct, dt):
    if ball.stopped:
        return
    ball.x += ball.vx
    ball.y += ball.vy
    if (ball.right >= WIDTH or ball.left <= 0):
        ball.vx = -ball.vx
    
    if (ball.top >= HEIGHT or ball.bottom <= 0):
        ball.vy = -ball.vy


@app.event
def render(ct, dt):
    if not ball.stopped:
        app.window.clear(red=0.8, green=0.8, blue=0.8)
        ball.draw()


@app.event
def key_event(key, action, modifiers):
    keys = app.window.keys
    if action  == keys.ACTION_PRESS:
        if key == keys.P:
            ball.stopped = not ball.stopped
        if key ==   keys.Q:
            app.close()


app.run()
