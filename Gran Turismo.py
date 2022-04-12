"""
This game was created and designed by ITAI BEAR.
23.5.2020
"""

'''These constants can and should be adjusted and customized'''
DEFAULT_SPEED = 15
DEFAULT_HORIZONTAL_SPEED = 13
DEFAULT_CARS_SPEED = 7
LANE_WIDTH = 130
LINES_HEIGHT = 70
LINES_WIDTH = 10
LINES_MARGIN = 80
SIDE_LINES_HEIGHT = 90
SIDE_LINES_WIDTH = 10
MARGIN_FROM_ROAD = 10
TREE_DENSITY = 10
COW_DENSITY = 200
CAR_DENSITY = 30
CARS_MARGIN = 30
DEFAULT_VOLUME = 0.4

'''These constants can be changed but may cause instability and unexpected behavior'''
REFRESH_RATE = 60
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 700

'''These constants should not be changed'''
LEFT_LANE = 1
MIDDLE_LANE = 2
RIGHT_LANE = 3
BACKGROUND_GREEN = (0, 130, 0)
LANE_GRAY = (71, 71, 64)
WHITE = (255, 255, 255)
GREEN = (34,177,76)
GREEN2 = (25,186,84)
PINK = (255, 174, 201)
RED = (237, 28, 36)
BLUE = (28,68,155)
RED2 = (240, 10, 10)
ORANGE = (251, 100, 0)
BLACK = (0,0,0)
LIGHT_GRAY = (190, 190, 190)
GRAY = (50,50,50)
GOLD = (255,201,14)
TREE_BACKGROUND_COLOR = (210, 211,203)
TREE_HEIGHT = 200
TREE_WIDTH = 200


import random, pygame
from pygame import *
import os.path
from os import path
import ctypes

def set_background():
    '''Function draws the background to the screen, thereby erasing the screen.
    No input and no output.'''
    screen.fill(BACKGROUND_GREEN) 
    pygame.draw.rect(screen, LANE_GRAY, [(WINDOW_WIDTH // 2) - int((LANE_WIDTH * 1.5)), 0, LANE_WIDTH * 3, WINDOW_HEIGHT])

    
def add_background(trees, cows, tree_density, cow_density):
    '''Function adds more elements such as trees to the top of the screen.
    Input: lists which hold all trees and cows and their density.
    Output: updated lists which hold all trees and cows.''' 
    if (random.randint(0,tree_density) == 1):
        trees = create_object(trees, TREE_HEIGHT)
    if (random.randint(0,cow_density) == 1):
        cows = create_object(cows, 200)
    return trees, cows

def move_background(trees, cows, speed):
    '''Function moves all background elements such as trees down at a certain speed
    while removing elements out of the screen.
    Input: lists which hold all trees and cows and the number of pixels to move.
    Output: updated lists which hold all trees and cows.'''
    for tree in trees:
        tree[1] += speed
        if tree[1] > WINDOW_HEIGHT:
            trees.remove(tree)
    for cow in cows:
        cow[1] += speed
        if cow[1] > WINDOW_HEIGHT:
            cows.remove(cow)
    return trees, cows

def change_background(trees, cows, speed, tree_density, cow_density):
    '''Function moves all background elements down and creates new ones.
    Input: lists which hold all trees and cows, speed to moven
    and the density of which the trees and cows will appear on the screen.
    Output: updated lists of the trees and cows.'''
    trees, cows = move_background(trees, cows, speed)
    trees, cows = add_background(trees, cows, tree_density, cow_density)
    return trees, cows

def create_object(object_list, object_height):
    '''Function created an idividual object at a random spot in the top of the screen
    while not interrupting the visibility of the road.
    Input: list which holds all the objects and the height of the object.
    Output: updated list which holds all the objects.'''
    object_x = random.choice([random.randint(-TREE_WIDTH, (WINDOW_WIDTH / 2) - (LANE_WIDTH * 1.5) - TREE_WIDTH - MARGIN_FROM_ROAD), random.randint((WINDOW_WIDTH / 2) + (LANE_WIDTH * 1.5) + MARGIN_FROM_ROAD, WINDOW_WIDTH)])
    object_list.append([object_x, -object_height])
    return object_list

def set_lines():
    '''Function creates a new list which holds all positions of the road lines.
    Input: none.
    Output: a list which holds all positions of the road lines.'''
    y = -LINES_HEIGHT 
    first_x = (WINDOW_WIDTH // 2) - (LANE_WIDTH // 2) - (LINES_WIDTH // 2)
    second_x = (WINDOW_WIDTH // 2) + (LANE_WIDTH // 2) - (LINES_WIDTH // 2)
    lines = []
    while y < WINDOW_HEIGHT :
        lines.append([first_x, y])
        lines.append([second_x, y])
        y += LINES_HEIGHT + LINES_MARGIN
    return lines

def move_lines(lines,speed):
    '''Function moves all road lines downward at a certain speed.
    Input: a list which holds all positions of the road lines and the number of pixels to move.
    Output: an updated list which holds all positions of the road lines.'''
    new_line = True
    for line in lines:
        line[1] += speed
    if lines[0][1] >= WINDOW_HEIGHT:
        lines.pop(0)
        lines.pop(0)
    if lines[-1][1] <= LINES_MARGIN:
        new_line = False
    if new_line:
        first_x = (WINDOW_WIDTH // 2) - (LANE_WIDTH // 2) - (LINES_WIDTH // 2)
        second_x = (WINDOW_WIDTH // 2) + (LANE_WIDTH // 2) - (LINES_WIDTH // 2)
        lines.append([first_x, -LINES_HEIGHT])
        lines.append([second_x, -LINES_HEIGHT])
    return lines

def set_side_lines():
    y = -SIDE_LINES_HEIGHT 
    first_x = (WINDOW_WIDTH // 2) - int(LANE_WIDTH * 1.5) - SIDE_LINES_WIDTH
    second_x = (WINDOW_WIDTH // 2) + int(LANE_WIDTH * 1.5)
    side_lines = []
    cnt = 0
    while y < WINDOW_HEIGHT :
        if cnt % 2 == 0:
            side_lines.append([first_x, y, RED])
            side_lines.append([second_x, y, RED])
        else:
            side_lines.append([first_x, y, WHITE])
            side_lines.append([second_x, y, WHITE])
        y += SIDE_LINES_HEIGHT
        cnt += 1
    return side_lines

def move_side_lines(side_lines, speed):
    new_side_line = True
    for line in side_lines:
        line[1] += speed
    if side_lines[0][1] >= WINDOW_HEIGHT:
        side_lines.pop(0)
        side_lines.pop(0)
    if side_lines[-1][1] <= 0:
        new_side_line = False
    if new_side_line:
        first_x = (WINDOW_WIDTH // 2) - int(LANE_WIDTH * 1.5) - SIDE_LINES_WIDTH
        second_x = (WINDOW_WIDTH // 2) + int(LANE_WIDTH * 1.5)
        if side_lines[-1][2] == RED:
            side_lines.append([first_x, side_lines[-2][1] - SIDE_LINES_HEIGHT, WHITE])
            side_lines.append([second_x, side_lines[-2][1] - SIDE_LINES_HEIGHT, WHITE])
        else:
            side_lines.append([first_x, side_lines[-2][1] - SIDE_LINES_HEIGHT, RED])
            side_lines.append([second_x, side_lines[-2][1] - SIDE_LINES_HEIGHT, RED])
    return side_lines

def move_lanes(car, move_to_lane):
    '''Function moves a car horizontally to a certain lane.
    Input: a car list which holds position of the car, model and size and a lane to be moved to.
    Output: an updated car list which holds position of the car, model and size.'''
    horizontal_speed = DEFAULT_HORIZONTAL_SPEED
    if car[0] < lane_pos(move_to_lane, car[4]) - horizontal_speed:
        car[0] += horizontal_speed
    elif car[0] > lane_pos(move_to_lane, car[4]) + horizontal_speed:
        car[0] -= horizontal_speed
    else:
        car[0] = lane_pos(move_to_lane, car[4])
    return car

def move_car(car,speed):
    '''Function moves a single car vertically at a certain speed.
    Input: a car list which holds position of the car, model and size and the number of pixels to move.
    Output: an updated car list which holds position of the car, model and size.'''
    car[1] -= speed
    speed += 1
    return car, speed
        
def lane_pos(lane, car_width):
    '''Function returns the x position of a lane number
    of which a car would be in the middle of the lane.
    Input: a lane number and the width of a car.
    Output: x position.'''
    if lane == LEFT_LANE:
        return (WINDOW_WIDTH // 2) - LANE_WIDTH - (car_width // 2)
    elif lane == MIDDLE_LANE:
        return (WINDOW_WIDTH // 2) - (car_width // 2)
    else:
        return (WINDOW_WIDTH // 2) + LANE_WIDTH - (car_width // 2)

def create_cars(cars, car_models, player_car_height):
    '''Function creates a random car object on the top of the screen at a random lane only if its valid.
    Input: a list of all car objects, a list of all car models and the height of the player car.
    Output: an updated list of all car objects.'''
    if (random.randint(0,car_density(cars)) == 0):
        car_model = random.choice(car_models)
        car_x = lane_pos(random.randint(1,4), car_model[2])
        if (car_valid(car_x, cars, player_car_height)):
            cars.append([car_x, -car_model[1]] + car_model)
    return cars

def car_density(cars):
    '''Function determines the density of which the cars will be created
    based on how many cars are currently on the road.
    Input: a list of all car objects.
    Output: the density of which car objects will be created.'''
    car_density = CAR_DENSITY
    if len(cars) < 2:
        car_density = car_density // 2
        if len(cars) == 1:
            if cars[0][1] > (WINDOW_HEIGHT / 2) + cars[0][3] + (CARS_MARGIN * 2) :
                car_density = car_density // 2
        else:
            car_density = car_density // 4
    return car_density
    
def car_valid(car_x, cars, player_car_height):
    '''Functions determines whether a car can be created at a certain lane
    based on the height of the player car so there would be no roadblocks for the player car
    and no cars on top of each other.
    Input: lane position of the car to be created, a list of all car objects
    and the height of the player car.
    Output: a boolean indicating whether the car can be created.'''
    valid = 0
    cars_on_same_lane = 0
    for car in cars:
        if car_x < car[0] + 15 and car_x > car[0] - 15:
            cars_on_same_lane += 1
            if not car[1] > player_car_height + CARS_MARGIN * 2:
                return False
        elif not car[1] > player_car_height + CARS_MARGIN * 2:
            valid += 1
            for car2 in cars:
                if not (car_x < car2[0] + 15 and car_x > car2[0] - 15):
                    if (abs(car2[0] - car[0]) > LANE_WIDTH - 15 and abs(car2[0] - car[0]) < LANE_WIDTH + 15):
                        if (abs(car[1] - car2[1]) - max(car[3], car2[3]) < (player_car_height + (CARS_MARGIN * 2))):
                            valid += 1
        if valid > 1 or cars_on_same_lane > 2:
            return False
    return True

def move_cars(cars, speed, cars_speed):
    '''Function moves all non player cars to make the illusion they move at a cetain speed.
    Input: a list of all car objects, speed of the player car and speed of all non player cars.
    Output: an updated list of all non player car objects.'''
    for car in cars:
        car[1] += speed - cars_speed
        if car[1] > WINDOW_HEIGHT:
            cars.remove(car)
    return cars
        
def is_crash(player_car ,cars):
    '''Function determines whether the player car crashed with another car.
    Input: a car object of player and a list of all non player car objects.
    Output: a boolean indicating whether there is a collision.'''
    for car in cars:
        if (player_car[1] + 5 <= car[1] - 5 and player_car[1] + player_car[3] - 5 >= car[1] + 5) or \
           (player_car[1] + 5 <= car[1] + car[3] - 5 and player_car[1] + player_car[3] - 5 >= car[1] + car[3] + 5):
            if (player_car[0] + 5 <= car[0] + 5 and player_car[0] + player_car[4] - 5 >= car[0] + 5) or \
               (player_car[0] + 5 <= car[0] + car[4] - 5 and player_car[0] + player_car[4] - 5 >= car[0] + car[4] - 5):
                return True
    return False

def create_text(t,center,font="Arial",size=72,color=(255,255,0), bold=False,italic=False):
    '''Function blits text to the screen based on center position given.
    Input: a text to blitted, center positions to blit the text, font of the text, size of the text,
    color of the text, a boolean wheter the text is in bold and a boolean whether the text is in italic.
    Output: none.'''
    font = pygame.font.SysFont(font, size, bold, italic)
    text = font.render(t, True, color)
    text_rect = text.get_rect()
    text_rect.center = center
    screen.blit(text,text_rect)

def round_rect(surface, rect, color, rad=20, border=0, inside=(0,0,0,0)):
    """
    Draw a rect with rounded corners to surface.  Argument rad can be specified
    to adjust curvature of edges (given in pixels).  An optional border
    width can also be supplied; if not provided the rect will be filled.
    Both the color and optional interior color (the inside argument) support
    alpha.
    """
    rect = Rect(rect)
    zeroed_rect = rect.copy()
    zeroed_rect.topleft = 0,0
    image = Surface(rect.size).convert_alpha()
    image.fill((0,0,0,0))
    _render_region(image, zeroed_rect, color, rad)
    if border:
        zeroed_rect.inflate_ip(-2*border, -2*border)
        _render_region(image, zeroed_rect, inside, rad)
    surface.blit(image, rect)


def _render_region(image, rect, color, rad):
    """Helper function for round_rect."""
    corners = rect.inflate(-2*rad, -2*rad)
    for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
        pygame.draw.circle(image, color, getattr(corners,attribute), rad)
    image.fill(color, rect.inflate(-2*rad,0))
    image.fill(color, rect.inflate(0,-2*rad))

def game_menu(menu_center_pos, in_out, speed, main_or_end,rank=False,score=0):
    '''Functions blits to the screen the game menus.
    Input: the center position of menu, whether the menu is sliding in or out,
    speed of the menu slide, whether it is the main menu or end menu,
    a boolean whether the player succeded in getting to the leaderboard and the score.
    Output: the center position of the menu, whether the menu is sliding in or out,
    speed of the menu slide and button rectangles.
    
    in_out: 0 - no slide, 1 - slide in from the top, 2 - slide out from below,
    3 - slide out from the top, -1 - menu out of the screen
    main_or_end: 1 - main menu, 2 - end menu'''
    
    menu_height = int(WINDOW_HEIGHT // 1.4)
    menu_width = WINDOW_WIDTH // 2
    if in_out == 1:
        menu_center_pos[1] += speed
        speed -= 1
        if menu_center_pos[1] >= WINDOW_HEIGHT // 2 - 100:
            speed -= 1
        if menu_center_pos[1] >= WINDOW_HEIGHT // 2:
            speed -= 5
        if menu_center_pos[1] >= WINDOW_HEIGHT // 2 + 100:
            speed -= 3
        if menu_center_pos[1] <= WINDOW_HEIGHT // 2 + 15 and speed < 0:
            in_out = 0
            speed = 0
    elif in_out == 2:
        menu_center_pos[1] += speed
        speed += 3
        if menu_center_pos[1] - (menu_height // 2) >= WINDOW_HEIGHT:
            in_out = -1
    elif in_out == 3:
        menu_center_pos[1] -= speed
        speed += 4
        if menu_center_pos[1] + (menu_height // 2) <= 0:
            in_out = -1
    if in_out == -1:
        return menu_center_pos, in_out, speed, None, None, None
        
                    
    background_rect = ((menu_center_pos[0] - (menu_width // 2)), (menu_center_pos[1] - (menu_height // 2)), menu_width, menu_height)
    round_rect(screen,background_rect,LIGHT_GRAY + (180,), 25)

    margin = 30
    if main_or_end == 1:
        screen.blit(logo, (menu_center_pos[0] - 150, menu_center_pos[1] - 200))
        playnow_pos = (menu_center_pos[0] - int(menu_width * 0.22), menu_center_pos[1] + (margin*2))
        playnow_size = (int(menu_width * 0.44), int((menu_height * 0.25) - (margin * 1.5)))
        round_rect(screen,playnow_pos + playnow_size,ORANGE, 35)
        create_text("Play Now", (playnow_pos[0] + (playnow_size[0] // 2), playnow_pos[1] + (playnow_size[1] // 2)), 'Calibri', 40, GRAY, True)
        create_text("Created and Designed by Itai Bear, May 2020", (menu_center_pos[0], playnow_pos[1] + playnow_size[1] + 50), 'Calibri', 20, BLACK, True, True)
        return menu_center_pos, in_out, speed, playnow_pos + playnow_size, None, None

    else:
        leaderboard_pos = ((menu_center_pos[0] - (menu_width // 2) + margin), (menu_center_pos[1] - (menu_height // 2) + margin))
        leaderboard_size = (int((menu_width * 0.45) - (margin * 1.5)), menu_height - (margin * 2))
        round_rect(screen,leaderboard_pos + leaderboard_size,GRAY + (245,), 20)
        create_text("Leaderboard", (leaderboard_pos[0] + (leaderboard_size[0] // 2) - 20, leaderboard_pos[1] + 30), 'Calibri', 30, ORANGE, True)
        reset_pos = (leaderboard_pos[0] + leaderboard_size[0] - 45, leaderboard_pos[1] + 15)
        screen.blit(reset, reset_pos)
        leaderboard_file = open("./contents/leaderboard.txt", 'r')
        lines = leaderboard_file.readlines()
        leaderboard_file.close()
        line_pos = [leaderboard_pos[0] + 30, leaderboard_pos[1] + 70]
        for line in lines:
            font = pygame.font.SysFont('Calibri', 20, True)
            text = font.render(line[:len(line)-1], True, ORANGE)
            screen.blit(text,line_pos) 
            line_pos[1] += 45
        
        score_pos = (leaderboard_pos[0] + leaderboard_size[0] + margin, leaderboard_pos[1])
        score_size = (int((menu_width * 0.55 - (margin * 1.5))), int(menu_height * 0.4) - margin)
        round_rect(screen,score_pos + score_size,GRAY + (240,), 20)
        
        if rank:
            create_text(lines[rank-1][:-1],(score_pos[0] + (score_size[0] // 2), score_pos[1] + int(score_size[1] * 0.3)), "Calibri", 35,ORANGE, True)
            create_text("Enter your name to display it",(score_pos[0] + (score_size[0] // 2), score_pos[1] + int(score_size[1] * 0.7)), "Calibri", 14,ORANGE, True)
            create_text("on the leaderboard!", (score_pos[0] + (score_size[0] // 2), score_pos[1] + int(score_size[1] * 0.7) + 15), "Calibri", 14, ORANGE, True)
        else:
            create_text(str(score), (score_pos[0] + (score_size[0] // 2), score_pos[1] + (score_size[1] // 2)), "Calibri", 70,ORANGE, True)
        playagain_pos = (score_pos[0], score_pos[1] + score_size[1] + margin)
        playagain_size = (score_size[0], int(menu_height * 0.3) - int(margin * 1.5))
        mainmenu_pos = (playagain_pos[0], playagain_pos[1] + playagain_size[1] + margin)
        mainmenu_size = (score_size[0], int(menu_height * 0.3) - int(margin * 1.5))
        
        round_rect(screen,playagain_pos + playagain_size,ORANGE, 20)
        create_text("Play Again", (playagain_pos[0] + (playagain_size[0] // 2), playagain_pos[1] + (playagain_size[1] // 2)), "Calibri", 45, GRAY, True)
        round_rect(screen,mainmenu_pos + mainmenu_size,ORANGE, 20)
        create_text("Main Menu", (mainmenu_pos[0] + (mainmenu_size[0] // 2), mainmenu_pos[1] + (mainmenu_size[1] // 2)), "Calibri", 45, GRAY, True)

                    
                
        return menu_center_pos, in_out, speed, playagain_pos + playagain_size, mainmenu_pos + mainmenu_size, reset_pos

def side_score(score):
    '''Function blits to the side of the screen the current score during the game.
    Input: the current score.
    Output: none.'''
    score_rect = (WINDOW_WIDTH - (30 * len(str(score))) - 35,6,(35 * len(str(score))) + 40,65)
    round_rect(screen, score_rect, (255,255,255,90),15)
    create_text(str(score),(score_rect[0] + (score_rect[2] // 2) - 10, score_rect[1] + (score_rect[3] // 2)-2),'Comicsans MS', 47, ORANGE, True)

def reset_leaderboard():
    '''Function resets the leaderboard text file also creating new one if it doesn't exist.
    No input and no output.'''
    leaderboard = open("./contents/leaderboard.txt", 'w')
    for i in range(8):
        leaderboard.write("%d. ______ - 0\n" % (i + 1))
    leaderboard.close()

def find_score_rank(score):
    '''Function finds the rank in the leaderboard of the score.
    Input: score.
    Output: the rank in the leaderboard of False if it didn't get in.'''
    leaderboard = open("./contents/leaderboard.txt", 'r')
    lines = leaderboard.readlines()
    for i in range(8):
        if score >= int(lines[i][12:]):
            leaderboard.close()
            return i+1
    return False

def update_leaderboard(rank, name, score):
    '''Recursive function updates leaderboard ranks based on a new entry to the leaderboard.
    Input: the rank in the leaderboard, the name of the player and score received.
    Output: none.'''
    if rank == 9:
        return
    leaderboard = open("./contents/leaderboard.txt", 'r')
    lines = leaderboard.readlines()
    leaderboard.close()
    down_name = lines[rank-1][3:9]
    down_score = lines[rank-1][12:-1]
    lines[rank-1] = (str(rank) + ". " + name + " - " + score + "\n")
    leaderboard = open("./contents/leaderboard.txt", 'w')
    leaderboard.write("".join(lines))
    leaderboard.close()
    update_leaderboard(rank+1, down_name, down_score)

def update_leaderboard_name(rank,name,score):
    '''Function updates player's name and score based on rank in the leaderboard.
    Input: rank entry to be updated, a name to update and a score to update.
    Output: none.'''
    leaderboard = open("./contents/leaderboard.txt", 'r')
    lines = leaderboard.readlines()
    leaderboard.close()
    lines[rank-1] = (str(rank) + ". " + name + " - " + score + "\n")
    leaderboard = open("./contents/leaderboard.txt", 'w')
    leaderboard.write("".join(lines))
    leaderboard.close()

def reset_vehicles(finish, trees, cows, lines, side_lines, cars):
    '''Function is a minor phase in the game which ressets all cars on the road elegantly
    by moving the background fast to make the illusion it moved to a different part of the road.
    Input: a boolean indicating whether the exit button was pressed, a list of all trees,
    a list of all cows, a list of all road lines and a list of all cars.
    Output: a boolean indicating whether the exit button was pressed.'''
    speed = 10
    cars_speed = 0
    speed_limit = False
    done = False
    while(not finish and not done):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True

        set_background()
        trees, cows = change_background(trees, cows, speed, TREE_DENSITY // 3, COW_DENSITY // 3)
        lines = move_lines(lines, speed)
        side_lines = move_side_lines(side_lines, speed)
        for side_line in side_lines:
            pygame.draw.rect(screen, side_line[2], side_line[:2] + [SIDE_LINES_WIDTH, SIDE_LINES_HEIGHT])
        for line in lines:
            pygame.draw.rect(screen, WHITE, line + [LINES_WIDTH, LINES_HEIGHT])
        for tree in trees:
            screen.blit(tree1, tree)
        cars = move_cars(cars, speed, cars_speed)
        for car in cars:
            screen.blit(car[2], car[:2])
            
        if speed >= 80 or speed_limit:
            speed -= 1
            speed_limit = True
        else:
            speed += 2
        if speed <= 0:
            done = True
        pygame.display.flip()
        clock.tick(REFRESH_RATE)
    return finish

def pause(finish):
    '''Function pauses the game and resumes after a any key was pressed.
    Input: a boolean indicating whether exit button was pressed.
    Output: a boolean indicating whether exit button was pressed.'''
    pygame.mixer.music.pause()
    s = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
    s.set_alpha(128)            
    s.fill(WHITE)           
    screen.blit(s, (0,0))
    create_text("Press any key to continue", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), "Calibri", 50, BLACK, True)
    pygame.display.flip()
    unpause = False
    while not finish and not unpause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                unpause = True
        clock.tick(REFRESH_RATE)
    pygame.mixer.music.unpause()
    return finish

def mute(muted, volume):
    '''Functions mutes and unmutes the music in the game.
    Input: a boolean indicating whether the game was muted beforehand.
    Output: a boolean indicating whether the game is currently muted.'''
    if muted:
        muted = False
        pygame.mixer.music.set_volume(volume)
    else:
        muted = True
        pygame.mixer.music.set_volume(0)
    return muted

def get_keyboard_language():
        """
        Gets the keyboard language in use by the current
        active window process.
        """

        languages = {'0x409': 'English'}

        user32 = ctypes.WinDLL('user32', use_last_error=True)
        # Get the current active window handle
        handle = user32.GetForegroundWindow()
        # Get the thread id from that window handle
        threadid = user32.GetWindowThreadProcessId(handle)
        # Get the keyboard layout id from the threadid
        layout_id = user32.GetKeyboardLayout(threadid)
        # Extract the keyboard language id from the keyboard layout id
        language_id = layout_id & (2 ** 16 - 1)
        # Convert the keyboard language id from decimal to hexadecimal
        language_id_hex = hex(language_id)
        # Check if the hex value is in the dictionary.
        if language_id_hex in languages.keys():
            return languages[language_id_hex]
        else:
            # Return language id hexadecimal value if not found.
            return str(language_id_hex)
    
    
            

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gran Turismo")
clock = pygame.time.Clock()

go_sign = pygame.image.load('./contents/go.png').convert()
go_sign.set_colorkey(PINK)
sign_1 = pygame.image.load('./contents/1.png').convert()
sign_1.set_colorkey(PINK)
sign_2 = pygame.image.load('./contents/2.png').convert()
sign_2.set_colorkey(PINK)
sign_3 = pygame.image.load('./contents/3.png').convert()
sign_3.set_colorkey(PINK)
logo = pygame.image.load('./contents/logo.png')
pause_logo = pygame.image.load('./contents/pause.png').convert()
pause_logo.set_colorkey(PINK)
mute_logo = pygame.image.load('./contents/mute.png')
unmute_logo = pygame.image.load('./contents/unmute.png')
reset = pygame.image.load('./contents/reset.png')

tree1 = pygame.image.load('./contents/tree1.png').convert()
tree1.set_colorkey(PINK)

car_yellow = pygame.image.load('./contents/car-yellow.png').convert()
car_yellow.set_colorkey(GREEN)
car_green = pygame.image.load('./contents/car-green.png').convert()
car_green.set_colorkey(PINK)
car_tourquese = pygame.image.load('./contents/car-tourquise.png').convert()
car_tourquese.set_colorkey(PINK)
car_orange = pygame.image.load('./contents/car-orange.png').convert()
car_orange.set_colorkey(PINK)
car_red = pygame.image.load('./contents/car-red.png').convert()
car_red.set_colorkey(PINK)
car_blue = pygame.image.load('./contents/car-blue.png').convert()
car_blue.set_colorkey(PINK)

pygame.mixer.init()
pygame.mixer.music.load('./contents/Moon Over The Castle.mp3')
pygame.mixer.music.set_volume(DEFAULT_VOLUME)
pygame.mixer.music.play(-1)




    
def main():
    '''Function is the main function where the main loop takes place and all game is managed.
    No input and no output.'''
    if not path.exists("./contents/leaderboard.txt"):
        reset_leaderboard()
    car_models = [[car_green, 142, 70], [car_tourquese, 114, 70], [car_orange,153,70],[car_red,137,65],[car_blue,137,70]]
    player_car_model = [car_yellow, 137, 70]
    
    trees = []
    cows = []
    cars = []
    lines = set_lines()
    side_lines = set_side_lines()
    finish = False
    main_menu = True
    muted = False
    volume = DEFAULT_VOLUME
    print("\nWelcome to Gran Turismo!")

    while not finish:
        menu_speed = 50
        menu_center_pos = [WINDOW_WIDTH // 2, int(-((WINDOW_HEIGHT // 1.4) // 2))]
        in_out = 1
        speed = DEFAULT_SPEED
        cars_speed = DEFAULT_CARS_SPEED
        start_ticks = pygame.time.get_ticks()

        while not finish and in_out != -1 and main_menu:
            """
            Main menu
            """
            
            set_background()
                
            trees, cows = change_background(trees, cows, speed, TREE_DENSITY, COW_DENSITY)
            lines = move_lines(lines, speed)
            side_lines = move_side_lines(side_lines, speed)
            for side_line in side_lines:
                pygame.draw.rect(screen, side_line[2], side_line[:2] + [SIDE_LINES_WIDTH, SIDE_LINES_HEIGHT])
            for line in lines:
                pygame.draw.rect(screen, WHITE, line + [LINES_WIDTH, LINES_HEIGHT])
            for tree in trees:
                screen.blit(tree1, tree)
            cars = create_cars(cars, car_models, player_car_model[2])
            cars = move_cars(cars, speed, cars_speed)
            for car in cars:
                screen.blit(car[2], car[:2])

            menu_center_pos, in_out, menu_speed, playnow_rect, none, none2 = game_menu(menu_center_pos, in_out, menu_speed, 1,rank=False,score=0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] > playnow_rect[0] and mouse_pos[0] < playnow_rect[0] + playnow_rect[2] and \
                        mouse_pos[1] > playnow_rect[1] and mouse_pos[1] < playnow_rect[1] + playnow_rect[3]:
                        in_out = 2
                        menu_speed = 10
                    elif mouse_pos[0] > 60 and mouse_pos[0] < 100 and mouse_pos[1] > 0 and mouse_pos[1] < 50:
                        muted = mute(muted, volume)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        muted = mute(muted, volume)
                    elif event.key == pygame.K_r:
                        speed = DEFAULT_SPEED
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                        volume += 0.1
                        pygame.mixer.music.set_volume(volume)
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        volume -= 0.1
                        pygame.mixer.music.set_volume(volume)

            if muted:
                screen.blit(mute_logo, (60, 10))
            else:
                screen.blit(unmute_logo, (60, 10))

            seconds = (pygame.time.get_ticks()-start_ticks)/1000
            if seconds > 10:
                start_ticks = pygame.time.get_ticks()
                speed += 1

            
            pygame.display.flip()
            clock.tick(REFRESH_RATE)
        if main_menu:
            finish = reset_vehicles(finish, trees, cows, lines, side_lines, cars)
            
        score = 0
        cars = []
        player_car = [lane_pos(MIDDLE_LANE,player_car_model[2]), WINDOW_HEIGHT] + player_car_model
        temp_speed = 1
        go = False
        start_ticks = pygame.time.get_ticks()
        counter = 0
        sign_pos = [(WINDOW_WIDTH // 2) - 50, int(WINDOW_HEIGHT * 0.25)]
        
        while not go and not finish:
            """
            Game start phase
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] > 0 and mouse_pos[0] < 50 and mouse_pos[1] > 0 and mouse_pos[1] < 57:
                        finish = pause(finish)
                    elif mouse_pos[0] > 60 and mouse_pos[0] < 100 and mouse_pos[1] > 0 and mouse_pos[1] < 50:
                        muted = mute(muted, volume)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        finish = pause(finish)
                    elif event.key == pygame.K_m:
                        muted = mute(muted, volume)
                    
            seconds = (pygame.time.get_ticks()-start_ticks)/1000
            if seconds > 1:
                start_ticks = pygame.time.get_ticks()
                counter += 1
            if player_car[1] > int(WINDOW_HEIGHT * 0.74):
                if player_car[1] < int(WINDOW_HEIGHT * 0.85):
                    temp_speed -= 2
                player_car, temp_speed = move_car(player_car, temp_speed)
                
            set_background()
            for side_line in side_lines:
                pygame.draw.rect(screen, side_line[2], side_line[:2] + [SIDE_LINES_WIDTH, SIDE_LINES_HEIGHT])
            for line in lines:
                pygame.draw.rect(screen, WHITE, line + [LINES_WIDTH, LINES_HEIGHT])
            for tree in trees:
                screen.blit(tree1, tree)
            screen.blit(player_car[2], player_car[:2])
            
            if counter == 4:
                screen.blit(go_sign, sign_pos)
                go = True
            elif counter == 3:
                screen.blit(sign_1, sign_pos)
            elif counter == 2:
                screen.blit(sign_2, sign_pos)
            elif counter == 1:
                screen.blit(sign_3, sign_pos)

            side_score(score)
            screen.blit(pause_logo,(10,10))
            if muted:
                screen.blit(mute_logo, (60, 10))
            else:
                screen.blit(unmute_logo, (60, 10))
            
            pygame.display.flip()
            clock.tick(REFRESH_RATE)
            
        move_to_lane = MIDDLE_LANE
        speed = 0
        cars_speed = DEFAULT_CARS_SPEED
        start_ticks = pygame.time.get_ticks()
        while (not (is_crash(player_car, cars) or finish)):
            """
            Actual game phase
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] > 0 and mouse_pos[0] < 50 and mouse_pos[1] > 0 and mouse_pos[1] < 57:
                        finish = pause(finish)
                    elif mouse_pos[0] > 60 and mouse_pos[0] < 100 and mouse_pos[1] > 0 and mouse_pos[1] < 50:
                        muted = mute(muted, volume)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and move_to_lane < RIGHT_LANE:
                        move_to_lane += 1
                    elif event.key == pygame.K_LEFT and move_to_lane > LEFT_LANE:
                        move_to_lane -= 1
                    elif event.key == pygame.K_p:
                        finish = pause(finish)
                    elif event.key == pygame.K_m:
                        muted = mute(muted, volume)
                        
            if speed < DEFAULT_SPEED:
                speed += 1

            seconds = (pygame.time.get_ticks()-start_ticks)/1000
            if seconds > 25:
                start_ticks = pygame.time.get_ticks()
                speed += 1
            
            set_background()
            
            trees, cows = change_background(trees, cows, speed, TREE_DENSITY, COW_DENSITY)
            lines = move_lines(lines, speed)
            side_lines = move_side_lines(side_lines, speed)
            for side_line in side_lines:
                pygame.draw.rect(screen, side_line[2], side_line[:2] + [SIDE_LINES_WIDTH, SIDE_LINES_HEIGHT])
            for line in lines:
                pygame.draw.rect(screen, WHITE, line + [LINES_WIDTH, LINES_HEIGHT])
            for tree in trees:
                screen.blit(tree1, tree)

            if sign_pos[1] < WINDOW_HEIGHT:
                sign_pos[1] += speed
                screen.blit(go_sign, sign_pos)
            
            cars = create_cars(cars, car_models, player_car[3])
            cars = move_cars(cars, speed, cars_speed)
            for car in cars:
                screen.blit(car[2], car[:2])
                
            player_car = move_lanes(player_car, move_to_lane)
            screen.blit(player_car[2], player_car[:2])

            score += speed
            side_score(score)
            screen.blit(pause_logo,(10,10))
            if muted:
                screen.blit(mute_logo, (60, 10))
            else:
                screen.blit(unmute_logo, (60, 10))
            
            pygame.display.flip()
            clock.tick(REFRESH_RATE)

        if not finish :
            name = "______"
            rank = find_score_rank(score)
            if rank:
                update_leaderboard(rank,name,str(score))
            pygame.time.wait(500)
            menu_center_pos = [WINDOW_WIDTH // 2, int(-((WINDOW_HEIGHT // 1.4) // 2))]
            in_out = 1
            menu_speed = 50
        while((not finish) and not in_out == -1):
            """
            End menu phase
            """
            
            set_background()
            for side_line in side_lines:
                pygame.draw.rect(screen, side_line[2], side_line[:2] + [SIDE_LINES_WIDTH, SIDE_LINES_HEIGHT])
            for line in lines:
                pygame.draw.rect(screen, WHITE, line + [LINES_WIDTH, LINES_HEIGHT])
            for tree in trees:
                screen.blit(tree1, tree)
            for car in cars:
                screen.blit(car[2], car[:2])
            screen.blit(player_car[2], player_car[:2])
            menu_center_pos, in_out, menu_speed, playagain_rect, mainmenu_rect, reset_pos = game_menu(menu_center_pos,in_out,menu_speed,2,rank, score)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                if event.type == KEYDOWN and rank:
                    if event.unicode.isalpha() and name[-1] == "_" and get_keyboard_language() == "English":
                        name = name.replace("_", event.unicode,1)
                        update_leaderboard_name(rank,name,str(score))
                    elif event.key == K_BACKSPACE:
                        deleted = False
                        for tav in name[::-1]:
                            if tav != "_" and not deleted:
                                deleted = True
                                name = name[::-1].replace(tav, "_",1)
                                name = name[::-1]
                                update_leaderboard_name(rank,name,str(score))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        in_out = 3
                        menu_speed = 10
                        main_menu = False
                    elif event.key == pygame.K_m:
                        muted = mute(muted, volume)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] > playagain_rect[0] and mouse_pos[0] < playagain_rect[0] + playagain_rect[2] and \
                        mouse_pos[1] > playagain_rect[1] and mouse_pos[1] < playagain_rect[1] + playagain_rect[3]:
                        in_out = 3
                        menu_speed = 10
                        main_menu = False
                    elif mouse_pos[0] > mainmenu_rect[0] and mouse_pos[0] < mainmenu_rect[0] + mainmenu_rect[2] and \
                        mouse_pos[1] > mainmenu_rect[1] and mouse_pos[1] < mainmenu_rect[1] + mainmenu_rect[3]:
                        in_out = 2
                        menu_speed = 10
                        main_menu = True
                    elif mouse_pos[0] > 60 and mouse_pos[0] < 100 and mouse_pos[1] > 0 and mouse_pos[1] < 50:
                        muted = mute(muted, volume)
                    elif mouse_pos[0] > reset_pos[0] and mouse_pos[0] < reset_pos[0] + 35 and mouse_pos[1] > reset_pos[1] and mouse_pos[1] < reset_pos[1] + 30:
                        reset_leaderboard()

            if muted:
                screen.blit(mute_logo, (60, 10))
            else:
                screen.blit(unmute_logo, (60, 10))
                        
            pygame.display.flip()
            clock.tick(REFRESH_RATE)

        cars.append(player_car)
        finish = reset_vehicles(finish, trees, cows, lines, side_lines, cars)
                 
    pygame.quit()

main()

    
