"""
Access and modify NRV Parameters
Authors: Florian Kolbl / Roland Giraud / Louis Regnacq / Thomas Couppey
(c) ETIS - University Cergy-Pontoise - CNRS
"""
from .NRV_Class import NRV_class
from .NRV_Results import NRV_results

class sim_results(NRV_results):
    def __init__(self, context=None):
        super().__init__(context)


class NRV_simulable(NRV_class):
    """
    
    """
    def __init__(
        self,
        t_sim=2e1,
        dt=0.001,
        record_V_mem=True,
        record_I_mem=False,
        record_I_ions=False,
        record_particles=False,
        record_g_mem=False,
        record_g_ions=False,
        loaded_footprints=None,
    ):
        super().__init__()
        self.t_sim = t_sim
        self.record_V_mem = record_V_mem
        self.record_I_mem = record_I_mem
        self.record_I_ions = record_I_ions
        self.record_particles = record_particles
        self.record_g_mem = record_g_mem
        self.record_g_ions = record_g_ions
        self.loaded_footprints = loaded_footprints

        self.dt = dt

    def extracel_status(self):
        if "extra_stim" in self.__dict__:
            if self.__dict__["extra_stim"] is not None:
                return True
        else:
            return False

    def intracel_status(self):
        if "intra_current_stim" in self.__dict__:
            if self.__dict__["intra_current_stim"] != [] and self.__dict__["intra_current_stim"] is not None:
                return True
        elif "intra_voltage_stim" in self.__dict__:
            if self.__dict__["intra_voltage_stim"] is not None:
                return True
        else:
            return False

    def rec_status(self):
        if "recorder" in self.__dict__:
            if self.__dict__["recorder"] is not None:
                return True
        else:
            return False

    def __call__(self, **kwds):
        return self.simulate(**kwds)

    def simulate(self, **kwargs) -> sim_results:
        self.set_parameters(**kwargs)
        results = sim_results(
                self.save(
                save=False,
                extracel_context=self.extracel_status(),
                intracel_context=self.intracel_status(),
                rec_context=self.rec_status(),
            )
        )
        return results