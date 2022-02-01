"""
NRV-extracellular contexts
Authors: Florian Kolbl / Roland Giraud / Louis Regnacq / Thomas Couppey
(c) ETIS - University Cergy-Pontoise - CNRS
"""
import faulthandler
import numpy as np
from .materials import *
from .units import *
from .log_interface import rise_error, rise_warning, pass_info

import matplotlib.pyplot as plt

def is_recording_point(point):
    """
    Check if the specified object is a recording point
    """
    return isinstance(point, recording_point)

def is_recorder(rec):
    """
    Check if the specified object is a recorder
    """
    return isinstance(rec, recorder)

class recording_point():
    """
    Object equivalent to a point source electrode for extracellular potential recording only (No stimulation)
    """
    def __init__(self, x, y, z, ID=0, method='PSA'):
        """
        Instantiation of a recording point.

        Parameters
        ----------
        x       : float
            x position of the recording point, in um
        y       : float
            y position of the recording point, in um
        z       : float
            z position of the recording point, in um
        ID      : int
            electrode identification number, set to 0 by default
        method  : string
            electrical potential approximation method, can be 'PSA' (Point Source Approximation)
            or 'LSA' (Line Source Approximation).
            set to 'PSA' by default. Note that if LSA is requested with an anisotropic material, computation
            will automatically be performed using 'PSA'
        """
        # properties
        self.ID = ID
        self.x = x
        self.y = y
        self.z = z
        self.method = method
        # footprints
        self.footprints = dict()    # footprints are stored for each axon with the key beeing the axon's ID
        self.recording = None

    def get_ID(self):
        """
        get the ID of a recording point

        Returns
        -------
        id : int
            ID number of the recording point
        """
        return self.ID

    def get_method(self):
        """
        get the method for a recording point

        Returns
        -------
        method : str
            name of the method, either 'PSA' for point source approximation or 'LSA' for line Source Approximation
        """
        return self.method

    def set_method(self,method):
        """
        Set the approximation to compute the extracellular potential

        Parameters
        ----------
        method : str
            name of the method, either 'PSA' for point source approximation or 'LSA' for line Source Approximation
        """
        self.method = method

    def compute_PSA_isotropic_footprint(self, x_axon, y_axon, z_axon, d, ID, sigma):
        """
        Compute the footprint for Point Source approximation an isotropic material

        Parameters
        ----------
        x_axon  : array
            array of the positions of the axon along the x-axis at which there is a current source, in [um]
        y_axon  : float
            y-axis position of the axon, in [um]
        z-axon  : float
            z-axis position of the axon, in [um]
        d       : float
            diameter of the axon, in [um]
        ID      : int
            axon ID number
        sigma   : float
            conductivity of the isotropic extracellular material, in [S.m]
        """
        electrical_distance = 4*np.pi*sigma*(((self.x - x_axon)*m)**2 + ((self.y - y_axon)*m)**2+ ((self.z - z_axon)*m)**2)**0.5
        surface = np.pi * (d*cm) * (np.gradient(x_axon)*cm)
        self.footprints[str(ID)] = np.divide(surface,electrical_distance)

    def compute_PSA_anisotropic_footprint(self, x_axon, y_axon, z_axon, d, ID, sigma_xx, sigma_yy, sigma_zz):
        """
        Compute the footprint for Point Source approximation an anisotropic material

        Parameters
        ----------
        x_axon      : array
            array of the positions of the axon along the x-axis at which there is a current source, in [um]
        y_axon      : float
            y-axis position of the axon, in [um]
        z-axon      : float
            z-axis position of the axon, in [um]
        d           : float
            diameter of the axon, in [um]
        ID          : int
            axon ID number
        sigma_xx    : float
            conductivity of the isotropic extracellular material alog the x-axis, in [S.m]
        sigma_yy    : float
            conductivity of the isotropic extracellular material alog the y-axis, in [S.m]
        sigma_zz    : float
            conductivity of the isotropic extracellular material alog the z-axis, in [S.m]
        """
        sx = sigma_yy * sigma_zz
        sy = sigma_xx * sigma_zz
        sz = sigma_xx * sigma_yy
        electrical_distance = 4*np.pi*((sx*(self.x - x_axon)*m)**2 + (sy*(self.y - y_axon)*m)**2+ (sz*(self.z - z_axon)*m)**2)**0.5
        surface = np.pi * (d*cm) * (np.gradient(x_axon)*cm)
        self.footprints[str(ID)] = np.divide(surface,electrical_distance)

    def init_recording(self, N_points):
        """
        Initializes the recorded extracellular potential. if a recording already exists,
        nothing is performed (usefull at the multi-axons level for instance)

        Parameters
        ----------
        N_points : int
            length of the extracellular potential vector along temporal dimension
        """
        if self.recording == None:
            self.recording = np.zeros(N_points)
        else:
            if len(self.recording)!=N_points:
                rise_error('Trying to compute an extracellular potential of a wrong temporal size')

    def reset_recording(self, N_points):
        """
        Sets the recorded extracellular potential to zero whatever the conditions

        Parameters
        ----------
        N_points : int
            length of the extracellular potential vector along temporal dimension
        """
        self.recording = np.zeros(N_points)

    def add_axon_contribution(self, I_membrane, ID):
        """
        Adds the and axon extracellular potential to the recording computed as the matrix product of
        I_membrane computed from neuron with the footprint computed below and stored in the object
        for a specific axons ID.

        Parameters
        ----------
        I_membrane  : array
            membrane current as a matrix over times (columns) and position (lines)
            in mA/cm2
        ID          : int
            axon ID as footprint are stored in a dictionnary with their ID as key
        """
        self.recording += np.matmul(np.transpose(I_membrane),self.footprints[str(ID)])

class recorder():
    """
    Object for recording extracellular potential of axons.
    """
    def __init__(self, material=None):
        """
        Instantiation of an extracellular potential recording mechanism. A mecanism can store recording points,
        be associated with a material and properties. The mechanism will perform the extracellular potential
        computation at each point for an axon when a simulation is performed.
        """
        self.material = None
        self.is_isotropic = True
        # if no material specified, sigma is 1S/m, else everything is loaded from signal
        if material == None:
            self.sigma = 1
            self.isotropic = True
            self.material = None
            self.sigma_xx = None
            self.sigma_yy = None
            self.sigma_zz = None
        else:
            self.material = material
            temporary_material = load_material(self.material)
            if temporary_material.is_isotropic():
                self.isotropic = True
                self.sigma = temporary_material.sigma
                self.sigma_xx = None
                self.sigma_yy = None
                self.sigma_zz = None
            else:
                self.isotropic = False
                self.sigma = None
                self.sigma_xx = temporary_material.sigma_xx
                self.sigma_yy = temporary_material.sigma_yy
                self.sigma_zz = temporary_material.sigma_zz
        # for internal use
        self.recording_points = []

    def is_empty(self):
        """
        check if a recorder has no recording points (empty) or not.

        Returns
        -------
        """
        return self.recording_points == []

    def add_recording_point(self, point):
        """
        add an object of type recording_point to the list of recording points.

        Parameters
        ----------
        point : recording_point
            recording point to add to the recording points list
        """
        if is_recording_point(point):
            self.recording_points.append(point)

    def set_recording_point(self, x, y, z, method='PSA'):
        """
        Set a recording point at a given location and add to the recording points list

        Parameters
        ----------
        x       : float
            x position of the recording point, in um
        y       : float
            y position of the recording point, in um
        z       : float
            z position of the recording point, in um
        method  : string
            electrical potential approximation method, can be 'PSA' (Point Source Approximation)
            or 'LSA' (Line Source Approximation).
            set to 'PSA' by default. Note that if LSA is requested with an anisotropic material, computation
            will automatically be performed using 'PSA'
        """
        if self.is_empty():
            new_point = recording_point(x, y, z, method=method)
        else:
            lowest_ID = self.recording_points[-1].get_ID()
            new_point = recording_point(x, y, z, ID=lowest_ID+1, method=method)
        self.add_recording_point(new_point)

    def compute_footprints(self, x_axon, y_axon, z_axon, d, ID):
        """
        compute all footprints for a given axon on all recording points of the recorder

        Parameters
        ----------
        x_axon      : array
            array of the positions of the axon along the x-axis at which there is a current source, in [um]
        y_axon      : float
            y-axis position of the axon, in [um]
        z-axon      : float
            z-axis position of the axon, in [um]
        d           : float
            diameter of the axon, in [um]
        ID          : int
            axon ID number
        """
        if not self.is_empty():
            for point in self.recording_points:
                if self.isotropic:
                    point.compute_PSA_isotropic_footprint(x_axon, y_axon, z_axon, d, ID, self.sigma)
                else:
                    point.compute_PSA_anisotropic_footprint(x_axon, y_axon, z_axon, d, ID, self.sigma_xx, self.sigma_yy, self.sigma_zz)

    def init_recordings(self, N_points):
        """
        Initializes the recorded extracellular potential for all recodgin points. If a potential already exists,
        nothing will be performed

        Parameters
        ----------
        N_points : int
            length of the extracellular potential vector along temporal dimension
        """
        if not self.is_empty():
            for point in self.recording_points:
                point.init_recording(N_points)

    def reset_recordings(self, N_points):
        """
        Sets the recorded extracellular potential to zero whatever the conditions for all recording points

        Parameters
        ----------
        N_points : int
            length of the extracellular potential vector along temporal dimension
        """
        if not self.is_empty():
            for point in self.recording_points:
                point.reset_recording(N_points)

    def add_axon_contribution(self, I_membrane, ID):
        """
        Add one axon contribution to the extracellular potential of all recording points.

        Parameters
        ----------
        I_membrane  : array
            membrane current as a matrix over times (columns) and position (lines)
            in mA/cm2
        ID          : int
            axon ID as footprint are stored in a dictionnary with their ID as key
        """
        if not self.is_empty():
            for point in self.recording_points:
                point.add_axon_contribution(I_membrane, ID)