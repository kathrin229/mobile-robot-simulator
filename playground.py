import pygame
import sys
from robot import Robot
import room
import math
import numpy as np


def draw_walls(screen, walls, wall_thickness, wall_color):

    for left_wall in walls["left"]:
        pygame.draw.line(surface=screen, color=wall_color, width=wall_thickness,
                         start_pos=left_wall[0],
                         end_pos=left_wall[1])

    for top_wall in walls["top"]:
        pygame.draw.line(surface=screen, color=wall_color, width=wall_thickness,
                         start_pos=top_wall[0],
                         end_pos=top_wall[1])

    for right_wall in walls["right"]:
        pygame.draw.line(surface=screen, color=wall_color, width=wall_thickness,
                         start_pos=right_wall[0],
                         end_pos=right_wall[1])

    for bottom_wall in walls["bottom"]:
        pygame.draw.line(surface=screen, color=wall_color, width=wall_thickness,
                         start_pos=bottom_wall[0],
                         end_pos=bottom_wall[1])
                         

def draw_robot(screen, robot, robot_color, distance_values, draw_sensors=False):
    # body of robot
    pygame.draw.circle(surface=screen, color=robot_color, center=(robot.x, robot.y), radius=robot.radius)
    # orientation of robot
    pygame.draw.line(surface=screen, color=(0, 0, 0), width=2,
                     start_pos=(robot.x, robot.y), end_pos=robot.orientation)
    # sensors
    if draw_sensors:
        for i_sensor, (x_sensor, y_sensor) in enumerate(robot.sensor_list):
            angle = (i_sensor + 1) * 360 / robot.num_sensors
            sensor_start_x = robot.x + math.cos(angle * math.pi / 180) * robot.radius
            sensor_start_y = robot.y + math.sin(angle * math.pi / 180) * robot.radius

            sensor_length = robot.radius + distance_values[i_sensor]

            sensor_end_x = robot.x + math.cos(angle * math.pi / 180) * sensor_length
            sensor_end_y = robot.y + math.sin(angle * math.pi / 180) * sensor_length

            pygame.draw.line(surface=screen, color=(255, 0, 0), width=1,
                             start_pos=(sensor_start_x, sensor_start_y), end_pos=(sensor_end_x, sensor_end_y))

            # display sensor values
            text = str(int(distance_values[i_sensor]))
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface, (sensor_end_x - 7 + math.cos(angle * math.pi / 180) * robot.radius / 4,
                                      sensor_end_y - 7 + math.sin(angle * math.pi / 180) * robot.radius / 4))

    # display motor speed values
    text = str(int(robot.v_wheel_r))
    textsurface = myfont.render(text, False, (0, 0, 0))
    screen.blit(textsurface, (robot.x + np.cos(robot.line_angle + math.pi /2) * robot.radius /2,
                              robot.y + np.sin(robot.line_angle + math.pi /2) * robot.radius /2))

    text = str(int(robot.v_wheel_l))
    textsurface = myfont.render(text, False, (0, 0, 0))
    screen.blit(textsurface, (robot.x + np.cos(robot.line_angle + 3 * math.pi/2) * robot.radius / 2,
                              robot.y + np.sin(robot.line_angle + 3 * math.pi/2) * robot.radius / 2))


def init_walls_coordinates(env_width, env_height, wall_length):
    # wall frame distance
    dist_l_r = (env_width - wall_length) / 2  # distance to frame, left and right
    dist_t_b = (env_height - wall_length) / 2  # distance to frame, top and bottom

    left_start = (dist_l_r, dist_t_b)
    left_end = (dist_l_r, dist_t_b + wall_length)

    top_start = (dist_l_r, dist_t_b)
    top_end = (dist_l_r + wall_length, dist_t_b)

    right_start = (dist_l_r + wall_length, dist_t_b)
    right_end = (dist_l_r + wall_length, dist_t_b + wall_length)

    bottom_start = (dist_l_r, dist_t_b + wall_length)
    bottom_end = (dist_l_r + wall_length, dist_t_b + wall_length)

    walls = {
        'left': [left_start, left_end],
        'top': [top_start, top_end],
        'right': [right_start, right_end],
        'bottom': [bottom_start, bottom_end],
    }

    return walls

# Work distribution:
# Sensor model by Lena
# Motion model by Kathrin
# Collision detection by Lena and Kathrin
if __name__ == '__main__':
    # environment
    env_width = 750
    env_height = env_width
    wall_length = 600
    wall_thickness = 6
    wall_color = (204, 0, 102)

    # robot
    x = env_width / 5
    y = env_height / 5
    v = 0.5
    v_max = 15
    radius = env_width / 20
    num_sensors = 12
    max_sensor_reach = 2 * radius
    robot_color = (153,204,255)
    robot = Robot(x, y, radius, num_sensors, max_sensor_reach)
    room_shape = 'square'  # square, rectangle, rectangle_double, trapezoid, trapezoid_double

    # walls
    walls = room.init_walls_coordinates(env_width, env_height, wall_length, room_shape)

    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode([env_width, env_height])
    clock = pygame.time.Clock()

    # initialize display numbers
    myfont = pygame.font.SysFont('Arial', 14)
    screen.fill((255, 255, 255))

    # initialize timer in order to provide constant timer-events
    timer_event = pygame.USEREVENT + 1
    time = 250
    pygame.time.set_timer(timer_event, time)

    # run animation
    go = True
    while go:
        for event in pygame.event.get():
            # for key / action
            if event.type == pygame.QUIT:
                # termination
                sys.exit()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_0]:
                sys.exit()

            if (robot.v_wheel_l + robot.v_wheel_r) / 2 < v_max:

                if pressed_keys[pygame.K_LEFT]:
                    robot.v_wheel_l += v
                if pressed_keys[pygame.K_RIGHT]:
                    robot.v_wheel_r += v
                if pressed_keys[pygame.K_UP]:
                    robot.v_wheel_l += v
                    robot.v_wheel_r += v
                if pressed_keys[pygame.K_x]:
                    robot.v_wheel_l = 0
                    robot.v_wheel_r = 0

            if (robot.v_wheel_l + robot.v_wheel_r) / 2 > - v_max:
                if pressed_keys[pygame.K_a]:
                    robot.v_wheel_l -= v
                if pressed_keys[pygame.K_d]:
                    robot.v_wheel_r -= v
                if pressed_keys[pygame.K_DOWN]:
                    robot.v_wheel_l -= v
                    robot.v_wheel_r -= v
                if pressed_keys[pygame.K_x]:
                    robot.v_wheel_l = 0
                    robot.v_wheel_r = 0

            # update screen by providing timer-event
            if event.type == timer_event:
                # update robot position with delta_t = 0.1
                robot.set_new_position(0.1, v_left=robot.v_wheel_l, v_right=robot.v_wheel_r)

                # check for collision
                robot.robot_is_crossing_wall(walls)

                # sensor value update
                # robot.update_sensors()
                sensor_d = robot.get_sensor_distance_values(walls)
                robot.update_sensors()

                # clear screen
                screen.fill((255, 255, 255))

                # draw scene
                draw_walls(screen, walls, wall_thickness, wall_color)
                draw_robot(screen, robot, robot_color, sensor_d, draw_sensors=True)

                # update
                pygame.display.update()