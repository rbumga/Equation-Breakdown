import csv

from Classes.Equation import Equation
import pandas as pd

class EquationLoader:
    def __init__(self, load_file_location, latex_image_dir):
        self.latex_image_dir = latex_image_dir
        self.load_file_location = load_file_location
        self.equation_dictionary = {}
        equation_read_df = pd.read_csv(self.load_file_location)
        first_eqtn_name = None
        for i in range(len(equation_read_df)):
            eqtn_name = equation_read_df.iloc[i]['equation_name']
            if not first_eqtn_name:
                first_eqtn_name = eqtn_name
            eqtn_variables_string = equation_read_df.iloc[i]['variable_string']
            eqtn_sequence_string = equation_read_df.iloc[i]['equation_string']
            new_eqtn = Equation(eqtn_variables_string, eqtn_sequence_string, eqtn_name, self.latex_image_dir)
            self.equation_dictionary[eqtn_name] = new_eqtn
        self.equation_dictionary[first_eqtn_name].variable_solve({'v_x0': 10.0, 'a_x': -9.8, 't': 3.0}, self.latex_image_dir)
