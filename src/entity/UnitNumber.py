import re


class UnitNumber:
    original = ''
    value = 0
    unit = ''

    def __init__(self, number_str):
        self.original = number_str
        self.__split_from_unit(number_str)

    def __split_from_unit(self, number_str):
        if re.search("[\\d.e-]+", number_str):
            start = re.search("[\\d.e-]+", number_str).start()
            end = re.search("[\\d.e-]+", number_str).end()
            number = float(number_str[start:end])

            number_str = number_str[end:].strip()
            end = len(number_str)
            if re.search(" ", number_str):
                end = re.search(" ", number_str)
            unit = number_str[0:end]

            self.value = number
            self.unit = unit

    def set_unit(self, unit):
        self.unit = unit
        return self

    def set_value(self, value):
        self.value = value
        return self

    def reset(self):
        self.__init__(self.original)
        return self

    def convert_to_ul(self):
        liter_converter = {
            'µl': 1,
            'ul': 1,
            'ml': 1000,
            'dm^3': 1e+6,
            'dm3': 1e+6
        }
        self.value = self.value * liter_converter[self.unit]
        self.unit = 'µl'
        return self

    def convert_to_mol_per_ul(self):
        mol_converter = {
            'mol': 1,
            'kmol': 1000,
            'mmol': 0.001,
            'umol': 1e-6,
            'µmol': 1e-6
        }
        liter_converter = {
            'µl': 1,
            'ul': 1,
            'ml': 1000,
            'dm^3': 1e+6,
            'dm3': 1e+6
        }
        if re.search("/", self.unit):
            split = re.search("/", self.unit).start()
            mol_unit = self.unit[:split]
            lit_unit = self.unit[split + 1:]

            self.value = self.value * mol_converter[mol_unit] / liter_converter[lit_unit]
            self.unit = "mol/µl"
        return self

    def convert_watt_to(self, unit):
        watt_converter = {
            'cal': 0.2388458966275,
            'ucal': 238845.8966275,
            'kj': 0.001
        }
        self.value = self.value * watt_converter[unit]
        self.unit = unit
        return self

    def convert_cal_to(self, unit):
        cal_converter = {
            'kj': 4.184
        }
        self.value = self.value * cal_converter[unit]
        self.unit = unit
        return self
