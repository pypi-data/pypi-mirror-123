from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from openspace.propagators import ClohessyWiltshireModel
from openspace.math.linear_algebra import Vector
from openspace.math.time_conversions import SECONDS_IN_DAY, SECONDS_IN_MINUTE
import pkg_resources
import sys
import math

class SDAwindow(QtWidgets.QDialog):
    def __init__(self):

        super(SDAwindow, self).__init__()
        ui = pkg_resources.resource_filename(
            __name__, 
            "resources/ui_files/sda_demo.ui"
            )
        uic.loadUi(ui, self)

        self.ecf_plot.addLegend()
        self.ecf_plot.plot(
            [0], 
            [0], 
            pen=None,
            symbol="o",
            symbolPen=pg.mkPen(color='g'),
            symbolBrush=pg.mkBrush(color='g'),
            name="Ground Sensor Location"
            )
        self.ecf_plot.plot(
            [42164], 
            [0], 
            pen=None,
            symbol="o",
            symbolPen=pg.mkPen(color='w'),
            symbolBrush=pg.mkBrush(color='w'),
            name="RSO Location"
            )
        self.geo_pos = self.ecf_plot.plot(
            [42164], 
            [0],
            pen=None,
            symbol="o",
            symbolPen=pg.mkPen(color='b'),
            symbolBrush=pg.mkBrush(color='b'),
            name="GEO Sensor Location"
            )
        self.clos_plot.addLegend()
        self.ecf_plot.setAspectLocked()
        self.geo_clos = self.clos_plot.plot(
            [], 
            [], 
            pen = pg.mkPen(color="b"), 
            name = "GEO Range Error"
            )

        self.gnd_clos = self.clos_plot.plot(
            [], 
            [], 
            pen = pg.mkPen(color="g"), 
            name = "Ground Range Error"
            )

        self.update_clos()
        self.r_slider.valueChanged.connect(self.update_clos)
        self.i_slider.valueChanged.connect(self.update_clos)
        self.c_slider.valueChanged.connect(self.update_clos)
        self.pos_slider.valueChanged.connect(self.update_clos)

    def update_clos(self):
        rot_ang = math.radians(self.pos_slider.value())
        geo_sensor_pos = Vector([42164000, 0, 0]).rotate_about_z(rot_ang)
        geo_expected = Vector([42164000, 0, 0]).minus(geo_sensor_pos)
        self.geo_pos.setData(
            [geo_sensor_pos.get_element(0)/1000],
            [geo_sensor_pos.get_element(1)/1000]
            )
        ground_expected = Vector([36000000, 0, 0])

        vx = self.r_slider.value()/100
        vy = self.i_slider.value()/100
        vz = self.c_slider.value()/100

        self.r_label.setText("%.2f" % vx + " m/s")
        self.i_label.setText("%.2f" % vy + " m/s")
        self.c_label.setText("%.2f" % vz + " m/s")
        self.pos_label.setText(
            "%d" % self.pos_slider.value() + " deg from target"
            )
        tgt = ClohessyWiltshireModel([0, 0, 0, vx, vy, vz], 42164000)

        t, geo_clos, gnd_clos = tgt.get_clos_over_interval(
            0, 
            SECONDS_IN_DAY, 
            SECONDS_IN_MINUTE*10, 
            geo_expected, 
            ground_expected
            )
        self.geo_clos.setData(t, geo_clos)
        self.gnd_clos.setData(t, gnd_clos)


def run():
    app = QtWidgets.QApplication(sys.argv)
    main = SDAwindow()
    main.show()
    sys.exit(app.exec_())