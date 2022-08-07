from  PygameCrew.constants import*
from .base import*
from .pad import*
from typing import final, Iterable, Union
import pygame,math
import PygameCrew.ctrl as ctrl
@final
class window():
    def __init__(self,start:Pos,end:Pos,headlength:int=50,body:str="",title:str="",textsize:int=20,outlinesize:int=1,bottombuttons:"Iterable[str|button|inputbox,]"=("OK",),bottomsize:Pos_Like=(70,30),movable:bool=False,colors:"tuple[rgb,rgb,rgb,rgb,rgb,rgb,rgb]"=WINDOW_DEFAULT):
        """Colors: [Window_Head, Window_Head_Highlighted, Window_Body, Window_Outline, Head_Color, Body_Color]
Important features:
- Everything follows layerrect
- Also, a button pressed makes returning the FRONT text, NOT back text.
- Having CROSS button pressed = returning QUIT (The Constant defined in constants.py)
- Put str "__inputbox__" in bottombuttons to involve an inputbox.
- The order of bottom buttons is reversed to the inputs.
- Input box + RETURN = return the result given
- Input box unfinished + button down = return (button_name, the answers)"""
        self.layerrect=VerRect((res(start[0],1),res(start[1],-1)),res(end),True)
        self.headrect=VerRect(self.layerrect.start,(self.layerrect.end[0],self.layerrect.start[1]+res(headlength,-1)))
        self.headlength=res(headlength,-1)
        self.outlinesize=res(outlinesize)
        self.bottomsize=bottomsize
        self.textsize=textsize
        self.startpoint=None
        self.movable=movable
        self.toplen=res(30);self.sepbottom=res(10,1)
        self.outlinestartpoint=None
        self.bottombuttons=bottombuttons
        self.body=body
        self.title=title
        self.colors=colors
        self.outlinerect=VerRect(overlap(self.headrect.start,(-self.outlinesize,-self.outlinesize)),overlap(self.layerrect.end,(self.outlinesize,self.outlinesize)))
        self.bodyimg=text_part(self.headrect.lb,self.body,self.textsize,self.colors[5])
        self.titleimg=text_part(self.headrect.start,self.title,self.textsize,self.colors[4])
        self.bottom:"list[button,]"=[]
        self.lowxlimit=max(self.titleimg.rect.differed[0]+2*self.toplen,self.bodyimg.rect.differed[0],len(self.bottombuttons)*(self.bottomsize[0]+self.sepbottom))+PyCr_Value.window_shift
        self.lowylimit=self.titleimg.rect.differed[1]+self.bodyimg.rect.differed[1]+self.bottomsize[1]-PyCr_Value.window_shift
        current=VerRect(overlap(self.layerrect.end,(-self.bottomsize[0],-self.bottomsize[1])),self.layerrect.end)
        for bt in self.bottombuttons:
            if isinstance(bt,(button,inputbox)):
                bt.innerrect.follows(self.layerrect)
                self.bottom.append(bt)
            elif type(bt) == str:
                if bt.startswith("__inputbox__"):self.bottom.append(inputbox(current.start,current.end,self.bottomsize[1],math.ceil(self.bottomsize[0]/self.bottomsize[1]),bt[12:]))
                else:self.bottom.append(button(current.start,current.end,(bt,bt),int(self.bottomsize[1]*0.8)))
                self.bottom[-1].innerrect.follows(self.layerrect)
            current.move(-self.bottomsize[0]-self.sepbottom,0)
        self.top=(ctrlbutton(overlap(self.layerrect.ru,(-self.toplen*2-self.outlinesize,self.outlinesize)),self.toplen),crossbutton(overlap(self.layerrect.ru,(-self.toplen*1-self.outlinesize,self.outlinesize)),self.toplen))
        self.allbuttons=tuple(self.bottom)+self.top
        self.layerrect.befollowed(self.headrect,followmode="x")
        self.layerrect.befollowed(self.outlinerect,followmode="xy")
        self.layerrect.befollowed(self.top[0].innerrect,self.top[1].innerrect,followmode="rx")
        self.layerrect.befollowed(self.bodyimg.rect,self.titleimg.rect,followmode="")
    def __pycrput__(self)->bool:
        if self.movable:
            Touched=PyCr_Value.mouse in self.headrect
            LeftTouched=Touched and PyCr_Value.leftclick
            if LeftTouched and self.startpoint is None:self.startpoint=PyCr_Value.mouse;self.realstartpoint=self.layerrect.start
            elif self.startpoint is not None:self.layerrect.absolute(PyCr_Value.mouse[0]-self.startpoint[0]+self.realstartpoint[0],PyCr_Value.mouse[1]-self.startpoint[1]+self.realstartpoint[1])
            if not PyCr_Value.left and self.startpoint is not None:self.startpoint=self.realstartpoint=None
        pygame.draw.rect(ctrl.screen,self.colors[3],self.outlinerect.rectvalue)
        pygame.draw.rect(ctrl.screen,self.colors[2],self.layerrect.rectvalue)
        pygame.draw.rect(ctrl.screen,self.colors[1],self.headrect.rectvalue)
        puts(self.titleimg,self.bodyimg)
        result=puts(*self.allbuttons)
        if PyCr_Value.ctrl:
            if PyCr_Value.unikey == "=" and self.layerrect.differed[0] < PyCr_Value.length and self.layerrect.differed[1] < PyCr_Value.height:self.layerrect.expand(PyCr_Value.window_shift)
            elif PyCr_Value.unikey == "-" and self.layerrect.differed[0] > self.lowxlimit and self.layerrect.differed[1] > self.lowylimit:self.layerrect.expand(-PyCr_Value.window_shift)
        results=[];output=None
        for r in self.allbuttons:
            if type(r)==inputbox:results.append(r.inputing)
        for r in result:
            if type(r[1])==str:output=r[1]
        for r in result:
            if r[1] is True:
                if r[0] is self.top[1]:return QUIT
                return (r[0].text[1] if len(results) == 0 else (r[0].text[1],)+tuple(results))
        if output is not None:return output
        return None