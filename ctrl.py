"""The Pygame Crew used basic values."""
from numbers import Rational
import time

from .constants import*
from .base import*
from typing import Any, final,Iterable
from calca.unicode import shift
import pygame,_thread
_Auto_Exec:"list[FunctionType]"=list()
ResolutionShift=0.8
@final
class _PyCr_Value():
    def __init__(self):
        self.keyup=self.unikeyup=self.unikey=self.key=None
        self.mouse=(-1,-1)
        self.xshift=self.yshift=None
        self.middleclick=self.middleup=self.leftup=self.rightup=self.leftclick=self.rightclick=self.ctrl=self.alt=self.shift=self.left=self.right=self.middle=False
        self.event=self.press=self.mod=tuple()
        self.background=BACKGROUND_LIGHTBLUE
        self.fps=40
        self.screen:pygame.Surface=None
        self.window_shift=30
        self.counter=0
        """Counter 0 - 99, refresh every get_interect() in + 1"""
    def get_interact(self,wait_mode=False):
        """WARNING: Doing this clears all the event data the pygame *should* give you."""
        self.event=(pygame.event.wait(),) if wait_mode else pygame.event.get()
        self.press=pygame.key.get_pressed()
        self.mod=pygame.key.get_mods()
        self.mouse=pygame.mouse.get_pos()
        self.counter=(self.counter+1)%100
        self.left,self.middle,self.right=pygame.mouse.get_pressed()
        self.ctrl=(self.mod & pygame.KMOD_CTRL) != 0
        self.shift=(self.mod & pygame.KMOD_SHIFT) != 0
        self.caps=(self.mod & pygame.KMOD_CAPS) != 0
        self.alt=(self.mod & pygame.KMOD_ALT) != 0
        self.keyup=self.unikeyup=self.unikey=self.key=None
        self.middleclick=self.middleup=self.leftup=self.rightup=self.leftclick=self.rightclick=False
        for f in _Auto_Exec:f()
        for event in self.event:
            if event.type == pygame.KEYDOWN:
                self.key=event.key
                self.unikey=event.unicode
                if self.unikey == '\r':self.unikey="\n"
            elif event.type == pygame.KEYUP:
                self.keyup=event.key
                self.unikeyup=event.unicode
                if self.unikeyup == '\r':self.unikeyup="\n"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.leftclick:self.leftclick=event.button==1
                if not self.middleclick:self.middleclick=event.button==2
                if not self.rightclick:self.rightclick=event.button==3
            elif event.type == pygame.MOUSEBUTTONUP:
                if not self.leftup:self.leftup=event.button==1
                if not self.middleup:self.middleup=event.button==2
                if not self.rightup:self.rightup=event.button==3
    def is_pressed(self,key:int):return self.press[key]
    def any_pressed(self,keys:"Iterable[int]"):return any(map(self.is_pressed,keys))
    def all_pressed(self,keys:"Iterable[int]"):return all(map(self.is_pressed,keys))
PyCr_Value=_PyCr_Value()
PyCr_Value.get_interact()
def res(a,b=None):return a
def _res(num:"int|tuple[int]",effect:int=0):
    """effect (What will the number changed by): 
1 : X only
-1 : Y only
0 : X and Y"""
    if PyCr_Value.converts:
        if isinstance(num,Rational):
            if effect >= 0:num=num*PyCr_Value.xshift
            if effect <= 0:num=num*PyCr_Value.yshift
            return math.ceil(num)
        elif isinstance(num, Iterable):
            if effect == 0:
                if len(num) == 2:return (res(num[0],1),res(num[1],-1))
                elif len(num) == 4:return (res(num[0],1),res(num[1],-1),res(num[2],1),res(num[3],-1))
            else:
                result=[]
                for q in num:result.append(res(q,effect))
                return tuple(result)
    else:return num
screen:pygame.Surface=None
def Define_Screen(scr:pygame.Surface):
    global screen
    screen=scr
    PyCr_Value.screen=scr
def auto(f:FunctionType)->None:
    """Add a function to call when PyCr_Value.get_interact() is called."""
    _Auto_Exec.append(f)
def limshow(obj:SupportsPyCrOperations,backcolor:rgb=BACKGROUND_LIGHTBLUE,fps:int=30)->Any:
    """Show the object alone. Quit if the object returned anything than None.
    
If backcolor is None, nothing will be filled."""
    while True:
        if backcolor is not None:screen.fill(backcolor)
        result=put(obj)
        if result is not None:
            return result
        clock.tick(fps)
        pygame.display.flip()