import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

# Dummy AI logic to simulate optimization based on patterns
def ai_optimize(settings):
    optimized = settings.copy()
    optimized['Thermostat'] = max(18, min(settings['Thermostat'] - 1, 24))
    optimized['Lighting'] = max(0.5, settings['Lighting'] - 0.2)
    optimized['Appliance Usage'] = max(0.5, settings['Appliance Usage'] - 0.3)
    return optimized

# Suggestion generator based on AI output
def generate_suggestions(optimized):
    suggestions = []
    if optimized['Thermostat'] < 20:
        suggestions.append("Consider wearing warmer clothes to save heating energy.")
    if optimized['Lighting'] < 0.8:
        suggestions.append("Make use of natural daylight whenever possible.")
    if optimized['Appliance Usage'] < 0.8:
        suggestions.append("Unplug appliances when not in use to avoid phantom loads.")
    return suggestions

class EnergyOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Energy Efficiency Optimizer")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f7")

        self.settings = {
            'Thermostat': 22,
            'Lighting': 1.0,
            'Appliance Usage': 1.0
        }

        self.optimized_settings = self.settings.copy()
        self.suggestions = []

        self.build_gui()

    def build_gui(self):
        title = tk.Label(self.root, text="Energy Efficiency Optimization", font=("Arial", 20, "bold"), bg="#f0f4f7")
        title.pack(pady=10)

        # Frame for sliders
        controls_frame = tk.Frame(self.root, bg="#f0f4f7")
        controls_frame.pack(pady=10)

        # Thermostat input (Spinbox)
        tk.Label(controls_frame, text="Thermostat (°C):", bg="#f0f4f7").grid(row=0, column=0, sticky="w")
        self.thermostat_var = tk.IntVar(value=self.settings['Thermostat'])
        thermostat_spinbox = ttk.Spinbox(controls_frame, from_=18, to=24, textvariable=self.thermostat_var, width=5)
        thermostat_spinbox.grid(row=0, column=1, padx=10)

        # Lighting input (Spinbox)
        tk.Label(controls_frame, text="Lighting (0.0 - 1.0):", bg="#f0f4f7").grid(row=1, column=0, sticky="w")
        self.lighting_var = tk.DoubleVar(value=self.settings['Lighting'])
        lighting_spinbox = ttk.Spinbox(controls_frame, from_=0.0, to=1.0, increment=0.1, textvariable=self.lighting_var, width=5, format="%.1f")
        lighting_spinbox.grid(row=1, column=1, padx=10)

        # Appliance Usage input (Spinbox)
        tk.Label(controls_frame, text="Appliance Usage (0.0 - 1.0):", bg="#f0f4f7").grid(row=2, column=0, sticky="w")
        self.appliance_var = tk.DoubleVar(value=self.settings['Appliance Usage'])
        appliance_spinbox = ttk.Spinbox(controls_frame, from_=0.0, to=1.0, increment=0.1, textvariable=self.appliance_var, width=5, format="%.1f")
        appliance_spinbox.grid(row=2, column=1, padx=10)

        # Optimize button
        optimize_button = ttk.Button(self.root, text="Optimize", command=self.optimize)
        optimize_button.pack(pady=10)

        # Suggestions label
        self.suggestions_label = tk.Label(self.root, text="", bg="#f0f4f7", justify="left", font=("Arial", 12))
        self.suggestions_label.pack(pady=10)

        # Plot area
        self.figure = plt.Figure(figsize=(6,3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.plot_settings(self.settings, self.optimized_settings)

    def optimize(self):
        # Get current settings from sliders
        current_settings = {
            'Thermostat': self.thermostat_var.get(),
            'Lighting': self.lighting_var.get(),
            'Appliance Usage': self.appliance_var.get()
        }

        # Run AI optimization in a separate thread to avoid UI freeze
        threading.Thread(target=self.run_optimization, args=(current_settings,), daemon=True).start()

    def run_optimization(self, current_settings):
        optimized = ai_optimize(current_settings)
        suggestions = generate_suggestions(optimized)

        # Update UI in the main thread
        self.root.after(0, self.update_ui, optimized, suggestions)

    def update_ui(self, optimized, suggestions):
        self.optimized_settings = optimized
        self.suggestions = suggestions

        # Update suggestions label
        suggestions_text = "Suggestions:\n" + "\n".join(f"- {s}" for s in suggestions) if suggestions else "No suggestions. Your settings are optimized!"
        self.suggestions_label.config(text=suggestions_text)

        # Update plot
        self.plot_settings(self.settings, optimized)

    def plot_settings(self, original, optimized):
        self.ax.clear()
        categories = list(original.keys())
        original_values = [original[c] for c in categories]
        optimized_values = [optimized[c] for c in categories]

        bar_width = 0.35
        indices = range(len(categories))

        self.ax.bar(indices, original_values, bar_width, label='Original')
        self.ax.bar([i + bar_width for i in indices], optimized_values, bar_width, label='Optimized')

        self.ax.set_xticks([i + bar_width / 2 for i in indices])
        self.ax.set_xticklabels(categories)
        self.ax.set_ylim(0, max(max(original_values), max(optimized_values)) + 5)
        self.ax.legend()
        self.ax.set_title("Energy Settings Comparison")

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnergyOptimizerApp(root)
    root.mainloop()
