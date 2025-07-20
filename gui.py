import customtkinter as ctk
from solver import resolver_ecuacion
from sympy import preview, Symbol, latex
from PIL import Image
import os
import tempfile

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Solucionador de Ecuaciones Diferenciales")
        self.geometry("700x800") # Aumentamos el tamaño para los botones y procedimiento

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1) # Ajustamos la fila para la solución

        self.label_ecuacion = ctk.CTkLabel(self, text="Ecuación diferencial (ej: y' = 2*x / y ):")
        self.label_ecuacion.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.entry_ecuacion = ctk.CTkEntry(self, placeholder_text="y' = (x**2 + 2) / (3*y**2)")
        self.entry_ecuacion.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Frame para los botones de símbolos
        self.simbolos_frame = ctk.CTkFrame(self)
        self.simbolos_frame.grid(row=2, column=0, padx=10, pady=5)
        self.simbolos_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        simbolos_fila1 = ['+', '-', '*', '/', '^', '(', ')', "y'", 'x', 'dy/dx']
        for i, simbolo in enumerate(simbolos_fila1):
            boton = ctk.CTkButton(self.simbolos_frame, text=simbolo, width=60, command=lambda s=simbolo: self.insertar_simbolo(s))
            boton.grid(row=0, column=i, padx=5, pady=5)

        simbolos_fila2 = ['e', 'sqrt()', 'sin()', 'cos()', 'tan()', 'log()', 'pi', '=']
        for i, simbolo in enumerate(simbolos_fila2):
            boton = ctk.CTkButton(self.simbolos_frame, text=simbolo, width=60, command=lambda s=simbolo: self.insertar_simbolo(s))
            boton.grid(row=1, column=i, padx=5, pady=5)

        self.label_tipo = ctk.CTkLabel(self, text="Tipo de ecuación:")
        self.label_tipo.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.tipo_ecuacion = ctk.CTkOptionMenu(self, values=["Autodetectar", "Variables Separables", "Lineal", "Homogénea", "Exacta"])
        self.tipo_ecuacion.grid(row=4, column=0, padx=10, pady=5)

        self.boton_resolver = ctk.CTkButton(self, text="Resolver", command=self.resolver)
        self.boton_resolver.grid(row=5, column=0, padx=10, pady=10)

        # Nuevo: Área para el procedimiento
        self.label_procedimiento = ctk.CTkLabel(self, text="Procedimiento:")
        self.label_procedimiento.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.texto_procedimiento = ctk.CTkTextbox(self, height=150) # Altura para el procedimiento
        self.texto_procedimiento.grid(row=7, column=0, padx=10, pady=5, sticky="nsew")

        self.label_solucion = ctk.CTkLabel(self, text="Solución:")
        self.label_solucion.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="ew")

        # Frame para contener la solución (texto o imagen)
        self.solucion_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.solucion_frame.grid(row=9, column=0, padx=10, pady=5, sticky="nsew")
        self.solucion_frame.grid_rowconfigure(0, weight=1)
        self.solucion_frame.grid_columnconfigure(0, weight=1)

        # Widget de texto (para errores o fallback)
        self.texto_solucion = ctk.CTkTextbox(self.solucion_frame, height=100)
        # Se mostrará u ocultará según sea necesario

        # Nuevo: ScrollableFrame para la imagen de la solución
        self.scrollable_solucion_frame = ctk.CTkScrollableFrame(self.solucion_frame, fg_color="transparent")
        self.scrollable_solucion_frame.grid(row=0, column=0, sticky="nsew")
        self.scrollable_solucion_frame.grid_columnconfigure(0, weight=1)

        # Widget de imagen (para la solución LaTeX) dentro del scrollable frame
        self.imagen_solucion_label = ctk.CTkLabel(self.scrollable_solucion_frame, text="")
        self.solucion_img = None # Para mantener una referencia a la imagen

        # Nuevo: Label para mensajes de estado/error
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.grid(row=10, column=0, padx=10, pady=5, sticky="ew")

    def insertar_simbolo(self, simbolo):
        self.entry_ecuacion.insert(ctk.INSERT, simbolo)

    def _limpiar_resultados(self):
        self.texto_procedimiento.delete("1.0", "end")
        self.texto_solucion.delete("1.0", "end")
        self.imagen_solucion_label.grid_forget()
        self.texto_solucion.grid_forget()
        self.status_label.configure(text="")
        # Asegurarse de ocultar el scrollable frame también
        self.scrollable_solucion_frame.grid_forget()

    def _mostrar_mensaje_estado(self, mensaje, es_error=False):
        color = "red" if es_error else "green"
        self.status_label.configure(text=mensaje, text_color=color)

    def mostrar_texto_solucion(self, texto):
        self.scrollable_solucion_frame.grid_forget() # Ocultar scrollable frame
        self.texto_solucion.grid(row=0, column=0, sticky="nsew") # Mostrar texto
        self.texto_solucion.delete("1.0", "end")
        self.texto_solucion.insert("1.0", texto)

    def mostrar_imagen_solucion(self, ruta_imagen):
        self.texto_solucion.grid_forget() # Ocultar texto
        self.scrollable_solucion_frame.grid(row=0, column=0, sticky="nsew") # Mostrar scrollable frame
        try:
            img = Image.open(ruta_imagen)
            img_width, img_height = img.size

            # Definir un tamaño máximo para la visualización inicial sin scroll
            # Si la imagen es más grande que esto, se mostrará en su tamaño original dentro del scrollable frame
            max_display_width = self.solucion_frame.winfo_width() # Ancho del frame contenedor
            max_display_height = 400 # Altura máxima deseada para la imagen sin scroll

            # Escalar solo si la imagen es significativamente más grande que el área visible
            if img_width > max_display_width or img_height > max_display_height:
                ratio = min(max_display_width / img_width, max_display_height / img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                # Solo escalamos si la imagen es realmente grande, de lo contrario, la mostramos en su tamaño original
                if new_width < img_width or new_height < img_height:
                    img = img.resize((new_width, new_height), Image.LANCZOS)

            self.solucion_img = ctk.CTkImage(light_image=img, size=img.size)
            self.imagen_solucion_label.configure(image=self.solucion_img)
            self.imagen_solucion_label.grid(row=0, column=0, sticky="nsew") # Mostrar imagen dentro del scrollable frame
        except Exception as e:
            self._mostrar_mensaje_estado(f"Error al mostrar la imagen: {e}", es_error=True)
            self.mostrar_texto_solucion(f"No se pudo mostrar la imagen de la solución.\nError: {e}")
        finally:
            # Asegurarse de eliminar el archivo temporal después de usarlo
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)

    def resolver(self):
        self._limpiar_resultados()
        self._mostrar_mensaje_estado("Resolviendo...", es_error=False)
        self.boton_resolver.configure(state="disabled")

        ecuacion = self.entry_ecuacion.get()
        tipo = self.tipo_ecuacion.get()

        if not ecuacion:
            self._mostrar_mensaje_estado("Por favor, introduce una ecuación.", es_error=True)
            self.boton_resolver.configure(state="normal")
            return

        solucion_obj, procedimiento_texto = resolver_ecuacion(ecuacion, tipo)

        # Mostrar el procedimiento
        self.texto_procedimiento.insert("1.0", procedimiento_texto)

        # Si la solución es None, es un error o un mensaje.
        if solucion_obj is None:
            self._mostrar_mensaje_estado(f"Error al resolver: {procedimiento_texto}", es_error=True)
            self.mostrar_texto_solucion("No se pudo encontrar una solución o hubo un error. Revisa el mensaje de error.")
            self.boton_resolver.configure(state="normal")
            return

        # Si es una solución de SymPy, intentamos renderizarla con LaTeX
        try:
            # Generar la representación LaTeX de la solución
            # Usamos mode='inline' y lo envolvemos en '$' para que preview funcione correctamente
            latex_solucion = f"${latex(solucion_obj, mode='inline')}$"

            # Crear un archivo temporal para guardar la imagen de la solución
            # delete=False porque la función mostrar_imagen_solucion lo eliminará
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                temp_filename = tmpfile.name
            
            # Generar la imagen PNG a partir del código LaTeX
            preview(latex_solucion, viewer='file', filename=temp_filename, euler=False, dvioptions=['-D', '200'])

            # Mostrar la imagen en la GUI
            self.mostrar_imagen_solucion(temp_filename)
            self._mostrar_mensaje_estado("Solución renderizada con éxito.", es_error=False)

        except Exception as e:
            # Si la generación de LaTeX/imagen falla, mostramos la versión en texto plano como fallback.
            self._mostrar_mensaje_estado(f"No se pudo renderizar la solución con LaTeX: {e}", es_error=True)
            fallback_texto = f"Solución (texto plano):\n{str(solucion_obj)}"
            self.mostrar_texto_solucion(fallback_texto)
        finally:
            self.boton_resolver.configure(state="normal")