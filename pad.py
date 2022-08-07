from .base import*
from PygameCrew.constants import*
from .ctrl import*
from calca.overall import INFINITY
from typing import final, overload
import pygame,PygameCrew.base
import PygameCrew.ctrl as ctrl

_font=PygameCrew.base._font
def _f():...
button_react:FunctionType=_f
class button():
    def __init__(self,start:Pos,end:Pos,text:"tuple[str,str]"=("",""),textsize:int=20,outlinesize:int=1,colors:"tuple[rgb,rgb,rgb,rgb,rgb,rgb]"=BUTTON_DEFAULT):
        """Colors: [Background_Back, Background_Front, Outline_Back, Outline_Front, Text_Back, Text_Front]
Important features:
- Everything follows innerrect
- Texts will be automatically centered"""
        self.text=text
        self.textsize=res(textsize)
        self.font=_font[self.textsize]
        self.sizebacktext=self.font.size(self.text[0])
        self.sizefronttext=self.font.size(self.text[1])
        self.outlinesize=res(outlinesize)
        self.innerrect=VerRect(res(start),res(end),True)
        self.outlinerect=VerRect(overlap(start,(-self.outlinesize,-self.outlinesize)),overlap(end,(self.outlinesize,self.outlinesize)))
        self.outlinerect.follows(self.innerrect,"xy")
        self.colors=colors
        self.backtext=text_part(((self.innerrect.start[0]+self.innerrect.end[0]-self.sizebacktext[0])//2,(self.innerrect.start[1]+self.innerrect.end[1]-self.sizebacktext[1])//2),self.text[0],self.textsize,self.colors[4])
        self.fronttext=text_part(((self.innerrect.start[0]+self.innerrect.end[0]-self.sizefronttext[0])//2,(self.innerrect.start[1]+self.innerrect.end[1]-self.sizefronttext[1])//2),self.text[1],self.textsize,self.colors[5])
        self.innerrect.befollowed(self.backtext.rect,self.fronttext.rect,followmode="xy")
        self.redraw_components()
    def PointerIn(self)->bool:return PyCr_Value.mouse in self.innerrect
    def redraw_components(self)->None:
        self.setfront=(self.colors[1],self.colors[3])
        self.setback=(self.colors[0],self.colors[2])
    def __contains__(self,t:Pos)->bool:return t in self.innerrect
    def __pycrput__(self):
        MouseInside=self.PointerIn()
        CurColor=self.setfront if MouseInside else self.setback
        pygame.draw.rect(ctrl.screen,CurColor[1],self.outlinerect.rectvalue)
        pygame.draw.rect(ctrl.screen,CurColor[0],self.innerrect.rectvalue)
        if MouseInside:put(self.fronttext)
        else:put(self.backtext)
        clicked=MouseInside and PyCr_Value.leftclick
        if clicked:button_react()
        return clicked
class text_part():
    def __init__(self,start:Pos,text:str,textsize:int=20,color:rgb=BLACK):
        self.originaltext=text
        self.font=_font[res(textsize)]
        self.textsize=textsize
        self.color=color
        self.revcolor=reverse(self.color)
        self.text=text.split("\n")
        self.textimgs=list()
        for t in self.text:self.textimgs.append(self.font.render(t,True,self.color))
        result=0
        for l in self.text:
            x=self.font.size(l)[0]
            if x > result:result=x
        self.rect=VerRect(res(start),overlap2((result,self.textsize*len(self.text)),res(start)))
    def changecolor(self,c:rgb):
        self.color=c
        self.revcolor=reverse(self.color)
        self.textimgs=list()
        for t in self.text:self.textimgs.append(self.font.render(t,True,self.color))
    def __str__(self):
        return "text_part(%s, \"\"\"%s\"\"\", %s, %s)"%(str(self.rect.start),self.originaltext,str(self.textsize),str(self.color))
    def __pycrput__(self):
        curx=self.rect.start[0]
        cury=self.rect.start[1]
        for img in self.textimgs:ctrl.screen.blit(img,(curx,cury));cury+=self.textsize
class inputbox():
    def __init__(self,start:Pos,end:Pos,textsize:int=20,limit:int=INFINITY,default_text:str="",outlinesize:int=1,terminate_on_return:bool=True,textpos:Pos=None,colors:"tuple[rgb,rgb,rgb]"=INPUTBOX_DEFAULT):
        """Colors: [Background, Outline, Text]
Important features:
- Everything follows innerrect"""
        self.innerrect=VerRect(res(start),end,True)
        self.outlinesize=res(outlinesize)
        self.outlinerect=VerRect(overlap(self.innerrect.start,(-self.outlinesize,-self.outlinesize)),overlap(end,(self.outlinesize,self.outlinesize)))
        self.outlinerect.follows(self.innerrect,"xy")
        self.font=_font[res(textsize)]
        self.limit=limit
        self.default_text=default_text
        self._textpos=textpos
        self.inputing=""
        self.selected=False
        self.terminate_on_return=terminate_on_return
        self.textsize=self.font.size(" ")[1]
        self.colors=colors
        self.redraw_components()
    def redraw_components(self):
        if self._textpos is None:self.textpos=(self.innerrect.start[0],(self.innerrect.start[1]+self.innerrect.end[1]-self.textsize)//2)
        else:self.textpos=self._textpos
        self.default_text_part=text_part(self.textpos,self.default_text,self.textsize,dim(self.colors[2],100))
    def move(self,x,y):
        self.innerrect.move(x,y)
        self.redraw_components()
    def absolute(self,x:int,y:int)->None:
        self.innerrect.absolute(x,y)
        self.redraw_components()
    def expand(self,x:int,y:int)->None:
        self.innerrect.expand(x,y)
        self.redraw_components()
    def ratio(self,r:int)->None:
        self.innerrect.ratio(r)
        self.redraw_components()
    def __pycrput__(self):
        pygame.draw.rect(ctrl.screen,self.colors[1],self.outlinerect.rectvalue)
        pygame.draw.rect(ctrl.screen,self.colors[0],self.innerrect.rectvalue)
        Touched=PyCr_Value.mouse in self.innerrect
        LeftTouched=Touched and PyCr_Value.leftclick
        if LeftTouched:self.selected = True
        elif PyCr_Value.leftclick:self.selected=False
        if len(self.inputing) == 0:put(self.default_text_part)
        put(text_part(self.textpos,self.inputing+("|"if self.selected and PyCr_Value.counter%20 <= 12 else ""),self.textsize,self.colors[2]))
        if PyCr_Value.unikey is not None and self.selected:
            if PyCr_Value.key == pygame.K_c and PyCr_Value.ctrl and PyCr_Value.alt:
                self.inputing=""
            elif PyCr_Value.unikey == "\b":
                self.inputing=self.inputing[:-1]
            elif PyCr_Value.unikey == '\n' and self.terminate_on_return:
                record=self.inputing;self.inputing="";return record
            elif len(self.inputing) < self.limit:
                self.inputing += PyCr_Value.unikey
                
def change_button_react(f:FunctionType):
    global button_react
    button_react=f
def crossbutton(start:Pos,length:int=30)->button:
    """Gets a cross button faster."""
    return button(start,(start[0]+length,start[1]+length),('×','×'),length*4//3,colors=CROSSBUTTON_COLORS)
def ctrlbutton(start:Pos,length:int=30,text=("-","-"))->button:
    """Gets a control button faster."""
    return button(start,(start[0]+length,start[1]+length),text,length*5//4,colors=CTRLBUTTON_COLORS)
def serie_button(start:Pos,each:Pos_Like,*text:str,move:Pos_Like=None,textsize:int=None)->"tuple[button]":
    result=[]
    if textsize is None:ts=int(min(each)/10*9)
    else:ts=textsize
    if move is None:move=(each[0],0)
    for t in text:
        result.append(button(start,overlap2(start,each),(t,t),ts))
        start=(start[0]+move[0],start[1]+move[1])
    return tuple(result)
def serie_inputbox(start:Pos,each:Pos_Like,*text,move:Pos_Like=None,textsize:int=None)->"tuple[inputbox]":
    result=[]
    if textsize is None:ts=int(min(each)/10*9)
    else:ts=textsize
    lim=math.ceil(each[0]/ts)
    if move is None:move=(each[0],0)
    for t in text:
        result.append(inputbox(start,overlap2(start,each),ts,limit=lim,default_text=t))
        start=(start[0]+move[0],start[1]+move[1])
    return tuple(result)
def chamber(vr:"VerRect",color:rgb,height:int=1)->pygame.Surface:
    tvr=VerRect(overlap2(vr.start,(-height,-height)),overlap2(vr.end,(height,height)))
    surf=pygame.Surface(tvr.differed)
    surf.fill(color)
    pygame.draw.rect(surf,TEMP,(height,height)+vr.differed)
    surf.set_colorkey(TEMP)
    return surf
def semi(vr:"VerRect",color:rgb,alpha:int)->pygame.Surface:
    surf=pygame.Surface(vr.differed)
    surf.fill(color)
    surf.set_alpha(alpha)
    return surf
def drawsemi(vr:"VerRect",color:rgb,alpha:int)->pygame.Surface:
    surf=semi(vr,color,alpha)
    ctrl.screen.blit(surf,vr.start)
    return surf