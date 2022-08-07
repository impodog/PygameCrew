import traceback
from .constants import*
from .base import*
from .pad import*
from typing import final, Iterable, Union, overload
import pygame,math
import PygameCrew.ctrl as ctrl
import numpy as np
import os
import sys
_iter_of_surface=SubType(Iterable,pygame.Surface)
_iter_of_array=SubType(Iterable,np.ndarray)
class Frame():
    @overload
    def __init__(self,surf:pygame.Surface=screen,target:Pos=None):...
    @overload
    def __init__(self,path:str,colorkeys:"tuple[rgb]"=None,replace_group:"dict[rgb,rgb]"=None,alpha:"int"=None,target:Pos=None):...
    def __init__(self,*args,**kwargs):
        self.surf:pygame.Surface
        self.position:Pos=(0,0)
        try:init_analysis=overloaded(args,kwargs,{"surf":DefaultsTo_WithType(PyCr_Value.screen,pygame.Surface),"target":DefaultsTo_WithType((0,0),Pos_)},{"path":str,"colorkeys":DefaultsTo_WithType(None,SubType(tuple,rgb_)),"replace_group":DefaultsTo_WithType(None,SubType(dict,rgb_,rgb_)),"alpha":DefaultsTo_WithType(None,int),"target":DefaultsTo_WithType((0,0),Pos_)})
        except AnalyzingError as e:raise ValueError("not matched argument for 'Frame.__init__()'",e)
        if init_analysis.get("path") is not None:
            self.surf=pygame.image.load(init_analysis.get("path")).convert()
            if init_analysis.get("replace_group") is not None:
                for old,new in init_analysis.get("replace_group").items():
                    self.surf=ReplaceColor(self.surf,old,new)
            if init_analysis.get("colorkeys") is not None:
                for colorkey in init_analysis.get("colorkeys"):
                    self.surf.set_colorkey(colorkey)
        elif init_analysis.get("surf") is not None:self.surf=init_analysis.get("surf")
        if init_analysis.get("alpha") is not None:self.surf.set_alpha(init_analysis.get("alpha"))
        if init_analysis.get("target") is not None:self.position=init_analysis.get("target")
    def chpos(self,target:Pos):self.position=target
    def rot(self,deg:int=90):
        """Rotate self counter-clockwise"""
        self.surf=pygame.transform.rotate(self.surf,deg)
    def alpha(self,a:int):self.surf.set_alpha(a)
    def copy(self)->"Frame":return Frame(self.surf,self.position)
    def deepcopy(self)->"Frame":return Frame(self.surf.copy(),self.position)
    def flipx(self):self.surf=pygame.transform.flip(self.surf,True,False)
    def flipy(self):self.surf=pygame.transform.flip(self.surf,False,True)
    def __pycrput__(self):ctrl.screen.blit(self.surf,self.position);return
    def __repr__(self):return "%s(surf=%s, target=%s)"%(self.__class__.__name__,repr(self.surf),self.position)
    def __str__(self):return self.__repr__()
class FrameArray():
    """On __pycrput__(): returns the running time if no more frames left; returns True if a frame is put
    
When the frame is over, nothing will show and the return will be total time used to finish

framerate skips a frame if the time of last frame is less than framerate

When pos is defined, blit all frames at the given pos"""
    def __init__(self,frames:"Iterable[Frame]",repeat:bool=False,framerate:float=0,pos:Pos=None):
        self.frames:"tuple[Frame]"=tuple(frames)
        self.repeat:bool=repeat
        self.curframe:int=0
        self.endtime:float=time.time()
        self.starttime:float=self.endtime
        self.lasttime:float=self.endtime
        self.maxdepth:int=len(self.frames)
        self.pos=pos
        self.framerate=framerate
    def __iter__(self):return self.copy()
    def __next__(self)->Frame:
        if self.curframe == 0:self.refresh()
        self.endtime=time.time()
        result=self.frames[self.curframe]
        add_frame=False
        if self.endtime-self.lasttime >= self.framerate:self.curframe+=1;add_frame=True
        if self.curframe >= self.maxdepth:
            if self.repeat:self.refresh()
            else:self.curframe-=2;result=None;raise StopIteration(self.endtime-self.starttime)
        if self.curframe < 0:raise ValueError("frame number less than 0")
        if add_frame:self.lasttime=self.endtime
        return result
    def __pycrput__(self):
        try:
            opt_frame=next(self)
            if self.pos is not None:
                PyCr_Value.screen.blit(opt_frame.surf,self.pos)
            else:
                put(opt_frame)
            return True
        except StopIteration as t:return t
    def refresh(self):self.curframe=0;self.starttime=time.time()
    def set_repeat(self,repeat:bool):self.repeat=repeat
    def get_repeat(self):return self.repeat
    def set_framerate(self,framerate:bool):self.framerate=framerate
    def get_framerate(self):return self.framerate
    def rot(self,deg:int=90):
        """Rotate all frames(ccw)"""
        for frame in self.frames:frame.surf=pygame.transform.rotate(frame.surf,deg)
    def jump(self,frame:int):self.curframe=frame
    def reljump(self,forward:int):self.curframe+=forward
    def copy(self):return FrameArray(self.frames,self.repeat,self.framerate,self.pos)
    def deepcopy(self):return FrameArray(map(Frame.deepcopy,self.frames),self.repeat,self.framerate,self.pos)
    def reverse(self):self.frames=tuple(reversed(self.frames))
    def flipxall(self):
        for fr in self.frames:fr.flipx()
    def flipyall(self):
        for fr in self.frames:fr.flipy()
    def chposall(self,target:Pos):
        for f in self.frames:f.chpos(target)
    def chpos(self,pos:Pos=None):self.pos=pos
    def alphaall(self,a:int):
        for fr in self.frames:fr.alpha(a)
def Create_FrameArray(from_obj:str,position:Pos=(0,0),colorkeys:"tuple[rgb]"=None,replace_group:"dict[rgb,rgb]"=None,alpha:int=None,repeat:bool=False,framerate:float=0,pos:Pos=None):
    """
## Paths
    
If the from_obj is a file(image or video), load from it and get all frames.

If the from_obj is a directory, load all usable frame img resources in the name order.

## Surface

On inputing the surface iterable, create it by creating multiple Frames.

On inputing the ndarray, first create surfaces, then create Frames.

## pos

If pos is given and not None, override the given target"""
    frames:"list[Frame]"=list()
    if pos is not None:position = pos
    if isinstance(from_obj,str):
        if not from_obj.endswith(('/','\\')):from_obj=from_obj+'/'
        if os.path.exists(from_obj):
            if os.path.isfile(from_obj):
                frames=(Frame(from_obj,target=position,colorkeys=colorkeys,replace_group=replace_group,alpha=alpha),)
            else:
                allfile=os.listdir(from_obj)
                for file in allfile:
                    filepath=from_obj+file
                    if os.path.isfile(filepath):
                        try:frames.append(Frame(filepath,target=position,colorkeys=colorkeys,replace_group=replace_group,alpha=alpha))
                        except:traceback.print_exc()
        else:raise FileNotFoundError("file %s does not exist"%from_obj)
    elif _iter_of_surface.check(from_obj):frames=tuple(map(Frame,from_obj))
    elif _iter_of_array.check(from_obj):frames=tuple(map(Frame,map(pygame.surfarray.make_surface,from_obj)))
    else:raise ValueError("not matched argument for 'Create_FrameArray'")
    return FrameArray(frames,repeat,framerate,pos)