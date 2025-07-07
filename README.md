# Solucionador de Ecuaciones Diferenciales

Este proyecto es una aplicación de escritorio desarrollada en Python que permite a los usuarios resolver diferentes tipos de ecuaciones diferenciales ordinarias de primer orden. La aplicación cuenta con una interfaz gráfica intuitiva construida con `customtkinter`.


## Características

-   **Resolución de Ecuaciones Diferenciales**: Soporta la resolución de ecuaciones:
    -   De variables separables
    -   Lineales
    -   Homogéneas
    -   Exactas
-   **Detección Automática**: Puede detectar automáticamente el tipo de ecuación diferencial introducida.
-   **Interfaz Gráfica de Usuario**: Interfaz amigable y fácil de usar para introducir las ecuaciones y ver las soluciones.
-   **Visualización de Soluciones**: Muestra la solución de la ecuación de forma clara, utilizando LaTeX para una mejor presentación si está disponible en el sistema.
-   **Procedimiento Conceptual**: Ofrece una breve explicación del método utilizado para resolver la ecuación, ayudando al usuario a comprender el proceso.

## Requisitos

Para ejecutar este proyecto, es necesario tener Python y ciertas librerías instaladas. A continuación se detallan los requisitos para Windows y Linux.

### Requisitos Comunes

-   **Python 3**: Asegúrate de tener Python 3.6 o una versión más reciente.
-   **Git**: Necesario para clonar el repositorio.

### Windows

1.  **Instalar Python**: Si no lo tienes, descarga e instala la última versión de Python desde [python.org](https://www.python.org/downloads/). **Importante**: Durante la instalación, asegúrate de marcar la casilla que dice "Add Python to PATH".

2.  **Clonar el Repositorio**: Abre una terminal (Command Prompt o PowerShell) y ejecuta:
    ```bash
    git clone git@github.com:Abraham-Orta/Solucionador_Ecuaciones_Diferenciales.git
    cd Solucionador_Ecuaciones_Diferenciales
    ```

3.  **Crear un Entorno Virtual (Recomendado)**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

4.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Instalar LaTeX (Opcional pero Recomendado)**: Para que las soluciones se muestren con formato matemático (LaTeX), se recomienda instalar [MiKTeX](https://miktex.org/download). Instálalo y asegúrate de que los paquetes se instalen automáticamente la primera vez que se usen.

### Linux

1.  **Instalar Python y Git**: La mayoría de las distribuciones de Linux ya vienen con Python y Git. Si no, puedes instalarlos con el gestor de paquetes de tu distribución. Para sistemas basados en Debian/Ubuntu:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv git -y
    ```

2.  **Clonar el Repositorio**:
    ```bash
    git clone https://github.com/Abraham-Lozano/solucionador_ecuaciones_diferenciales.git
    cd solucionador_ecuaciones_diferenciales
    ```

3.  **Crear un Entorno Virtual (Recomendado)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Instalar LaTeX (Opcional pero Recomendado)**: Para el renderizado de ecuaciones con LaTeX, necesitas una distribución de TeX. Puedes instalar TeX Live, que es una opción completa:
    ```bash
    sudo apt install texlive-full -y
    ```
    **Nota**: Esta instalación puede ser grande. Una alternativa más ligera es `texlive-latex-base` junto con `dvipng`:
    ```bash
    sudo apt install texlive-latex-base dvipng -y
    ```

## Uso

1.  Clona este repositorio en tu máquina local.
2.  Instala las dependencias como se describe en la sección de Requisitos.
3.  Ejecuta el programa principal:

```bash
python main.py
```

4.  Introduce la ecuación diferencial en el campo de texto. Asegúrate de usar la notación correcta (por ejemplo, `y'` para la derivada de y).
5.  Selecciona el tipo de ecuación o deja que el programa lo detecte automáticamente.
6.  Haz clic en "Resolver" para obtener la solución y el procedimiento.

## Estructura del Proyecto y Detalles Técnicos

El proyecto está estructurado en varios ficheros Python, cada uno con una responsabilidad clara:

-   `main.py`: Es el punto de entrada de la aplicación. Su única función es instanciar y ejecutar la interfaz gráfica.
-   `gui.py`: Contiene toda la lógica de la interfaz de usuario. Se encarga de:
    -   Crear y posicionar los widgets (etiquetas, campos de texto, botones) usando `customtkinter`.
    -   Capturar la entrada del usuario (la ecuación y el tipo seleccionado).
    -   Llamar al `solver.py` para procesar la ecuación.
    -   Mostrar el procedimiento y la solución en la interfaz. Si LaTeX está instalado, intenta renderizar la solución como una imagen para una mejor legibilidad. En caso contrario, muestra la solución como texto plano.
-   `solver.py`: Es el cerebro de la aplicación. Aquí reside la lógica para resolver las ecuaciones diferenciales:
    -   Utiliza la librería `sympy` para el manejo simbólico de las matemáticas.
    -   **Parsing de la Ecuación**: Convierte la cadena de texto introducida por el usuario en una expresión simbólica que `sympy` pueda entender.
    -   **Clasificación**: Emplea la función `classify_ode` de `sympy` para determinar el tipo de la ecuación diferencial si el usuario elige la opción "Autodetectar".
    -   **Resolución**: Utiliza `dsolve` de `sympy` para encontrar la solución a la ecuación. Se le pasa un "hint" (pista) basado en la selección del usuario o en la clasificación automática para guiar al solver.
    -   **Generación de Procedimiento**: Proporciona una explicación conceptual de alto nivel sobre el método de resolución que se está utilizando.
-   `requirements.txt`: Lista las dependencias de Python necesarias para el proyecto.

### Flujo de Funcionamiento

1.  El usuario ejecuta `main.py`.
2.  Se crea una instancia de la clase `App` de `gui.py`, mostrando la ventana principal.
3.  El usuario introduce una ecuación (p. ej., `y' = 2*x`), selecciona un tipo (p. ej., "Variables Separables") y hace clic en "Resolver".
4.  El método `resolver` en `gui.py` se activa. Recoge la ecuación y el tipo.
5.  Se llama a la función `resolver_ecuacion` de `solver.py`.
6.  En `solver.py`:
    -   La ecuación se parsea a un objeto `Eq` de `sympy`.
    -   Se determina el `hint` para `dsolve`.
    -   `dsolve` resuelve la ecuación.
    -   Se genera el texto del procedimiento conceptual.
7.  `solver.py` devuelve el objeto de la solución de `sympy` y el texto del procedimiento a `gui.py`.
8.  En `gui.py`:
    -   El texto del procedimiento se muestra en su área correspondiente.
    -   Se intenta renderizar la solución con `sympy.preview`, que usa LaTeX para crear una imagen PNG (`solucion.png`).
    -   Si tiene éxito, la imagen se muestra en la GUI. Si falla (p. ej., no hay LaTeX), la solución se convierte a texto plano y se muestra en su lugar.

