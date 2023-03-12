"""."""

# Experimenting with the pyglet library
import pyglet
from pyglet.window import key
from collections import deque
from random import sample


window = pyglet.window.Window(600, 400)
# print(f"WINDOW: {window.height}")

# Create the visual rail guides
railsbatch = pyglet.graphics.Batch()
rails = []
for h in range(20, window.height, 40):
    rails.append(
        pyglet.shapes.Line(x=0, x2=window.width,
                           y=h, y2=h,
                           batch=railsbatch)
    )
for w in range(20, window.width, 40):
    rails.append(
        pyglet.shapes.Line(x=w, x2=w,
                           y=0, y2=window.height,
                           batch=railsbatch)
    )

intersection_to_event = {}
intersections = []
for h in range(20, window.height, 40):
    for w in range(20, window.width, 40):
        intersection_to_event[(w, h)] = None
        intersections.append((w, h))


# Create the visual board guides
boardbatch = pyglet.graphics.Batch()
board = []
for h in range(0, window.height, 40):
    board.append(
        pyglet.shapes.Line(x=0, x2=window.width,
                           y=h, y2=h,
                           batch=boardbatch)
    )
for w in range(0, window.width, 40):
    board.append(
        pyglet.shapes.Line(x=w, x2=w,
                           y=0, y2=window.height,
                           batch=boardbatch)
    )


applebatch = pyglet.graphics.Batch()
apples = []

def put_random_apple():
    random_intersection = sample(
        intersections,
        1
    )[0]
    apples.append(
        pyglet.shapes.Circle(
            x=random_intersection[0],
            y=random_intersection[1],
            radius=20,
            color=(255, 0, 0),
            batch=applebatch
        )
    )


def is_vertex(x, y):
    """."""
    if (x - 20) % 40 == 0 and (y - 20) % 40 == 0:
        return True
    return False

pyglet.shapes.Rectangle._anchor_x = 20
pyglet.shapes.Rectangle._anchor_y = 20
pyglet.shapes.BorderedRectangle._anchor_x = 20
pyglet.shapes.BorderedRectangle._anchor_y = 20

snakebatch = pyglet.graphics.Batch()
ds = deque()
snake = deque()
xstart = 20
# for i in range(10):
#     snake.insert(0,
#                  pyglet.shapes.BorderedRectangle(
#                      x=xstart,
#                      y=20,
#                      width=40,
#                      height=40,
#                      border_color=(0, 0, 0),
#                      border=5,
#                      batch=snakebatch
#                  ))
#     ds.insert(0, [0, 0])
#     xstart += 40

for i in range(10):
    snake.insert(0,
                 pyglet.shapes.Circle(
                     x=xstart,
                     y=20,
                     radius=20,
                     batch=snakebatch
                 ))
    ds.insert(0, [0, 0])
    xstart += 40

# rectangle.anchor_position = 20, 20

dx, dy = 0, 0
velocity = 2


def go_left():
    """."""
    global dx, dy, velocity
    dx, dy = -velocity, 0
    return dx, dy


def go_right():
    """."""
    global dx, dy, velocity
    dx, dy = velocity, 0
    return dx, dy


def go_up():
    """."""
    global dx, dy, velocity
    dx, dy = 0, velocity
    return dx, dy


def go_down():
    """."""
    global dx, dy, velocity
    dx, dy = 0, -velocity
    return dx, dy


event = None


@window.event
def on_key_press(symbol, modifiers):
    """."""
    global dx
    global dy
    global rotation
    global event
    if symbol == key.W:
        event = go_up
        print("Pressed: W")
    if symbol == key.S:
        event = go_down
        print("Pressed: S")
    if symbol == key.D:
        event = go_right
        print("Pressed: D")
    if symbol == key.A:
        event = go_left
        print("Pressed: A")

__iframe = 0


def draw_snake():
    global dx
    global dy
    global ds
    global snake
    global event
    global __iframe
    if is_vertex(snake[0].x, snake[0].y):
        if event is not None:
            intersection_to_event[(snake[0].x, snake[0].y)] = event()
        for ipiece in range(len(snake)):
            ev = intersection_to_event[
                (snake[ipiece].x, snake[ipiece].y)
            ]
            if ev is not None:
                ds[ipiece] = ev
    if is_vertex(snake[len(snake)-1].x, snake[len(snake)-1].y):
        intersection_to_event[
            (snake[len(snake)-1].x,
             snake[len(snake)-1].y)
        ] = None
    for ipiece in range(1, len(snake)):
        if ds[0] == [0, 0]:
            break
        if ds[ipiece] == [0, 0]:
            # ds[ipiece] = ds[ipiece - 1]
            ds[ipiece] = [velocity, 0]
    for ipiece in range(len(snake)):
        snake[ipiece].x += ds[ipiece][0]
        snake[ipiece].y += ds[ipiece][1]


def point_in_square(point, squarecenter):
    if (
            point[0] <= squarecenter[0] + 20 and
            point[0] >= squarecenter[0] - 20 and
            point[1] <= squarecenter[1] + 20 and
            point[1] >= squarecenter[1] - 20
    ):
        return True
    return False


@window.event
def on_draw():
    """."""
    window.clear()
    global dx
    global dy
    global ds
    global snake
    global event
    global __iframe
    global apples
    draw_snake()
    direction = 0 if dx == 0 else dx / abs(dx), 0 if dy == 0 else dy / abs(dy)
    head = snake[0]
    tip = head.x + direction[0] * 20, head.y + direction[1] * 20
    apple = apples[0]
    if point_in_square(tip, (apple.x, apple.y)):
        snake.insert(
            0,
            pyglet.shapes.Circle(
                x=apple.x,
                y=apple.y,
                radius=20,
                batch=snakebatch
            )
        )
        ds.insert(0, ds[0])
        apple.delete()
        apples = []
        put_random_apple()
    snakebatch.draw()
    boardbatch.draw()
    applebatch.draw()
    # railsbatch.draw()

    if __iframe % 60 == 0:
        print(ds)

    __iframe += 1

put_random_apple()

pyglet.app.run()
