import sys
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
from strings import game_over, win
from maps import *
from utils import *

class Snake:
    REV_DIR_MAP = {
        KEY_RIGHT: KEY_LEFT,
        KEY_LEFT: KEY_RIGHT,
        KEY_DOWN: KEY_UP,
        KEY_UP: KEY_DOWN
    }

    def __init__(self, x, y, window):
        self.bodylist = []
        self.hit_score = 0
        self.timeout = TIMEOUT

        for i in range(SNAKE_LENGTH, 0, -1):
            self.bodylist.append(Body(x - i, y))
        
        self.window = window
        self.bodylist.append(Body(x, y, '0'))
        self.last_head_coor = (x, y)
        self.direction = KEY_RIGHT

        self.direction_map = {
            KEY_RIGHT: self.move_right,
            KEY_LEFT: self.move_left,
            KEY_UP: self.move_up,
            KEY_DOWN: self.move_down,
        }

    @property
    def coor(self):
        return self.x, self.y

    @property
    def head(self):
        return self.bodylist[-1]

    def eat_food(self, food):
        food.coor_gen()

        body = Body(self.last_head_coor[0], self.last_head_coor[1])
        self.bodylist.insert(-1, body)
        self.hit_score += 1
        
        if self.hit_score == 10:
             self.timeout -= 1
             self.window.timeout(self.timeout)

    @property
    def score(self):
        return ' Score: {} / {} '.format(self.hit_score, level_list[level][2])

    def change_direction(self, direction):
        if Snake.REV_DIR_MAP[self.direction] != direction:
            self.direction = direction

    def collided(self):
        return any(body.coor == self.head.coor for body in self.bodylist[:-1]) or any(snake.head.x == coor_pair[0] and snake.head.y == coor_pair[1] for coor_pair in level_list[level][0].coor)
    
    
    def render(self):
        for body in self.bodylist:
            self.window.addstr(body.y, body.x, body.char)
    
    def update(self):
        body = self.bodylist.pop(0)

        body.x = self.bodylist[-1].x
        body.y = self.bodylist[-1].y
        self.bodylist.insert(-1, body)

        self.last_head_coor = (self.head.x, self.head.y)
        self.direction_map[self.direction]()

    def reset(self, head_coor, length):
        self.bodylist = []
        x = head_coor[0]
        y = head_coor[1]

        for i in range(length, 0, -1):
            self.bodylist.append(Body(x - i, y))
        
        self.bodylist.append(Body(x, y, '0'))
        self.direction = KEY_RIGHT
        self.timeout = TIMEOUT
        self.window.timeout(self.timeout)

    def move_right(self):
        self.head.x += 1
        if self.head.x > MAX_X:
            self.head.x = 1
    
    def move_left(self):
        self.head.x -= 1
        if self.head.x < 1:
            self.head.x = MAX_X
        
    def move_up(self):
        self.head.y -= 1
        if self.head.y < 1:
            self.head.y = MAX_Y
    
    def move_down(self):
        self.head.y += 1
        if self.head.y > MAX_Y:
            self.head.y = 1

class Body:
    def __init__(self, x, y, char = '='):
        self.x = x
        self.y = y
        self.char = char
    
    @property
    def coor(self):
        return self.x, self.y

class Food:
    def __init__(self, window, loc_coor, char= '*'):
        self.loc_coor = loc_coor
        self.coor_gen()
        self.window = window
        self.char = char
    
    def coor_gen(self):
        while True:
            xy = (randint(1, MAX_X), randint(1, MAX_Y))
            snake_xy = [body.coor for body in snake.bodylist]

            if xy not in self.loc_coor and xy not in snake_xy:
                self.x = xy[0]
                self.y = xy[1]
                break

    def render(self):
        self.window.addstr(self.y, self.x, self.char)

if __name__ == '__main__':
    curses.initscr()
    window = curses.newwin(HEIGHT, WIDTH, 5, 40)
    curses.beep()
    window.timeout(TIMEOUT)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)

    snake = Snake(SNAKE_X, SNAKE_Y, window)
    food = Food(window, loc1_coor)
    

    map1 = Location(loc1_coor, window)
    map2 = Location(loc2_coor, window)
    map3 = Location(loc3_coor, window)

    newlevel = True
    level = 0
    level_list = [(map1, loc1_safe, point1), (map2, loc2_safe, point2), (map3, loc3_safe, point3)]

    while True:
        window.clear()

        if newlevel:
            key = -1
            while key != 32:
                window.border(0)
                window.addstr(9, 3, 'Level {}. Press "Space" to start'.format(level + 1))
                snake.reset(level_list[level][1], 5)
                food.loc_coor = level_list[level][0].coordinates
                food.coor_gen()
                key = window.getch()

            newlevel = False

        food.render()
        snake.render()
        level_list[level][0].render()
        window.border(0)

        window.addstr(0, 5, snake.score)

        event = window.getch()

        if event == 27:
            break
        
        if snake.hit_score == level_list[level][2]:
            if level + 1 == len(level_list):
                key = -1
                while True:
                    window.clear()
                    window.addstr(3, 1, win)
                    key = window.getch()

                    if key == 27:
                        sys.exit()
                    elif key == 32:
                        level = -1
                        break
            
            newlevel = True
            level += 1
            snake.hit_score = 0
            continue

        if event in (KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN):
            snake.change_direction(event)
        
        if snake.head.x == food.x and snake.head.y == food.y:
            snake.eat_food(food)

        if event == 32:
            key = -1

            while key != 32:
                key = window.getch()
        
        snake.update()

        if snake.collided():
            key = -1
            while True:
                window.clear()
                window.addstr(1,1, game_over)
                snake.hit_score = 0
                window.timeout(TIMEOUT)
                key = window.getch()

                if key == 27:
                    sys.exit()
                elif key == 32:
                    level = 0
                    newlevel = True
                    break
    
    curses.endwin()