from tkinter import *
from tkinter.ttk import *



class RangeSliderH(Frame):
    LINE_COLOR = "#476b6b"
    LINE_S_COLOR="#0a50ff"
    LINE_WIDTH = 3
    BAR_COLOR_INNER = "#5c8a8a"
    BAR_COLOR_OUTTER = "#c2d6d6"
    BAR_RADIUS = 10
    BAR_RADIUS_INNER = 5
    DIGIT_PRECISION = '.1f' # for showing in the canvas
    FONT_SIZE=16
    FONT_FAMILY='Times'
    IMAGE_ANCHOR_L=CENTER
    IMAGE_ANCHOR_R=CENTER
    def __init__(self, master, variables, Width = 400, Height = 80, min_val = 0, max_val = 1, padX=3,
                    image_anchorR=CENTER, image_anchorL=CENTER, imageL=None, imageR=None,
                    auto=True, line_width=3, bar_radius=10,
                    bar_color_inner='#5c8a8a', line_s_color="#0a50ff", bar_color_outer='#c2d6d6', line_color = '#476b6b', bgColor= '#ffffff',
                    show_value = True, digit_precision='.1f', valueSide='TOP', font_family='Times', font_size=16, suffix=""):
        RangeSliderH.LINE_COLOR=line_color
        RangeSliderH.LINE_WIDTH=line_width
        RangeSliderH.BAR_COLOR_INNER=bar_color_inner
        RangeSliderH.BAR_COLOR_OUTTER=bar_color_outer
        RangeSliderH.BAR_RADIUS=bar_radius
        RangeSliderH.BAR_RADIUS_INNER=bar_radius-5
        RangeSliderH.DIGIT_PRECISION=digit_precision
        RangeSliderH.FONT_SIZE=font_size
        RangeSliderH.FONT_FAMILY=font_family
        RangeSliderH.IMAGE_ANCHOR_L=image_anchorL
        RangeSliderH.IMAGE_ANCHOR_R=image_anchorR
        RangeSliderH.LINE_S_COLOR=line_s_color
        if auto:
            if imageL!=None or imageR!=None:
                raise Exception("Can't decide if to use auto shape or images!")
            else:
                critical1=max(max(len(str(min_val)+suffix),len(str(max_val)+suffix))*RangeSliderH.FONT_SIZE*1.33/4,RangeSliderH.BAR_RADIUS)
                critical2=2*(padX+RangeSliderH.BAR_RADIUS)
                critical3=2*(1.33*RangeSliderH.FONT_SIZE+RangeSliderH.BAR_RADIUS)
                if show_value and padX<critical1:
                    raise Exception("padX too small, value won't be visible completely, expected padX to be atleast "+ str(critical1+1)+"px.")
                if Width<critical2:
                    raise Exception("Dimensions incompatible, consider decreasing padX or bar_radius or consider increasing widget width, as per given configuration width should be atleast ."+str(critical2+1)+"px.")
                if Height<critical3:
                    raise Exception("Dimensions incompatible, consider decreasing bar_radius or consider increasing widget height, as per given configuration height should be atleast ."+str(critical3+1)+"px.")
                if RangeSliderH.BAR_RADIUS<=line_width:
                    raise Exception("bar_radius too small, should be atleast equal to line_width(default=10)")
                self.draw='auto'
        else:
            if imageL==None or imageR==None:
                raise Exception("Handle for one image missing.")
            else:
                critical1=imageL.height()+2*1.33*RangeSliderH.FONT_SIZE
                critical2=imageR.width()*2+2*padX
                critical3=max(len(str(min_val)+suffix),len(str(max_val)+suffix))*RangeSliderH.FONT_SIZE*1.33/4
                if imageL.height()==imageR.height() and imageL.width()==imageR.width():
                    if critical1<Height and critical2< Width:
                        if show_value and padX<critical3:
                            raise Exception("padX too small, value won't be visible completely, expected padX to be atleast "+str(critical3+1)+"px.")
                        self.draw='image'
                    else:
                        raise Exception("Image dimensions not suited with widget Height and width, as per given configuration height should be atleast "+str(critical1+1)+"px and width should be atleast "+str(critical2+1)+"px.")
                else:
                    raise Exception("Image dimensions incompatible, both handles should have same height and width respectively.")
        Frame.__init__(self, master, height = Height, width = Width)
        self.padx=padX
        self.ImageL=imageL
        self.ImageR=imageR
        self.master = master
        self.max_val = max_val
        self.min_val = min_val
        self.show_value = show_value
        self.valueSide=valueSide
        self.H = Height
        self.W = Width
        self.canv_H = self.H
        self.canv_W = self.W
        self.suffix=suffix
        self.variables = variables
        try:
            self.init_lis = [variables[0].get(), variables[1].get()]
        except Exception:
            self.init_lis = [min_val, max_val]
        if not show_value:
            self.slider_y = self.canv_H/2 # y pos of the slider
        else:
            if self.valueSide=='BOTTOM':
                if self.draw=='auto':
                    self.slider_y = RangeSliderH.BAR_RADIUS+2
                else:
                    self.slider_y = imageL.height()/2 + 2
            elif self.valueSide=='TOP':
                if self.draw=='auto':
                    self.slider_y = self.canv_H - RangeSliderH.BAR_RADIUS - 2
                else:
                    self.slider_y = self.canv_H - imageL.height()/2 - 2
            else:
                raise Exception("valueSide can either be TOP or BOTTOM.")
        if self.draw=='auto':
            self.slider_x = RangeSliderH.BAR_RADIUS+self.padx # x pos of the slider (left side)
        else:
            self.slider_x = self.ImageL.width()/2+self.padx

        self.bars = []
        self.selected_idx = None # current selection bar index
        for value in self.init_lis:
            pos = (value-min_val)/(max_val-min_val)
            ids = []
            bar = {"Pos":pos, "Ids":ids, "Value":value}
            self.bars.append(bar)


        self.canv = Canvas(self, height = self.canv_H, width = self.canv_W, bg=bgColor, bd=0 , highlightthickness=0, relief='ridge')
        self.canv.pack()
        self.canv.bind("<Motion>", self._mouseMotion)
        self.canv.bind("<B1-Motion>", self._moveBar)

        self.track = self.__addTrack(self.slider_x, self.slider_y, self.canv_W-self.slider_x, self.slider_y, self.bars[0]["Pos"], self.bars[1]["Pos"])
        tempIdx=0
        for bar in self.bars:
            bar["Ids"] = self.__addBar(bar["Pos"],tempIdx)
            tempIdx+=1

        self.__setValues()


    def getValues(self):
        values = [bar["Value"] for bar in self.bars]
        return values

    def __setValues(self):
        values=self.getValues()
        self.variables[0].set(values[0])
        self.variables[1].set(values[1])

    def getPos(self):
        poss = [bar["Pos"] for bar in self.bars]
        return poss

    def _mouseMotion(self, event):
        x = event.x; y = event.y
        selection = self.__checkSelection(x,y)
        if selection[0]:
            self.canv.config(cursor = "hand2")
            self.selected_idx = selection[1]
        else:
            self.canv.config(cursor = "")
            self.selected_idx = None

    def _moveBar(self, event):
        x = event.x; y = event.y
        if self.selected_idx == None:
            return False
        pos = self.__calcPos(x)
        idx = self.selected_idx
        self.__moveBar(idx,pos)

    def __addTrack(self, startx, starty, endx, endy, posL, posR):
        rangeOutL = self.canv.create_line(startx, starty, startx+posL*(endx-startx), endy, fill = RangeSliderH.LINE_COLOR, width = RangeSliderH.LINE_WIDTH)
        rangeS = self.canv.create_line(startx+posL*(endx-startx), starty, endx-(1-posR)*(endx-startx), endy, fill = RangeSliderH.LINE_S_COLOR, width = RangeSliderH.LINE_WIDTH)
        rangeOutR = self.canv.create_line(endx-(1-posR)*(endx-startx), starty, endx, endy, fill = RangeSliderH.LINE_COLOR, width = RangeSliderH.LINE_WIDTH)
        return [rangeOutL, rangeS, rangeOutR]

    def __addTrackL(self, startx, starty, endx, endy, posL, posR):
        rangeOutL = self.canv.create_line(startx, starty, startx+posL*(endx-startx), endy, fill = RangeSliderH.LINE_COLOR, width = RangeSliderH.LINE_WIDTH)
        rangeS = self.canv.create_line(startx+posL*(endx-startx), starty, endx-(1-posR)*(endx-startx), endy, fill = RangeSliderH.LINE_S_COLOR, width = RangeSliderH.LINE_WIDTH)
        # rangeOutR = self.canv.create_line(endx-(1-posR)*(endx-startx), starty, endx, endy, fill = RangeSliderH.LINE_COLOR, width = RangeSliderH.LINE_WIDTH)
        return [rangeOutL, rangeS]

    def __addTrackR(self, startx, starty, endx, endy, posL, posR):
        # rangeOutL = self.canv.create_line(startx, starty, startx+posL*(endx-startx), endy, fill = RangeSliderH.LINE_COLOR, width = RangeSliderH.LINE_WIDTH)
        rangeS = self.canv.create_line(startx+posL*(endx-startx), starty, endx-(1-posR)*(endx-startx), endy, fill = RangeSliderH.LINE_S_COLOR, width = RangeSliderH.LINE_WIDTH)
        rangeOutR = self.canv.create_line(endx-(1-posR)*(endx-startx), starty, endx, endy, fill = RangeSliderH.LINE_COLOR, width = RangeSliderH.LINE_WIDTH)
        return [rangeS, rangeOutR]

    def __addBar(self, pos, tempIdx=None):
        """@ pos: position of the bar, ranged from (0,1)"""
        if pos <0 or pos >1:
            raise Exception("Pos error - Pos: "+str(pos))
        if self.draw=='auto':
            R = RangeSliderH.BAR_RADIUS
            r = RangeSliderH.BAR_RADIUS_INNER
            L = self.canv_W - 2*self.slider_x
            y = self.slider_y
            x = self.slider_x+pos*L
            id_outer = self.canv.create_oval(x-R,y-R,x+R,y+R, fill = RangeSliderH.BAR_COLOR_OUTTER, width = 2, outline = "")
            id_inner = self.canv.create_oval(x-r,y-r,x+r,y+r, fill = RangeSliderH.BAR_COLOR_INNER, outline = "")
            if self.show_value:
                if self.valueSide=='TOP':
                    y_value = y-RangeSliderH.BAR_RADIUS-RangeSliderH.FONT_SIZE/2
                    value = pos*(self.max_val - self.min_val)+self.min_val
                    id_value = self.canv.create_text(x,y_value,anchor=S, text = format(value, RangeSliderH.DIGIT_PRECISION)+self.suffix,font=(RangeSliderH.FONT_FAMILY,RangeSliderH.FONT_SIZE))
                elif self.valueSide=='BOTTOM':
                    y_value = y+RangeSliderH.BAR_RADIUS+RangeSliderH.FONT_SIZE/2
                    value = pos*(self.max_val - self.min_val)+self.min_val
                    id_value = self.canv.create_text(x,y_value,anchor=N, text = format(value, RangeSliderH.DIGIT_PRECISION)+self.suffix,font=(RangeSliderH.FONT_FAMILY,RangeSliderH.FONT_SIZE))
                else:
                    raise Exception("valueSide can either be TOP or BOTTOM")
                return [id_outer, id_inner, id_value]
            else:
                return [id_outer, id_inner]
        elif self.draw=='image':
            L=self.canv_W - 2*self.slider_x
            y=self.slider_y
            x=self.slider_x+pos*L
            if tempIdx==0:
                imageH=self.canv.create_image(x,y,anchor=RangeSliderH.IMAGE_ANCHOR_L,image=self.ImageL)
            elif tempIdx==1:
                imageH=self.canv.create_image(x,y,anchor=RangeSliderH.IMAGE_ANCHOR_R,image=self.ImageR)
            if self.show_value:
                if self.valueSide=='TOP':
                    y_value = y-self.ImageL.height()/2-RangeSliderH.FONT_SIZE/2
                    value = pos*(self.max_val - self.min_val)+self.min_val
                    id_value = self.canv.create_text(x,y_value,anchor=S, text = format(value, RangeSliderH.DIGIT_PRECISION)+self.suffix,font=(RangeSliderH.FONT_FAMILY,RangeSliderH.FONT_SIZE))
                elif self.valueSide=='BOTTOM':
                    y_value = y+self.ImageL.height()/2+RangeSliderH.FONT_SIZE/2
                    value = pos*(self.max_val - self.min_val)+self.min_val
                    id_value = self.canv.create_text(x,y_value,anchor=N, text = format(value, RangeSliderH.DIGIT_PRECISION)+self.suffix,font=(RangeSliderH.FONT_FAMILY,RangeSliderH.FONT_SIZE))
                else:
                    raise Exception("valueSide can either be TOP or BOTTOM")
                return [imageH, id_value]
            else:
                return [imageH]


    def __moveBar(self, idx, pos):
        positions=self.getPos()
        current_pos=self.bars[idx]["Pos"]
        for i in range(0,2):
            ids=self.bars[i]["Ids"]
            for id in ids:
                self.canv.delete(id)
        for trackComponentsId in self.track[idx:idx+2]:
            self.canv.delete(trackComponentsId)
        if idx==0:
            otherIdx=1
            otherPos=positions[1]
            if pos<=otherPos:
                pos=pos
            else:
                pos=current_pos
            self.track[0:2] = self.__addTrackL(self.slider_x, self.slider_y, self.canv_W-self.slider_x, self.slider_y, pos, otherPos)
        else:
            otherIdx=0
            otherPos=positions[0]
            if pos>=otherPos:
                pos=pos
            else:
                pos=current_pos
            self.track[1:3] = self.__addTrackR(self.slider_x, self.slider_y, self.canv_W-self.slider_x, self.slider_y, otherPos, pos)
        
        self.bars[idx]["Ids"] = self.__addBar(pos, idx)
        self.bars[idx]["Pos"] = pos
        self.bars[idx]["Value"] = pos*(self.max_val - self.min_val)+self.min_val

        self.bars[otherIdx]["Ids"] = self.__addBar(otherPos, otherIdx)
        self.bars[otherIdx]["Pos"] = otherPos
        self.bars[otherIdx]["Value"] = otherPos*(self.max_val - self.min_val)+self.min_val

        self.__setValues()

    def __calcPos(self, x):
        """calculate position from x coordinate"""
        pos = (x - self.slider_x)/(self.canv_W-2*self.slider_x)
        if pos<0:
            return 0
        elif pos>1:
            return 1
        else:
            return pos

    def __getValue(self, idx):
        """#######Not used function#####"""
        bar = self.bars[idx]
        ids = bar["Ids"]
        x = self.canv.coords(ids[0])[0] + RangeSliderH.BAR_RADIUS
        pos = self.__calcPos(x)
        return pos*(self.max_val - self.min_val)+self.min_val

    def __checkSelection(self, x, y):
        """
        To check if the position is inside the bounding rectangle of a Bar
        Return [True, bar_index] or [False, None]
        """
        for idx in range(len(self.bars)):
            id = self.bars[idx]["Ids"][0]
            bbox = self.canv.bbox(id)
            if bbox[0] < x and bbox[2] > x and bbox[1] < y and bbox[3] > y:
                return [True, idx]
        return [False, None]


class RangeSliderV(Frame):
    LINE_COLOR = "#476b6b"
    LINE_S_COLOR="#0a50ff"
    LINE_WIDTH = 3
    BAR_COLOR_INNER = "#5c8a8a"
    BAR_COLOR_OUTTER = "#c2d6d6"
    BAR_RADIUS = 10
    BAR_RADIUS_INNER = 5
    DIGIT_PRECISION = '.1f' # for showing in the canvas
    FONT_SIZE=16
    FONT_FAMILY='Times'
    IMAGE_ANCHOR_L=CENTER
    IMAGE_ANCHOR_U=CENTER
    def __init__(self, master, variables, Width = 80, Height = 400, min_val = 0, max_val = 1, padY=3,
                    image_anchorU=CENTER, image_anchorL=CENTER, imageL=None, imageU=None,
                    auto=True, line_width=3, bar_radius=10,
                    bar_color_inner='#5c8a8a', line_s_color="#0a50ff", bar_color_outer='#c2d6d6', line_color = '#476b6b', bgColor='#ffffff',
                    show_value = True, digit_precision='.1f', valueSide='LEFT', font_family='Times', font_size=16, suffix=""):
        RangeSliderV.LINE_COLOR=line_color
        RangeSliderV.LINE_WIDTH=line_width
        RangeSliderV.BAR_COLOR_INNER=bar_color_inner
        RangeSliderV.BAR_COLOR_OUTTER=bar_color_outer
        RangeSliderV.BAR_RADIUS=bar_radius
        RangeSliderV.BAR_RADIUS_INNER=bar_radius-5
        RangeSliderV.DIGIT_PRECISION=digit_precision
        RangeSliderV.FONT_SIZE=font_size
        RangeSliderV.FONT_FAMILY=font_family
        RangeSliderV.IMAGE_ANCHOR_L=image_anchorL
        RangeSliderV.IMAGE_ANCHOR_U=image_anchorU
        RangeSliderV.LINE_S_COLOR=line_s_color
        if auto:
            if imageL!=None or imageU!=None:
                raise Exception("Can't decide if to use auto shape or images!")
            else:
                critical1=max(RangeSliderV.BAR_RADIUS, RangeSliderV.FONT_SIZE*1.33/2)
                critical2=2*(RangeSliderV.BAR_RADIUS+max(len(str(min_val)),len(str(max_val)))*RangeSliderV.FONT_SIZE/1.2)
                critical3=2*(padY+RangeSliderV.BAR_RADIUS)
                if show_value and padY<critical1:
                    raise Exception("padY too small, handle won't be visible completely, as per given condition padY should be atleast "+str(critical1+1)+"px.")
                if Width<critical2:
                    raise Exception("Dimensions incompatible, consider decreasing bar_radius or FONT_SIZE or consider increasing widget width, as per given conditios width should be atleast "+str(critical2+1)+"px.")
                if Height<critical3:
                    raise Exception("Dimensions incompatible, consider decreasing bar_radius or consider increasing widget height, as per given conditios height should be atleast "+str(critical3+1)+"px.")
                if RangeSliderV.BAR_RADIUS<=line_width:
                    raise Exception("bar_radius too small, should be minimum equal to line_width(default=3).")
                self.draw='auto'
        else:
            if imageL==None or imageU==None:
                raise Exception("Handle for one image missing.")
            else:
                critical1=(imageL.height()+padY)*2
                critical2=imageL.width()+max(len(str(min_val)),len(str(max_val)))*RangeSliderV.FONT_SIZE/1.2
                critical3=max(imageU.height()/2, RangeSliderV.FONT_SIZE*1.33/2)
                if imageL.height()==imageU.height() and imageL.width()==imageU.width():
                    if critical1<Height and critical2< Width:
                        if show_value and padY<critical3:
                            raise Exception("padY too small, value won't be visible completely, padY mimumum expected is "+str(critical3)+"px.")
                        self.draw='image'
                    else:
                        raise Exception("Image dimensions not suited with widget Height and width, minimum height expected is "+str(critical1)+"px and minimum width expected is "+str(critical2)+"px.")
                else:
                    raise Exception("Image dimensions incompatible, width and height of both handles should be same respectively.")
        Frame.__init__(self, master, height = Height, width = Width)
        self.pady=padY
        self.ImageL=imageL
        self.ImageU=imageU
        self.master = master
        self.max_val = max_val
        self.min_val = min_val
        self.show_value = show_value
        self.valueSide=valueSide
        self.H = Height
        self.W = Width
        self.canv_H = self.H
        self.canv_W = self.W
        self.suffix=suffix
        self.variables = variables
        try:
            self.init_lis = [variables[0].get(), variables[1].get()]
        except Exception:
            self.init_lis = [min_val, max_val]
        if not show_value:
            self.slider_x = self.canv_W/2 # y pos of the slider
        else:
            if self.valueSide=='LEFT':
                if self.draw=='auto':
                    self.slider_x = self.canv_W-RangeSliderV.BAR_RADIUS-2
                elif self.draw=='image':
                    self.slider_x = self.canv_W-self.ImageL.width()/2-2
            elif self.valueSide=='RIGHT':
                if self.draw=='auto':
                    self.slider_x = RangeSliderV.BAR_RADIUS+2
                else:
                    self.slider_x = self.ImageL.width()/2+2
            else:
                raise Exception("valueSide can either be LEFT or RIGHT")
        self.slider_y=self.pady

        self.bars = []
        self.selected_idx = None # current selection bar index
        for value in self.init_lis:
            pos = (value-min_val)/(max_val-min_val)
            ids = []
            bar = {"Pos":pos, "Ids":ids, "Value":value}
            self.bars.append(bar)


        self.canv = Canvas(self, height = self.canv_H, width = self.canv_W, bg=bgColor ,bd=0, highlightthickness=0, relief='ridge')
        self.canv.pack()
        self.canv.bind("<Motion>", self._mouseMotion)
        self.canv.bind("<B1-Motion>", self._moveBar)
        self.track = self.__addTrack(self.slider_x, self.slider_y, self.slider_x, self.canv_H-self.slider_y, self.bars[0]["Pos"], self.bars[1]["Pos"])
        tempIdx=0
        for bar in self.bars:
            bar["Ids"] = self.__addBar(bar["Pos"],tempIdx)
            tempIdx+=1

        self.__setValues()


    def getValues(self):
        values = [bar["Value"] for bar in self.bars]
        return values

    def __setValues(self):
        values=self.getValues()
        self.variables[0].set(values[0])
        self.variables[1].set(values[1])

    def getPos(self):
        poss = [bar["Pos"] for bar in self.bars]
        return poss

    def _mouseMotion(self, event):
        x = event.x; y = event.y
        selection = self.__checkSelection(x,y)
        if selection[0]:
            self.canv.config(cursor = "hand2")
            self.selected_idx = selection[1]
        else:
            self.canv.config(cursor = "")
            self.selected_idx = None

    def _moveBar(self, event):
        x = event.x; y = event.y
        if self.selected_idx == None:
            return False
        pos = self.__calcPos(y)
        idx = self.selected_idx
        self.__moveBar(idx,pos)

    def __addTrack(self, startx, starty, endx, endy, posL, posU):
        rangeOutL = self.canv.create_line(startx, starty+(1-posL)*(endy-starty), startx, endy, fill = RangeSliderV.LINE_COLOR, width = RangeSliderV.LINE_WIDTH)
        rangeS = self.canv.create_line(startx, starty+(1-posU)*(endy-starty), startx, starty+(1-posL)*(endy-starty), fill = RangeSliderV.LINE_S_COLOR, width = RangeSliderV.LINE_WIDTH)
        rangeOutU = self.canv.create_line(startx, starty, endx, starty+(1-posU)*(endy-starty), fill = RangeSliderV.LINE_COLOR, width = RangeSliderV.LINE_WIDTH)
        return [rangeOutL, rangeS, rangeOutU]

    def __addTrackL(self, startx, starty, endx, endy, posL, posU):
        rangeOutL = self.canv.create_line(startx, starty+(1-posL)*(endy-starty), startx, endy, fill = RangeSliderV.LINE_COLOR, width = RangeSliderV.LINE_WIDTH)
        rangeS = self.canv.create_line(startx, starty+(1-posU)*(endy-starty), startx, starty+(1-posL)*(endy-starty), fill = RangeSliderV.LINE_S_COLOR, width = RangeSliderV.LINE_WIDTH)
        # rangeOutU = self.canv.create_line(startx, starty, endx, starty+(1-posU)*(endy-starty), fill = RangeSliderV.LINE_COLOR, width = RangeSliderV.LINE_WIDTH)
        return [rangeOutL, rangeS]

    def __addTrackR(self, startx, starty, endx, endy, posL, posU):
        # rangeOutL = self.canv.create_line(startx, starty+(1-posL)*(endy-starty), startx, endy, fill = RangeSliderV.LINE_COLOR, width = RangeSliderV.LINE_WIDTH)
        rangeS = self.canv.create_line(startx, starty+(1-posU)*(endy-starty), startx, starty+(1-posL)*(endy-starty), fill = RangeSliderV.LINE_S_COLOR, width = RangeSliderV.LINE_WIDTH)
        rangeOutU = self.canv.create_line(startx, starty, endx, starty+(1-posU)*(endy-starty), fill = RangeSliderV.LINE_COLOR, width = RangeSliderV.LINE_WIDTH)
        return [rangeS, rangeOutU]

    def __addBar(self, pos, tempIdx=None):
        """@ pos: position of the bar, ranged from (0,1)"""
        if pos <0 or pos >1:
            raise Exception("Pos error - Pos: "+str(pos))
        if self.draw=='auto':
            R = RangeSliderV.BAR_RADIUS
            r = RangeSliderV.BAR_RADIUS_INNER
            L = self.canv_H - 2*self.slider_y
            y = self.slider_y+(1-pos)*L
            x = self.slider_x
            id_outer = self.canv.create_oval(x-R,y-R,x+R,y+R, fill = RangeSliderV.BAR_COLOR_OUTTER, width = 2, outline = "")
            id_inner = self.canv.create_oval(x-r,y-r,x+r,y+r, fill = RangeSliderV.BAR_COLOR_INNER, outline = "")
            if self.show_value:
                if self.valueSide=='LEFT':
                    x_value = x-RangeSliderV.BAR_RADIUS-RangeSliderV.FONT_SIZE/2
                    value = pos*(self.max_val - self.min_val)+self.min_val
                    id_value = self.canv.create_text(x_value,y,anchor=E, text = format(value, RangeSliderV.DIGIT_PRECISION)+self.suffix,font=(RangeSliderV.FONT_FAMILY,RangeSliderV.FONT_SIZE))
                elif self.valueSide=='RIGHT':
                    x_value = x+RangeSliderV.BAR_RADIUS+RangeSliderV.FONT_SIZE/2
                    value = pos*(self.max_val - self.min_val)+self.min_val
                    id_value = self.canv.create_text(x_value,y,anchor=W, text = format(value, RangeSliderV.DIGIT_PRECISION)+self.suffix,font=(RangeSliderV.FONT_FAMILY,RangeSliderV.FONT_SIZE))
                else:
                    raise Exception("valueSide can either be LEFT or RIGHT.")
                return [id_outer, id_inner, id_value]
            else:
                return [id_outer, id_inner]
        elif self.draw=='image':
            L=self.canv_H - 2*self.slider_y
            y=self.slider_y+(1-pos)*L
            x=self.slider_x
            if tempIdx==0:
                imageH=self.canv.create_image(x,y,anchor=RangeSliderV.IMAGE_ANCHOR_L,image=self.ImageL)
            elif tempIdx==1:
                imageH=self.canv.create_image(x,y,anchor=RangeSliderV.IMAGE_ANCHOR_U,image=self.ImageU)
            if self.show_value:
                if self.valueSide=='LEFT':
                    x_value = x-self.ImageL.width()/2-RangeSliderV.FONT_SIZE/2
                    value = pos*(self.max_val - self.min_val)+self.min_val
                    id_value = self.canv.create_text(x_value,y, anchor=E, text = format(value, RangeSliderV.DIGIT_PRECISION)+self.suffix,font=(RangeSliderV.FONT_FAMILY,RangeSliderV.FONT_SIZE))
                elif self.valueSide=='RIGHT':
                    x_value = x+self.ImageL.width()/2+RangeSliderV.FONT_SIZE/2
                    value = pos*(self.max_val - self.min_val)+self.min_val
                    id_value = self.canv.create_text(x_value,y, anchor=W, text = format(value, RangeSliderV.DIGIT_PRECISION)+self.suffix,font=(RangeSliderV.FONT_FAMILY,RangeSliderV.FONT_SIZE))
                else:
                    raise Exception("valueSide can either be LEFT or RIGHT")  
                return [imageH, id_value]
            else:
                return [imageH]


    def __moveBar(self, idx, pos):
        positions=self.getPos()
        current_pos=self.bars[idx]["Pos"]
        for i in range(0,2):
            ids=self.bars[i]["Ids"]
            for id in ids:
                self.canv.delete(id)
        for trackComponentsId in self.track[idx:idx+2]:
            self.canv.delete(trackComponentsId)
        if idx==0:
            otherIdx=1
            otherPos=positions[1]
            if pos<=otherPos:
                pos=pos
            else:
                pos=current_pos
            self.track[0:2] = self.__addTrackL(self.slider_x, self.slider_y, self.slider_x, self.canv_H-self.slider_y, pos, otherPos)
        else:
            otherIdx=0
            otherPos=positions[0]
            if pos>=otherPos:
                pos=pos
            else:
                pos=current_pos
            self.track[1:3] = self.__addTrackR(self.slider_x, self.slider_y, self.slider_x, self.canv_H-self.slider_y, otherPos, pos)
        
        self.bars[idx]["Ids"] = self.__addBar(pos, idx)
        self.bars[idx]["Pos"] = pos
        self.bars[idx]["Value"] = pos*(self.max_val - self.min_val)+self.min_val

        self.bars[otherIdx]["Ids"] = self.__addBar(otherPos, otherIdx)
        self.bars[otherIdx]["Pos"] = otherPos
        self.bars[otherIdx]["Value"] = otherPos*(self.max_val - self.min_val)+self.min_val

        self.__setValues()

    def __calcPos(self, y):
        """calculate position from x coordinate"""
        pos = (y - self.slider_y)/(self.canv_H-2*self.slider_y)
        pos = 1-pos
        if pos<0:
            return 0
        elif pos>1:
            return 1
        else:
            return pos

    def __checkSelection(self, x, y):
        """
        To check if the position is inside the bounding rectangle of a Bar
        Return [True, bar_index] or [False, None]
        """
        for idx in range(len(self.bars)):
            id = self.bars[idx]["Ids"][0]
            bbox = self.canv.bbox(id)
            if bbox[0] < x and bbox[2] > x and bbox[1] < y and bbox[3] > y:
                return [True, idx]
        return [False, None]
