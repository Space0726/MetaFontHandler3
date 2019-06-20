from mojo.events import BaseEventTool, installTool, EditingTool
from mojo.drawingTools import *
from mojo.roboFont import CurrentFont,CurrentGlyph
import math
from vanilla import *
from Attribute_handler import Attribute_handler
from defconAppKit.windows.baseWindow import BaseWindowController
import depend

class AttributeTool(BaseEventTool, BaseWindowController):

    def set_attr(self, point, name, value):
        removing_attr = None
        temp_list = point._get_labels()
        temp_set = set(temp_list)
        for each in temp_set:
            if each.startswith("'" + name + "'"):
                removing_attr = each
        if removing_attr != None:
            temp_set.remove(removing_attr)
        if value != 'REMOVE':
            temp_set.add("'" + name + "': '" + value  + "'")
        point._set_labels(temp_set)

    def get_attr(self,point, name):
        value = None
        
        try:
            temp_list = point._get_name().split(',')
        except AttributeError:
            return None
        temp_set = set(temp_list)
        
        for each in temp_set:
            if each.startswith("'" + name + "'"):
                value = each[each.strip().find(":") + 2:-1]
                return value
        return None


    def get_closest(self,clicked_point, glyph):
        shortest = 9999
        return_point = -1

        for contour in glyph.contours:
            for point in contour.points:
                x = clicked_point.x - point.x
                y = clicked_point.y - point.y
                distance = math.sqrt((x ** 2) + (y ** 2))

                if distance < shortest:
                    shortest = distance
                    return_point = point

        if math.sqrt(((return_point.x - clicked_point.x) ** 2) + (return_point.y - clicked_point.y) ** 2) < 20:
            return return_point

        else: return None


    def buttonCallback(self, sender):
        if self.radio == 0:
            self.set_attr(self.here, 'serif', '1')

        elif self.radio == 1:
            self.set_attr(self.here, 'round', '1')

        elif self.radio == 2:
            self.set_attr(self.selected[self.here], 'round', self.get_attr(self.here, 'penPair'))

        elif self.radio == 3:
            self.set_attr(self.selected[self.here], 'dependX', self.get_attr(self.here, 'penPair'))

        elif self.radio == 4:
            self.set_attr(self.selected[self.here], 'dependY', self.get_attr(self.here, 'penPair'))

        elif self.radio == 5:
            depend.dependAll(self.selected[self.here],self.here,'x')

        elif self.radio == 6:
            depend.dependAll(self.selected[self.here],self.here,'y')

    def delbuttonCallback(self, sender):
        if self.radio == 0:
            self.set_attr(self.here, "serif", "REMOVE")
        if self.radio == 1:
            self.set_attr(self.here, "round", "REMOVE")
        if self.radio == 2:
            self.set_attr(self.here, "round", "REMOVE")
        if self.radio == 3:
            self.set_attr(self.here, "dependX", "REMOVE")
        if self.radio == 4:
            self.set_attr(self.here, "dependY", "REMOVE")

    def radioGroupCallback(self, sender):
        self.radio = sender.get()


    def becomeActive(self):

        self.radio = -1
        self.shift_down = 0
        self.position = None
        self.hereOld = None
        self.positionOld = None
        self.serifs = []
        self.dependXs = []
        self.dependYs = []
        self.rounds = []
        #############################
        self.here = None
        #############################

        for contour in CurrentGlyph().contours:
            contour._set_selected(False)

        self.w = FloatingWindow((180, 380), "MetaFont Options" , closable=False)
        self.w.radioGroup = RadioGroup((20, 20, -20, 90), ["Serif","Round Type1","Round Type2","Depend X","Depend Y","Depend X ALL","Depend Y ALL"], callback=self.radioGroupCallback)
        self.w.button = Button((20, 120, -20, 20), "Confirm", callback=self.buttonCallback)

        self.w.myList = List((20, 160, -20, 180), [{"Attr": "X", "Value": ""}, {"Attr": "Y", "Value": ""}, {"Attr": "", "Value": ""}], columnDescriptions=[{"title": "Attr"}, {"title": "Value"}])

        self.w.delbutton = Button((20, 240, -20, 180), "Delete", callback=self.delbuttonCallback)

        self.setUpBaseWindowBehavior()
        self.w.open()

    def becomeInactive(self):
        self.windowCloseCallback(None)
        self.w.close()

    def mouseDown(self, point, clickCount):
        g = CurrentGlyph()
        last_selected = None
        self.selected = {}

        if self.shift_down == 1:
            self.shift_down = 2
        elif self.shift_down == 2:
            self.shift_down = 0
            self.hereOld = None
            self.positionOld = None

        self.position = point
        self.here = self.get_closest(point, g)

        if self.getModifiers()['shiftDown'] == 0:
            self.first_selected = self.here
            self.selected[self.here] = None

        if self.getModifiers()['shiftDown']:
            last_selected = self.here
            self.selected[self.here] = self.first_selected

        for contour in g.contours:
            contour._set_selected(False)

        self.here._set_selected(True)
        if not self.shiftDown:
            if len(self.w.myList) > 2:
                for x in range(len(self.w.myList) - 1, 1, -1):
                    del self.w.myList[x]

            self.w.myList[0]["Value"] = self.first_selected.x
            self.w.myList[1]["Value"] = self.first_selected.y
            attrs = []
            if self.get_attr(self.first_selected, "serif") != None:
                attrs.append({"Attr": "serif", "Value": self.get_attr(self.first_selected, "serif")})
            if self.get_attr(self.first_selected, "dependX") != None:
                attrs.append({"Attr": "dependX", "Value": self.get_attr(self.first_selected, "dependX")})
            if self.get_attr(self.first_selected, "dependY") != None:
                attrs.append({"Attr": "dependY", "Value": self.get_attr(self.first_selected, "dependY")})
            if self.get_attr(self.first_selected, "round") != None:
                attrs.append({"Attr": "round", "Value": self.get_attr(self.first_selected, "round")})


            for attr in attrs:
                self.w.myList.append(attr)

        if self.first_selected != None:
            self.first_selected._set_selected(True)

    def rightMouseDown(self, point, event):
        pass

    def mouseDragged(self, point, delta):
        pass

    def rightMouseDragged(self, point, delta):
        pass

    def mouseUp(self, point):
        pass

    def keyDown(self, event):
        # a dict of all modifiers, shift, command, alt, option
        pass

    def keyUp(self, event):
        pass

    def modifiersChanged(self):
        if self.getModifiers()['shiftDown']:
            self.shift_down = 1
            self.hereOld = self.here
            self.positionOld = self.position

    def drawBackground(self, scale):
        pass

    def draw(self, scale):

        size = 12
        x = 0
        y = 0
        fill(255, 0, 0, 1.0)
        fontSize(20)
        stroke(1,0,0)
        
        for contour in CurrentGlyph().contours:
            for point in contour.points :
                gap = 0
                x = point.x
                y = point.y

                if self.get_attr(point, "penPair") != None :
                    stroke(2,0,0)
                    fill(0,0,1,1.0)
                    fontSize(30)
                    text(self.get_attr(point, "penPair"), (x + 20, y - 20))
                    fill(255, 0, 0, 1.0)
                    stroke(1, 0, 0)

                if self.get_attr(point,"serif") != None :
                    text("S", (x + 20, y + 20))
                    rect(x - size*1, y - size*1, size*2, size*2)
                    gap = gap + 20

                if self.get_attr(point,"round") != None :
                    if gap != 0 :
                        text(", R", (x + 20 + gap, y + 20))
                    else :
                        text("R", (x + 20 + gap, y + 20))
                        rect(x - size*1, y - size*1, size*2, size*2)
                    gap = gap + 20

                if self.get_attr(point,"dependX") != None :
                    if gap != 0 :
                        text(", Dx", (x + 20 + gap, y + 20))
                    else :
                        text("Dx", (x + 20 + gap, y + 20))
                        rect(x - size*1, y - size*1, size*2, size*2)
                    gap = gap + 40

                if self.get_attr(point,"dependY") != None :
                    if gap != 0 :
                        text(", Dy", (x + 20 + gap, y + 20))
                    else :
                        text("Dy", (x + 20 + gap, y + 20))
                        rect(x - size*1, y - size*1, size*2, size*2)

        if self.position == None :
            return

        size = 12
        x = self.position.x - size
        y = self.position.y - size
        fill(0, 0, 180, 1.0)
        fontSize(30)
        text(str(int(self.position.x)) + ", " + str(int(self.position.y)), (x + 20, y + 20))
        stroke(1,0,0)
        rect(self.here.x - size*1, self.here.y - size*1, size*2, size*2)

        if self.hereOld != None:
            xx = self.positionOld.x - size
            yy = self.positionOld.y - size
            fill(0, 255, 255, 1.0)
            fontSize(30)
            text(str(int(self.positionOld.x)) + ", " + str(int(self.positionOld.y)), (xx+20, yy+20))
            stroke(1,0,0)

            rect(self.hereOld.x - size*1, self.hereOld.y - size*1, size*2, size*2)

    def getToolbarTip(self):
        pass

    def viewDidChangeGlyph(self):
        pass

    def preferencesChanged(self):
        pass

installTool(AttributeTool())
