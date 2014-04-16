import math

def drange(start, end, step):
    while (step > 0 and start <= end) or (step < 0 and start >= end):
        yield start
        start += step
    if (step > 0 and start - step < end) or (step < 0 and start + step > end):
    	yield end;

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
	safety_height = 6
	def __init__(self, file):
		self.file = file

	def  abs_coords(self):
		self.file.write("G90")

	def go_to_safety_height(self):
		self.file.write("G00 Z{0:0.4f}\n".format(self.safety_height))
	
	def go_to(self, v):
		self.file.write("G00 X{0:0.4f} Y{1:0.4f}\n".format(v.x, v.y))

	def horizontal_feed_to(self, v):
		self.file.write("G01 X{0:0.4f} Y{1:0.4f} F{2:0.4f}\n".format(v.x, v.y, self.horizontal_feed))

	def vertical_feed_to(self, z):
		self.file.write("G01 Z{0:0.4f} F{1:0.4f}\n".format(z, self.vertial_feed))

	def go_to_arc_start(self, center, radius, start_angle, stop_angle, cw):
		start = center + v2_from_angle(start_angle) * radius;
		self.go_to(start)

	def go_to_circle_start(self, center, radius, cw):
		if(cw):
			self.go_to_arc_start(center, radius, math.pi * 2, 0, cw)
		else:
			self.go_to_arc_start(center, radius, 0, math.pi * 2, cw)

	def horizontal_circle(self, center, radius, cw):
		if(cw):
			self.horizontal_arc(center, radius, math.pi * 2, 0, cw)
		else:
			self.horizontal_arc(center, radius, 0, math.pi * 2, cw)

	def horizontal_ring(self, center, radius1, radius2, step, cw):
		for radius in drange(radius1, radius2, step):
			self.horizontal_circle(center, radius, cw)

	def horizontal_arc(self, center, radius, start_angle, stop_angle, cw):
		start = center + v2_from_angle(start_angle) * radius;
		start_offset = center - start 
		end = center + v2_from_angle(stop_angle) * radius
		self.horizontal_feed_to(start)
		if(cw):
			self.file.write("G02")
		else:
			self.file.write("G03")
		self.file.write(" X{0:0.4f} Y{1:0.4f} I{2:0.4f} J{3:0.4f} F{4:0.4f}\n".format(end.x, end.y, start_offset.x, start_offset.y, self.horizontal_feed))
