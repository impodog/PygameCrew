"""The Pygame Crew used constants"""
from numbers import Rational
from types import ModuleType
from typing import Sequence,Union,overload,Iterable,final
import pygame,sys,pyautogui,warnings,pyperclip
from calca.pysp import analyze, AnalyzingError, overloaded, typecheck
from calca import rangeac
import pyautogui,random,math
from abc import abstractmethod
from typing import Protocol, runtime_checkable, T_co, final, TypeVar
from ast import FunctionType
from calca.pysp import*
import numpy as np

ScreenLength,ScreenWidth=pyautogui.size()
Pos_=Pos_Like_=SubType(Iterable,(Rational,Rational))
rgb_=SubType(Iterable,(int,int,int))
rgb=TypeVar("rgb")
Pos=TypeVar("Pos")
Pos_Like=TypeVar("Pos_Like")
FilePathStr=str
#Unicode Options
CAPSABLE='abcdefghijklmnopqrstuvwxyz'
VISABLE=CAPSABLE+"`1234567890-=[]\\;',./"
#Regular colors
BLACK=(0,0,0)
WHITE=(255,255,255)
BACKGROUND_LIGHTBLUE=(42,194,213)
#Padding Colors
BUTTON_BACK_GREY=(225,225,225)
BUTTON_OUTLINE_GREY=(173,173,173)
BUTTON_BACKHIGHLIGHTED_BLUEGREY=(229,241,251)
BUTTON_OUTLINEHIGHLIGHTED_BLUEGREY=(0,120,215)

WINDOW_BODY_GREY=(200,200,200)
WINDOW_HEAD_WHITE=(240,240,240)
WINDOW_HEADHIGHLIGHTED_WHITE=(255,255,255)
WINDOW_OUTLINE_BLACK=(11,11,11)
WINDOW_DISHIGHLIGHTED_TEXT=(153,153,153)
BUTTON_DEFAULT=(BUTTON_BACK_GREY,BUTTON_BACKHIGHLIGHTED_BLUEGREY,BUTTON_OUTLINE_GREY,BUTTON_OUTLINEHIGHLIGHTED_BLUEGREY,BLACK,BLACK)
WINDOW_DEFAULT=(WINDOW_HEAD_WHITE,WINDOW_HEADHIGHLIGHTED_WHITE,WINDOW_BODY_GREY,WINDOW_OUTLINE_BLACK,BLACK,BLACK)

INPUTBOX_OUTLINE_GREY=(187,187,187)
INPUTBOX_DEFAULT=(WHITE,INPUTBOX_OUTLINE_GREY,BLACK)

WHITEBUTTON_BACKHIGHLIGHTED_GREY=(229,229,229)
CROSS_RED=(232,17,35)
CROSSBUTTON_COLORS=(WHITE,CROSS_RED,WHITE,CROSS_RED,BLACK,WHITE)
CTRLBUTTON_COLORS=(WHITE,WHITEBUTTON_BACKHIGHLIGHTED_GREY,WHITE,WHITEBUTTON_BACKHIGHLIGHTED_GREY,BLACK,BLACK)

TEMP = (13,13,13)
"""Don't actually use this color. It's for temporary use."""
QUIT=object()