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

def get_procedimiento_conceptual(tipo_resuelto):
    procedimiento = f"Tipo de Ecuación Detectado/Seleccionado: {tipo_resuelto}\n\n"

    if tipo_resuelto == "separable":
        procedimiento += "Procedimiento Conceptual:\n"
        procedimiento += "1. Separar las variables x e y en lados opuestos de la ecuación.\n"
        procedimiento += "2. Integrar ambos lados de la ecuación con respecto a sus respectivas variables.\n"
        procedimiento += "3. Despejar y(x) para obtener la solución general.\n"
    elif tipo_resuelto == "1st_linear":
        procedimiento += "Procedimiento Conceptual:\n"
        procedimiento += "1. Asegurarse de que la ecuación esté en la forma estándar: y' + P(x)y = Q(x).\n"
        procedimiento += "2. Calcular el factor integrante: e^(∫P(x)dx).\n"
        procedimiento += "3. Multiplicar toda la ecuación por el factor integrante.\n"
        procedimiento += "4. Integrar ambos lados para encontrar la solución general.\n"
    elif tipo_resuelto == "1st_homogeneous_coeff_best":
        procedimiento += "Procedimiento Conceptual:\n"
        procedimiento += "1. Realizar la sustitución y = v*x, donde v es una función de x.\n"
        procedimiento += "2. Transformar la ecuación homogénea en una ecuación de variables separables en términos de v y x.\n"
        procedimiento += "3. Resolver la ecuación de variables separables para v.\n"
        procedimiento += "4. Sustituir v = y/x de nuevo para obtener la solución en términos de y y x.\n"
    elif tipo_resuelto == "1st_exact":
        procedimiento += "Procedimiento Conceptual:\n"
        procedimiento += "1. Asegurarse de que la ecuación esté en la forma M(x,y)dx + N(x,y)dy = 0.\n"
        procedimiento += "2. Verificar la condición de exactitud: ∂M/∂y = ∂N/∂x.\n"
        procedimiento += "3. Encontrar una función potencial F(x,y) tal que ∂F/∂x = M y ∂F/∂y = N.\n"
        procedimiento += "4. La solución general es F(x,y) = C.\n"
    else:
        procedimiento += "Procedimiento Conceptual: No se dispone de un procedimiento detallado para este tipo específico o la clasificación.\n"

    return procedimiento

def resolver_ecuacion(ecuacion_str, tipo):
    try:
        x = symbols('x')
        y_func = Function('y')(x)

        local_dict = {
            'y': y_func,
            'x': x
        }

        if '=' not in ecuacion_str:
            return None, "Error: La ecuación debe contener un signo '='."

        partes = ecuacion_str.split('=', 1)
        lhs_str = partes[0].strip()
        rhs_str = partes[1].strip()

        rhs_expr = parse_expr(rhs_str, local_dict=local_dict)

        if lhs_str == "y'":
            lhs_expr = Derivative(y_func, x)
        else:
            lhs_expr = parse_expr(lhs_str, local_dict=local_dict)

        ecuacion = Eq(lhs_expr, rhs_expr)

        hint = ''
        tipo_resuelto = tipo # Guardamos el tipo seleccionado o autodetectado

        if tipo == "Autodetectar":
            hint = clasificar_ecuacion(ecuacion, y_func)
            if not hint:
                return None, "No se pudo clasificar la ecuación automáticamente. Intente especificar el tipo."
            tipo_resuelto = hint # Actualizamos el tipo resuelto al hint de sympy
        elif tipo == "Lineal":
            hint = '1st_Clinear'
        elif tipo == "Variables Separables":
            hint = 'separable'
        elif tipo == "Homogénea":
            hint = '1st_homogeneous_coeff_best'
        elif tipo == "Exacta":
            hint = '1st_exact'

        solucion = dsolve(ecuacion, y_func, hint=hint)
        procedimiento_texto = get_procedimiento_conceptual(tipo_resuelto)

        return solucion, procedimiento_texto

    except Exception as e:
        return None, f"Error al procesar la ecuación: {e}"