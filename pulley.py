import GCodeGen
import math

file = open('pulley.nc', 'w')
codeGen = GCodeGen.GCodeGenerator(file)

def drange(start, end, step):
    while (step > 0 and start <= end) or (step < 0 and start >= end):
        yield start
        start += step
    if (step > 0 and start - step < end) or (step < 0 and start + step > end):
    	yield end;

tool_radius = (25.4 * 0.0591) / 2

socket_radius = 2
socket_deep = 1.6
tooth_count = 66
tooth_angle = math.pi * 2 / tooth_count
socket_angle = tooth_angle * (25.6211 / 36)
pulley_radius = tooth_count * 1.5 #1.45 - 10 tooth
fillet_r = 0.5
edges = []

print(pulley_radius)

a = pulley_radius - socket_deep
b = pulley_radius - fillet_r
k = math.sqrt(a*a + b*b - 2*a*b * math.cos(socket_angle / 2))
z = math.acos((socket_radius + fillet_r) / k)
u = math.acos((b*b + k*k - a*a)/(2*b*k))
fillet_angle = math.pi - (u + z);
socket_ang = math.pi - (fillet_angle - socket_angle / 2)

codeGen.abs_coords()
codeGen.go_to_safety_height()

for z in drange(11, 11-5, -1):
	codeGen.go_to_safety_height()
	for tooth in range(0, 5):
		tooth_a_begin = tooth * tooth_angle;
		tooth_a_end = (tooth + 1) * tooth_angle - socket_angle;
		tooth_a_next = (tooth + 1) * tooth_angle;
		socket_a_center = (tooth + 1) * tooth_angle - socket_angle/2

		socket_pos = GCodeGen.v2_from_angle(socket_a_center) * (pulley_radius - socket_deep)
	
		socket_end_pos  = socket_pos + GCodeGen.v2_from_angle(socket_a_center + socket_ang) * socket_radius
		socket_begin_pos  = socket_pos + GCodeGen.v2_from_angle(socket_a_center - socket_ang) * socket_radius
	
		fillet_pos1 = GCodeGen.v2_from_angle(tooth_a_end) * (pulley_radius - fillet_r)
		fillet_pos2 = GCodeGen.v2_from_angle(tooth_a_next) * (pulley_radius - fillet_r)
	
		tooth_pos1 = GCodeGen.v2_from_angle(tooth_a_next) * pulley_radius
		tooth_pos2 = GCodeGen.v2_from_angle(tooth_a_end) * pulley_radius

		codeGen.go_to_arc_start(GCodeGen.v2(0, 0), pulley_radius + tool_radius, tooth_a_begin, tooth_a_end, 0)
		codeGen.vertical_feed_to(z)
		codeGen.horizontal_arc(GCodeGen.v2(0, 0), pulley_radius + tool_radius, tooth_a_begin, tooth_a_end, 0)
		codeGen.horizontal_arc(fillet_pos1, fillet_r + tool_radius, tooth_a_end, tooth_a_end + fillet_angle, 0)

		codeGen.horizontal_arc(socket_pos, socket_radius - tool_radius, socket_a_center - socket_ang, socket_a_center + socket_ang, 1)

		codeGen.horizontal_arc(fillet_pos2, fillet_r + tool_radius, tooth_a_next - fillet_angle, tooth_a_next, 0)
codeGen.go_to_safety_height()
