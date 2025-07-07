import customtkinter as ctk
from solver import resolver_ecuacion
from sympy import preview, Symbol
from PIL import Image
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Solucionador de Ecuaciones Diferenciales")
        self.geometry("700x700") # Aumentamos el tamaño para el procedimiento

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1) # Ajustamos la fila para la solución

        self.label_ecuacion = ctk.CTkLabel(self, text="Ecuación diferencial (ej: y' = 2*x / y ):")
        self.label_ecuacion.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.entry_ecuacion = ctk.CTkEntry(self, placeholder_text="y' = (x**2 + 2) / (3*y**2)")
        self.entry_ecuacion.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.label_tipo = ctk.CTkLabel(self, text="Tipo de ecuación:")
        self.label_tipo.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.tipo_ecuacion = ctk.CTkOptionMenu(self, values=["Autodetectar", "Variables Separables", "Lineal", "Homogénea", "Exacta"])
        self.tipo_ecuacion.grid(row=3, column=0, padx=10, pady=5)

        self.boton_resolver = ctk.CTkButton(self, text="Resolver", command=self.resolver)
        self.boton_resolver.grid(row=4, column=0, padx=10, pady=10)

        # Nuevo: Área para el procedimiento
        self.label_procedimiento = ctk.CTkLabel(self, text="Procedimiento:")
        self.label_procedimiento.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.texto_procedimiento = ctk.CTkTextbox(self, height=150) # Altura para el procedimiento
        self.texto_procedimiento.grid(row=6, column=0, padx=10, pady=5, sticky="nsew")

        self.label_solucion = ctk.CTkLabel(self, text="Solución:")
        self.label_solucion.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="ew")

        # Frame para contener la solución (texto o imagen)
        self.solucion_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.solucion_frame.grid(row=8, column=0, padx=10, pady=5, sticky="nsew")
        self.solucion_frame.grid_rowconfigure(0, weight=1)
        self.solucion_frame.grid_columnconfigure(0, weight=1)

        # Widget de texto (para errores o fallback)
        self.texto_solucion = ctk.CTkTextbox(self.solucion_frame, height=100)
        # Se mostrará u ocultará según sea necesario

        # Widget de imagen (para la solución LaTeX)
        self.imagen_solucion_label = ctk.CTkLabel(self.solucion_frame, text="")
        self.solucion_img = None # Para mantener una referencia a la imagen

    def mostrar_texto(self, texto):
        self.imagen_solucion_label.grid_forget() # Ocultar imagen
        self.texto_solucion.grid(row=0, column=0, sticky="nsew") # Mostrar texto
        self.texto_solucion.delete("1.0", "end")
        self.texto_solucion.insert("1.0", texto)

    def mostrar_imagen(self, ruta_imagen):
        self.texto_solucion.grid_forget() # Ocultar texto
        try:
            self.solucion_img = ctk.CTkImage(light_image=Image.open(ruta_imagen), size=Image.open(ruta_imagen).size)
            self.imagen_solucion_label.configure(image=self.solucion_img)
            self.imagen_solucion_label.grid(row=0, column=0, sticky="nsew") # Mostrar imagen
        except Exception as e:
            self.mostrar_texto(f"No se pudo mostrar la imagen de la solución.\nError: {e}")

    def resolver(self):
        ecuacion = self.entry_ecuacion.get()
        tipo = self.tipo_ecuacion.get()

        if not ecuacion:
            self.mostrar_texto("Por favor, introduce una ecuación.")
            return

        solucion_obj, procedimiento_texto = resolver_ecuacion(ecuacion, tipo)

        # Mostrar el procedimiento
        self.texto_procedimiento.delete("1.0", "end")
        self.texto_procedimiento.insert("1.0", procedimiento_texto)

        # Si la solución es None, es un error o un mensaje.
        if solucion_obj is None:
            self.mostrar_texto(procedimiento_texto) # El procedimiento_texto ya contiene el error
            return

        # Si es una solución de SymPy, intentamos renderizarla con LaTeX.
        try:
            # Usamos un nombre de archivo temporal para la imagen
            nombre_archivo = "solucion.png"
            # viewer='file' y output='png' son claves para que guarde el archivo
            preview(solucion_obj, viewer='file', filename=nombre_archivo, dvioptions=["-D", "170"])
            
            # Si preview() funcionó, el archivo existe. Lo mostramos.
            self.mostrar_imagen(nombre_archivo)

        except Exception as e:
            # Si preview() falla (ej. no hay LaTeX), mostramos la versión en texto.
            fallback_texto = f"No se pudo renderizar con LaTeX.\n\nError específico: {e}\n\nSolución (texto plano):\n{str(solucion_obj)}"
            self.mostrar_texto(fallback_texto)
