from reportlab.platypus import Flowable
from reportlab.graphics.charts.axes import Color
from common import canv_utils


class WeekAxis(Flowable):
    def __init__(self, canvFig, Grid=False, width=500, height=250):
        Flowable.__init__(self)
        self.Stats = {}
        self.CanvFig = canvFig
        self.Grid = Grid
        self.width = width
        self.height = height
        self.aw = 0
        self.ah = 0
        self.InitStats()

    def InitStats(self):
        self.Stats['xAxis'] = {}
        self.Stats['yAxis'] = {}
        self.Stats = self.CanvFig.dp.Stats
        self.xAxisDataFormator = self.CanvFig.dp.xAxisDataFormator
        self.yAxisDataFormator = self.CanvFig.dp.yAxisDataFormator

    def wrap(self, availWidth, availHeight):
        # print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height + 50

    def DrawWeeks(self, grid=True):
        weeks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for wk in weeks:
            canv_utils.WriteText(self.canv, wk, 0, 0)

    def DrawHGrid(self, grid=True):
        rows = self.Stats['yAxis']['major']
        minV = self.Stats['yAxis']['min']
        maxV = self.Stats['yAxis']['max']

        w, h = canv_utils.GetFontWidhHeight('12', self.canv._fontname, self.canv._fontsize)
        gridW = 0
        if grid: gridW = self.width

        for rowV in rows:
            posY = canv_utils.Point2Pixel(minV, maxV, 0, self.height, rowV)
            pos = [-h*3, posY]
            self.canv.line(-(h/3), pos[1], gridW, pos[1])

            strLabel = str(rowV)
            if self.yAxisDataFormator is not None:
                strLabel = self.yAxisDataFormator(rowV)
            self.canv.drawString(pos[0], pos[1] - (h/3), strLabel)

    def convert_xAxis_pixels(self, data):
        xMin = self.Stats['xAxis']['min']
        xMax = self.Stats['xAxis']['max']
        newData = []
        for i in range(len(data)):
            newData.append(canv_utils.Point2Pixel(xMin, xMax, 0, self.width, data[i]))
        return newData

    def convert_yAxis_pixels(self, data):
        xMin = self.Stats['yAxis']['min']
        xMax = self.Stats['yAxis']['max']

        newData = []
        for i in range(len(data)):
            newData.append(canv_utils.Point2Pixel(xMin, xMax, 0, self.height, data[i]))

        return newData

    def draw(self):

        canv_utils.DrawRectangle(self.canv, (0, 0), (self.width, self.height))
        self.DrawWeeks()
