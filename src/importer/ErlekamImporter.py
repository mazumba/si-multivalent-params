import os.path
from openpyxl import load_workbook
from scipy.interpolate import UnivariateSpline
from src.entity.ExtractCollection import ExtractCollection
from src.entity.UnitNumber import UnitNumber
import numpy as np


def extract_collection(filename: str, convert=True, integral_range=0) -> ExtractCollection:
    return from_any(filename, convert, integral_range)


def from_any(filename, convert: bool, integral_range: int):
    ext = os.path.splitext(filename)[1]
    if '.xlsx' == ext:
        return from_xlsx(filename, convert, integral_range)


def from_xlsx(filename, convert=True, integral_range=0):
    wb = load_workbook(filename)

    is_data_row = False
    time = []
    heat_flow = []
    injections = []
    injections_time = []

    # The ITC data sheet.
    # time_col
    # heat_flow_col: ucal/s
    # injections_col: just a marker
    sheet = wb.worksheets[0]
    # column ids
    e_col = 0  # E=dQ/dt (ucal/s)
    delta_col = 1  # ∆E/∆t
    time_col = 2  # t aus Experi.
    heat_flow_col = 3  # Edc (ucal/s)
    injections_col = 4
    is_injection = True
    injection_range = 200
    injection_count = 0
    for row in sheet.rows:
        # first row is just titles
        injection_count += 1
        if row[0].value is None:
            break
        if is_data_row:
            # If injections_col is not empty, then an injection took place.
            # if row[injections_col].value:
            if ('00000000' != row[heat_flow_col].fill.bgColor.index or 1 == injection_count) and is_injection:
                injection_count = 1
                is_injection = False
                injections_time.append(row[time_col].value)
            if ('00000000' == row[heat_flow_col].fill.bgColor.index and injection_count >= injection_range) \
                    and not is_injection:
                injection_count = 0
                is_injection = True
            time.append(row[time_col].value)
            # EDC (ucal/s): 12.5 * B + A
            heat = float(12.5 * row[delta_col].value + row[e_col].value)
            # heat = float(row[0].value + row[1].value*12.5)
            heat_flow.append(heat)
        is_data_row = True
    sheet = wb.worksheets[1]
    vol_amp = UnitNumber(str(sheet['E4'].value) + "ul")
    con_amp = UnitNumber(str(sheet['B4'].value) + "mmol/ul")
    con_syr = UnitNumber(str(sheet['C4'].value) + "mmol/ul")
    if convert:
        vol_amp = vol_amp.convert_to_ul()
        con_amp = con_amp.convert_to_ul()
        con_syr = con_syr.convert_to_ul()

    # The Injection sheets
    for inj in range(0, len(injections_time)):
        try:
            sheet = wb.worksheets[inj + 1]
        except IndexError:
            sheet = wb.worksheets[-1]
        vol_syr = sheet['D4'].value
        if 1 == sheet['E8'].value:
            vol_syr = sheet['D8'].value
        elif 1 == sheet['E7'].value:
            vol_syr = sheet['D7'].value
        injection = UnitNumber(str(vol_syr) + "ul")
        if convert:
            injections.append(injection.convert_to_ul())
        else:
            injections.append(injection)

    return ExtractCollection(__get_l_con__(injections[:14], con_syr, vol_amp),
                             __get_m_con__(injections[:14], con_amp, vol_amp),
                             __get_heat_per_injection__(time[:3200],
                                                        heat_flow[:3200],
                                                        injections_time[:14], int_range=integral_range),
                             np.array(time[:3100]), np.array(heat_flow[:3100]))


# Get the ligand concentration for each injection
# based on injection volume and concentration and ampoule volume.
def __get_l_con__(injections: list, con_syr: UnitNumber, vol_amp: UnitNumber):
    con = []
    l_i = 0
    # C4 * ((E8 * D4 * (2 * E4 - E8 * D4)) / (2 * (E4)^2))
    for n in range(0, len(injections)):
        l_i = l_i + injections[n].value
        con.append(con_syr.value * l_i * (2 * vol_amp.value - l_i) / (2 * vol_amp.value * vol_amp.value))
    return np.array(con)


def __get_m_con__(injections: list, con_amp: UnitNumber, vol_amp: UnitNumber):
    con = []
    l_i = 0
    # B4 * ((2 * E4 - E8 * D4) / (2 * E4 + E8 * D4))
    for n in range(0, len(injections)):
        l_i = l_i + injections[n].value
        con.append(con_amp.value * (2 * vol_amp.value - l_i) / (2 * vol_amp.value + l_i))
    return np.array(con)


def __get_heat_per_injection__(time: list, heat_flow: list, injections_time: list, int_range: int):
    heat_per_injection = []
    int_start = None
    f_heat_flow = UnivariateSpline(time, np.array(heat_flow), k=5, s=0)
    for n in range(0, len(injections_time)):
        inj = injections_time[n]
        int_end = inj
        if int_start:
            if int_range != 0:
                int_end = time[time.index(int_start) + int_range]
            heat_per_injection.append(f_heat_flow.integral(int_start, int_end))
        int_start = inj
    int_start = injections_time[-1]
    int_end = time[-1]
    if int_range != 0:
        int_end = int_start + int_range
    heat_per_injection.append(f_heat_flow.integral(int_start, int_end))
    return np.array(heat_per_injection)
