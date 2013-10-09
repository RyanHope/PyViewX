# -*- coding:	utf-8 -*-
#===============================================================================
# This file is part of PyViewX.
# Copyright (C) 2012 Ryan Hope <rmh3093@gmail.com>
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

def mean(l): return sum(l) / len(l)

class Calibrator(object):

	d = Dispatcher()

	def __init__(self, client, screen=None, escape=False, reactor=None, eye=0):
		if reactor is None:
			from twisted.internet import reactor
		self.eye = eye
		self.reactor = reactor
		self.escape = escape
		self.client = client
		self.client.addDispatcher(self.d)
		if screen:
			self.screen = screen
		else:
			pygame.display.init()
			pygame.font.init()
			self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.width, self.height = self.screen.get_size()
		self.center_x = int(self.width / 2)
		self.center_y = int(self.height / 2)
		self.worldsurf = self.screen.copy()
		self.worldsurf_rect = self.worldsurf.get_rect()

		self.spinner = ['|', '|', '|', '/', '/', '/', '-', '-', '-', '\\', '\\', '\\']
		self.spinnerIndex = 0

		pygame.mouse.set_visible(False)

		self.complete = False
		self.lc = None
		self._reset()

	def _reset(self):
		self.eye_position = ()
		self.calibrationResults = []
		self.calibrationPoints = []
		self.currentPoint = -1
		self.state = 0

	def _draw_text(self, text, font, color, loc):
		t = font.render(text, True, color)
		tr = t.get_rect()
		tr.center = loc
		self.worldsurf.blit(t, tr)

	def _update(self):
		self.worldsurf.fill((51, 51, 153))
		if self.state == 0:
			r = pygame.Rect(0, 0, 0, 0)
			r.width = int((40 * self.width) / 100)
			r.height = int((20 * self.height) / 100)
			r.center = (self.center_x, self.center_y)
			pygame.draw.rect(self.worldsurf, (0, 0, 0), r, 1)
			f = pygame.font.Font(None, 18)
			if self.eye_position and self.eye_position[4] > 550 and self.eye_position[5] > 550 and self.eye_position[4] < 850 and self.eye_position[5] < 850:
				left = map(int, (self.eye_position[0] / 99.999 * self.center_x + self.center_x, self.eye_position[2] / -99.999 * self.center_y + self.center_y))
				right = map(int, (self.eye_position[1] / 99.999 * self.center_x + self.center_x, self.eye_position[3] / -99.999 * self.center_y + self.center_y))
				l = int((700 - self.eye_position[4]) / 7 + 20)
				r = int((700 - self.eye_position[5]) / 7 + 20)
				if l > 0:
					pygame.draw.circle(self.worldsurf, (255, 255, 255), left, l)
				if r > 0:
					pygame.draw.circle(self.worldsurf, (255, 255, 255), right, r)
				self._draw_text('%d' % int(self.eye_position[4] - 700), f, (0, 0, 0), left)
				self._draw_text('%d' % int(self.eye_position[5] - 700), f, (0, 0, 0), right)
			if not self.currentPoint < 0:
				pygame.draw.circle(self.worldsurf, (255, 255, 0), self.calibrationPoints[self.currentPoint], 8)
				pygame.draw.circle(self.worldsurf, (0, 0, 0), self.calibrationPoints[self.currentPoint], 2)
		if self.state > 0:
			f = pygame.font.Font(None, 28)
			if not self.calibrationResults:
				self._draw_text('Calculating calibration accuracy %s' % self.spinner[self.spinnerIndex], f, (255, 255, 255), (self.center_x, self.center_y))
			else:
				self._draw_text(' '.join(self.calibrationResults[0]), f, (255, 255, 255), (self.center_x, self.center_y))
				if len(self.calibrationResults) > 1:
					self._draw_text(' '.join(self.calibrationResults[1]), f, (255, 255, 255), (self.center_x, self.center_y + 30))
				self._draw_text("Press 'R' to recalibrate, press 'Space Bar' to continue...", f, (255, 255, 255), (self.center_x, self.height - 60))
		self.screen.blit(self.worldsurf, self.worldsurf_rect)
		pygame.display.flip()
		self.spinnerIndex += 1
		if self.spinnerIndex == 12:
			self.spinnerIndex = 0
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if self.escape and event.key == pygame.K_ESCAPE:
					if self.lc:
						self.lc.stop()
						return
				if self.state == 0:
					if event.key == pygame.K_SPACE:
						self.client.acceptCalibrationPoint()
				elif self.state == 2:
					if event.key == pygame.K_r:
						self._reset()
						self.client.startCalibration(9, self.eye)
					elif event.key == pygame.K_SPACE:
						self.complete = True
						self.lc.stop()

	def start(self, stopCallback, wait=1, randomize=1, auto=0, speed=1, level=3, *args, **kwargs):
		self.client.setDataFormat('%TS %ET %SX %SY %DX %DY %EX %EY %EZ')
		self.client.startDataStreaming()
		self.client.setSizeCalibrationArea(self.width, self.height)
		self.client.setCalibrationParam(0, wait)
		self.client.setCalibrationParam(1, randomize)
		self.client.setCalibrationParam(2, auto)
		self.client.setCalibrationParam(3, speed)
		self.client.setCalibrationCheckLevel(level)
		self.client.startCalibration(9, self.eye)
		self.lc = LoopingCall(self._update)
		dd = self.lc.start(1.0 / 30)
		if not stopCallback:
			stopCallback = self.stop
		dd.addCallback(stopCallback, self.calibrationResults, *args, **kwargs)

	def stop(self, lc):
		self.reactor.stop()
		pygame.quit()

	@d.listen('ET_SPL')
	def iViewXEvent(self, inResponse):
		self.ts = int(inResponse[0])
		self.eye_position = map(float, inResponse[10:])

	@d.listen('ET_CAL')
	def iViewXEvent(self, inResponse):
		self.calibrationPoints = [None] * int(inResponse[0])

	@d.listen('ET_CSZ')
	def iViewXEvent(self, inResponse):
		pass

	@d.listen('ET_PNT')
	def iViewXEvent(self, inResponse):
		self.calibrationPoints[int(inResponse[0]) - 1] = (int(inResponse[1]), int(inResponse[2]))

	@d.listen('ET_CHG')
	def iViewXEvent(self, inResponse):
		self.currentPoint = int(inResponse[0]) - 1

	@d.listen('ET_VLS')
	def iViewXEvent(self, inResponse):
		self.state = 2
		self.calibrationResults.append(inResponse)

	@d.listen('ET_CSP')
	def iViewXEvent(self, inResponse):
		pass

	@d.listen('ET_FIN')
	def iViewXEvent(self, inResponse):
		self.state = 1
		self.client.requestCalibrationResults()
		self.client.validateCalibrationAccuracy()
