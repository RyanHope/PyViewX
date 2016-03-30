# -*- coding:	utf-8 -*-
#===============================================================================
# This file is part of PyViewX.
# Copyright (C) 2012-2013 Ryan Hope <rmh3093@gmail.com>
#
# PyViewX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyViewX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyViewX.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================
from __future__ import division
from pyviewx.client import Dispatcher
from twisted.internet.task import LoopingCall
import pygame
import pygl2d

from .calibrator import Calibrator

def mean(l): return sum(l) / len(l)

class CalibratorGL(Calibrator):

	def _init_screen(self):
		if screen:
			self.screen = screen
		else:
			pygame.display.init()
			pygame.font.init()
			self.screen = pygl2d.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)

	def _draw_text(self, text, font, color, loc):
		t = pygl2d.font.RenderText(text, color, font)
		tr = t.get_rect()
		tr.center = loc
		t.draw(tr.topleft)

	def _display(self):
		pygl2d.display.begin_draw(self.screen_size)
		pygl2d.draw.rect(self.worldsurf_rect, (51, 51, 153))
		if self.state == 0:
			r = pygame.Rect(0, 0, 0, 0)
			r.width = int((40 * self.width) / 100)
			r.height = int((20 * self.height) / 100)
			r.center = (self.center_x, self.center_y)
			pygl2d.draw.rect(r, (0, 0, 0), 1)
			f = pygame.font.Font(None, 18)
			if self.eye_position and self.eye_position[4] > 550 and self.eye_position[5] > 550 and self.eye_position[4] < 850 and self.eye_position[5] < 850:
				left = map(int, (self.eye_position[0] / 99.999 * self.center_x + self.center_x, self.eye_position[2] / -99.999 * self.center_y + self.center_y))
				right = map(int, (self.eye_position[1] / 99.999 * self.center_x + self.center_x, self.eye_position[3] / -99.999 * self.center_y + self.center_y))
				l = int((700 - self.eye_position[4]) / 7 + 20)
				r = int((700 - self.eye_position[5]) / 7 + 20)
				if l > 0:
					pygl2d.draw.circle(left, l, (255, 255, 255))
				if r > 0:
					pygl2d.draw.circle(right, r, (255, 255, 255))
				self._draw_text('%d' % int(self.eye_position[4] - 700), f, (0, 0, 0), left)
				self._draw_text('%d' % int(self.eye_position[5] - 700), f, (0, 0, 0), right)
			if not self.currentPoint < 0:
				pygl2d.draw.circle(self.calibrationPoints[self.currentPoint], 8, (255, 255, 0))
				pygl2d.draw.circle(self.calibrationPoints[self.currentPoint], 2, (0, 0, 0))
		if self.state > 0:
			f = pygame.font.Font(None, 28)
			if not self.calibrationResults:
				self._draw_text('Calculating calibration accuracy %s' % self.spinner[self.spinnerIndex], f, (255, 255, 255), (self.center_x, self.center_y))
			else:
				self._draw_text(' '.join(self.calibrationResults[0]), f, (255, 255, 255), (self.center_x, self.center_y))
				if len(self.calibrationResults) > 1:
					self._draw_text(' '.join(self.calibrationResults[1]), f, (255, 255, 255), (self.center_x, self.center_y + 30))
				self._draw_text("Press 'R' to recalibrate, press 'Space Bar' to continue...", f, (255, 255, 255), (self.center_x, self.height - 60))
		pygl2d.display.end_draw()
