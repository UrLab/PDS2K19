#!/usr/bin/env python

import nxt.locator
from time import sleep
from nxt.motor import *
from SimpleCV import Image, Camera
import datetime
from utils import normalize_img

FORTH = 100
BACK = -100


class Interface(object):

    def __init__(self):
        self.b = nxt.locator.find_one_brick()
        self.cam = Camera()
        self.path = None

    def take_pic(self):
        img = self.cam.getImage()
        return normalize_img(img)
        
    def save_img(self, img):
        now = datetime.datetime.now()
        path = '{}-{}-{}-{}-{}-{}'.format(now.year, now.month, now.day,
                                          now.hour, now.minute, now.second)
        path += ".jpg"
        img.save(path)
        self.path = path

    def left(self):
        m_left = Motor(self.b, PORT_C)
        m_right = Motor(self.b, PORT_B)
        m_left.turn(-100, 15)
        m_right.turn(100, 15)

    def right(self):
        m_left = Motor(self.b, PORT_C)
        m_right = Motor(self.b, PORT_B)
        m_right.turn(-100, 15)
        m_left.turn(100, 15)

    def forward(self):
        legs = [Motor(self.b, PORT_B), Motor(self.b, PORT_C)]

        legs[0].run(FORTH)
        legs[1].run(FORTH)
        sleep(1)
        legs[0].idle()
        legs[1].idle()

    def back(self):
        legs = [Motor(self.b, PORT_B), Motor(self.b, PORT_C)]
        legs[0].run(BACK)
        legs[1].run(BACK)
        sleep(1)
        legs[0].idle()
        legs[1].idle()
