import numpy as np
from src.entity.UnitNumber import UnitNumber


class ITCEntity:
    time = []
    heat_flow = []
    injections = []
    injections_time = []
    con_amp = UnitNumber
    vol_amp = UnitNumber
    con_syr = UnitNumber

    def __init__(self, time, heat_flow, injections, injections_time, con_syr, vol_amp, con_amp):
        self.time = time
        self.heat_flow = heat_flow
        self.injections = injections
        self.injections_time = injections_time
        self.inj_index = np.array(range(0, len(injections))).ravel()
        self.inj_removed = np.empty(0, dtype=int).ravel()
        self.con_syr = con_syr
        self.vol_amp = vol_amp
        self.con_amp = con_amp

    def set_time(self, time):
        self.time = time

    def set_heat_flow(self, heat_flow):
        self.heat_flow = heat_flow

    def set_injections(self, injections, injections_time):
        self.injections = injections
        self.injections_time = injections_time

    def set_con_syr(self, con_syr):
        self.con_syr = con_syr

    def set_ampoule(self, vol_amp, con_amp):
        self.vol_amp = vol_amp
        self.con_amp = con_amp

    def remove_injection(self, inj):
        self.inj_removed = np.append(self.inj_removed.ravel(), self.inj_index[inj])
        self.inj_index = np.delete(self.inj_index, [inj])