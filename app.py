import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box

# --- App Title ---
st.title("U.S. Grid Explorer 🌎")
st.markdown("Adjust the grid size below to overlay different resolutions on the U.S. map.")

# --- User Grid Selection ---
grid_km = st.radio(
    "Choose grid size (in kilometers):",
    [20, 50, 100],
    index=1,
    horizontal=True
)
grid_size = grid_km * 1000  # convert km to meters

# --- Load US shapefile (Albers Equal Area) ---
shp_path = "cb_2022_us_nation_20m/cb_2022_us_nation_20m.shp"
us = gpd.read_file(shp_path).to_crs(epsg=5070)

# --- Create grid over US bounding box ---
minx, miny, maxx, maxy = us.total_bounds
grid_cells = []
x = minx
while x < maxx:
    y = miny
    while y < maxy:
        cell = box(x, y, x + grid_size, y + grid_size)
        grid_cells.append(cell)
        y += grid_size
    x += grid_size

grid = gpd.GeoDataFrame({'geometry': grid_cells}, crs=us.crs)
grid_clipped = gpd.clip(grid, us)

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 8))
grid_clipped.boundary.plot(ax=ax, edgecolor="gray", linewidth=0.5)
us.boundary.plot(ax=ax, color="black", linewidth=0.8)
ax.set_title(f"Grid Overlay: {grid_km}×{grid_km} km", fontsize=14)
ax.set_axis_off()

st.pyplot(fig)
