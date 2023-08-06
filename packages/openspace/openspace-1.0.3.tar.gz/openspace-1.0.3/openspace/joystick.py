from PyQt5 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from openspace.propagators import ClohessyWiltshireModel
from openspace.math.linear_algebra import Vector
from openspace.math.time_conversions import SECONDS_IN_DAY, SECONDS_IN_MINUTE
import pkg_resources
import sys
import math
import time
from pynput import keyboard

SIM_TIME_SCALE = 144
REFRESH_RATE_MS = 10
DT = REFRESH_RATE_MS/1000*SIM_TIME_SCALE
TIME_ALLOWED = 86400
FUEL_ALLOWED = 100

class RelWindow(QtWidgets.QDialog):
    def __init__(self):

        self.thrust = 10
        self.mass = 4000
        self.dt = DT
        self.time_remaining = TIME_ALLOWED
        self.fuel_remaining = FUEL_ALLOWED
        self.acceleration = self.thrust/self.mass
        self.stop_game = False
        self.maneuver_x = []
        self.maneuver_y = []
        self.past_x = []
        self.past_y = []

        self.rel_state = ClohessyWiltshireModel(
            [0, -500000, 0, 0, 0, 0], 
            42164000
            )

        self.r, self.i, _ = self.rel_state.get_positions_over_interval(
            0, 
            SECONDS_IN_DAY, 
            SECONDS_IN_MINUTE*10, 
            scale=1000
            )

        self.up_acceleration = Vector([0,0,0])
        self.down_acceleration = Vector([0,0,0])
        self.right_acceleration = Vector([0,0,0])
        self.left_acceleration = Vector([0,0,0])
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()

        self.acceleration_vector = Vector([0,0,0])
        super(RelWindow, self).__init__()
        ui = pkg_resources.resource_filename(
            __name__, 
            "resources/ui_files/joystick.ui"
            )
        uic.loadUi(ui, self)
        self.rel_state_plot.addLegend()
        self.future_state = self.rel_state_plot.plot(
            [], 
            [], 
            pen = pg.mkPen(color="w"), 
            name = "Propagated State"
            )

        self.free_flight = self.rel_state_plot.plot(
            [], 
            [],
            pen=None,
            symbol="o",
            symbolPen=pg.mkPen(color='b'),
            symbolBrush=pg.mkBrush(color='b'),
            name = "Past Free-Flight",
            size=1
            )

        self.maneuvers = self.rel_state_plot.plot(
            [], 
            [],
            pen=None,
            symbol="o",
            symbolPen=pg.mkPen(color='r'),
            symbolBrush=pg.mkBrush(color='r'),
            name="Maneuvers",
            size=1
            )

        circle = pg.QtGui.QGraphicsEllipseItem(-2, -2, 4, 4)
        circle.setPen(pg.mkPen(color='g'))
        self.rel_state_plot.addItem(circle)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(REFRESH_RATE_MS)
        self.timer.start()
        self.timer.timeout.connect(self.update)

    def on_press(self, key):

        if key == keyboard.Key.shift:
            self.dt = DT*10

        if key == keyboard.Key.up:
            self.up_acceleration = Vector([1,0,0])
        
        if key == keyboard.Key.down:
            self.down_acceleration = Vector([-1,0,0])

        if key == keyboard.Key.left:
            self.left_acceleration = Vector([0,-1,0])

        if key == keyboard.Key.right:
            self.right_acceleration = Vector([0,1,0])

    def on_release(self, key):

        if key == keyboard.Key.shift:
            self.dt = DT

        if key == keyboard.Key.up:
            self.up_acceleration = Vector([0,0,0])
        
        if key == keyboard.Key.down:
            self.down_acceleration = Vector([0,0,0])

        if key == keyboard.Key.left:
            self.left_acceleration = Vector([0,0,0])

        if key == keyboard.Key.right:
            self.right_acceleration = Vector([0,0,0])

        if key == keyboard.Key.esc:
            self.stop_game = True

        

    def update(self):

        add_maneuver = False

        self.acceleration_vector = self.up_acceleration.plus(
            self.down_acceleration.plus(self.right_acceleration.plus(
                self.left_acceleration
            ))
        ).scale(self.acceleration)

        self.rel_state.apply_velocity_change(
            self.acceleration_vector.scale(self.dt)
            )


        if self.acceleration_vector.magnitude() < 1e-6:
            add_maneuver = False
            self.past_x.append(
                self.rel_state.init_state.scale(.001).get_element(0)
                )
            self.past_y.append(
                self.rel_state.init_state.scale(.001).get_element(1)
                )
        else:
            add_maneuver = True
            self.fuel_remaining-=self.acceleration_vector.scale(
                self.dt
                ).magnitude()
            self.maneuver_x.append(
                self.rel_state.init_state.scale(.001).get_element(0)
                )
            self.maneuver_y.append(
                self.rel_state.init_state.scale(.001).get_element(1)
                )

        self.rel_state = ClohessyWiltshireModel(
            self.rel_state.solve_next_state(self.dt), 
            42164000
            )

        if add_maneuver:
            self.maneuver_x.append(
                self.rel_state.init_state.scale(.001).get_element(0)
                )
            self.maneuver_y.append(
                self.rel_state.init_state.scale(.001).get_element(1)
                )
        else:
            self.past_x.append(
                self.rel_state.init_state.scale(.001).get_element(0)
                )
            self.past_y.append(
                self.rel_state.init_state.scale(.001).get_element(1)
                )

        self.r, self.i, _ = self.rel_state.get_positions_over_interval(
            0, 
            int(self.time_remaining), 
            SECONDS_IN_MINUTE*10, 
            scale=1000
            )
        _, max_range = self.rel_state.get_max_range_over_interval(
            0, 
            SECONDS_IN_DAY, 
            10*SECONDS_IN_MINUTE, 
            scale=.001
            )
        if self.fuel_remaining <= 0 or self.time_remaining <= 0:
            self.timer.timeout.disconnect()
            self.time_remaining = 0
            print("Better luck next time!")
        elif max_range < 2:
            self.timer.timeout.disconnect()
            print("Winner!")
        
        self.time_remaining-=self.dt
        self.time_lcd.display(self.time_remaining)
        self.fuel_lcd.display(self.fuel_remaining)
        self.future_state.setData(self.i, self.r)
        self.free_flight.setData(self.past_y, self.past_x)
        self.maneuvers.setData(self.maneuver_y, self.maneuver_x)
        
        

def run():
    app = QtWidgets.QApplication(sys.argv)
    main = RelWindow()
    main.show()
    sys.exit(app.exec_())