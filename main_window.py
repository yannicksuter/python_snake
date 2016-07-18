#!/usr/local/bin/python
# coding: utf-8

import curses
import time
import traceback
from random import randrange

SPEED = .1

class SnakeGame:
    def __init__(self, screen):
        self.screen = screen
        self.size = screen.getmaxyx()
        self.canvasDim = [self.size[0]-10, self.size[1]-20]
        self.canvas = screen.subwin(self.canvasDim[0], self.canvasDim[1], (self.size[0] - self.canvasDim[0]) / 2, (self.size[1] - self.canvasDim[1]) / 2)
        self.canvas.keypad(1)
        self.canvas.nodelay(True)

        curses.init_pair(3, curses.COLOR_WHITE, 10)
        self.canvas.bkgd(' ', curses.color_pair(3))

        # initial worm direction
        midY, midX = self.canvasDim[0] >> 1, self.canvasDim[1] >> 1
        self.worm = [[midX, midY+1],[midX, midY],[midX, midY-1],[midX, midY-2]]
        self.dirX = 0
        self.dirY = 1
        self.lockedKey = curses.KEY_DOWN
        self.score = 0

    def getCharAt(self, x, y):
        return chr(self.canvas.inch(y, x) & 0xFF)

    def newStrawberryPos(self):
        while True:
            x, y = randrange(1, self.size[0]), randrange(1, self.size[1])
            if (self.getCharAt(x, y)) == ' ':
                self.canvas.addch(y, x, '@')
                return [x, y]

    def moveHeadTail(self):
        # new position & check for collision
        newHeadPos = [(self.worm[0][0]+self.dirX) % (self.canvasDim[1]), (self.worm[0][1]+self.dirY) % self.canvasDim[0]]
        ch = self.getCharAt(newHeadPos[0], newHeadPos[1])
        if ch == '@':
            # define new strawberry and grow worm
            self.newStrawberryPos()
            self.worm = [newHeadPos] + self.worm
            self.score += 1
            self.screen.addstr(0,0,"\033[22;31m%dScore: {}".format(self.score))
        elif ch == ' ':
            # rotate and move head
            self.canvas.addch(self.worm[-1][1], self.worm[-1][0], ' ')
            self.worm = self.worm[-1:] + self.worm[:-1]
            self.worm[0] = newHeadPos
        elif ch == '#':
            # worm collision! baem...
            return False

        # self.screen.addstr(1, 0, "{}/{}               ".format(self.worm[0][1], self.worm[0][0]))
        self.canvas.addch(self.worm[0][1], self.worm[0][0], '#')
        return True

    def main(self):
        # draw initial worm
        for wormElement in self.worm:
            self.canvas.addch(wormElement[1], wormElement[0], '#')
        # initial eat item
        self.newStrawberryPos()

        # game loop
        while True:
            c = self.canvas.getch()
            if c != -1 and c != self.lockedKey:
                if c == curses.KEY_RIGHT:
                    self.dirX, self.dirY, self.lockedKey = 1, 0, curses.KEY_RIGHT
                elif c == curses.KEY_LEFT:
                    self.dirX, self.dirY, self.lockedKey =-1, 0, curses.KEY_LEFT
                elif c == curses.KEY_UP:
                    self.dirX, self.dirY, self.lockedKey = 0,-1, curses.KEY_UP
                elif c == curses.KEY_DOWN:
                    self.dirX, self.dirY, self.lockedKey = 0, 1, curses.KEY_DOWN

            if self.moveHeadTail() == False:
                return

            self.screen.refresh()
            time.sleep(SPEED)

def drawKitty():
    with open("hk.ascii", "r") as file:
        for line in file:
            stdscr.addstr(line)

if __name__=='__main__':
    try:
        # Initialize curses
        stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        #start main loop
        drawKitty()
        snake = SnakeGame(stdscr)
        snake.main()

        # Set everything back to normal
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

        print "Your final score: {}".format(snake.score)
    except:
        # In event of error, restore terminal to sane state.
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()
        traceback.print_exc()