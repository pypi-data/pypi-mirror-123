"""
Created on 15/10/2021

@author: Lucas V. dos Santos
"""
import os

try:
    import gurobipy as gp
except ImportError:
    raise ImportError(f"""
    gurobipy not installed. 
    Download at {'https://www.gurobi.com/documentation/6.5/quickstart_mac/the_gurobi_python_interfac.html'}
    """)


def str_to_lp(text):
    def ident(string):
        return " " + string

    new_lines = []
    count = 0

    obj = {
        'max': 'Maximize',
        'min': 'Minimize'
    }
    for line in text.splitlines():

        line = line.strip()
        if len(line) > 0 and line[-1] == ';':

            line = line[:-1]

            if count == 0:
                lhs, rhs = line.split(':')
                new_lines.append(obj[lhs.lower()])
                new_lines.append(ident(rhs))
                new_lines.append('Subject To')
            else:
                if line.startswith('int '):
                    new_lines.append('Integer')
                    new_lines.append(ident(" ".join(line.split()[1:])))
                else:
                    new_lines.append(ident(line))

            count += 1

    new_lines.append('End')
    return new_lines


def read(text):
    cwd = os.getcwd()
    if '.lp' in text:
        m = gp.read(text)
    else:
        lines = str_to_lp(text)
        with open(f'{cwd}/model_temp.lp', 'w') as f:
            for line in lines:
                f.write(line + '\n')

        m = gp.read(f'{cwd}/model_temp.lp')
        os.remove(f'{cwd}/model_temp.lp')

    return m


def solution(model, prt=True):
    sol = {}
    for var in model.getVars():
        sol[var.varName] = var.x
    if prt:
        print(sol)
    return sol


class Model(gp.Model):
    """Add functionalities to gurobi Model"""

    def solution(self):
        return solution(self)


def main():
    pass


if __name__ == "__main__":
    main()
