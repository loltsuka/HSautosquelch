#!/usr/bin/env python

import os
import win32gui
from pynput.mouse import Controller, Button
import sys
from time import sleep

class Squelcher():
    def __init__(self):
        self.path_to_log            = ''
        self.step_list              = []
        self.window_top_coord       = 0
        self.window_bottom_coord    = 0
        self.window_left_coord      = 0
        self.window_right_coord     = 0
        self.window_size            = [0, 0] #x, y
        self.hwnd                   = 0
        self.enemy_face_x           = 0
        self.enemy_face_y           = 0
        self.bubble_x               = 0
        self.bubble_y               = 0
        self.m                      = Controller()
        self.m.position             = (0, 0)
        self.GetPathToLog()        
        self.main()

    def main(self):
        #Main loop
        try:
            while True:
                self.FindHearthstone()
                try:
                    self.GetLog()
                except:
                    continue

                try:
                    if self.CurrentGameStep() == 'game_start':
                        print('New game found, waiting for mulligan phase to end.')
                        while True:
                            self.GetLog()
                            if self.CurrentGameStep() == 'main':
                                print('Muting opponent')
                                self.GetWindowCoords()
                                self.CalcWindowSize()
                                self.EnemyPosition()
                                self.SquelchBubblePosition()
                                self.Squelch()
                                print('Muted opponent')
                                break

                            sleep(1)
                except:
                    pass

                sleep(0.5)

        except Exception as e:
            print(e)

    def FindHearthstone(self):
        try:
            while True:
                hs_hwnd = win32gui.FindWindowEx(None, None, None, 'hearthstone')
                if hs_hwnd != 0:
                    self.hwnd = hs_hwnd
                    break
                else:
                    print('Hearthstone not found')
                    sleep(1)
        except Exception as e:
            print(e)

    def GetWindowCoords(self):
        window_specs = win32gui.GetWindowRect(self.hwnd)
        self.window_left_coord      = window_specs[0]
        self.window_top_coord       = window_specs[1]
        self.window_right_coord     = window_specs[2]     
        self.window_bottom_coord    = window_specs[3]
        #print(window_specs)

    def CalcWindowSize(self):
        self.window_size[0] = self.window_right_coord  - self.window_left_coord
        self.window_size[1] = self.window_bottom_coord - self.window_top_coord 

    def CurrentGameStep(self):
        current_game_step = list(reversed(self.step_list))[0]
        if current_game_step == 'value=BEGIN_MULLIGAN':
            return 'game_start'
        elif current_game_step == 'value=MAIN_ACTION':
            return 'main'
        elif current_game_step == 'value=FINAL_GAMEOVER':
            return 'game_over'
        else:
            return 'something'

    def GetLog(self):
        with open(self.path_to_log, 'r') as f:
            for line in f:
                split_line = line.split(' ')
                if len(split_line) == 13:
                    if 'tag=STEP' in split_line:
                        self.step_list.append(split_line[11])

    def PrintLog(self):
        for line in self.step_list:
            print(Line)

    def GetPathToLog(self):
        #self.path_to_log = 'E:\\Hearthstone\\Logs\\Power.log'
        self.path_to_log = os.getcwd() + '\\Power.log'
        print(self.path_to_log)

    def EnemyPosition(self):
        self.enemy_face_x = int((self.window_size[0] / 2) + self.window_left_coord)
        self.enemy_face_y= int((0.25 * self.window_size[1]) + self.window_top_coord)

    def SquelchBubblePosition(self):
        self.bubble_x = int((0.42 * self.window_size[0]) + self.window_left_coord)
        self.bubble_y = int((0.1 * self.window_size[1]) + self.window_top_coord)

    def Squelch(self):
        current_x = self.m.position[0]
        current_y = self.m.position[1]  
        self.m.position = (self.enemy_face_x, self.enemy_face_y)
        sleep(0.05)
        self.m.click(Button.right, 1)
        sleep(0.2)
        self.m.position = (self.bubble_x, self.bubble_y)
        sleep(0.05)
        self.m.click(Button.left, 1)
        sleep(0.05)
        self.m.position = (current_x, current_y)

if __name__ == "__main__":
    Squelcher()
