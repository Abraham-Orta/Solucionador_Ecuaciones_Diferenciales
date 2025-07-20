import customtkinter as ctk
from solver import resolver_ecuacion
from sympy import preview, latex
from PIL import Image
import os
import tempfile

# Establece la apariencia de la aplicación (light/dark) y el tema de color
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Solucionador de Ecuaciones Diferenciales")
        self.geometry("600x950")

        # --- Configuración del Grid Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Permite que el frame de la solución se expanda

        # --- Frame Superior (Entrada y Botones de Símbolos) ---
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        self.label_ecuacion = ctk.CTkLabel(input_frame, text="Ecuación diferencial (ej: y' = x / y)")
        self.label_ecuacion.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

        self.entry_ecuacion = ctk.CTkEntry(input_frame, height=40, font=("Arial", 14))
        self.entry_ecuacion.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # --- Botonera de Símbolos ---
        simbolos_frame = ctk.CTkFrame(input_frame)
        simbolos_frame.grid(row=2, column=0, padx=5, pady=10)

        # Fila 1 de símbolos
        ctk.CTkButton(simbolos_frame, text="+", width=50, command=lambda: self.insertar_simbolo('+')).grid(row=0, column=0, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="-", width=50, command=lambda: self.insertar_simbolo('-')).grid(row=0, column=1, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="%", width=50, command=lambda: self.insertar_simbolo('%')).grid(row=0, column=2, padx=4, pady=4)
        # Separador visual
        
        ctk.CTkButton(simbolos_frame, text="/", width=50, command=lambda: self.insertar_simbolo('/')).grid(row=0, column=4, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="dy/dx", width=50, command=lambda: self.insertar_simbolo("dy/dx")).grid(row=0, column=5, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="dx/dy", width=50, command=lambda: self.insertar_simbolo("dx/dy")).grid(row=0, column=6, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="x", width=50, command=lambda: self.insertar_simbolo('x')).grid(row=0, column=7, padx=4, pady=4)
        
        # Fila 2 de símbolos
        ctk.CTkButton(simbolos_frame, text="e", width=50, command=lambda: self.insertar_simbolo('e')).grid(row=1, column=0, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="√()", width=50, command=lambda: self.insertar_simbolo_con_parentesis("sqrt")).grid(row=1, column=1, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="sin()", width=50, command=lambda: self.insertar_simbolo_con_parentesis("sin")).grid(row=1, column=2, padx=4, pady=4)
        # El separador ya ocupa la columna 3
        ctk.CTkButton(simbolos_frame, text="cos()", width=50, command=lambda: self.insertar_simbolo_con_parentesis("cos")).grid(row=1, column=4, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="tan()", width=50, command=lambda: self.insertar_simbolo_con_parentesis("tan")).grid(row=1, column=5, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="π", width=50, command=lambda: self.insertar_simbolo("pi")).grid(row=1, column=6, padx=4, pady=4)
        ctk.CTkButton(simbolos_frame, text="=", width=50, command=lambda: self.insertar_simbolo('=')).grid(row=1, column=7, padx=4, pady=4)

# --- Frame de Controles (Tipo de Ecuación y Acciones) ---
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        # Columna 1 (espacio flexible) tomará todo el espacio extra, empujando los botones a la derecha
        controls_frame.grid_columnconfigure(1, weight=1) 

        # --- Tipo de Ecuación ---
        ctk.CTkLabel(controls_frame, text="Tipo de ecuación:").grid(row=0, column=0, padx=(5,0), pady=5, sticky="w")
        self.tipo_ecuacion = ctk.CTkOptionMenu(controls_frame, values=["Autodetectar", "Variables Separables", "Lineal", "Homogénea", "Exacta"])
        self.tipo_ecuacion.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="w")

        # --- Botones de Acción ---
        self.boton_resolver = ctk.CTkButton(controls_frame, text="Resolver", height=35, command=self.resolver)
        self.boton_resolver.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.boton_limpiar = ctk.CTkButton(controls_frame, text="Limpiar", height=35, command=self.limpiar_todo,
                                           fg_color="transparent", 
                                           text_color=("gray10", "gray90"), 
                                           border_width=1,
                                           border_color="gray70")
        self.boton_limpiar.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Configurar las columnas para que los botones se expandan
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)

        # --- Frame de Procedimiento ---
        procedimiento_frame = ctk.CTkFrame(self)
        procedimiento_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        procedimiento_frame.grid_columnconfigure(0, weight=1)

        self.label_procedimiento = ctk.CTkLabel(procedimiento_frame, text="Procedimiento:", font=ctk.CTkFont(weight="bold"))
        self.label_procedimiento.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.texto_procedimiento = ctk.CTkTextbox(procedimiento_frame, height=150, wrap="word")
        self.texto_procedimiento.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

        # --- Frame de Solución ---
        solucion_frame = ctk.CTkFrame(self)
        solucion_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        solucion_frame.grid_columnconfigure(0, weight=1)
        solucion_frame.grid_rowconfigure(1, weight=1)

        self.label_solucion = ctk.CTkLabel(solucion_frame, text="Solución:", font=ctk.CTkFont(weight="bold"))
        self.label_solucion.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Scrollable frame para contener la imagen/texto de la solución
        self.solucion_container = ctk.CTkScrollableFrame(solucion_frame, fg_color="transparent")
        self.solucion_container.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.solucion_container.grid_columnconfigure(0, weight=1)
        self.solucion_widgets = [] # Lista para mantener referencia a los widgets de la solución

        # --- Label de Estado ---
        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(slant="italic"))
        self.status_label.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="w")


    def insertar_simbolo(self, simbolo):
        self.entry_ecuacion.insert(ctk.INSERT, simbolo)

    def insertar_simbolo_con_parentesis(self, funcion):
        """Inserta una función y coloca el cursor dentro de los paréntesis."""
        self.entry_ecuacion.insert(ctk.INSERT, f"{funcion}()")
        self.entry_ecuacion.icursor(self.entry_ecuacion.index(ctk.INSERT) - 1)

    def limpiar_todo(self):
        """Limpia la entrada, el procedimiento, la solución y el estado."""
        self.entry_ecuacion.delete(0, "end")
        self.texto_procedimiento.delete("1.0", "end")
        for widget in self.solucion_widgets:
            widget.destroy()
        self.solucion_widgets = []
        self.status_label.configure(text="")

    def _limpiar_resultados_anteriores(self):
        """Limpia solo las áreas de resultado antes de resolver."""
        self.texto_procedimiento.delete("1.0", "end")
        for widget in self.solucion_widgets:
            widget.destroy()
        self.solucion_widgets = []
        self.status_label.configure(text="")

    def _mostrar_mensaje_estado(self, mensaje, es_error=False):
        color = "#D32F2F" if es_error else "#388E3C" # Rojo para error, Verde para éxito
        self.status_label.configure(text=mensaje, text_color=color)

    def mostrar_texto_solucion(self, texto):
        label = ctk.CTkLabel(self.solucion_container, text=texto, wraplength=500)
        label.pack(pady=5, padx=5)
        self.solucion_widgets.append(label)

    def mostrar_imagen_solucion(self, ruta_imagen):
        try:
            img_original = Image.open(ruta_imagen)
            
            # Escalar la imagen para que se ajuste al ancho del contenedor
            container_width = self.solucion_container.winfo_width() - 30 # Ancho del frame - padding
            if container_width < 50: container_width = 500 # Valor por defecto si el frame no se ha dibujado

            ratio = container_width / img_original.width
            new_height = int(img_original.height * ratio)
            
            img_redimensionada = img_original.resize((container_width, new_height), Image.LANCZOS)

            solucion_img = ctk.CTkImage(light_image=img_redimensionada, size=(container_width, new_height))
            label = ctk.CTkLabel(self.solucion_container, image=solucion_img, text="")
            label.pack(pady=5, padx=5, expand=True)
            self.solucion_widgets.append(label)

        except Exception as e:
            self._mostrar_mensaje_estado(f"Error al mostrar imagen: {e}", es_error=True)
            self.mostrar_texto_solucion(f"No se pudo mostrar la imagen de la solución.\nError: {e}")
        finally:
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)

    def resolver(self):
        self._limpiar_resultados_anteriores()
        ecuacion = self.entry_ecuacion.get()

        if not ecuacion:
            self._mostrar_mensaje_estado("Por favor, introduce una ecuación.", es_error=True)
            return

        self._mostrar_mensaje_estado("Resolviendo...", es_error=False)
        self.boton_resolver.configure(state="disabled")
        self.update_idletasks() # Forzar actualización de la GUI

        try:
            tipo = self.tipo_ecuacion.get()
            solucion_obj, procedimiento_texto = resolver_ecuacion(ecuacion, tipo)
            
            self.texto_procedimiento.insert("1.0", procedimiento_texto)

            if solucion_obj is None:
                # If solver returns None, assume procedimiento_texto contains the error
                raise ValueError(procedimiento_texto if procedimiento_texto else "No se pudo resolver la ecuación.")

            # --- CORRECTED LATEX GENERATION ---
            # Use the align* environment for robust formatting of one or more lines.
            if isinstance(solucion_obj, list):
                latex_contenido = r"\\ ".join([latex(sol) for sol in solucion_obj])
            else:
                latex_contenido = latex(solucion_obj)
            
            # This format is more standard for sympy's preview function.
            latex_solucion = r"\begin{align*}" + latex_contenido + r"\end{align*}"
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                temp_filename = tmpfile.name
            
            # Call preview without the explicit preamble. It will load amsmath automatically for align*.
            preview(latex_solucion, viewer='file', filename=temp_filename, euler=False, dvioptions=["-D", "300"])

            self.mostrar_imagen_solucion(temp_filename)
            self._mostrar_mensaje_estado("Solución renderizada con éxito.", es_error=False)

        except Exception as e:
            error_msg = f"Error: {e}"
            self._mostrar_mensaje_estado(error_msg, es_error=True)
            self.mostrar_texto_solucion("No se pudo encontrar o renderizar la solución. Revisa la ecuación y el procedimiento.")
            # Ensure the error message from the solver is visible in the procedure box
            if not self.texto_procedimiento.get("1.0", "end").strip():
                self.texto_procedimiento.insert("1.0", error_msg)

        finally:
            self.boton_resolver.configure(state="normal")