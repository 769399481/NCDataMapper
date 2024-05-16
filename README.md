# NCDataMapper

 "NCDataMapper" is a Python application designed for exploring and visualizing geographical data stored in NetCDF files. With GeoPlotter, users can effortlessly upload NetCDF files, select parameters such as longitude, latitude, and data values, and generate interactive plots to visualize the spatial distribution of the data. The application offers features like zooming, panning, and saving images, providing users with the flexibility to analyze and interpret geographical datasets effectively. 

## Features

- Upload NetCDF Files: Easily upload NetCDF files for data exploration.
- Parameter Selection: Select parameters like longitude, latitude, and data values.
- Interactive Plots: Generate interactive plots for visualizing spatial data distribution.
- Zoom and Pan: Zoom in/out and pan across the plot for detailed analysis.
- Save Images: Save generated images for future reference.

## How to Use

1. Install Dependencies: Ensure you have Python installed, along with required libraries such as tkinter, numpy, matplotlib, cartopy, and netCDF4. You can install these dependencies using pip.
2. Run the Application: Execute the main.py script to launch NCDataMapper.
   ```
   python main.py
   ```
3. Upload File: Click on the "Upload NC File" button to select and upload your NetCDF file.
4. Select Parameters: Choose parameters for longitude, latitude, and data value from the dropdown menus.
5. Generate Plot: Click on "Generating" to generate the plot based on the selected parameters.
6. Interact with Plot: Zoom in/out, pan across the plot for detailed analysis.
7. Save Image: Save the generated plot as an image for future reference using the "Save Image" button.

![example image](https://github.com/769399481/NCDataMapper/blob/main/example.png)

## License:
This project is licensed under the MIT License. See the LICENSE file for details.
