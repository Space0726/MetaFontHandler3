import codecs
import os.path, time
from xml.dom import minidom
import sys
from fontParts.world import CurrentFont
from mojo.UI import GetFolder,GetFile,PutFile

def fnextension ( filename ):
    try :
      basename,extension = filename.split('.')
    except :
           extension="garbage"
           basename=""
    return extension

def ufo2mf(destPath):
	f = CurrentFont()

	DIR_UFO = f.path+"/glyphs" 

	DIR_METAFONT_RADICAL = destPath+"/radical.mf"
	DIR_METAFONT_COMBINATION = destPath+"/combination.mf"
		
	print("Target:", DIR_UFO)
	print("Destination Path:", destPath)
	# Remove exist Metafont file for renew
	try:
		os.remove(DIR_METAFONT_RADICAL)
		os.remove(DIR_METAFONT_COMBINATION)
	except:
		notthing = 0

	# Get glyphs from UFO and Convert to Metafont
	glyphList = [f for f in os.listdir(DIR_UFO) if fnextension (f) == 'glif']
	for glyph in glyphList:
		convertToMetafont(glyph, DIR_UFO, DIR_METAFONT_RADICAL, DIR_METAFONT_COMBINATION)

	return None

class Point:
	name = ""
	idx = ""
	type = ""
	x = ""
	y = ""
	controlPoints = []
	dependX = ""
	dependY = ""
	penWidth = ""
	penHeight = ""
	startP = ""
	serif = ""
	customer = ""

def getValueByNode(tag, attribute):
	node = xmlData.getElementsByTagName(tag)
	try:
		return node[0].attributes[attribute].value
	except:
	 	return None
	 	
def convertFloatToStr(value, decimalPlace=4):
    strVal = str(float(value))
    return strVal[:strVal.find('.') + decimalPlace]

class numberToCharacterDict:
    n2c = {'1':'o', '2':'t', '3':'h', '4':'u', '5':'i', '6':'s', '7':'v', '8':'g', '9':'n', '0':'z', '_':'_'}
    @classmethod
    def getChar(cls, number):
        return cls.n2c[number]

def numberToCharacter(string):
    return ''.join([w if w.isalpha() else numberToCharacterDict.getChar(w) for w in list(string)])

def convertToMetafont(glyphName, dirUFO, dirRadical, dirCombination):
	global xmlData

	# Initialize points
	points = []
	for i in range(0, 200):
		points.append(Point())
		points[i].controlPoints = []

	# Get glyph's UFO file
	dirGlyph = dirUFO + "/" + glyphName
	xmlData = minidom.parse(dirGlyph)

	# If combination file, create characters for using glyph
	components = xmlData.getElementsByTagName('component')
	if len(components) != 0:
		fp = open(dirCombination, "a")
		# Write beginchar
		# glyphName = getValueByNode('glyph', 'name')

		unicodeList = xmlData.getElementsByTagName("unicode")
		if len(unicodeList) == 1:        # Need Change if unicode is more than 1
		    code = str(int(unicodeList[0].getAttribute('hex'), 16))
		fp.write('\nbeginchar('  + code + ', Width#, Height#, 0);\n')
		# fp.write('\nbeginchar('  + glyphName + ', Width#, Height#, 0);\n')
		fp.write("	currenttransform := identity slanted slant;\n\n")

		# Write componenet
		cnt = 0
		for component in components:
			name = component.attributes['base'].value
			# *** Changed *** #
			fp.write("	" + numberToCharacter(name))
			# Apply each parameter
			if cnt == 0:
				fp.write("(firstMoveSizeOfH, firstMoveSizeOfV)\n")
			elif cnt == 1:
				fp.write("(middleMoveSizeOfH, middleMoveSizeOfV)\n")
			if cnt == 2:
				fp.write("(finalMoveSizeOfH, finalMoveSizeOfV)\n")
			cnt = cnt + 1

		# Write end
		fp.write("endchar;\n");
		fp.close()
	else: # If glyph file
		fp = open(dirRadical, "a")

		glyphName = getValueByNode('glyph', 'name')
		fp.write("% File parsed with MetaUFO %\n")
		# *** Changed *** #
		fp.write('def ' + numberToCharacter(glyphName) + '(expr moveSizeOfH, moveSizeOfV) =\n')

		# Get UFO data by xml parser
		UNDEFINED = 9999
		leftP = [[UNDEFINED for col in range(2)] for row in range(200)]
		rightP = [[UNDEFINED for col in range(2)] for row in range(200)]
		diffP = [[0 for col in range(2)] for row in range(200)]
		dependLX = [0 for i in range(200)]
		dependRX = [0 for i in range(200)]
		dependLY = [0 for i in range(200)]
		dependRY = [0 for i in range(200)]
		penWidth = [-1 for i in range(200)]
		penHeight = [-1 for i in range(200)]
		cp = []
		cpX = []
		cpY = []
		type = []
		pointOrder = []
		pointCnt = 0
		cpCnt = 0


		########################################################################################
		# Get point's tag information
		node = xmlData.getElementsByTagName('point')

		for i in range(len(node)):
			# if have a penPair attribute
			try:
				name = node[i].attributes['penPair'].value
				# Get pointNumber and Store point order
				pointNumber = int(name[1:-1])
				if name.find('l') != -1:
					idx = pointNumber * 2 - 1
				elif name.find('r') != -1:
					idx = pointNumber * 2
				else:
					print('Error : penPair attribute have a incorrect format value (' + name + ')')
					return

				pointOrder.append(idx)

				# Store basic information of point having a penPair attribute
				# print("length:", len(points), ", idx:", idx)
				points[idx].name = name
				points[idx].type = node[i].attributes['type'].value
				points[idx].x = str(float(node[i].attributes['x'].value)/1000)
				points[idx].y = str(float(node[i].attributes['y'].value)/1000)
				points[idx].idx = pointCnt
				pointCnt = pointCnt + 1

				# If point have a special attributes, stroe it
				try:
					points[idx].dependX = node[i].attributes['dependX'].value
				except:
					notting = 0

				try:
					points[idx].dependY = node[i].attributes['dependY'].value
				except:
					notting = 0

				try:
					points[idx].startP = node[i].attributes['innerType'].value
					firstIdx = idx
				except:
					notting = 0

				try:
					points[idx].serif = node[i].attributes['serif'].value
				except:
					notting = 0

				try:
					points[idx].customer = node[i].attributes['customer'].value
				except:
					notting = 0

			# if not have penPair attribute, it is control point
			except:
				print(glyphName)
				idx = pointOrder[-1]
				xValue = node[i].attributes['x'].value
				yValue = node[i].attributes['y'].value
				points[idx].controlPoints.append([xValue, yValue])


		##############################################################################
		# Set pen's paramter
		fp.write("\n% pen parameter \n")
		for i in range(1, 100):
			l = i * 2 - 1
			r = i * 2

			if points[l].name == "" or points[r].name == "":
				continue

			penWidth[i] = float(points[l].x) - float(points[r].x)
			penHeight[i] = float(points[l].y) - float(points[r].y)

			# *** Changed *** #
			fp.write("penWidth_" + str(i) + " := (((penWidthRate - 1) * "
				+ convertFloatToStr(penWidth[i]) + ") / 2) * Width;	")
			# *** Changed *** #
			fp.write("penHeight_" + str(i) + " := (((penHeightRate - 1) * "
				+ convertFloatToStr(penHeight[i]) + ") / 2) * Height;\n")

		##############################################################################
		# L, R points
		fp.write("\n% point coordinates \n")
		for i in range(len(pointOrder)):
			idx = pointOrder[i]
			name = points[idx].name[1:]

			if name.find("l") != -1:
				op = "+"
			else:
				op = "-"

			fp.write("x" + name + " := (" + points[idx].x)

			if points[idx].customer != "":
				fp.write(" + " + points[idx].customer)

			fp.write(" + " + "moveSizeOfH) * " + "Width ")
			if points[idx].dependX != "":
				dependXValue = points[idx].dependX
				if dependXValue.find("l") != -1:
					fp.write("+ penWidth_" + dependXValue[1:-1])
				else:
					fp.write("- penWidth_" + dependXValue[1:-1])
			elif penWidth[int(name[0:-1])] != -1:
				fp.write(op + " penWidth_" + name[0:-1])
			fp.write(";	")

			fp.write("y"+ name + " := (" + points[idx].y + " + " + "moveSizeOfV) * " + "Height ")
			if points[idx].dependY != "":
				dependYValue = points[idx].dependY
				if dependYValue.find("l") != -1:
					fp.write("+ penHeight_" + dependYValue[1:-1])
				else:
					fp.write("- penHeight_" + dependYValue[1:-1])
			elif penHeight[int(name[0:-1])] != -1:
				fp.write(op + " penHeight_" + name[0:-1])
			fp.write(";\n")
			"""
		##############################################################################
		# Set dependency
		fp.write("\n% dependency\n")
		for i in range(len(pointOrder)):
			idx = pointOrder[i]
			name = points[idx].name[1:]

			if points[idx].dependX != "":
				dependIdx = points[idx].dependX[1:-1]
				if points[idx].dependX.find("r") > -1 :
					fp.write("x" + name + " := x" + name + " - penWidth_" + dependIdx + ";\n")
				else:
					fp.write("x" + name + " := x" + name + " + penWidth_" + dependIdx + ";\n")
			if points[idx].dependY != "":
				dependIdx = points[idx].dependY[1:-1]
				if points[idx].dependY.find("r") > -1 :
					fp.write("y" + name + " := y" + name + " - penHeight_" + dependIdx + ";\n")
				else:
					fp.write("y" + name + " := y" + name + " + penHeight_" + dependIdx + ";\n")
		"""
		###############################################################################
		fp.write("\n% control point\n")
		for i in range(0, len(pointOrder)):
			if points[pointOrder[i]].startP != "":
				firstIdx = pointOrder[i]

			if i == len(pointOrder)-1 or points[pointOrder[i+1]].startP != "":
				curIdx = pointOrder[i]
				nextIdx = firstIdx
			else:
				curIdx = pointOrder[i]
				nextIdx = pointOrder[i+1]

			if points[nextIdx].name == "" or points[nextIdx].type == "line":
				continue

			name = points[curIdx].name[1:-1]
			nextName = points[nextIdx].name[1:-1]
			way = points[curIdx].name[-1]

			if points[curIdx].name.find("l") != -1:
				curOp = "+"
			else:
				curOp = "-"

			if points[nextIdx].name.find("l") != -1:
				nextOp = "+"
			else:
				nextOp = "-"

			curPenWidthIdx = int(name)
			curPenHeightIdx = int(name)
			nextPenWidthIdx = int(nextName)
			nextPenHeightIdx = int(nextName)

			dependXValue = points[curIdx].dependX
			if dependXValue != "":
				if dependXValue.find("l") != -1:
					curPenW = "+ penWidth_" + dependXValue[1:-1]
				else:
					curPenW = "- penWidth_" + dependXValue[1:-1]
				curPenWidthIdx = int(dependXValue[1:-1])
			elif penWidth[int(name)] != -1:
				curPenW = curOp + " penWidth_" + name
			else:
				curPenW = ""

			dependYValue = points[curIdx].dependY
			if dependYValue != "":
				if dependYValue.find("l") != -1:
					curPenH = "+ penHeight_" + dependYValue[1:-1]
				else:
					curPenH = "- penHeight_" + dependYValue[1:-1]
				curPenHeightIdx = int(dependYValue[1:-1])
			elif penHeight[int(name)] != -1:
				curPenH = curOp + " penHeight_" + name
			else:
				curPenH = ""

			dependXValue = points[nextIdx].dependX
			if dependXValue != "":
				if dependXValue.find("l") != -1:
					nextPenW = "+ penWidth_" + dependXValue[1:-1]
				else:
					nextPenW = "- penWidth_" + dependXValue[1:-1]
				nextPenWidthIdx = int(dependXValue[1:-1])
			elif penWidth[int(nextName)] != -1:
				nextPenW = nextOp + " penWidth_" + nextName
			else:
				nextPenW = ""

			dependYValue = points[nextIdx].dependY
			if dependYValue != "":
				if dependYValue.find("l") != -1:
					nextPenH = "+ penHeight_" + dependYValue[1:-1]
				else:
					nextPenH = "- penHeight_" + dependYValue[1:-1]
				nextPenHeightIdx = int(dependYValue[1:-1])
			elif penHeight[int(nextName)] != -1:
				nextPenH = nextOp + " penHeight_" + nextName
			else:
				nextPenH = ""

			if points[curIdx].customer != "":
				curCustomer = points[curIdx].customer
			else:
				curCustomer = ""

			if points[nextIdx].customer != "":
				nextCustomer = points[nextIdx].customer
			else:
				nextCustomer = ""

			pointName = points[curIdx].name[1:]
			# *** Changed float -> convertFloatToStr() *** #
			if points[nextIdx].type == "curve":
				fp.write("x" + pointName + "1 := (" + convertFloatToStr(float(points[curIdx].controlPoints[0][0]) * 0.001) + " + " + curCustomer + " + moveSizeOfH) * Width " + curPenW +";	")
				fp.write("y" + pointName + "1 := (" + convertFloatToStr(float(points[curIdx].controlPoints[0][1]) * 0.001) + " + moveSizeOfV) * Height " + curPenH +";\n")
			#	fp.write("x" + pointName + "1 := x" + pointName + "1 - (1 - curveRate)*(" + "x" + pointName + "1 - x" + pointName + ");	")
			#	fp.write("y" + pointName + "1 := y" + pointName + "1 - (1 - curveRate)*(" + "y" + pointName + "1 - y" + pointName + ");\n")
				fp.write("x" + pointName + "2 := (" + convertFloatToStr(float(points[curIdx].controlPoints[1][0]) * 0.001) + " + " + nextCustomer + " + moveSizeOfH) * Width " + nextPenW +";	")
				fp.write("y" + pointName + "2 := (" + convertFloatToStr(float(points[curIdx].controlPoints[1][1]) * 0.001) + " + moveSizeOfV) * Height " + nextPenH +";\n")
			#	fp.write("x" + pointName + "2 := x" + pointName + "2 - (1 - curveRate)*(" + "x" + pointName + "2 - x" + pointName + ");	")
			#	fp.write("y" + pointName + "2 := y" + pointName + "2 - (1 - curveRate)*(" + "y" + pointName + "2 - y" + pointName + ");\n")
			elif points[nextIdx].type == "qcurve":
				size = len(points[curIdx].controlPoints)
				for j in range(0, size):
					if size % 2 == 1 and j == size / 2:
						if penWidth[curPenWidthIdx] > penWidth[nextPenWidthIdx]:
							fp.write("x" + pointName + str(j+1) + " := (" + convertFloatToStr(float(points[curIdx].controlPoints[j][0]) * 0.001) + " + " + curCustomer + " + moveSizeOfH) * Width " + curPenW +";	")
						else:
							fp.write("x" + pointName + str(j+1) + " := (" + convertFloatToStr(float(points[curIdx].controlPoints[j][0]) * 0.001) + " + " + nextCustomer + " + moveSizeOfH) * Width " + nextPenW +";	")

						if penHeight[curPenHeightIdx] > penHeight[nextPenHeightIdx]:
							fp.write("y" + pointName + str(j+1) + " := (" + convertFloatToStr(float(points[curIdx].controlPoints[j][1]) * 0.001) + " + moveSizeOfV) * Height " + curPenH +";\n")
						else:
							fp.write("y" + pointName + str(j+1) + " := (" + convertFloatToStr(float(points[curIdx].controlPoints[j][1]) * 0.001) + " + moveSizeOfV) * Height " + nextPenH +";\n")

					elif j < size / 2:
						fp.write("x" + pointName + str(j+1) + " := (" + convertFloatToStr(float(points[curIdx].controlPoints[j][0]) * 0.001) + " + " + curCustomer + " + moveSizeOfH) * Width " + curPenW +";	")
						fp.write("y" + pointName + str(j+1) + " := (" + convertFloatToStr(float(points[curIdx].controlPoints[j][1]) * 0.001) + " + moveSizeOfV) * Height " + curPenH +";\n")
					else:
						fp.write("x" + pointName + str(j+1) + " := (" + convertFloatToStr(float(points[curIdx].controlPoints[j][0]) * 0.001) + " + " + nextCustomer + " + moveSizeOfH) * Width " + nextPenW +";	")
						fp.write("y" + pointName + str(j+1) + " := (" + convertFloatToStr(float(points[curIdx].controlPoints[j][1]) * 0.001) + " + moveSizeOfV) * Height " + nextPenH +";\n")

			#		fp.write("x" + pointName + str(j+1) + " := x" + pointName + str(j+1) + " - (1 - curveRate) * (" + "x" + pointName + str(j+1) + " - x" + pointName + ");	")
			#		fp.write("y" + pointName + str(j+1) + " := y" + pointName + str(j+1) + " - (1 - curveRate) * (" + "y" + pointName + str(j+1) + " - y" + pointName + ");\n")

		# *** Changed ***
		#####################################################################################################################################
		# Get draw

		fp.write("\n% Get draw \n");

		source = ""
		dash = ""
		startIdx = 0
		for i in range(0, len(pointOrder)) :
			idx = pointOrder[i]

			if i + 1 != len(pointOrder) and points[pointOrder[i+1]].startP == "":
				nextIdx = pointOrder[i+1]
			else:
				nextIdx = startIdx

			if points[idx].startP != "":
				if i != 0:
					fp.write("cycle;\n")
				startIdx = idx
				if points[idx].startP == "fill":
					source = "fill "
				else:
					source = "unfill "
			else:
				source = ""

			source += points[pointOrder[i]].name
			dash = " .. "

			if points[nextIdx].type == "line":
				dash = " -- "
			elif points[nextIdx].type == "None":
				dash = " .. "
			elif points[nextIdx].type == "curve":
				dash = " .. "
				dash = dash + "controls (z" + points[idx].name[1:] + "1) and (z" + points[idx].name[1:] + "2) .. "
			elif points[nextIdx].type == "qcurve":
				dash = " .. "
				controlPoints = points[idx].controlPoints
				for j in range(0, len(controlPoints)):
					if j == 0:
						QP0 = points[idx].name
					else:
						QP0 = QP2

					QP1 = points[idx].name + str(j+1)
					if j != len(controlPoints) - 1:
						newX = "(x" + points[idx].name[1:] + str(j+1) + " + x" + points[idx].name[1:] + str(j+2) + ") / 2"
						newY = "(y" + points[idx].name[1:] + str(j+1) + " + y" + points[idx].name[1:] + str(j+2) + ") / 2"
						QP2 = "(" + newX + ", " + newY + ")"
					else:
						QP2 = points[nextIdx].name

					CP1 = QP0 + " + 2 / 3 * (" + QP1 + " - " + QP0 + ")"
					CP2 = QP2 + " + 2 / 3 * (" + QP1 + " - " + QP2 + ")"
					dash = dash + "controls (" + CP1 + ") and (" + CP2 + ") .. "

					if j != len(controlPoints) - 1:
						dash = dash + QP2 + " .. "


			source = source + dash
			fp.write(source + "\n")
		fp.write("cycle;\n")

		#########################################################################################################
		# Set serif attribute
		for i in range(0, len(points)):
			if points[i].serif == "1":
				idx = points[i].name[1:-1]
				fp.write("serif_i(x" + idx + "l, y" + idx + "l, x" + idx + "r, y" + idx + "r);\n")
			elif points[i].serif == "2":
				idx = points[i].name[1:-1]
				fp.write("serif_ii(x" + idx + "l, y" + idx + "l, x" + idx + "r, y" + idx + "r);\n")
			# end serif test by ghj (1710A) /w glyphs.mf UFO2mf.py	xmltomf.py				
			elif points[i].serif == "3":
				idx = points[i].name[1:-1]
				fp.write("serif_iii(x" + idx + "l, y" + idx + "l, x" + idx + "r, y" + idx + "r, curveRate);\n")
			# end serif test by ghj (1710A) /w glyphs.mf UFO2mf.py	xmltomf.py				
			elif points[i].serif == "4":
				idx = points[i].name[1:-1]
				fp.write("serif_iv(x" + idx + "l, y" + idx + "l, x" + idx + "r, y" + idx + "r, curveRate);\n")
			elif points[i].serif == "5":
				idx = points[i].name[1:-1]
				fp.write("serif_v(x" + idx + "l, y" + idx + "l, x" + idx + "r, y" + idx + "r, curveRate);\n")


		##########################################################################################################
		# last

		fp.write("\n% pen labels\n");
		fp.write("penlabels(range 1 thru 200);\n");
		fp.write("enddef;\n\n");

		fp.close()
	return None

# ufo2mf()
