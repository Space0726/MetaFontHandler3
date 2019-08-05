#Robo font Class
from vanilla import *
from xml.etree.ElementTree import parse , SubElement ,dump
from xml.etree.ElementTree import ElementTree
from mojo.UI import GetFolder, GetFile, PutFile
from mojo.events import installTool, uninstallTool
import os
import AttributeTool
import makeufobyrobofab
import point_rotator
import base_maker
import circle2_7
import unfill_vowel
import make_dir
import reverse
import name_attr
import mf_maker
import CenterLine

class Start(object):
    """Gui 창을 띄우는 클래스"""

    def __init__(self):

        self._metaGlyphs = []

        self.w = FloatingWindow((200, 200), "MetaFont Handler")
        self.w.pairingButton = Button((10, 10, -10, 20), "Letter Pairing",callback = self.buttonClick)
        self.w.constButton = Button((10, 40, -10, 20), "Vowel Attribute",callback = self.buttonClick)
        self.w.vowelButton = Button((10, 70, -10, 20), "Consonant Attribute",callback = self.buttonClick)
        self.w.combineButton = Button((10, 100, -10, 20), "Make an ufo file",callback = self.buttonClick)
        self.w.mf_maker = Button((10, 130, -10, 20), "Generate MF files",callback = self.buttonClick)

        self.w.open()


    def buttonClick(self,sender) :
    	if sender.getTitle() == "Letter Pairing":
    	    self.pairing()
    	#elif sender.getTitle() == "Install Attribute Tool" :
        #    self.InstallTool()
    	elif sender.getTitle() == "Uninstall Attribute Tool":
    	    self.UnTool()
    	elif sender.getTitle() == "Vowel Attribute":
    	    self.addVowelAttr()
    	elif sender.getTitle() == "Consonant Attribute":
    	    self.addConsonantAttr()
    	elif sender.getTitle() == "Make an ufo file":
    	    self.combineufo()
    	elif sender.getTitle() == "Generate MF files":
    	    self.make_mf()

    def addVowelAttr(self):
        glyphpath = GetFile("Choose a UFO")
        filelist = os.listdir(glyphpath)

        filelist2 = []
        for f in filelist:
            f2 = glyphpath +"/"+ f
            filelist2.append(f2)


        for f in filelist2:
            if f.endswith(".glif"):
                print(f + " <- glif file\n")
                doc = parse(f)
                root = doc.getroot()

                for outline in root.iter("outline"):
                    serifCount = 1
                    roundCount = 1

                    for contour in outline.iter("contour"):
                        minX = 1000
                        minY = 1000
                        maxX = -1000
                        maxY = -1000

                        for point in contour.iter("point"):
                            pointX = int(float(point.get('x')))
                            pointY = int(float(point.get('y')))
                            if minX > pointX:
                                minX = pointX
                            if maxX <= pointX:
                                maxX = pointX
                            if minY > pointY:
                                minY = pointY
                            if maxY <= pointY:
                                maxY = pointY

                        horizontalLine = maxX - minX
                        verticalLine = maxY - minY

                        if horizontalLine * 6 < verticalLine:
                            for point in contour.iter("point"):
                                pointX = int(float(point.get('x')))
                                pointY = int(float(point.get('y')))
                                if pointX == minX and pointY == maxY:
                                    point.set("serif",str(serifCount))
                                    serifCount+=1
                                    serifPenPair = point.get("penPair")
                                    if serifPenPair[-1] == "r":
                                        pairSerifPenPair = serifPenPair
                                        serifPenPair = serifPenPair[:2] + "l"
                                        point.set("penPair", serifPenPair)
                                        for pairPoint in contour.iter("point"):
                                            if point == pairPoint:
                                                continue
                                            if pairPoint.get("penPair").find(serifPenPair) != -1:
                                                pairPoint.set("penPair", pairSerifPenPair)
                                                break
                                elif pointX == minX and pointY == minY:
                                    point.set("round",str(roundCount))
                                    roundCount+=1
                                    roundPenPair = point.get("penPair")
                                    if roundPenPair[-1] == "r":
                                        pairRoundPenPair = roundPenPair
                                        roundPenPair = roundPenPair[:2] + "l"
                                        point.set("penPair", roundPenPair)
                                        for pairPoint in contour.iter("point"):
                                            if point == pairPoint:
                                                continue
                                            if pairPoint.get("penPair").find(roundPenPair) != -1:
                                                pairPoint.set("penPair", pairRoundPenPair)
                                                break
                doc.write(f, encoding="utf-8", xml_declaration=True)

    def addConsonantAttr(self):
        glyphpath = GetFile("Choose a UFO")
        filelist = os.listdir(glyphpath)

        filelist2 = []
        for f in filelist:
            f2 = glyphpath +"/"+ f
            filelist2.append(f2)

        for f in filelist2:
        	if f.endswith(".glif"):
        		doc = parse(f)
        		root = doc.getroot()
        		totalminX=1000
        		for outline in root.iter("outline"):
        			for contour in outline.iter("contour"):
        				minX = 1000
        				minY = 1000
        				maxX = 0
        				maxY = 0
        				for point in contour.iter("point"):
        					pointX = int(float(point.get('x')))
        					pointY = int(float(point.get('y')))
        					if minX > pointX:
        						minX = pointX
        					if maxX < pointX:
        						maxX = pointX
        					if minY > pointY:
        						minY = pointY
        					if maxY < pointY:
        						maxY = pointY
        					if totalminX > minX:
        						totalminX = minX

        		for outline in root.iter("outline"):
        			connerCount = 1
        			for contour in outline.iter("contour"):
        				minX = 1000
        				minY = 1000
        				maxX = 0
        				maxY = 0

        				vessel = []
        				for point in contour.iter("point"):
        					pointX = int(float(point.get('x')))
        					pointY = int(float(point.get('y')))
        					if minX > pointX:
        						minX = pointX
        					if maxX < pointX:
        						maxX = pointX
        					if minY > pointY:
        						minY = pointY
        					if maxY < pointY:
        						maxY = pointY

        				horizontalLine = maxX - minX
        				verticalLine = maxY - minY
        				for point in contour.iter("point"):
        					x = int(float(point.get('x')))
        					y = int(float(point.get('y')))
        					dx = 0
        					dy = 0
        					for point2 in contour.iter("point"):
        						compX = int(float(point2.get('x')))
        						compY = int(float(point2.get('y')))

        						if x == compX:
        							if y == compY:
        								continue
        							elif y > compY:
        								dy = -1
        							else:
        								dy = 1

        						if y == compY:
        							if x == compX:
        								continue
        							elif x > compX:
        								dx = -1
        							else:
        								dx = 1
        					if dx == 1 and dy == 1:
        						vessel.append(point)
        				result = sorted(vessel,key=lambda vessel: int(float(vessel.get('x'))))
        				result2 = sorted(vessel,key=lambda vessel: int(float(vessel.get('y'))))
        				if len(vessel) ==0:
        					pass
        				elif len(vessel) == 1:
        					if horizontalLine*3  < verticalLine:
        						tmpx = int(float(result[0].get('x')))
        						if tmpx == totalminX:
        							result[0].set('corner',str(connerCount))
        							connerCount+=1
        				elif int(float(result[0].get('x'))) == int(float(result2[0].get('x'))) :
        					result[0].set('corner',str(connerCount))
        					connerCount+=1
        		doc.write(f, encoding="utf-8", xml_declaration=True)
        	else:
        		pass

    def InstallTool(self) :
        #installTool(AttributeTool.AttributeTool())
        pass

    def UnTool(self) :
        uninstallTool(AttributeTool.AttributeTool())

    def pairing(self) :

        curPath = os.getcwd()

        path = curPath.split('/')

        #혹시 경로에 공백이 존재할 경우
        for i in range(len(path)) :
            path[i] = path[i].replace(" ","\ ")
        curPath = curPath.replace(' ','\ ')

        #자바 실행
        curPath = os.path.dirname(os.path.abspath(__file__))

        for i in range(len(path)) :
            path[i] = path[i].replace(" ","\ ")
        curPath = curPath.replace(' ','\ ')

        os.system("java -jar "+curPath+"/LetterPairing.jar")

    def point_rotator(self, path):
        point_rotator.point_rotator(path, 1)
        point_rotator.point_rotator(path, 2)
        point_rotator.point_rotator(path, 3)

    def combineufo(self):
        ufo_name = 'Y740_2350'

        path_w = GetFolder('Choose a working directory')
        path_a = path_w + '/' + ufo_name + '_A.ufo'
        path_b = path_w + '/' + ufo_name + '_B.ufo'
        path_c = path_w + '/' + ufo_name + '_C.ufo'
        path_ufo = path_w + '/' + ufo_name + '.ufo'

        path_t = make_dir.make_dir(path_w, path_a, path_b, path_c)
        self.point_rotator(path_t)
        path_g = base_maker.base_maker(path_t)
        circle2_7.circle2_7(path_g)
        unfill_vowel.unfill_vowel(path_g)
        makeufobyrobofab.makeufo(path_g, path_a, path_ufo)

        reverse.reverse(path_ufo)   #ufo 내의 속성들을 name 으로 모아서 보여주기 위한 함수

        os.system('rm -r '+path_t)

    def make_mf(self):
        # destPath = GetFolder("pick a folder to include result files")
        destPath = GetFolder("Choose a folder to include result files")
        name_attr.name_attr() 
        mf_maker.ufo2mf(destPath)



Start()
