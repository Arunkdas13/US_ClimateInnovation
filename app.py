import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import box
import streamlit as st

# --- Function to create grid ---
def create_grid(us_shape, grid_size):
    minx, miny, maxx, maxy = us_shape.total_bounds
    grid_cells = []
    x = minx
    while x < maxx:
        y = miny
        while y < maxy:
            grid_cells.append(box(x, y, x + grid_size, y + grid_size))
            y += grid_size
        x += grid_size
    grid = gpd.GeoDataFrame({'geometry': grid_cells}, crs=us_shape.crs)
    return gpd.clip(grid, us_shape)

# --- Function to simulate innovation data ---
def simulate_density(grid_gdf):
    np.random.seed(42)
    grid_gdf['hidden_champions'] = np.random.poisson(10, len(grid_gdf))
    return grid_gdf

# --- Main Streamlit App ---
st.set_page_config(layout="wide")
st.title("US Climate Innovation Grid Explorer")

# --- Grid size selection ---
grid_choice_km = st.selectbox("Select Grid Size (km):", [20, 50, 100])
grid_size_m = grid_choice_km * 1000

# --- Load U.S. shapefile ---
us = gpd.read_file('cb_2022_us_nation_20m/cb_2022_us_nation_20m.shp')
us = us.to_crs(epsg=5070)

# --- Generate and clip grid ---
grid = create_grid(us, grid_size_m)

# --- Simulate innovation data ---
grid_density = simulate_density(grid.copy())

# --- Plot 1: Grid only ---
fig1, ax1 = plt.subplots(figsize=(10, 6))
grid.boundary.plot(ax=ax1, edgecolor='red', linewidth=0.5)
us.boundary.plot(ax=ax1, color='black', linewidth=0.8)
ax1.set_title(f"{grid_choice_km}km Grid Overlay of U.S.", fontsize=14)
ax1.set_axis_off()
st.pyplot(fig1)

# --- Plot 2: Grid with Innovation Density ---
fig2, ax2 = plt.subplots(figsize=(10, 6))
grid_density.plot(
    column='hidden_champions',
    cmap='viridis_r',
    linewidth=0.2,
    edgecolor='white',
    ax=ax2,
    legend=True,
    legend_kwds={
        'label': "Simulated Innovation Density",
        'shrink': 0.6,
        'orientation': "vertical"
    },
    alpha=0.9
)
us.boundary.plot(ax=ax2, color='black', linewidth=0.5)
ax2.set_title(f"Simulated Innovation Density ({grid_choice_km}km Grid)", fontsize=14)
ax2.set_axis_off()
st.pyplot(fig2)
