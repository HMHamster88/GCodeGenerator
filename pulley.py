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

material_height = 4
step_down = -1
pulley_center = GCodeGen.v2(0, 0)
center_hole_radius = 16
mount_hole_count = 4
mount_hole_radius = 2.5
mount_hole_distance = 19

lw_hole_count = 5
lw_hole_fill = 0.5
lw_hole_min_radius = 25
lw_hole_max_radius = 70
lw_hole_fillet_min_radius = 5
lw_hole_fillet_max_radius = 8

codeGen.abs_coords()
codeGen.go_to_safety_height()

def make_hole(center, radius, start_z, stop_z):
	for z in drange(start_z, stop_z, step_down):
		codeGen.go_to_circle_start(center, radius - tool_radius, 1)
		codeGen.vertical_feed_to(z)
		codeGen.horizontal_circle(center, radius - tool_radius, 1)

def make_holes(center, radius, start_z, stop_z, distance, hole_count):
	for hole in range(0, hole_count):
		hole_center = GCodeGen.v2_from_angle(math.pi * 2 * (hole / hole_count)) * distance
		make_hole(center + hole_center, radius, start_z, stop_z)
		codeGen.go_to_safety_height()

make_hole(pulley_center, center_hole_radius, material_height + step_down, 0)
codeGen.go_to_safety_height()
make_holes(pulley_center, mount_hole_radius, material_height + step_down, 0, mount_hole_distance, mount_hole_count)

for lw_hole in range(0, lw_hole_count):
	lw_hole_start_angle = math.pi * 2 * (lw_hole / lw_hole_count)
	lw_hole_stop_angle = math.pi * 2 * ((lw_hole +  lw_hole_fill) / lw_hole_count)
	codeGen.horizontal_arc(pulley_center, lw_hole_min_radius, lw_hole_stop_angle, lw_hole_start_angle, 1)
	codeGen.horizontal_arc(GCodeGen.v2_from_angle(lw_hole_start_angle) * (lw_hole_min_radius + lw_hole_fillet_min_radius), lw_hole_fillet_min_radius, lw_hole_start_angle - math.pi, lw_hole_start_angle - math.pi / 2, 0)
	codeGen.horizontal_arc(GCodeGen.v2_from_angle(lw_hole_start_angle) * (lw_hole_max_radius - lw_hole_fillet_max_radius), lw_hole_fillet_max_radius, lw_hole_start_angle - math.pi / 2, lw_hole_start_angle , 0)
	codeGen.horizontal_arc(pulley_center, lw_hole_max_radius, lw_hole_start_angle, lw_hole_stop_angle, 0)
	codeGen.horizontal_arc(GCodeGen.v2_from_angle(lw_hole_stop_angle) * (lw_hole_max_radius - lw_hole_fillet_max_radius), lw_hole_fillet_max_radius, lw_hole_stop_angle, lw_hole_stop_angle + math.pi / 2, 0)
	codeGen.horizontal_arc(GCodeGen.v2_from_angle(lw_hole_stop_angle) * (lw_hole_min_radius + lw_hole_fillet_min_radius), lw_hole_fillet_min_radius, lw_hole_stop_angle + math.pi / 2, lw_hole_stop_angle + math.pi, 0)

for z in drange(material_height + step_down, 0, step_down):
	codeGen.go_to_safety_height()
	for tooth in range(0, tooth_count):
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

		codeGen.go_to_arc_start(pulley_center, pulley_radius + tool_radius, tooth_a_begin, tooth_a_end, 0)
		codeGen.vertical_feed_to(z)
		codeGen.horizontal_arc(pulley_center, pulley_radius + tool_radius, tooth_a_begin, tooth_a_end, 0)
		codeGen.horizontal_arc(fillet_pos1, fillet_r + tool_radius, tooth_a_end, tooth_a_end + fillet_angle, 0)

		codeGen.horizontal_arc(socket_pos, socket_radius - tool_radius, socket_a_center - socket_ang, socket_a_center + socket_ang, 1)

		codeGen.horizontal_arc(fillet_pos2, fillet_r + tool_radius, tooth_a_next - fillet_angle, tooth_a_next, 0)
codeGen.go_to_safety_height()
