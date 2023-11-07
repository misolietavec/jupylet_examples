# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
from jupylet.sprite import Sprite
from jupylet.app import App
from jupylet.label import Label
from random import randint

# %%
WIDTH =  400
HEIGHT = 600
GAP = 150
GRAVITY = 0.2
FLAP_STRENGTH = 5
SPEED = 2

# %%
app = App(width=WIDTH, height=HEIGHT, resource_dir='images')

# %%
bird = Sprite('flappy1.png', scale=0.1)
birds = ['flappy1.png', 'flappy2.png']
msg = Label(text='Game is running!', color='#000000', font_size=18, 
            anchor_x='center', align='center', line_height=1.3)
background = Sprite('background.png', scale=1.12, anchor_y='bottom',anchor_x='left')


# %%
def reset_bird():
    bird.x, bird.y = WIDTH / 2, 260
    bird.count = bird.imgnum = 0
    bird.dead = False
    bird.score = bird.vy = 0
    bird.color = 'white'


# %%
pipe_bot = Sprite('pipe-green.png', anchor_y='top')
pipe_top = Sprite('pipe-green.png', flip=False, anchor_y='bottom')


# %%
def reset_pipes():
    by = randint(200, 300)
    pipe_bot.x = pipe_top.x = WIDTH
    pipe_bot.y = by
    pipe_top.y = by + GAP
    pipe_bot.scale = pipe_top.scale = 1.2


# %%
def setup():
    reset_bird()
    reset_pipes()
    msg.x, msg.y = WIDTH - 75, 25
    msg.text = 'Game is running!'


# %%
def bird_collides():
    if len(bird.collisions_with(pipe_bot)) or len(bird.collisions_with(pipe_top)):
        return True
    return False    


# %%
@app.event
def key_event(key, action, modifiers):
    keys = app.window.keys
    if action  == keys.ACTION_PRESS:
        if key == keys.P:
            if not bird.dead:
                bird.vy = -FLAP_STRENGTH
        if key == keys.N:
            setup()
        if key == keys.Q:
            app.close()


# %%
@app.event
def render(ct, dt):
    app.window.clear(red=0.8, green=0.8, blue=0.8)
    background.draw()
    pipe_top.draw()
    pipe_bot.draw()
    bird.draw()
    msg.draw()


# %%
@app.run_me_every(1 / 60)
def update(ct, dt):
    if bird_collides() or bird.bottom <= 0:
        bird.dead = True
        bird.color = 'red'
        msg.text = f'Score: {bird.score}\nNew game - N\nQuit - Q'
        return
    pipe_bot.x -= SPEED
    pipe_top.x = pipe_bot.x
    if pipe_bot.x <= 0:
        reset_pipes()
        if not bird.dead:
            bird.score += 1
    bird.count = (bird.count + 1) % 10
    if not bird.count:
        bird.imgnum = int(not bird.imgnum)
        bird.image = birds[bird.imgnum]
        bird.scale = 0.1
    uy = bird.vy
    bird.vy += GRAVITY
    bird.y -= (uy + bird.vy) / 2    


# %%
setup()
app.run()
