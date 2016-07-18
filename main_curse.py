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
        self.size = stdscr.getmaxyx()
        midY, midX = self.size[0] >> 1, self.size[1] >> 1
        self.worm = [[midX, midY+1],[midX, midY],[midX, midY-1],[midX, midY-2]]
        # initial worm direction
        self.dirX = 0
        self.dirY = 1
        self.lockedKey = curses.KEY_DOWN
        self.score = 0

    def getCharAt(self, x, y):
        return chr(self.screen.inch(y, x) & 0xFF)

    def newStrawberryPos(self):
        while True:
            x, y = randrange(1, self.size[0]), randrange(1, self.size[1])
            if (self.getCharAt(x, y)) == ' ':
                self.screen.addch(y, x, '@')
                return [x, y]

    def moveHeadTail(self):
        # new position & check for collision
        newHeadPos = [(self.worm[0][0]+self.dirX) % (self.size[1]-1), (self.worm[0][1]+self.dirY) % self.size[0]]
        ch = self.getCharAt(newHeadPos[0], newHeadPos[1])
        if ch == '@':
            # define new strawberry and grow worm
            self.newStrawberryPos()
            self.worm = [newHeadPos] + self.worm
            self.score += 1
        elif ch == ' ':
            # rotate and move head
            self.screen.addch(self.worm[-1][1], self.worm[-1][0], ' ')
            self.worm = self.worm[-1:] + self.worm[:-1]
            self.worm[0] = newHeadPos
        elif ch == '#':
            # worm collision! baem...
            return False

        self.screen.addch(self.worm[0][1], self.worm[0][0], '#')
        return True

    def main(self):
        # draw initial worm
        for wormElement in self.worm:
            self.screen.addch(wormElement[1], wormElement[0], '#')
        # initial eat item
        self.newStrawberryPos()

        # game loop
        self.screen.nodelay(True)
        while True:
            c = self.screen.getch()
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

if __name__=='__main__':
    try:
        # Initialize curses
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.keypad(1)

        #start main loop
        snake = SnakeGame(stdscr)
        snake.main()

        # Set everything back to normal
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

        print "Your final score: {}".format(snake.score)
    except:
        # In event of error, restore terminal to sane state.
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()
        traceback.print_exc()