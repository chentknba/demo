import pygame
from pygame.locals import *


KEY_NONE = 0
KEY_UP = 1
KEY_TOP_RIGHT = 2
KEY_RIGHT = 3
KEY_BTTOM_RIGHT = 4
KEY_DOWN = 5
KEY_BTTOM_LEFT = 6
KEY_LEFT = 7
KEY_TOP_LEFT = 8

# 没有按键按下
class NoneState(object):
	def __init__(self):
		self.value = KEY_NONE

	def keydown(self, key):
		if key == K_a:
			return KEY_LEFT, left_state
		elif key == K_d:
			return KEY_RIGHT, right_state
		elif key == K_w:
			return KEY_UP, up_state
		elif key == K_s:
			return KEY_DOWN, down_state
		else:
			return self.value, none_state

	def keyup(self, key):
		return self.value, none_state

# 上 W
class UpState(object):
	def __init__(self):
		self.value = KEY_UP

	def keydown(self, key):
		if key == K_a:
			return KEY_TOP_LEFT, top_left_state
		elif key == K_d:
			return KEY_TOP_RIGHT, top_right_state
		elif key == K_s:
			return KEY_DOWN, down_state
		else:
			return self.value, up_state

	def keyup(self, key):
		if key == K_w:
			return KEY_NONE, none_state
		else:
			return self.value, up_state

# 下 S
class DownState(object):
	def __init__(self):
		self.value = KEY_DOWN

	def keydown(self, key):
		if key == K_a:
			return KEY_BTTOM_LEFT, bottom_left_state
		elif key == K_d:
			return KEY_BTTOM_RIGHT, bottom_right_state
		elif key == K_w:
			return KEY_UP, up_state
		else:
			return self.value, down_state

	def keyup(self, key):
		if key == K_s:
			return KEY_NONE, none_state
		else:
			return self.value, down_state

# 左 A
class LeftState(object):
	def __init__(self):
		self.value = KEY_LEFT

	def keydown(self, key):
		if key == K_w:
			return KEY_TOP_LEFT, top_left_state
		elif key == K_s:
			return KEY_BTTOM_LEFT, bottom_left_state
		elif key == K_d:
			return KEY_RIGHT, right_state
		else:
			return self.value, left_state

	def keyup(self, key):
		if key == K_a:
			return KEY_NONE, none_state
		else:
			return self.value, left_state

# 右 D
class RightState(object):
	def __init__(self):
		self.value = KEY_RIGHT

	def keydown(self, key):
		if key == K_w:
			return KEY_TOP_RIGHT, top_right_state
		elif key == K_s:
			return KEY_BTTOM_RIGHT, bottom_right_state
		elif key == K_a:
			return KEY_LEFT, left_state
		else:
			return self.value, right_state

	def keyup(self, key):
		if key == K_d:
			return KEY_NONE, none_state
		else:
			return self.value, right_state

# 左上 WA
class TopLeftState(object):
	def __init__(self):
		self.value = KEY_TOP_LEFT


	def keydown(self, key):
		if key == K_d:
			return KEY_TOP_LEFT, top_left_state
		elif key == K_s:
			return KEY_BTTOM_LEFT, bottom_left_state
		return self.value, top_left_state

	def keyup(self, key):
		if key == K_w:
			return KEY_LEFT, left_state
		elif key == K_a:
			return KEY_UP, up_state
		else:
			return self.value, top_left_state

# 左下 SA
class BottomLeftState(object):
	def __init__(self):
		self.value = KEY_BTTOM_LEFT
	
	def keydown(self, key):
		if key == K_w:
			return KEY_TOP_LEFT, top_left_state
		elif key == K_d:
			return KEY_BTTOM_RIGHT, bottom_right_state
		return self.value, bottom_left_state

	def keyup(self, key):
		if key == K_s:
			return KEY_LEFT, left_state
		elif key == K_a:
			return KEY_DOWN, down_state
		else:
			return self.value, bottom_left_state

# 右上 WD
class TopRightState(object):
	def __init__(self):
		self.value = KEY_TOP_RIGHT

	def keydown(self, key):
		if key == K_a:
			return KEY_TOP_LEFT, top_left_state
		elif key == K_s:
			return KEY_BTTOM_RIGHT, bottom_right_state

		return self.value, top_right_state

	def keyup(self, key):
		if key == K_w:
			return KEY_RIGHT, right_state
		elif key == K_d:
			return KEY_UP, up_state
		else:
			return self.value, top_right_state

# 右下 SD
class BottomRightState(object):
	def __init__(self):
		self.value = KEY_BTTOM_RIGHT

	def keydown(self, key):
		if key == K_w:
			return KEY_TOP_RIGHT, top_right_state
		elif key == K_a:
			return KEY_BTTOM_LEFT, bottom_left_state

		return self.value, bottom_right_state

	def keyup(self, key):
		if key == K_s:
			return KEY_RIGHT, right_state
		elif key == K_d:
			return KEY_DOWN, down_state
		else:
			return self.value, bottom_right_state

# nothing happen
none_state = NoneState()
# 上
up_state = UpState()
# 下
down_state = DownState()
# 左
left_state = LeftState()
# 右
right_state = RightState()
# 左上
top_left_state = TopLeftState()
# 左下
bottom_left_state = BottomLeftState()
# 右上
top_right_state = TopRightState()
# 右下
bottom_right_state = BottomRightState()

