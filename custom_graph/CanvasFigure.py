from reportlab.platypus import Flowable

from custom_graph import generator
from custom_graph import canv_utils as canv_utils
from custom_graph.BPGraph import BPGraph

class CanvasFigure(Flowable):
    def __init__(self, dataX, dataY, width=600, height=500):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.dataX = dataX
        self.dataY = dataY
        self.Padding = {"left": 50, "right": 40, "top": 10, "bottom": 50}
        self.Init()

    def Init(self):
        self.pX = self.Padding['left']
        self.pY = self.Padding['bottom']
        self.pHeight = self.height - (self.Padding['top'] + self.Padding['bottom'])
        self.pWidth = self.width - (self.Padding['left'] + self.Padding['right'])


    def wrap(self, availWidth, availHeight):
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height


    def setXlabel(self, txt):
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.saveState()
        self.canv.translate((self.width/2) + (w/2), max(0, abs(h-self.Padding['bottom'])*0.3))
        self.canv.rotate(0)
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()

    def setYLabel(self, txt):
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.saveState()
        self.canv.translate(max(0, abs(h-self.Padding['left'])*0.5), (self.pHeight/2) + (w/2)+self.Padding['bottom'])
        self.canv.rotate(90)
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()

    def draw(self):
        """
        Draw the shape, text, etc
        """

        self.setXlabel("Time")
        self.setYLabel("Blood Pressure")
        canv_utils.DrawRectangle(self.canv, (0, 0), (self.width, self.height))
        canv_utils.DrawRectangle(self.canv, (self.pX, self.pY), (self.pWidth, self.pHeight), color=(0.0, 0.0, 0.0, 0.1), fill=1)
        data = generator.GenerateData()
        flowable = BPGraph(data, width=self.pWidth, height=self.pHeight)
        canv_utils.DrawCustomFlowable(self.canv, flowable, (self.pX, self.pY), (self.aw, self.ah))
