

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from solver import resolver_ecuacion

equation_str = "y' = -(3*x**2*y + y**3 + exp(x)) / (x**3 + 3*x*y**2 + sin(y))"

solucion, procedimiento = resolver_ecuacion(equation_str, "Autodetectar")

if solucion is not None:
    print("La solución a la ecuación es:")
    print(solucion)
    print("\n" + "="*20 + "\n")
    print(procedimiento)
else:
    print("No se pudo encontrar una solución.")
    print(procedimiento)

