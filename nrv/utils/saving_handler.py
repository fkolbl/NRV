"""
NRV-Cellular Level simulations
Authors: Florian Kolbl / Roland Giraud / Louis Regnacq / Thomas Couppey
(c) ETIS - University Cergy-Pontoise - CNRS
"""
from ..nmod.fascicles import *
from ..nmod.axons import *
from ..nmod.unmyelinated import *
from ..nmod.myelinated import *
from ..nmod.thin_myelinated import *
from ..fmod.extracellular import *
from ..fmod.electrodes import *
from ..fmod.materials import *
from ..fmod.stimulus import *
from ..backend.MCore import *
from ..backend.log_interface import rise_error, rise_warning, pass_info


###############################################################
#########################  Loaders  ###########################
###############################################################

def load_any_fascicle(data, extracel_context=False, intracel_context=False, rec_context=False):
    """
    generate any kind of fascicle from a dictionary or a json file

    Parameters
    ----------
    data    : str or dict
        json file path or dictionary containing fascicle information
    """
    synchronize_processes()
    if type(data) == str:
        fasc_dic = json_load(data)
    else: 
        fasc_dic = data
    fasc = fascicle()
    fasc.load_fascicle_configuration(fasc_dic, extracel_context=extracel_context, intracel_context=intracel_context, rec_context=rec_context)
    if extracel_context and rec_context:
        return fasc , fasc.extra_stim, fasc.recorder
    elif extracel_context:
        return fasc , fasc.extra_stim
    elif rec_context:
        return fasc , fasc.recorder
    else:
        return fasc

def load_any_axon(data, extracel_context=False, intracel_context=False, rec_context=False):
    """
    generate any kind of axon from a dictionary or a json file

    Parameters
    ----------
    data    : str or dict
        json file path or dictionary containing axon information
    """
    if type(data) == str:
        ax_dic = json_load(data)
    else: 
        ax_dic = data

    if ax_dic["myelinated"] is True:
        if ax_dic["thin"]:
            ax = thin_myelinated(0,0,1,10)
        else:
            ax = myelinated(0,0,1,10)
    elif ax_dic["myelinated"] is False:
        ax = unmyelinated(0,0,1,10)
    else:
        ax = axon(0,0,1,10)

    ax.load_axon(ax_dic, extracel_context=extracel_context, intracel_context=intracel_context, rec_context=rec_context)
    if extracel_context and rec_context:
        return ax , ax.extra_stim, ax.recorder
    elif extracel_context:
        return ax , ax.extra_stim
    elif rec_context:
        return ax , ax.recorder
    else:
        return ax


