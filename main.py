import numpy as np
import pygame
from interact import *

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def buddha_blessing():
##                        _oo0oo_
##                       o8888888o
##                       88" . "88
##                       (| -_- |)
##                       0\  =  /0
##                     ___/`---'\___
##                   .' \\|     |// '.
##                  / \\|||  :  |||// \
##                 / _||||| -:- |||||- \
##                |   | \\\  -  /// |   |
##                | \_|  ''\---/''  |_/ |
##                \  .-\__  '-'  ___/-. /
##             ___'. .'  /--.--\  `. .'___
##           ."" '<  `.___\_<|>_/___.' >' "".
##          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
##         \  \ `_.   \_ __\ /__ _/   .-` /  /
##     =====`-.____`.___ \_____/___.-`___.-'=====
##                        `=---='
    nope=0

pygame.init()

screen = Screen()

run = True
mode = 0
pos = 0
screen.Background()

def point_in_any_rect(point):
    for rect in screen.rects_array:
        if rect and rect.collidepoint(point):
            return True
    return False
#check xem node mới tạo có nằm quá gần bất cứ điểm nào đã tạo sẵn không
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_pressed()[0] == 1:
            if screen.mode[mode] == "setup":
                    pos = pygame.mouse.get_pos()
                    if screen.size < 10 and point_in_any_rect(pos)==False:
                        screen.Create_node(pos)
                    pygame.time.wait(200)

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                #bấm enter để chuyển sang giai đoạn mới
                mode = clamp(mode+1, 0, screen.mode.size-1)

                if screen.mode[mode] == "create_matrix":
                    screen.Create_matrix()

                if screen.mode[mode] == "it's_aco_time":
                    screen.ACO()
                
    pygame.display.update()

pygame.quit()