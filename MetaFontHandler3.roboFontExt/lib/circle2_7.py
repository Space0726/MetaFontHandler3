from xml.etree.ElementTree import *
import os

def search_curve(contours):
	circle = []
	for contour in contours:
		count = 0
		points = contour.getchildren()
		for point in points:
			if point.get("type") == "curve":
				count += 1
		if 4 <= count and count <= 8:
			circle.append((contour, count))

	return circle

def error_range(a, b, ranges):
	a = int(a)
	b = int(b)
	if ranges >= a - b and b - a <= ranges:
		return True
	else:
		return False

def circle2_7(wd):
	vowels = ['w', 'y', 'a', 'e', 'i', 'o', 'u', 'h'] # this has to be changed 
	path = wd
	files = os.listdir(path)
	os.chdir(path)
	for file in files:
		if file.rfind('_') != -1 and file[file.rfind('_') + 1] in vowels:
			files.remove(file)

	for file in files:
		if os.path.isdir(file)==False:
			continue
		glifs = os.listdir(file + '/')
		for glif in glifs:
			if glif.rfind('_') != -1 and glif[glif.rfind('_') + 1] in vowels:
				tree = parse(file + '/' + glif)
				glyph = tree.getroot()
				outline = glyph.find("outline")
				contours = outline.getchildren()
				circle = search_curve(contours)

				if len(circle) == 2:
					contour1 = circle[0][0]
					contour2 = circle[1][0]
					points1 = contour1.getchildren()	
					points2 = contour2.getchildren()
					xy = []
					lxy = []
					if len(points1) != len(points2):
						if len(points1) > len(points2):
							many = points1
							little = points2
							contour = contour1
						elif len(points1) < len(points2):
							little = points2
							many = points1
							contour = contour2

						for i, point in enumerate(many):
							if point.get("type") == "curve":
								if error_range(point.get("x"), many[i + 1].get("x"), 2):
									xy.append('y')
								elif error_range(point.get("y"), many[i + 1].get("y"), 2):
									xy.append('x')

								elif point.get("penPair") != None:
									xy.append('z')

								else:
									xy.append('c')
									continue
							else:
								xy.append('n')
								continue

						for i, type in enumerate(xy):
							if xy[i] == 'c':
								xy[i - 1] = xy[i - 2] = xy[i + 1] = xy[i + 2] = 'r'

						for i, point in enumerate(many):
							if xy[i] == 'c':
								if xy[i - 3] == 'y':
									many[i - 2].attrib["y"] = many[i - 1].attrib["y"]
									many[i + 2].attrib["x"] = many[i + 1].attrib["x"]
								elif xy[i - 3] == 'x':
									many[i - 2].attrib["x"] = many[i - 1].attrib["x"]
									many[i + 2].attrib["y"] = many[i + 1].attrib["y"]

						for i, point in enumerate(many):
							if many[i].get("penPair") == None and many[i].get("type") == "curve":
								contour1.remove(many[i - 1])
								contour1.remove(many[i - 1])
								contour1.remove(many[i - 1])

						for i, point in enumerate(little):
							if point.get("type") == "curve":
								if error_range(point.get("x"), little[i + 1].get("x"), 2):
									lxy.append('y')
								elif error_range(point.get("y"), little[i + 1].get("y"), 2):
									lxy.append('x')
								elif point.get("penPair") != None:
									lxy.append('z')
								else:
									lxy.append('c')
									continue
							else:
								lxy.append('n')
								continue

						for i, type in enumerate(lxy):
							if lxy[i] == 'c':
								lxy[i - 1] = lxy[i - 2] = lxy[i + 1] = lxy[i + 2] = 'r'

						for i, point in enumerate(little):
							if lxy[i] == 'c':
								if lxy[i - 3] == 'y':
									little[i - 2].attrib["y"] = little[i - 1].attrib["y"]
									little[i + 2].attrib["x"] = little[i + 1].attrib["x"]
								elif lxy[i - 3] == 'x':
									little[i - 2].attrib["x"] = little[i - 1].attrib["x"]
									little[i + 2].attrib["y"] = little[i + 1].attrib["y"]

						for i, point in enumerate(little):
							if little[i].get("penPair") == None and little[i].get("type") == "curve":
								contour2.remove(little[i - 1])
								contour2.remove(little[i - 1])
								contour2.remove(little[i - 1])

				ElementTree(glyph).write("../glyphs/" + file + '/' + glif)

'''

for file in files:
	if file.endswith('glif'):
		tree = parse(file)
		glyph = tree.getroot()
		outline = glyph.find("outline")

		contours = outline.getchildren()

		for contour in contours:
			points = contour.findall("point")
			#print(points)
'''

'''
def search_curve(contours):
	circle = []
	for contour in contours:
		count = 0
		points = contour.getchildren()
		for point in points:
			if point.get("type") == "curve":
				count += 1
		if count == 4 or count == 8:
			circle.append(contour)

	return circle
'''
