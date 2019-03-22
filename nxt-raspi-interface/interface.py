#!/usr/bin/env python

import nxt.locator
from time import sleep
from nxt.motor import *

FORTH = 100
BACK = -100


def left(b):
    m_left = Motor(b, PORT_B)
    m_left.turn(100, 15)


def right(b):
    m_right = Motor(b, PORT_C)
    m_right.turn(-100, 15)


def forward(b):
    legs = [Motor(b, PORT_B), Motor(b, PORT_C)]

    legs[0].run(FORTH)
    legs[1].run(FORTH)
    sleep(1)
    legs[0].idle()
    legs[1].idle()


def back(b):
    legs = [Motor(b, PORT_B), Motor(b, PORT_C)]
    legs[0].run(BACK)
    legs[1].run(BACK)
    sleep(1)
    legs[0].idle()
    legs[1].idle()


b = nxt.locator.find_one_brick()
forward(b)
back(b)
left(b)
right(b)
