from math import acos, cos, sin, asin, atan2, sqrt, pi
from numpy.core.numeric import cross
from openspace.bodies import Earth
from openspace.math.constants import ZERO

from openspace.math.measurements import Angle, Epoch
from openspace.math.time_conversions import SECONDS_IN_DAY, time_to_decimal_day
from openspace.math.linear_algebra import \
    (
        Matrix,
        Vector, 
        get_first_axis_rotation_matrix, 
        get_second_axis_rotation_matrix, 
        get_third_axis_rotation_matrix
    )

from openspace.configs.formats import STANDARD_EPOCH_FMT

import numpy as np

def vector_to_coes(r, v):
    r_mag = r.magnitude()
    v_mag = v.magnitude()

    h = r.cross(v)
    h_mag = h.magnitude()

    p = h_mag**2/Earth().mu
    a = 1/((2/r_mag) - v_mag*(v_mag/Earth().mu))
    e_vec = r.scale(v_mag**2 - Earth().mu/r_mag).minus(v.scale(r.dot(v))).scale(1/Earth().mu)
    e = e_vec.magnitude()

    period = 2*pi*sqrt(a**3/Earth().mu)
    n = 2*pi/period
    i = acos(h.get_element(2)/h_mag)


    arg = ((p/r_mag)-1)/e
    if arg > 1:
        arg = 1
    elif arg < -1:
        arg = -1

    ta = acos(arg)


    if np.any(Vector([0,0,1]).cross(h)):
        node_vec = Vector([0,0,1]).cross(h).normalized()
        aop = acos(node_vec.dot(e_vec.normalized()))
        raan = acos(node_vec.get_element(0))
    else:
        aop = 0
        raan = 0

    return a, e, i, ta, aop, raan


def coes_to_vector(
                    sma, 
                    eccentricity, 
                    inclination, 
                    true_anomaly, 
                    arg_perigee,
                    raan
                    ):

    p = sma*(1-eccentricity**2)

    r = p/(1+eccentricity*cos(true_anomaly))
    position = Vector([r*cos(true_anomaly), r*sin(true_anomaly), 0])
    velocity = Vector([
        -sqrt(Earth().mu/p)*sin(true_anomaly),
        sqrt(Earth().mu/p)*(eccentricity+cos(true_anomaly)),
        0
    ])

    Ti = Matrix([
        [cos(raan), -sin(raan), 0],
        [sin(raan), cos(raan), 0],
        [0, 0, 1]
    ])
    Tj = Matrix([
        [1, 0, 0],
        [0, cos(inclination), -sin(inclination)],
        [0, sin(inclination), cos(inclination)]
    ])
    Tk = Matrix([
        [cos(arg_perigee), -sin(arg_perigee), 0],
        [sin(arg_perigee), cos(arg_perigee), 0],
        [0, 0, 1]
    ])

    position = Ti.multiply(Tj.multiply(Tk.multiply(position)))
    velocity = Ti.multiply(Tj.multiply(Tk.multiply(velocity)))

    return position, velocity

def spherical_to_cartesian(vec):
    r = vec.get_element(0)
    lat = vec.get_element(1)
    long = vec.get_element(2)
    x = r*cos(lat)*cos(long)
    y = r*cos(lat)*sin(long)
    z = r*sin(lat)
    return Vector([x, y, z])

def cartesian_to_spherical(vec):
    x = vec.get_element(0)
    y = vec.get_element(1)
    z = vec.get_element(2)
    r = vec.magnitude()
    lat = asin(z/r)
    long = atan2(y, x)

    return Vector([r, lat, long])

def geodetic_to_geocentric(h, lat, long, f, r):
    R = r*(1/sqrt(cos(lat)**2 + ((1-f)*sin(lat))**2))
    x = (R+h)*cos(lat)*cos(long)
    y = (R+h)*cos(lat)*sin(long)
    z = ((1-f)**2*R + h)*sin(lat)
    return Vector([x, y, z])

def get_rnp_matrix(utc_epoch, eop):

    w = get_first_axis_rotation_matrix(eop.y_pole).multiply(get_second_axis_rotation_matrix(eop.x_pole))

    gst_day = utc_epoch.to_gst_decimal_day(eop)

    print(gst_day)

def eci_to_hill(position0, velocity0, position1, velocity1):

    """Credit to Dave Dayton for the eci to hill frame function"""

    magrtgt = position0.magnitude()
    magrint = position1.magnitude()
    eci_rsw_matrix = Matrix(Matrix([
        position0.normalized(),
        position0.cross(velocity0).cross(position0).normalized(),
        position0.cross(velocity0).normalized()
    ]).reshape((3,3)))

    vtgtrsw = eci_rsw_matrix.multiply(velocity0)
    rintrsw = eci_rsw_matrix.multiply(position1)
    vintrsw = eci_rsw_matrix.multiply(velocity1)

    sinphiint = rintrsw.get_element(2)/magrint
    phiint = asin(sinphiint)
    cosphiint = cos(phiint)
    lambdaint = atan2(rintrsw.get_element(1), rintrsw.get_element(0))
    sinlambdaint = sin(lambdaint)
    coslambdaint = cos(lambdaint)
    lambdadottgt = vtgtrsw.get_element(1)/magrtgt

    rhill = Vector([magrint-magrtgt, lambdaint*magrtgt, phiint*magrtgt])

    rsw_sez_matrix = Matrix(Matrix([
        Vector([sinphiint*coslambdaint, sinphiint*sinlambdaint, -cosphiint]),
        Vector([-sinlambdaint, coslambdaint, 0]),
        Vector([cosphiint*coslambdaint, cosphiint*sinlambdaint, sinphiint])
    ]).reshape((3,3)))

    vintsez = rsw_sez_matrix.multiply(vintrsw)
    phidotint = -vintsez.get_element(0)/magrint
    lambdadotint = vintsez.get_element(1)/(magrint*cosphiint)

    vhill = Vector([
        vintsez.get_element(2)-vtgtrsw.get_element(0),
        magrtgt*(lambdadotint-lambdadottgt),
        magrtgt*phidotint
    ])

    return rhill, vhill
