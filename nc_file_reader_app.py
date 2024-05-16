import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NCFileReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NetCDF File Reader")
        self.root.geometry("1500x700")  # Larger window size

        self.file_path = ""
        self.parameters = []
        self.selected_parameters = {"lon": "", "lat": "", "value": ""}
        self.data = {}

        self.create_widgets()

    def create_widgets(self):
        # Frame for parameter selection
        parameter_frame = tk.Frame(self.root, width=200)
        parameter_frame.pack(side="left", fill="y", padx=20, pady=20)

        # File upload button
        upload_button = tk.Button(parameter_frame, text="Upload NC File", command=self.upload_file, width=15, bg="#F0F8FF", font=("Helvetica", 10), relief="ridge")
        upload_button.pack(pady=(0, 10), anchor="w")

        # Parameter selection dropdown menus
        lon_label = tk.Label(parameter_frame, text="Select Lon Parameter:", font=("Helvetica", 10), bg="#F0F8FF")
        lon_label.pack(anchor="w", padx=5, pady=(10, 2))

        self.lon_menu = tk.StringVar()
        self.lon_option_menu = tk.OptionMenu(parameter_frame, self.lon_menu, "")
        self.lon_option_menu.config(width=15)
        self.lon_option_menu.pack(anchor="w", padx=5, pady=(0, 10))

        lat_label = tk.Label(parameter_frame, text="Select Lat Parameter:", font=("Helvetica", 10), bg="#F0F8FF")
        lat_label.pack(anchor="w", padx=5, pady=(10, 2))

        self.lat_menu = tk.StringVar()
        self.lat_option_menu = tk.OptionMenu(parameter_frame, self.lat_menu, "")
        self.lat_option_menu.config(width=15)
        self.lat_option_menu.pack(anchor="w", padx=5, pady=(0, 10))

        value_label = tk.Label(parameter_frame, text="Select Value Parameter:", font=("Helvetica", 10), bg="#F0F8FF")
        value_label.pack(anchor="w", padx=5, pady=(10, 2))

        self.value_menu = tk.StringVar()
        self.value_option_menu = tk.OptionMenu(parameter_frame, self.value_menu, "")
        self.value_option_menu.config(width=15)
        self.value_option_menu.pack(anchor="w", padx=5, pady=(0, 10))


        # Confirm parameter button
        confirm_params_button = tk.Button(parameter_frame, text="Generating", command=self.show_params, width=15, bg="#F0F8FF", font=("Helvetica", 10), relief="ridge")
        confirm_params_button.pack(pady=10, anchor="w")

        # Zoom and pan buttons
        zoom_pan_frame = tk.Frame(parameter_frame, bg="#F0F8FF")
        zoom_pan_frame.pack(pady=(20, 0), anchor="w")

        zoom_in_button = tk.Button(zoom_pan_frame, text="Zoom In", command=self.zoom_in, width=10, bg="#F0F8FF", font=("Helvetica", 10), relief="ridge")
        zoom_in_button.pack(side="left", padx=(0, 5))

        zoom_out_button = tk.Button(zoom_pan_frame, text="Zoom Out", command=self.zoom_out, width=10, bg="#F0F8FF", font=("Helvetica", 10), relief="ridge")
        zoom_out_button.pack(side="left", padx=(0, 5))

        pan_button = tk.Button(zoom_pan_frame, text="Pan", command=self.activate_pan_zoom, width=10, bg="#F0F8FF", font=("Helvetica", 10), relief="ridge")
        pan_button.pack(side="left")

        # Save image button
        save_button = tk.Button(parameter_frame, text="Save Image", command=self.save_image, width=15, bg="#F0F8FF", font=("Helvetica", 10), relief="ridge")
        save_button.pack(pady=(20, 5), anchor="w")

        # Frame for displaying image
        display_frame = tk.Frame(self.root)
        display_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Plotting area
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_visible(False)
        self.canvas = FigureCanvasTkAgg(self.fig, master=display_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("NetCDF Files", "*.nc")])
        if self.file_path:
            self.get_parameters()
            messagebox.showinfo("Success", f"File Uploaded: {self.file_path}")
        else:
            messagebox.showerror("Error", "No file selected")

    def get_parameters(self):
        try:
            nc_file = Dataset(self.file_path, "r")
            self.parameters = list(nc_file.variables.keys())
            for param in self.parameters:
                self.data[param] = nc_file.variables[param][:]
            nc_file.close()

            # Update option menus with parameters
            self.update_option_menus()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open file: {e}")

    def update_option_menus(self):
        # Clear previous options
        self.lon_menu.set("")
        self.lat_menu.set("")
        self.value_menu.set("")

        # Update options with new parameters
        for parameter in self.parameters:
            self.lon_option_menu["menu"].add_command(label=parameter, command=tk._setit(self.lon_menu, parameter))
            self.lat_option_menu["menu"].add_command(label=parameter, command=tk._setit(self.lat_menu, parameter))
            self.value_option_menu["menu"].add_command(label=parameter, command=tk._setit(self.value_menu, parameter))

    def show_params(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please upload a file first")
            return

        # Update selected parameters
        self.selected_parameters["lon"] = self.lon_menu.get()
        self.selected_parameters["lat"] = self.lat_menu.get()
        self.selected_parameters["value"] = self.value_menu.get()

        # Display selected parameters
        messagebox.showinfo("Selected Parameters", f"Lon: {self.selected_parameters['lon']}\nLat: {self.selected_parameters['lat']}\nValue: {self.selected_parameters['value']}")

        # Plot data
        self.plot_data()

    def plot_data(self):
        lon_param = self.selected_parameters["lon"]
        lat_param = self.selected_parameters["lat"]
        value_param = self.selected_parameters["value"]

        if not lon_param or not lat_param or not value_param:
            messagebox.showerror("Error", "Please select parameters first")
            return

        lon_data = self.data[lon_param][:]
        lat_data = self.data[lat_param][:]
        value_data = self.data[value_param]

        data_3d_subset = value_data[:, :, :]

        lon_indices = np.arange(len(lon_data))
        lat_indices = np.arange(len(lat_data))

        data_subset = data_3d_subset[:, lat_indices, :][:, :, lon_indices]

        self.ax.clear()
        self.ax = plt.subplot(111, projection=ccrs.PlateCarree())
        self.ax.set_global()

        self.ax.add_feature(cfeature.COASTLINE)
        self.ax.add_feature(cfeature.BORDERS, linestyle=':')

        lon_2d, lat_2d = np.meshgrid(lon_data, lat_data)
        contour = self.ax.contourf(lon_2d, lat_2d, data_subset.mean(axis=0), cmap='Blues')

        self.fig.colorbar(contour, ax=self.ax, shrink=0.5)

        self.ax.set_xlabel('Longitude')
        self.ax.set_ylabel('Latitude')
        self.ax.gridlines(draw_labels=True)
        self.ax.set_visible(True)

        self.canvas.draw()

    def zoom_in(self):
        self.ax.set_xlim(self.ax.get_xlim()[0] * 1.1, self.ax.get_xlim()[1] * 1.1)
        self.ax.set_ylim(self.ax.get_ylim()[0] * 1.1, self.ax.get_ylim()[1] * 1.1)
        self.canvas.draw()

    def zoom_out(self):
        self.ax.set_xlim(self.ax.get_xlim()[0] * 0.9, self.ax.get_xlim()[1] * 0.9)
        self.ax.set_ylim(self.ax.get_ylim()[0] * 0.9, self.ax.get_ylim()[1] * 0.9)
        self.canvas.draw()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
        if file_path:
            self.fig.savefig(file_path)

    def activate_pan_zoom(self):
        plt.connect("motion_notify_event", self._update_pan_zoom)
        plt.connect("button_press_event", self._on_click_pan_zoom)
        plt.connect("button_release_event", self._off_click_pan_zoom)

    def _update_pan_zoom(self, event):
        if hasattr(self, 'pan_start'):
            dx = event.xdata - self.pan_start[0]
            dy = event.ydata - self.pan_start[1]
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            self.ax.set_xlim(xlim - dx)
            self.ax.set_ylim(ylim - dy)
            self.pan_start = (event.xdata, event.ydata)
            self.canvas.draw()

    def _on_click_pan_zoom(self, event):
        if event.button == 1:
            self.pan_start = (event.xdata, event.ydata)

    def _off_click_pan_zoom(self, event):
        if event.button == 1:
            del self.pan_start
