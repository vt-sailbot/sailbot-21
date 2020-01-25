from src.tracking.kalman_filter import KalmanFilter
from src.tracking.classification_types import ObjectType

from src.utils.coord_conv import cartesian_to_polar, polar_to_cartesian
from src.utils.time_in_millis import time_in_millis

import numpy as np

class Object():

    def __init__(self, bearing, rng, lastSeen=time_in_millis(), rngRate=0, bearingRate=0, objectType=ObjectType.NONE):
        """ Initalizes object that tracks a detection in map

        bearing -- Relative angle of object (in deg)
        rng -- Range of object from boat (in m)
        lastSeen -- Time object was last seen (in ms)
        objectType -- Classification of object (None for unclassified object)
        rangeRate -- Velocity of object in radial direction (in m/s, + for object moving outwards)
        bearingRate -- Velocity of object in angular direction (in deg/s, + for object moving CCW)
        """
        self.bearing = bearing
        self.rng = rng
        self.lastSeen = lastSeen
        self.objectType = objectType
        self.rngRate = rngRate
        self.bearingRate = bearingRate
        self.histLength = 10
        self.updateHist = [None] * self.histLength        # list to store if track updates for past <histLength> update cycles

        self.prevRng = 0
        self.prevBearing = 0

        self.kalman = KalmanFilter(np.array([self.rng, self.bearing]), np.array([self.rngRate, self.bearingRate]))

    def update(self, rng, bearing, rngRate=None, bearingRate=None):
        """Updates object position and model based on new reading
        Inputs:
            rng -- range measured by sensors
            bearing -- bearing measured by sensors
            rngRate -- rate of change of range
            bearingRate -- rate of change of bearing
        """
        # rotate update history
        self.updateHist[1:self.histLength] = self.updateHist[0:self.histLength - 1]

        if (rng is None) and (bearing is None):
            self.updateHist[0] = 0                  # not updated
            return                                  # exit function

        self.updateHist[0] = 1                      # updated

        hist_score = self._calc_hist_score()

        if (rngRate is None) and (bearingRate is None):
            self.kalman.update([rng, bearing], [self.rngRate, self.bearingRate], hist_score)
        else:
            self.kalman.update([rng, bearing], [rngRate, bearingRate], hist_score)
        self._set_object_state()

        # update range and bearing rate for object
        self._find_object_rngRate()
        self._find_object_bearingRate()

        self.lastSeen = time_in_millis()
        self.prevRng = self.rng
        self.prevBearing = self.bearing

    def predict(self):
        """
        Predicts object position based on model
        Side Effects:
            Updates self.rng with predicted range
            Updates self.bearing with predicted bearing
        """
        self.kalman.predict()
        self._set_object_state()
        
    def _set_object_state(self):
        """
        Sets object state using kalman filter state (to be called after predict or update)
        Side Effects:
            self.rng -- Updated using kalman filter
            self.bearing -- Updated using kalman filter
            self.rngRate -- Updated using kalman filter
            self.bearingRate -- Updated using kalman filter
        """
        self.rng, self.bearing = (self.kalman.state[0], self.kalman.state[1])
        self.rngRate, self.bearingRate = (self.kalman.state[2], self.kalman.state[3])

    def _find_object_rngRate(self):
        """
        Finds and sets object range rate
        Side Effects:
            self.rngRate -- Updates range rate using new measurement
        """
        self.rngRate = 1000 * (self.rng - self.prevRng) / (time_in_millis() - self.lastSeen)

    def _find_object_bearingRate(self):
        """
        Finds and sets object bearing rate
        Side Effects:
            self.bearingRate -- Updates bearing rate using new measurement
        """
        self.bearingRate = 1000 * (self.bearing - self.prevBearing) / (time_in_millis() - self.lastSeen)

    def _calc_hist_score(self):
        """
        Calculates history score (/ obj certainty) for use by kalman filter update
        Returns:
            hist_score -- object certainty score (scaled from ~0.75 - 5)
        """
        return (5. - sum(filter(None, self.updateHist)) / 2.3529)
