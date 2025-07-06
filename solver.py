from sympy import dsolve, Eq, symbols, Function, Derivative, classify_ode
from sympy.parsing.sympy_parser import parse_expr

def clasificar_ecuacion(ecuacion, y_func):
    """Clasifica la ecuación diferencial y devuelve el mejor hint."""
    # dsolve hints a veces son diferentes a los de classify_ode, mapeamos los que necesitamos
    mapa_hints = {
        'separable': 'separable',
        '1st_linear': '1st_linear',
        '1st_homogeneous_coeff_best': '1st_homogeneous_coeff_best',
        'exact': '1st_exact'
    }
    clasificacion = classify_ode(ecuacion, y_func)
    # Devuelve el primer hint compatible que encontremos
    for hint in clasificacion:
        if hint in mapa_hints:
            return mapa_hints[hint]
    return clasificacion[0] if clasificacion else None

def resolver_ecuacion(ecuacion_str, tipo):
    try:
        x = symbols('x')
        y_func = Function('y')(x)

        # Creamos un diccionario para que el parser sepa qué es 'y' y qué es 'x'
        local_dict = {
            'y': y_func,
            'x': x
        }

        # Reemplazamos y' con la derivada real de y(x) DESPUÉS de parsear
        # Esto evita los errores de doble sustitución y de "no es llamable"
        if '=' not in ecuacion_str:
            return "Error: La ecuación debe contener un signo '='."

        partes = ecuacion_str.split('=', 1)
        lhs_str = partes[0].strip()
        rhs_str = partes[1].strip()

        # Parseamos el lado derecho
        rhs_expr = parse_expr(rhs_str, local_dict=local_dict)

        # Asumimos que el lado izquierdo es y'
        if lhs_str == "y'":
            lhs_expr = Derivative(y_func, x)
        else:
            # Si no es y', también lo parseamos (para ecuaciones tipo f(x,y) = g(x,y))
            lhs_expr = parse_expr(lhs_str, local_dict=local_dict)

        ecuacion = Eq(lhs_expr, rhs_expr)

        hint = ''
        if tipo == "Autodetectar":
            hint = clasificar_ecuacion(ecuacion, y_func)
            if not hint:
                return "No se pudo clasificar la ecuación automáticamente. Intente especificar el tipo."
        elif tipo == "Lineal":
            hint = '1st_linear'
        elif tipo == "Variables Separables":
            hint = 'separable'
        elif tipo == "Homogénea":
            hint = '1st_homogeneous_coeff_best'
        elif tipo == "Exacta":
            hint = '1st_exact'

        solucion = dsolve(ecuacion, y_func, hint=hint)
        return str(solucion)

    except Exception as e:
        return f"Error al procesar la ecuación: {e}"