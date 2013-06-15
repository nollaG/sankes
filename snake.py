#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from __future__ import division
from visual import *
from visual.controls import *
import random
import sys
import collections
import math

g_is_snooker=False
g_is_paused=False
color.brown=(0.64,0.18,0.18)
color.pink=(0.43,0.14,0.43)
color.lightgray=(0.2,0.2,0.2)

class Direction:
    up=vector(0,5,0)
    down=vector(0,-5,0)
    left=vector(-5,0,0)
    right=vector(5,0,0)

class Food:
    def __init__(self,ball,score):
        self.ball=ball
        self.score=score

class scoreColor:
    Color=[color.white,color.red,color.yellow,color.green,color.brown,color.blue,color.pink,color.black]

class Snake:
    def __init__(self,head=vector(2.5,2.5,0),scorepos=vector(0,-60,0),length=6,velocity=Direction.up):
        global g_is_snooker
        global g_is_paused
        self.body=collections.deque()
        for i in range(length):
            self.body.append(sphere(pos=head-velocity*i,radius=2.5,color=color.white))
        if length>0:
            self.body[0].color=color.blue
        self.velocity=velocity
        self.currentScore=0
        self.scoreDisplay=label(text="Score:{0}".format(self.currentScore),pos=scorepos,color=color.green,box=False,height=15)
        if g_is_snooker:
            self.wantDisplay=label(text="WantRed".format(self.currentScore),pos=scorepos+vector(40,0,0),color=color.green,box=False,height=15)
        self.wantRed=True
        self.pausedDisplay=label(text="paused",pos=(-30,-60,0),color=color.green,box=False,height=15)
        self.pausedDisplay.visible=g_is_paused

    def RefreshScore(self):
        global g_is_snooker
        self.scoreDisplay.text="Score:{0}".format(self.currentScore)
        if g_is_snooker:
            self.wantDisplay.text="WantRed" if self.wantRed else "WantColor"

    def isDie(self):
        if self.body[0].pos.x<-50:
            return true
        if self.body[0].pos.x>50:
            return true
        if self.body[0].pos.y<-50:
            return true
        if self.body[0].pos.y>50:
            return true
        for i in range(1,len(self.body)):
            if self.body[0].pos==self.body[i].pos:
                return true
        else:
            return false

    def Move(self):
        global foodList
        global g_is_snooker
        self.body.appendleft(sphere(pos=self.body[0].pos+self.velocity,radius=2.5,color=color.blue))
        self.body[1].color=color.white
        for i in range(len(foodList)):
            if foodList[i].ball.pos==snake.body[0].pos:
                foodList[i].ball.visible=False
                if not g_is_snooker:
                    self.currentScore+=foodList[i].score
                    self.RefreshScore()
                    foodList.append(CreateOneFood())
                else:
                    if foodList[i].score==1:
                        if self.wantRed:
                            self.currentScore+=foodList[i].score
                            self.wantRed=False
                            self.RefreshScore()
                        else:
                            self.currentScore-=4
                            self.RefreshScore()
                    else:
                        if self.wantRed:
                            self.currentScore-=max(4,foodList[i].score)
                            self.RefreshScore()
                        else:
                            self.currentScore+=foodList[i].score
                            self.wantRed=True
                            self.RefreshScore()
                        foodList.append(CreateOneFood(foodList[i].score))
                del foodList[i]
                break
        else:
            self.body[-1].visible=False
            del self.body[-1]
        if self.isDie():
            self.scoreDisplay.text="Game Over!Score:{0:d}".format(self.currentScore)
            exit()
        if g_is_snooker:
            CreateFood_snooker()
             




def Init():
    global g_is_snooker
    global foodList
    #Init the Window
    mainwindow=scene.get_selected()
    mainwindow.visible=False
    mainwindow.width=600
    mainwindow.height=600
    mainwindow.title="snake"
    mainwindow.background=color.lightgray
    mainwindow.visible=True
    #Just to see the score
    sphere(pos=(0,-70,0),radius=0)
    #Init the walls
    box(pos=(-51,0,0),size=(1,102,0),color=color.green)
    box(pos=(51,0,0),size=(1,102,0),color=color.green)
    box(pos=(0,51,0),size=(102,1,0),color=color.green)
    box(pos=(0,-51,0),size=(102,1,0),color=color.green)
    #Init the snake
    snake=Snake()
    if g_is_snooker:
        sphere(pos=(60,60,0),radius=2.5,color=color.red)
        sphere(pos=(60,50,0),radius=2.5,color=color.yellow)
        sphere(pos=(60,40,0),radius=2.5,color=color.green)
        sphere(pos=(60,30,0),radius=2.5,color=color.brown)
        sphere(pos=(60,20,0),radius=2.5,color=color.blue)
        sphere(pos=(60,10,0),radius=2.5,color=color.pink)
        sphere(pos=(60,0,0),radius=2.5,color=color.black)
        label(pos=(65,61,0),text='1',color=color.green,box=False)
        label(pos=(65,51,0),text='2',color=color.green,box=False)
        label(pos=(65,41,0),text='3',color=color.green,box=False)
        label(pos=(65,31,0),text='4',color=color.green,box=False)
        label(pos=(65,21,0),text='5',color=color.green,box=False)
        label(pos=(65,11,0),text='6',color=color.green,box=False)
        label(pos=(65,0,0),text='7',color=color.green,box=False)
    return snake


def CreateOneFood(score=1):
    while True:
        foodx=random.randint(-10,9)*5+2.5
        foody=random.randint(-10,9)*5+2.5
        if isOccupied(vector(foodx,foody,0)):
            continue
        else:
            food=Food(sphere(pos=(foodx,foody,0),radius=2.5,color=scoreColor.Color[score]),score)
            break
    return food

def isOccupied(pos):
    global foodList
    global snake
    for i in snake.body:
        if i.pos==pos:
            return true
    for i in foodList:
        if i.ball.pos==pos:
            return true
    return false



def CreateFood_snooker():
    global foodList
    global snake
    if len(foodList)>=10:
        return
    t=random.randint(0,80)
    rednum=filter(lambda x:x.score==1,foodList)
    if len(rednum)>5 and t<=5:
        return 
    if len(rednum)<2:
        t=0
    if t<=5:
        foodList.append(CreateOneFood(1))

        


if len(sys.argv)>1:
    if sys.argv[1]=='--snooker':
        g_is_snooker=True
foodList=[]
snake=Init()
if not g_is_snooker:
    foodList.append(CreateOneFood())
else:
    for i in range(2,8):
        foodList.append(CreateOneFood(i))
while True:
    if not g_is_snooker:
        rate(5+snake.currentScore/15)
    else:
        rate(5+snake.currentScore/100)
    if scene.kb.keys:
        s=scene.kb.getkey()
        if s==' ':
            g_is_paused=not g_is_paused
            snake.pausedDisplay.visible=g_is_paused
        if g_is_paused:
            continue
        if s=='left':
            if snake.velocity==Direction.left:
                snake.Move()
            elif snake.velocity!=Direction.right:
                snake.velocity=Direction.left
            snake.Move()
            continue
        if s=='right':
            if snake.velocity==Direction.right:
                snake.Move()
            elif snake.velocity!=Direction.left:
                snake.velocity=Direction.right
            snake.Move()
            continue
        if s=='up':
            if snake.velocity==Direction.up:
                snake.Move()
            elif snake.velocity!=Direction.down:
                snake.velocity=Direction.up
            snake.Move()
            continue
        if s=='down':
            if snake.velocity==Direction.down:
                snake.Move()
            elif snake.velocity!=Direction.up:
                snake.velocity=Direction.down
            snake.Move()
            continue
    if not g_is_paused:
        snake.Move()
