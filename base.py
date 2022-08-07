from .constants import*
from typing import final
import pygame,calca.coord as coord
import random,warnings
from VerRect import*
from abc import abstractmethod
from typing import Protocol, runtime_checkable, T_co

pygame.init()
clock=pygame.time.Clock()
def _ramming_map(num:int)->int:return num+random.randint(-2,2)
def ramming(colorrgb:rgb)->rgb:return tuple(map(_ramming_map,colorrgb))
def lowbound(x,y=0):return y if x<y else x
def upbound(x,y=255):return y if x>y else x
def _dim_map(up:int)->FunctionType:
    def result(num:int)->int:result=num+up;return upbound(lowbound(result))
    return result
def dim(colorrgb:rgb,up:int)->rgb:return tuple(map(_dim_map(up),colorrgb))
def _rdim_map(ratio:float)->FunctionType:
    def result(num:int)->int:result=num*ratio;return upbound(lowbound(result))
    return result
def rdim(colorrgb:rgb,ratio:float)->rgb:return tuple(map(_rdim_map(ratio),colorrgb))
def _reverse_map(num:int)->int:return 255 - num
def reverse(colorrgb:rgb)->rgb:
    return tuple(map(_reverse_map,colorrgb))
def overlap(a:tuple,b:tuple)->tuple:
    result=[]
    for i in range(min(len(a),len(b))):result.append(a[i]+b[i])
    return tuple(result)
def overlap2(a:"tuple[int,int]",b:"tuple[int,int]"):return a[0]+b[0],a[1]+b[1]

def stringify(o:object,addon:str=", ",strquote:str='"""')->str:
    if isinstance(o,(tuple,list,set,map)):
        if isinstance(o,list):brk="[]"
        elif isinstance(o,set):brk="{}"
        else:brk="()"
        result=brk[0]
        for i in o:result += stringify(i)+addon
        return result+brk[1]
    elif isinstance(o,dict):
        result="{"
        for k,v in o.items():result += stringify(k)+" : "+stringify(v)+addon
        return result +"}"
    else:
        if isinstance(o,str):
            if o.startswith('"') and o.endswith('"'):return o
            else:return strquote+o+strquote
        else:return str(o)
def center_size(size:Pos_Like):return (size[0]//2,size[1]//2)
def ReplaceColor(source:pygame.Surface,old:rgb,new:rgb)->pygame.Surface:
    """Do not use colorkeys in this function."""
    sourcecopy=source.copy()
    sourcecopy.set_colorkey(old)
    surf=pygame.Surface(sourcecopy.get_size())
    surf.fill(new)
    surf.blit(sourcecopy,(0,0))
    return surf
@runtime_checkable
class SupportsPyCrOperations(Protocol[T_co]):
    __slots__ = ()
    @abstractmethod
    def __pycrput__(self) -> T_co:...
def put(obj:SupportsPyCrOperations):
    return obj.__pycrput__()
def puts(*obj:SupportsPyCrOperations):
    final=[]
    for o in obj:
        result=o.__pycrput__()
        final.append((o,result))
    return final
def empty_string(string:str):return string.isspace() or len(string) == 0
def center_size(size:Pos_Like):return (size[0]//2,size[1]//2)

class named_object(object):
    def __init__(self,name:str):self.name=name
    def __str__(self):return self.name

@final
class font_family():
    def __init__(self,font_name:str):
        self.family={}
        self.font_name=font_name
    def __getitem__(self,size:int)->pygame.font.Font:
        try:return self.family[size]
        except:
            self.family[size]=pygame.font.SysFont(self.font_name,size)
            return self.family[size]
def set_font(name:"str"):
    """Sends a warning and return False on failure."""
    global _font
    _font=font_family(name)
    if name.lower().replace(' ','') not in Possible_Fonts:warnings.warn("font '%s' setting failed"%name,UserWarning);return False
    return True
Default_Font="arial"
Possible_Fonts=pygame.font.get_fonts()
_font=font_family(Default_Font)
NOTEXT=_font[30].render("",True,BLACK)
"""This is used to fill up a space where you don't want to show anything."""