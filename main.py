from vpython import *


WINDOW_WEIGHT = 1400
WINDOW_HEIGHT = 650
initial_speed = 18
initial_omega = 0.45 * pi
point_n = 60
SUPER_POINT_CHANCE = 0.05
SUPER_POINT_SCORE = 10
assist_length = 30
SNAKE_INITIAL_LENGHT = 5
room_size = 100
point_radius = 1
colors_iter = 0
camera_mode_n = 4
delta_speed = 6
delta_omega = 0.15 * pi
scene = canvas(width=WINDOW_WEIGHT, height=WINDOW_HEIGHT, align='left',
               title=f'score: 0    length: {SNAKE_INITIAL_LENGHT}', background=color.gray(0.5))
scene.lights = []
distant_light(direction=vec(1, 0, 0), color=color.gray(0.4))
distant_light(direction=vec(-1, 0, 0), color=color.gray(0.4))
distant_light(direction=vec(0, 1, 0), color=color.gray(0.4))
distant_light(direction=vec(0, -1, 0), color=color.gray(0.4))
distant_light(direction=vec(0, 0, 1), color=color.gray(0.4))
distant_light(direction=vec(0, 0, -1), color=color.gray(0.4))
wall = box(pos=vec(0, 0, 0), size=vec(room_size, room_size, room_size))
cylinder(pos=vec(room_size / 2, room_size / 2, room_size / 2),
         axis=vec(0, 0, -room_size), radius=0.3, color=color.black)
cylinder(pos=vec(room_size / 2, room_size / 2, room_size / 2),
         axis=vec(0, -room_size, 0), radius=0.3, color=color.black)
cylinder(pos=vec(room_size / 2, room_size / 2, room_size / 2),
         axis=vec(-room_size, 0, 0), radius=0.3, color=color.black)
cylinder(pos=vec(-room_size / 2, -room_size / 2, -room_size / 2),
         axis=vec(0, 0, room_size), radius=0.3, color=color.black)
cylinder(pos=vec(-room_size / 2, -room_size / 2, -room_size / 2),
         axis=vec(0, room_size, 0), radius=0.3, color=color.black)
cylinder(pos=vec(-room_size / 2, -room_size / 2, -room_size / 2),
         axis=vec(room_size, 0, 0), radius=0.3, color=color.black)
cylinder(pos=vec(-room_size / 2, room_size / 2, -room_size / 2),
         axis=vec(room_size, 0, 0), radius=0.3, color=color.black)
cylinder(pos=vec(-room_size / 2, room_size / 2, -room_size / 2),
         axis=vec(0, 0, room_size), radius=0.3, color=color.black)
cylinder(pos=vec(room_size / 2, -room_size / 2, room_size / 2),
         axis=vec(0, 0, -room_size), radius=0.3, color=color.black)
cylinder(pos=vec(room_size / 2, -room_size / 2, room_size / 2),
         axis=vec(-room_size, 0, 0), radius=0.3, color=color.black)
cylinder(pos=vec(-room_size / 2, room_size / 2, room_size / 2),
         axis=vec(0, -room_size, 0), radius=0.3, color=color.black)
cylinder(pos=vec(room_size / 2, room_size / 2, -room_size / 2),
         axis=vec(0, -room_size, 0), radius=0.3, color=color.black)
press = {'w': False, 'a': False, 's': False, 'd': False,
         'up': False, 'left': False, 'down': False, 'right': False}
assist = arrow(visible=False, shaftwidth=0.2, color=color.green)


def assist_mode(event):
    if event.key == 'h':
        assist.visible = not assist.visible


def pause_game(event):
    global pause
    if event.key == 'p':
        pause = not pause


def no_wall_mode(event):
    global no_wall
    if event.key == 'r':
        no_wall = not no_wall
        wall.opacity = 0.5 if no_wall else 1


def high_speed(event):
    global speed
    if event.key == 'q':
        speed += delta_speed


def low_speed(event):
    global speed
    if event.key == 'e' and speed > delta_speed:
        speed -= delta_speed


def high_omega(event):
    global omega
    if event.key == 'm':
        omega += delta_omega


def low_omega(event):
    global omega
    if event.key == 'n' and omega > delta_omega:
        omega -= delta_omega


def point_pos():
    x = random() * (room_size - 2 * point_radius) - room_size / 2 + point_radius
    y = random() * (room_size - 2 * point_radius) - room_size / 2 + point_radius
    z = random() * (room_size - 2 * point_radius) - room_size / 2 + point_radius
    return vec(x, y, z)


def key_down(event):
    global press
    if event.key in press:
        press[event.key] = True


def key_up(event):
    global press
    if event.key in press:
        press[event.key] = False


def maintain_camera():
    if camera_mode == 0:
        return
    scene.up = up_direction
    scene.camera.axis = 15 * head_direction
    if camera_mode == 1:
        scene.camera.pos = snake[0].pos - 8 * head_direction + 3 * up_direction
    if camera_mode == 2:
        scene.camera.pos = snake[0].pos + head_direction
    if camera_mode == 3:
        scene.camera.pos = snake[0].pos - 20 * \
            head_direction + 5 * up_direction


def control_camera(event):
    global camera_mode
    if event.key == 'c':
        camera_mode = (camera_mode + 1) % camera_mode_n
        maintain_camera()


def distance_from_assist(position):
    x0 = snake[0].pos.x
    y0 = snake[0].pos.y
    z0 = snake[0].pos.z
    p = head_direction.x
    q = head_direction.y
    r = head_direction.z
    a = position.x
    b = position.y
    c = position.z
    t = (a * p + b * q + c * r - p * x0 - q *
         y0 - r * z0) / (p ** 2 + q ** 2 + r ** 2)
    x = p * t + x0
    y = q * t + y0
    z = r * t + z0
    return dist((a, b, c), (x, y, z))


press = {'w': False, 'a': False, 's': False, 'd': False,
         'up': False, 'left': False, 'down': False, 'right': False}
dt = 0.01
pause = False
no_wall = False
camera_mode = 1
run_rate = int(1 / dt)
while True:
    speed = initial_speed
    omega = initial_omega
    snake = [sphere(pos=vec(0, 0, i * 2), radius=1, color=color.green)
             for i in range(SNAKE_INITIAL_LENGHT)]
    point = []
    for i in range(point_n):
        point.append(sphere(pos=point_pos(), radius=point_radius,
                     color=color.red, super_point=False))
        if random() < SUPER_POINT_CHANCE:
            point[i].super_point = True
            point[i].texture = textures.earth
    scene.title = f'score: 0    length: {str(SNAKE_INITIAL_LENGHT)}'
    game_over = False
    wall.opacity = 1
    score = 0
    length = SNAKE_INITIAL_LENGHT
    head_direction = vec(0, 0, -1)
    up_direction = vec(0, 1, 0)
    normal = cross(head_direction, up_direction)
    assist.pos = snake[0].pos
    assist.axis = head_direction * assist_length
    maintain_camera()
    t = text(text='click screen', pos=snake[0].pos - 3 *
             normal + 2 * up_direction, axis=normal, up=up_direction)
    scene.waitfor('mousedown')
    scene.bind('keydown', key_down)
    scene.bind('keyup', key_up)
    scene.bind('keydown', control_camera)
    scene.bind('keydown', assist_mode)
    scene.bind('keydown', pause_game)
    scene.bind('keydown', no_wall_mode)
    scene.bind('keydown', high_speed)
    scene.bind('keydown', low_speed)
    scene.bind('keydown', high_omega)
    scene.bind('keydown', low_omega)
    t.visible = False
    del t
    while not game_over:
        rate(run_rate)
        if pause:
            continue
        normal = cross(head_direction, up_direction)
        if press['w'] or press['up']:
            head_direction = head_direction.rotate(omega * dt, normal)
            up_direction = cross(normal, head_direction)
        if press['s'] or press['down']:
            head_direction = head_direction.rotate(-omega * dt, normal)
            up_direction = cross(normal, head_direction)
        if press['a'] or press['left']:
            head_direction = head_direction.rotate(omega * dt, up_direction)
        if press['d'] or press['right']:
            head_direction = head_direction.rotate(-omega * dt, up_direction)
        snake[0].pos += speed * dt * head_direction
        assist.pos = snake[0].pos
        assist.axis = head_direction * assist_length
        maintain_camera()
        for i in range(1, len(snake)):
            if mag(snake[i].pos - snake[0].pos) < 2:
                game_over = True
            snake[i].pos = snake[i - 1].pos + 2 * \
                norm(snake[i].pos - snake[i - 1].pos)
        for i in range(len(point)):
            x = point[i].pos.x
            y = point[i].pos.y
            z = point[i].pos.z
            x0 = snake[0].pos.x
            y0 = snake[0].pos.y
            z0 = snake[0].pos.z
            if assist.visible and distance_from_assist(point[i].pos) < (1 + point_radius) and assist_length * (assist_length + point_radius) > dot(assist.axis, point[i].pos - snake[0].pos) > 0:
                point[i].color = color.green
            else:
                point[i].color = color.red
            if mag(snake[0].pos - point[i].pos) < (1 + point_radius):
                score += SUPER_POINT_SCORE if point[i].super_point else 1
                length += 1
                scene.title = f'score: {str(score)}    length: {length}'
                temp = point[i]
                temp.visible = False
                point[i] = sphere(
                    pos=point_pos(), radius=point_radius, color=color.red, super_point=False)
                if random() < SUPER_POINT_CHANCE:
                    point[i].super_point = True
                    point[i].texture = textures.earth
                del temp
                snake.append(
                    sphere(pos=2 * snake[-1].pos - snake[-2].pos, radius=1, color=color.green))
        if not no_wall and (not room_size / 2 - 1 > snake[0].pos.x > -room_size / 2 + 1 or not room_size / 2 - 1 > snake[0].pos.y > -room_size / 2 + 1 or not room_size / 2 - 1 > snake[0].pos.z > -room_size / 2 + 1) and snake[0].pos.x >= -room_size / 2 - 1 and snake[0].pos.x <= room_size / 2 + 1 and snake[0].pos.y >= -room_size / 2 - 1 and snake[0].pos.y <= room_size / 2 + 1 and snake[0].pos.z >= -room_size / 2 - 1 and snake[0].pos.z <= room_size / 2 + 1:
            game_over = True
    scene.unbind('keydown', key_down)
    scene.unbind('keyup', key_up)
    scene.unbind('keydown', control_camera)
    scene.unbind('keydown', assist_mode)
    scene.unbind('keydown', pause_game)
    scene.unbind('keydown', no_wall_mode)
    scene.unbind('keydown', high_speed)
    scene.unbind('keydown', low_speed)
    scene.unbind('keydown', high_omega)
    scene.unbind('keydown', low_omega)
    wall.opacity = 0.5
    t = text(text='Game Over\nScore: ' + str(score) + '\nLength: ' + str(length),
             pos=snake[0].pos - 4 * normal + 4 * up_direction, axis=normal, up=up_direction)
    sleep(1)
    tt = text(text='press any key', pos=snake[0].pos - 3.5 *
              normal + 6 * up_direction, axis=normal, up=up_direction)
    scene.waitfor('keydown')
    t.visible = False
    del t
    tt.visible = False
    del tt
    for i in range(len(snake)):
        snake[i].visible = False
    del snake
    for item in point:
        item.visible = False
    del point
