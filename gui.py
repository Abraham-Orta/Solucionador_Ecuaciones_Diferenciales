import customtkinter as ctk
from solver import resolver_ecuacion

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Solucionador de Ecuaciones Diferenciales")
        self.geometry("600x400")

        self.grid_columnconfigure(0, weight=1)

        self.label_ecuacion = ctk.CTkLabel(self, text="Ecuación diferencial:")
        self.label_ecuacion.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.entry_ecuacion = ctk.CTkEntry(self, placeholder_text="Ej: y' = 2*x")
        self.entry_ecuacion.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.label_tipo = ctk.CTkLabel(self, text="Tipo de ecuación:")
        self.label_tipo.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.tipo_ecuacion = ctk.CTkOptionMenu(self, values=["Autodetectar", "Lineal", "Homogénea", "Variables Separables", "Exacta"])
        self.tipo_ecuacion.grid(row=3, column=0, padx=10, pady=10)

        self.boton_resolver = ctk.CTkButton(self, text="Resolver", command=self.resolver)
        self.boton_resolver.grid(row=4, column=0, padx=10, pady=20)

        self.label_solucion = ctk.CTkLabel(self, text="Solución:")
        self.label_solucion.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.texto_solucion = ctk.CTkTextbox(self, height=100)
        self.texto_solucion.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

    def resolver(self):
        ecuacion = self.entry_ecuacion.get()
        tipo = self.tipo_ecuacion.get()
        solucion = resolver_ecuacion(ecuacion, tipo)
        self.texto_solucion.delete("1.0", "end")
        self.texto_solucion.delete("1.0", "end")
        self.texto_solucion.insert("1.0", solucion)