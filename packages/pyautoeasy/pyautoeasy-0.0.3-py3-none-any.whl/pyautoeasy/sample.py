
"""
_________________________________________________________________________________________
ScreenPoint refers to a point in the screen. All the recorded points are generated here.
You may use these objects and its methods to quickly create an automation script.
_________________________________________________________________________________________
"""

from pyautoeasy import ScreenPoint

bar = ScreenPoint(pos=(1189, 47))
bar.double_click_here()

