"""
NRV-extracellular contexts
Authors: Florian Kolbl / Roland Giraud / Louis Regnacq / Thomas Couppey
(c) ETIS - University Cergy-Pontoise - CNRS
"""
import faulthandler
import numpy as np
from .electrodes import *
from .stimulus import *
from .materials import *
from .FEM import *
from ..backend.MCore import *
from ..backend.file_handler import *
from ..backend.log_interface import rise_error, rise_warning, pass_info

# enable faulthandler to ease 'segmentation faults' debug
faulthandler.enable()

def is_extra_stim(test_stim):
    """
    check if an object is a stimulation, return True if yes, else False
    """
    Flag = isinstance(test_stim, stimulation) or isinstance(test_stim, FEM_stimulation)\
        or isinstance(test_stim, extracellular_context)
    return Flag

def is_analytical_extra_stim(test_stim):
    """
    check if an object is a stimulation (analytical only), return True if yes, else False
    """
    return isinstance(test_stim, stimulation)

def is_FEM_extra_stim(test_stim):
    """
    check if an object is a FEM stimulation, return True if yes, else False
    """
    return isinstance(test_stim, FEM_stimulation)

def load_any_extracel_context(data):
    """
    return any kind of extracellular context properties from a dictionary or a json file

    Parameters
    ----------
    data    : str or dict
        json file path or dictionary containing extracel_context information
    """
    if type(data) == str:
        context_dic = json_load(data)
    else: 
        context_dic = data

    if context_dic["type"] is None:
        extracel = extracellular_context()
    elif context_dic["type"] == "stimulation":
        extracel = stimulation()
    elif context_dic["type"] == "FEM_stim":
        extracel = FEM_stimulation(data['model_fname'],comsol=False)
    else:
        rise_error("extra cellular context type not recognizede")

    extracel.load_extracel_context(context_dic)
    return extracel


class extracellular_context:
    """
    extracellular_context is a class to handle the computation of the extracellular voltage field induced by the electrical stimulation.
    This class should not be used directly by user, but user friendly classes (for Analitycal or FEM based computations) inherits from extracellular_context.
    """
    def __init__(self):
        """
        Instrantiation an extracellular_context object, empty shell to store electrodes and stimuli
        """
        # empty list to store electrodes and corresponding stimuli
        self.electrodes = []
        self.stimuli = []
        # list for synchronised stimuli
        self.synchronised = False
        self.synchronised_stimuli = []
        self.global_time_serie = []
        self.type = None

    ## Save and Load mehtods

    def save_extracel_context(self, save=False, fname='extracel_context.json'):
        """
        Return extracellular context as dictionary and eventually save it as json file

        Parameters
        ----------
        save    : bool
            if True, save in json files
        fname   : str
            Path and Name of the saving file, by default 'extracel_context.json'

        Returns
        -------
        context_dic : dict
            dictionary containing all information
        """
        context_dic = {}
        context_dic['electrodes'] = {}
        context_dic['stimuli'] = {}
        context_dic['synchronised_stimuli'] = {}
        context_dic['synchronised'] = self.synchronised
        context_dic['global_time_serie'] = self.global_time_serie
        context_dic['type'] = self.type
        for i in range(len(self.electrodes)):
            elec = self.electrodes[i]
            context_dic['electrodes'][i] = elec.save_electrode()
        for i in range(len(self.stimuli)):
            stim = self.stimuli[i]
            context_dic['stimuli'][i] = stim.save_stimulus()
        for i in range(len(self.synchronised_stimuli)):
            stim = self.synchronised_stimuli[i]
            context_dic['synchronised_stimuli'][i] = stim.save_stimulus()
        if save:
            json_dump(context_dic, fname)
        return context_dic

    def load_extracel_context(self, data='extracel_context.json'):
        """
        Load all extracellular context properties from a dictionary or a json file

        Parameters
        ----------
        data    : str or dict
            json file path or dictionary containing extracel_context information
        """
        if type(data) == str:
            context_dic = json_load(data)
        else: 
            context_dic = data
        self.electrodes = []
        self.stimuli = []
        self.synchronised_stimuli = []
        self.synchronised = context_dic['synchronised'] 
        self.global_time_serie = context_dic['global_time_serie']
        self.type = context_dic['type']
        for i in range(len(context_dic['electrodes'])):
            elec = load_any_electrode(context_dic['electrodes'][str(i)])
            self.electrodes += [elec]
            del elec

        for i in range(len(context_dic['stimuli'])):
            stim = stimulus()
            stim.load_stimulus(context_dic['stimuli'][str(i)])
            self.stimuli += [stim]
            del stim

        for i in range(len(context_dic['synchronised_stimuli'])):
            stim = stimulus()
            stim.load_stimulus(context_dic['synchronised_stimuli'][str(i)])
            self.synchronised_stimuli += [stim]
            del stim


    def is_empty(self):
        """
        check if a stimulation object is empty (No electrodes and stimuli, no external field can be computed).
        Returns True if empty, else False.

        Returns
        -------
        bool
            True if a simulation is empty, else False
        """
        return self.electrodes == []

    def add_electrode(self, electrode, stimulus):
        """
        Add a stimulation electrode and its stimulus to the stimulation.

        Parameters
        ----------
        electrode   : electrode object
            see Electrode.py or electrode object help for further details
        stimulus    : stimulus object
            see Stimulus.py or stimulus object help for further details
        """
        if self.electrodes == []:
            self.electrodes.append(electrode)
            self.stimuli.append(stimulus)
        else:
            electrode.set_ID_number(self.electrodes[-1].get_ID_number()+1)
            self.electrodes.append(electrode)
            self.stimuli.append(stimulus)
        self.synchronised = False

    def reset_stimuli(self):
        self.stimuli = []
        self.synchronised_stimuli = []
        self.synchronised = False
        self.global_time_serie = []

    def reset_electrodes(self):
        self.electrodes = []
        self.reset_stimuli()

    def synchronise_stimuli(self):
        """
        Synchronise all stimuli before simulation. Copies of the stimuli are created with the global number of samples
        from merging all stimuli time samples. Original stimuli are not affected.
        """
        if not (self.synchronised or self.is_empty()):
            if len(self.electrodes) == 1:
                self.synchronised_stimuli.append(self.stimuli[0])
            elif len(self.electrodes) == 2:
                stim_a, stim_b = get_equal_timing_copies(self.stimuli[0], self.stimuli[1])
                self.synchronised_stimuli.append(stim_a)
                self.synchronised_stimuli.append(stim_b)
            else:
                # init : put first two and synchronize them
                stim_a, stim_b = get_equal_timing_copies(self.stimuli[0], self.stimuli[1])
                self.synchronised_stimuli.append(stim_a)
                self.synchronised_stimuli.append(stim_b)
                # remaining stimuli to handle
                unsynchronized_stim = self.stimuli[2:]
                for stimulus in unsynchronized_stim:
                    # synchronise all the previously synchronised with the pending one
                    for s in self.synchronised_stimuli:
                        s.insert_samples(stimulus.t)
                    # synchronise the pending one with the already synchronised and add it to synchronised stim
                    stimulus.insert_samples(self.synchronised_stimuli[0].t)
                    self.synchronised_stimuli.append(stimulus)
            # anyway, take the first stimulus time serie as the global one
            self.global_time_serie = self.synchronised_stimuli[0].t
        self.synchronised = True

    def compute_vext(self, time_index):
        """
        Compute the external potential on a array of coordinate for a time sample of all synchronised stimuli with all
        electrodes.

        Parameters
        ----------
        time_index  : int
            time index of the synchronised stimuli to compute the field at.
            NB: as a safeguard, if the time_index is out of the sample list a null potential is returned

        Returns
        -------
        Vext : np.array
            external potential for the specified positions, in mV (numpy array)
        """
        Vext = np.zeros(len(self.electrodes[0].footprint))
        if not self.synchronised:
            self.synchronise_stimuli()
        if time_index < len(self.global_time_serie): # requested time index is in stimulus range (safeguard)
            for k in range(len(self.electrodes)):
                Istim = self.synchronised_stimuli[k].s[time_index]
                vext_elec = self.electrodes[k].compute_field(Istim)
                Vext = Vext + vext_elec
        return Vext

    def set_electrodes_footprints(self, footprints):
        """
        set the footprints for all electrodes from existing array

        Parameters
        ----------
        footprints  : list of array like
            list footprint for each electode of the extracellular context
        """
        i=0
        if len(footprints) == len(self.electrodes):
            for electrode in self.electrodes:
                electrode.set_footprint(footprints[i])
                i+=1
        else:
            rise_error("Footprint number different than electrode number")

class stimulation(extracellular_context):
    """
    Stimulation object are designed to connect all other objects requierd to analyticaly compute the external potential voltage for axons :
    - the material surrounding the axon (only one)
    - a list of electrode(s)
    - a list of corresponding current stimuli
    This class inherits from extracellular_context.
    """
    def __init__(self, material='endoneurium_ranck'):
        """
        Implement a stimulation object.

        Parameters
        ----------
        material    : str or material object
            extracellular medium see Material.py or material object help for further details
        """
        super().__init__()
        if is_mat(material):
            self.material = material
        else:
            self.material = load_material(material)
        self.type = "stimulation"

    ## Save and Load mehtods

    def save_extracel_context(self, save=False, fname='extracel_context.json'):
        """
        Return extracellular context as dictionary and eventually save it as json file

        Parameters
        ----------
        save    : bool
            if True, save in json files
        fname   : str
            Path and Name of the saving file, by default 'extracel_context.json'

        Returns
        -------
        context_dic : dict
            dictionary containing all information
        """
        context_dic = super().save_extracel_context()
        context_dic['material'] = self.material.save_material()
        if save:
            json_dump(context_dic, fname)
        return context_dic

    def load_extracel_context(self, data):
        """
        Load all extracellular context properties from a dictionary or a json file

        Parameters
        ----------
        data    : str or dict
            json file path or dictionary containing extracel_context information
        """
        if type(data) == str:
            context_dic = json_load(data)
        else: 
            context_dic = data
        super().load_extracel_context(data)
        self.material.load_material(context_dic['material'])

    def add_electrode(self, electrode, stimulus):
        """
        Add a stimulation electrode and its stimulus to the stimulation, only if the electrode is analytically described.

        Parameters
        ----------
        electrode   : electrode object
            see Electrode.py or electrode object help for further details
        stimulus    : stimulus object
            see Stimulus.py or stimulus object help for further details
        """
        if is_analytical_electrode(electrode):
            if self.electrodes == []:
                self.electrodes.append(electrode)
                self.stimuli.append(stimulus)
            else:
                electrode.set_ID_number(self.electrodes[-1].get_ID_number()+1)
                self.electrodes.append(electrode)
                self.stimuli.append(stimulus)
            self.synchronised = False

    def compute_electrodes_footprints(self, x, y, z, ID=0):
        """
        Compute the footprints for all electrodes

        Parameters
        ----------
        x           : np.array
            x position at which to compute the field, in um
        y           : float
            y position at which to compute the field, in um
        z           : float
            z position at which to compute the field, in um
        ID          : int
            axon ID, unused here, added to fit FEM_stimulation declaration of same method
        """
        for electrode in self.electrodes:
            electrode.compute_footprint(np.asarray(x), np.asarray(y), np.asarray(z), self.material)

class FEM_stimulation(extracellular_context):
    """
    FEM_based_simulation object are designed to connect all other objects requierd to compute the external potential voltage for axons using FEM :
    - the materials for the FEM stimulation : endoneurium, perineurium, epineurium and external material
    - a list of electrode(s)
    - a list of corresponding current stimuli
    """
    def __init__(self, model_fname, endo_mat='endoneurium_ranck',\
        peri_mat='perineurium', epi_mat='epineurium', ext_mat='saline',comsol=True):
        """
        Implement a FEM_based_stimulation object.

        Parameters
        ----------
        simuluation_fname   : str
            name of the simluation file to compute the field
        endo_mat            : material object
            specification of the endoneurium material, see Material.py or material object help for further details
        peri_mat            : material object
            specification of the perineurium material, see Material.py or material object help for further details
        epi_mat             : material object
            specification of the epineurium material, see Material.py or material object help for further details
        ext_mat             : material object
            specification of the external material (everything but the nerve), see Material.py or material object help for further details
        """
        super().__init__()
        self.electrodes_label = []
        self.model_fname = model_fname
        self.setup = False
        ## get material properties and add to model

        if is_mat(endo_mat):
            self.endoneurium = endo_mat
        else:
            self.endoneurium = load_material(endo_mat)
        if is_mat(peri_mat):
            self.perineurium = peri_mat
        else:
            self.perineurium = load_material(peri_mat)
        if is_mat(epi_mat):
            self.epineurium = epi_mat
        else:
            self.epineurium = load_material(epi_mat)
        if is_mat(ext_mat):
            self.external_material = ext_mat
        else:
            self.external_material = load_material(ext_mat)

        self.type ="FEM_stim"
        self.comsol=comsol
        ## load model
        if MCH.do_master_only_work():
            if comsol:
                self.model = COMSOL_model(self.model_fname)
        else:
            # check that COMSOL is not turned OFF in order to continue
            if not COMSOL_Status:
                rise_warning('Slave process abort as axon is supposed to used a COMSOL FEM and COMSOL turned off', abort=True)

    def __del__(self):
        if MCH.do_master_only_work() and COMSOL_Status and self.comsol: #added for safe del in case of COMSOL status turned OFF
            self.model.close()

    ## Save and Load mehtods

    def save_extracel_context(self, save=False, fname='extracel_context.json'):
        """
        Return extracellular context as dictionary and eventually save it as json file

        Parameters
        ----------
        save    : bool
            if True, save in json files
        fname   : str
            Path and Name of the saving file, by default 'extracel_context.json'

        Returns
        -------
        context_dic : dict
            dictionary containing all information
        """
        context_dic = super().save_extracel_context()
        context_dic['endoneurium'] = self.endoneurium.save_material()
        context_dic['perineurium'] = self.perineurium.save_material()
        context_dic['epineurium'] = self.epineurium.save_material()
        context_dic['external_material'] = self.external_material.save_material()
        context_dic['electrodes_label'] = self.electrodes_label
        context_dic['model_fname'] = self.model_fname
        context_dic['setup'] = self.setup
        if save:
            json_dump(context_dic, fname)
        return context_dic

    def load_extracel_context(self, data, C_model=False):
        """
        Load all extracellular context properties from a dictionary or a json file

        Parameters
        ----------
        data    : str or dict
            json file path or dictionary containing extracel_context information
        """
        if type(data) == str:
            context_dic = json_load(data)
        else: 
            context_dic = data
        super().load_extracel_context(data)

        self.electrodes_label = context_dic['electrodes_label']
        self.model_fname = context_dic['model_fname']
        self.setup = context_dic['setup']

        self.endoneurium.load_material(context_dic['endoneurium'])
        self.perineurium.load_material(context_dic['perineurium'])
        self.epineurium.load_material(context_dic['epineurium'])
        self.external_material.load_material(context_dic['external_material'])

        if C_model:
            if MCH.do_master_only_work():
                self.model = COMSOL_model(self.model_fname)
            else:
                # check that COMSOL is not turned OFF in order to continue
                if not COMSOL_Status:
                    rise_warning('Slave process abort as axon is supposed to used a COMSOL FEM and COMSOL turned off', abort=True)

    def reshape_outerBox(self, Outer_D):
        """
        Reshape the size of the FEM simulation outer box

        Parameters
        ----------
        outer_D : float
            FEM simulation outer box diameter, in mm, WARNING, this is the only parameter in mm !
        """
        if MCH.do_master_only_work():
            self.model.set_parameter('Outer_D', str(Outer_D)+'[mm]')

    def reshape_nerve(self, Nerve_D, Length, y_c=0, z_c=0, Perineurium_thickness=5):
        """
        Reshape the nerve of the FEM simulation

        Parameters
        ----------
        Nerve_D                 : float
            Nerve diameter, in um
        Length                  : float
            Nerve length, in um
        y_c                     : float
            Nerve center y-coordinate in um, 0 by default
        z_c                     : float
            Nerve z-coordinate center in um, 0 by default
        Perineurium_thickness   :float
            Thickness of the Perineurium sheet surounding the fascicles in um, 5 by default
        """
        if MCH.do_master_only_work():
            self.model.set_parameter('Nerve_D', str(Nerve_D)+'[um]')
            self.model.set_parameter('Length', str(Length)+'[um]')
            self.model.set_parameter('Nerve_y_c', str(y_c)+'[um]')
            self.model.set_parameter('Nerve_z_c', str(z_c)+'[um]')
            self.model.set_parameter('Perineurium_thickness', str(Perineurium_thickness)+'[um]')

    def reshape_fascicle(self, Fascicle_D, y_c=0, z_c=0, ID=None):
        """
        Reshape a fascicle of the FEM simulation

        Parameters
        ----------
        Fascicle_D  : float
            Fascicle diameter, in um
        y_c         : float
            Fascicle center y-coodinate in um, 0 by default
        z_c         : float
            Fascicle center y-coodinate in um, 0 by default
        ID          : int
            If the simulation contains more than one fascicles, ID number of the fascicle to reshape as in COMSOL
        """
        if MCH.do_master_only_work():
            if ID is None:
                self.model.set_parameter('Fascicle_D', str(Fascicle_D)+'[um]')
                self.model.set_parameter('Fascicle_y_c', str(y_c)+'[um]')
                self.model.set_parameter('Fascicle_z_c', str(z_c)+'[um]')
            else:
                self.model.set_parameter('Fascicle_'+'str(ID)'+'_D', str(Fascicle_D)+'[um]')
                self.model.set_parameter('Fascicle_'+'str(ID)'+'_y_c', str(y_c)+'[um]')
                self.model.set_parameter('Fascicle_'+'str(ID)'+'_z_c', str(z_c)+'[um]')

    def add_electrode(self, electrode, stimulus):
        """
        Add a stimulation electrode and its stimulus to the stimulation, only it the electrode is FEM based.

        Parameters
        ----------
        electrode   : electrode object
            see Electrode.py or electrode object help for further details
        stimulus    : stimulus object
            see Stimulus.py or stimulus object help for further details
        """
        if is_FEM_electrode(electrode):
            if self.electrodes == []:
                self.electrodes.append(electrode)
                self.electrodes_label.append(electrode.label)
                self.stimuli.append(stimulus)
            else:
                electrode.set_ID_number(self.electrodes[-1].get_ID_number()+1)
                self.electrodes.append(electrode)
                self.electrodes_label.append(electrode.label)
                self.stimuli.append(stimulus)
            self.synchronised = False
            self.setup = False

    def setup_FEM(self):
        """
        Parameter a model with all added electrodes parameters, material parameters, build geometry and mesh
        """
        # parameter electrodes
        for electrode in self.electrodes:
           electrode.parameter_model(self.model)
        # parameter materials
        self.model.set_parameter('Outer_conductivity', str(self.external_material.sigma)+'[S/m]')
        self.model.set_parameter('Epineurium_conductivity', str(self.epineurium.sigma)+'[S/m]')
        self.model.set_parameter('Perineurium_conductivity', str(self.perineurium.sigma)+'[S/m]')
        if self.endoneurium.is_isotropic():
            self.model.set_parameter('Endoneurium_conductivity_xx', str(self.endoneurium.sigma)+\
                '[S/m]')
            self.model.set_parameter('Endoneurium_conductivity_yy', str(self.endoneurium.sigma)+\
                '[S/m]')
            self.model.set_parameter('Endoneurium_conductivity_zz', str(self.endoneurium.sigma)+\
                '[S/m]')
        else:
            self.model.set_parameter('Endoneurium_conductivity_xx', str(self.endoneurium.sigma_xx)\
                +'[S/m]')
            self.model.set_parameter('Endoneurium_conductivity_yy', str(self.endoneurium.sigma_yy)\
                +'[S/m]')
            self.model.set_parameter('Endoneurium_conductivity_zz', str(self.endoneurium.sigma_zz)\
                +'[S/m]')
        ## create geometry and mesh
        self.model.build_and_mesh()
        ## stor the setup state
        self.setup = True

    def run_model(self):
        """
        Set materials properties, build geometry and mesh if not already done and solve the FEM model all in one.
        """
        if MCH.do_master_only_work():
            if not self.setup:
                self.setup_FEM()
            self.model.solve()

    def compute_electrodes_footprints(self, x, y, z, ID):
        """
        Compute the footprints for all electrodes

        Parameters
        ----------
        x           : np.array
            x position at which to compute the field, in um
        y           : float
            y position at which to compute the field, in um
        z           : float
            z position at which to compute the field, in um
        ID          : int
            ID of the axon
        """
        # test if the model is not solve and run simulation
        if MCH.do_master_only_work():
            if not self.model.is_computed:
                self.run_model()
            # get all potentials
            V = self.model.get_potentials(x, y, z)
        else:
            # send a request to the master to get all potentials
            data = {
                'rank': MCH.rank,
                'x': x,
                'y': y,
                'z': z,
                'ID': ID
            }
            MCH.send_data_to_master(data)
            # listen to the master to get V
            V = MCH.recieve_potential_array_from_master()['V']
        if len(self.electrodes) > 1:
            # sort electrodes by alphabetical order (COMSOL files should perform the parametric sweep by alphabetical order)
            sorter = np.argsort(self.electrodes_label)
            self.electrodes_label = list(np.asarray(self.electrodes_label)[sorter])
            self.electrodes = list(np.asarray(self.electrodes)[sorter])
            self.stimuli = list(np.asarray(self.stimuli)[sorter])
            # set the footprints
            for k, electrode in enumerate(self.electrodes):
                electrode.set_footprint(V[:, k])
        else:
            self.electrodes[0].set_footprint(V)
