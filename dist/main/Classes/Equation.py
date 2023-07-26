import os

from sympy import symbols, solve, latex, sympify, UnevaluatedExpr
from sympy.parsing.sympy_parser import parse_expr

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# from https://matplotlib.org/stable/gallery/text_labels_and_annotations/mathtext_asarray.html
def text_to_rgba(latex_equation, destination_name, dpi=400, **kwargs):
    fig = Figure(facecolor="none")
    fig.text(0, 0, r"$%s$" % latex_equation, **kwargs)
    fig.savefig(destination_name + "_rgba.jpg", dpi=dpi, format="jpg", bbox_inches="tight",
                pad_inches=0)


# def latex_to_png(latex_eqtn, png_destination):
#     # add text
#     text_object = plt.text(0, 0.6, r"$%s$" % latex_eqtn, fontsize=12)
#     figure_object = plt.figure()
#     renderer_object = figure_object.canvas.get_renderer()
#
#     # get dimensions
#     bb = text_object.get_window_extent(renderer=renderer_object)
#     eqtn_width = bb.width
#     eqtn_height = bb.height
#
#     # set plt dimensions
#     figure_object.set_figwidth(eqtn_width)
#     figure_object.set_figheight(eqtn_height)
#
#     # hide axes
#     fig = plt.gca()
#     fig.axes.get_xaxis().set_visible(False)
#     fig.axes.get_yaxis().set_visible(False)
#     text_object.savefig(png_destination + ".jpg", pad_inches=0.0)
#     plt.clf()


class Equation:
    def __init__(self, symbol_string, eqtn_string, eqtn_name, latex_image_dir, entity_name=None, time_period=None):
        self.latex_image_dir = latex_image_dir
        self.eqtn_name = eqtn_name
        self.equation_with_values = None
        self.symbol_dict = {}
        variable_split = symbol_string.split(sep=" ")
        for variable in variable_split:
            self.symbol_dict[variable] = symbols(variable)
        self.equation_parsed = parse_expr(eqtn_string, local_dict=self.symbol_dict)
        self.solved_dict = {}
        self.latex_string_dict = {}
        self.value_dict = {}
        file_destination = os.getcwd()
        for symbol_key in self.symbol_dict.keys():
            solution_list = solve(self.equation_parsed, self.symbol_dict[symbol_key])
            self.solved_dict[symbol_key] = solution_list
            equation_file_name = "{}_solved_for_{}".format(eqtn_name, symbol_key)
            self.latex_string_dict[str(symbol_key)] = []
            for i in range(len(solution_list)):
                simplified_eqtn = sympify(solution_list[i])
                self.latex_string_dict[str(symbol_key)].append(
                    latex(simplified_eqtn) + " = " + latex(self.symbol_dict[symbol_key]))
                equation_file_name_current = "\\local_equation_images\\" + equation_file_name + "_{}".format(i)
                file_destination_current = file_destination + equation_file_name_current
                text_to_rgba(self.latex_string_dict[str(symbol_key)][i], file_destination_current)
                # latex_to_png(self.latex_string_dict[str(symbol_key)][-1], file_destination_current)
        self.entity_name = entity_name
        self.time_period = time_period

    def variable_solve(self, passed_values_dict, file_destination):
        if passed_values_dict and len(passed_values_dict) == len(self.symbol_dict) - 1:
            for value_key in passed_values_dict.keys():
                symbol = self.symbol_dict[value_key]
                self.value_dict[symbol] = passed_values_dict[value_key]
            unevaluated_dict = {}
            for key in passed_values_dict:
                unevaluated_dict[key] = UnevaluatedExpr(passed_values_dict[key])
            equation_unevaluated_values = self.equation_parsed.subs(unevaluated_dict)
            equation_with_values = self.equation_parsed.subs(passed_values_dict)
            missing_var_list = list(set(self.symbol_dict.values()) - set(self.value_dict.keys()))
            missing_var = missing_var_list[0]
            solved_no_values = solve(self.equation_parsed, missing_var)
            unevaluated_eqtn_solutions = solve(equation_with_values, missing_var, evaluate=False)
            equation_solutions = solve(equation_with_values, missing_var)
            for i in range(len(equation_solutions)):
                for j in range(len(unevaluated_eqtn_solutions)):
                    latex_eqtn_solved_string = latex(solved_no_values) + "=" + latex(missing_var) + "=" + latex(unevaluated_eqtn_solutions[j]) + "=" + latex(equation_solutions[i])
                    filename = file_destination + "\\{}_solved_for{}_subs_{}_{}".format(self.eqtn_name, str(missing_var), j, i)
                    text_to_rgba(latex_eqtn_solved_string, filename)


if __name__ == '__main__':
    new_eqtn_list = [Equation('v_x0 a_x t v_x', 'v_x0 + a_x * t - v_x', 'first_kinematic',
                              r'C:\Users\rober\PycharmProjects\EquationBreakdown\local_equation_images'),
                     Equation('x_0 v_x0 t a_x x', 'x_0 + v_x0 * t + (1/2) * a_x * t**2 - x', 'second_kinematic',
                              r'C:\Users\rober\PycharmProjects\EquationBreakdown\local_equation_images'),
                     Equation('v_x0 a-x x x_0', 'v_x0**2 + 2 * a_x * (x - x_0) - v_x**2', 'third_kinematic',
                              r'C:\Users\rober\PycharmProjects\EquationBreakdown\local_equation_images')]
    values_dict = {'v_x0': 10.0, 'a_x': -9.8, 't': 3.0}
    new_eqtn_list[0].variable_solve(values_dict, r'C:\Users\rober\PycharmProjects\EquationBreakdown'
                                                 r'\local_equation_images')
