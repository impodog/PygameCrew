"""Pygame Crew (Or "pycr") gives ways to use the pygame better."""
__version__="1.3.3"
import pygame,sys,pyautogui,warnings
from .constants import*
from .base import*
from .ctrl import*
from .pad import*
from .window import*
from .animate import*
import PygameCrew.pad as pad
if sys.platform != "win32":
    warnings.warn("You aren't using Windows platform.",UserWarning)
pygame.init()

# Shortcuts
_font = pad._font
"""A shortcut for 'pycr.pad._font'."""
QuitDisplay=lambda :pygame.display.quit()
"""A shortcut function for 'pygame.display.quit()'."""
pcv=PyCr_Value
"""A shortcut for 'PyCr_Value', though we recommend you to use the full name."""
def get_interact(wait_mode:bool=False):
    """A shortcut for 'PyCr_Value.get_interact()'."""
    PyCr_Value.get_interact(wait_mode)
def get_event()->"list[pygame.event.Event]":
    """A shortcut for getting 'PyCr_Value.event'."""
    return PyCr_Value.event