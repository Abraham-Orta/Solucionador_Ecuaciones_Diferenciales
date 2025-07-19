from sympy import dsolve, Eq, symbols, Function, Derivative, classify_ode
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import re

def clasificar_ecuacion(ecuacion, y_func):
    """Clasifica la ecuación diferencial y devuelve el mejor hint."""
    mapa_hints = {
        'separable': 'separable',
        '1st_linear': '1st_linear',
        '1st_homogeneous_coeff_best': '1st_homogeneous_coeff_best',
        'exact': '1st_exact'
    }
    clasificacion = classify_ode(ecuacion, y_func)
    for hint in clasificacion:
        if hint in mapa_hints:
            return mapa_hints[hint]
    return clasificacion[0] if clasificacion else None

def get_procedimiento_conceptual(tipo_resuelto):
    procedimiento = f"Tipo de Ecuación Detectado/Seleccionado: {tipo_resuelto}\n\n"
    if tipo_resuelto == "separable":
        procedimiento += "Procedimiento Conceptual:\n1. Separar las variables x e y.\n2. Integrar ambos lados.\n3. Despejar y(x)."
    elif tipo_resuelto == "1st_linear":
        procedimiento += "Procedimiento Conceptual:\n1. Forma estándar: y' + P(x)y = Q(x).\n2. Factor integrante: e^(∫P(x)dx).\n3. Multiplicar por factor integrante.\n4. Integrar para solución general."
    elif tipo_resuelto == "1st_homogeneous_coeff_best":
        procedimiento += "Procedimiento Conceptual:\n1. Sustitución y = v*x.\n2. Transformar a ecuación de variables separables.\n3. Resolver para v.\n4. Sustituir v = y/x."
    elif tipo_resuelto == "1st_exact":
        procedimiento += "Procedimiento Conceptual:\n1. Forma M(x,y)dx + N(x,y)dy = 0.\n2. Verificar ∂M/∂y = ∂N/∂x.\n3. Encontrar función potencial F(x,y).\n4. Solución general F(x,y) = C."
    else:
        procedimiento += "Procedimiento no disponible."
    return procedimiento

def normalizar_ecuacion(ecuacion_str):
    """
    Normaliza la ecuación a y_prime para el solver.
    """
    # Reemplaza dy/dx por y_prime
    ecuacion_str = re.sub(r"d\s*y\s*/\s*d\s*x", "y_prime", ecuacion_str)
    # Reemplaza y'(x) o y' por y_prime
    ecuacion_str = re.sub(r"y\s*'(?:\s*\(\s*x\s*\))?", "y_prime", ecuacion_str)
    return ecuacion_str

def resolver_ecuacion(ecuacion_str, tipo):
    try:
        ecuacion_str_normalizada = normalizar_ecuacion(ecuacion_str)
        x = symbols('x')
        y_func = Function('y')(x)
        y_deriv = Derivative(y_func, x)

        local_dict = {
            'y': y_func,
            'x': x,
            'y_prime': y_deriv
        }

        transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

        if '=' not in ecuacion_str_normalizada:
            return None, "Error: La ecuación debe contener un signo '='."

        partes = ecuacion_str_normalizada.split('=', 1)
        lhs_str = partes[0].strip()
        rhs_str = partes[1].strip()

        lhs_expr = parse_expr(lhs_str, local_dict=local_dict, transformations=transformations)
        rhs_expr = parse_expr(rhs_str, local_dict=local_dict, transformations=transformations)

        ecuacion = Eq(lhs_expr, rhs_expr)

        hint = ''
        tipo_resuelto = tipo

        if tipo == "Autodetectar":
            hint = clasificar_ecuacion(ecuacion, y_func)
            if not hint:
                return None, "No se pudo clasificar la ecuación."
            tipo_resuelto = hint
        elif tipo == "Lineal":
            hint = '1st_linear'
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