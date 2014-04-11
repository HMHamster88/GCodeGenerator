import math
class v2:
	x = 0
	y = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, v):
		return v2(self.x + v.x, self.y + v.y)

	def __sub__(self, v):
		return v2(self.x - v.x, self.y - v.y)

	def __mul__(self, m):
		return v2(self.x * m, self.y * m)

def  v2_from_angle(angle):
	return v2(math.cos(angle), math.sin(angle))

class GCodeGenerator:
	horizontal_feed = 100
	vertial_feed = 100
	def __init__(self, file):
		self.file = file

	def horizontal_feed_to(self, v):
		self.file.write("G01 X{0} Y{1} F{2}\n".format(v.x, v.y, self.horizontal_feed))

	def vertical_feed_to(self, z):
		self.file.write("G01 Z{0} F{1}\n".format(z, self.vertial_feed))

	def horizontal_arc(self, center, radius, start_angle, stop_angle, cw):
		start = center + v2_from_angle(start_angle) * radius;
		start_offset = center - start 
		end = center + v2_from_angle(stop_angle) * radius
		self.horizontal_feed_to(start)
		if(cw):
			self.file.write("G02")
		else:
			self.file.write("G03")
		self.file.write(" X{0} Y{1} I{2} J{3} F{4}\n".format(end.x, end.y, start_offset.x, start_offset.y, self.horizontal_feed))
