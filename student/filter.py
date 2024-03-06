# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        self.dim_state = params.dim_state
        self.dt = params.dt
        self.q = params.q

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############
        dt = self.dt

        # State transformation matrix
        # Assuming that Pz does not change with rate (delta t * Vz)
        return np.matrix([
            [1, 0, 0, dt, 0, 0],
            [0, 1, 0, 0, dt, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]]
        )
        
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############
        q = self.q
        dt = self.dt

        tq = dt * q
        tq2 = (dt**2 * q) / 2
        tq3 = (dt**3 * q) / 3

        return np.matrix([
            [tq3, 0, 0, tq2, 0, 0],
            [0, tq3, 0, 0, tq2, 0],
            [0, 0, 0, 0, 0, 0],
            [tq2, 0, 0, tq, 0, 0],
            [0, tq2, 0, 0, tq, 0],
            [0, 0, 0, 0, 0, 0]
        ])
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############
        x = self.F() * track.x
        P = (self.F() * track.P * self.F().T) + self.Q()

        track.set_x(x)
        track.set_P(P)
        
        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############

        H = meas.sensor.get_H(track.x)
        S = self.S(track, meas, H)
        residual = self.gamma(track=track, meas=meas)
        
        K = track.P * H.T * np.linalg.inv(S)
        
        x = track.x + K * residual
        P = (np.matrix(np.eye(self.dim_state)) - K * H) * track.P

        track.set_x(x)
        track.set_P(P)
        
        ############
        # END student code
        ############ 
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############

        residual = meas.z - meas.sensor.get_hx(track.x)
        return residual
        
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############

        S = (H * track.P * H.T) + meas.R
        return S
        
        ############
        # END student code
        ############ 