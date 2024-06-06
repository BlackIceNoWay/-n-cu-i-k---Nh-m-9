import math
import random
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TSPSolver import Backtrack, BackTrackUp
import time
import tracemalloc

# Create the main window
root = tk.Tk()
root.title("TSP Solver")

# Define city names and coordinates
citis_name = ["Hà Nội", "HCM", "Hải Phòng", "Đà Nẵng"]
x_coordinates = [0, 6, 3, 3]
y_coordinates = [0, 0, 6, 3]

# Define distances between cities
locations = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
num_locations = len(locations)
# Create the TSP solver instances
solver = Backtrack(locations)
solverU = BackTrackUp(locations)

# Function to handle the Solve button click
def solbut():
    start = combo_box.current()
    v = [False] * num_locations
    v[start] = True

    # Solve using Backtrack
    start_time1 = time.perf_counter()
    tracemalloc.start()
    solver.tsp(locations, v, start, start, num_locations, 1, 0, [start])
    min_dist = min(solver.answer)
    for i, dist in enumerate(solver.answer):
        if dist == min_dist:
            best_paths = solver.paths[i]
            best_path_cities_name = [citis_name[j] for j in best_paths]
            best_dist = min_dist
    end_time1 = time.perf_counter()
    time_solve1 = (end_time1 - start_time1) * 10**3
    memory1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result_label1.config(text=f"Best path (BackTrack): {best_path_cities_name}\nBest distance: {best_dist:.2f}\nTime: {time_solve1:.2f}ms\nMemory: {memory1[1] / 1024:.2f}KB")
    plot_graph(best_paths, canvas1, ax1, "BackTrack Algorithm")
    update_table(solver.paths, solver.answer, start)

    # Solve using BackTrackUp
    solverU.reset()  # Reset the solver
    start_time2 = time.perf_counter()
    tracemalloc.start()
    solverU.tspu(locations, v, start, start, num_locations, 1, 0, [start],0)
    end_time2 = time.perf_counter()
    best_pathU = solverU.min_path
    best_path_cities_nameU = [citis_name[j] for j in best_pathU]
    best_distU = solverU.min_cost
    time_solve2 = (end_time2 - start_time2) * 10**3
    memory2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result_label2.config(text=f"Best path (BackTrackUp): {best_path_cities_nameU}\nBest distance: {best_distU:.2f}\nTime: {time_solve2:.2f}ms\nMemory: {memory2[1] / 1024:.2f}KB")
    plot_graph(best_pathU, canvas2, ax2, "BackTrackUp Algorithm")

# Function to reset the table when a new start point is selected
def reset_table(event):
    for row in tree.get_children():
        tree.delete(row)
    result_label1.config(text="")
    result_label2.config(text="")

# Create map frame
frame_map = ttk.Frame(root)
frame_map.pack(pady=10)

# Create control frame
frame_controls = ttk.Frame(frame_map)
frame_controls.pack(pady=10, padx=10, anchor="w")

# Create start point label
lbl_start_text = ttk.Label(frame_controls, text="Choose a starting point:")
lbl_start_text.grid(row=0, column=0, padx=5, sticky="E")

# Create Combobox for selecting start point
combo_box = ttk.Combobox(root, values=citis_name)
combo_box.pack()
combo_box.bind("<<ComboboxSelected>>", reset_table)  # Bind the reset_table function to combobox selection

# Create Solve button
solve_button = tk.Button(root, text="Solve", command=solbut)
solve_button.pack()

# Create labels for displaying results
result_label1 = tk.Label(root)
result_label1.pack()
result_label2 = tk.Label(root)
result_label2.pack()

# Create figure and axes for the graphs
fig1, ax1 = plt.subplots(figsize=(6, 6))
fig2, ax2 = plt.subplots(figsize=(6, 6))

# Create canvas to display the graphs
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.get_tk_widget().pack(side=tk.LEFT, padx=10)
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.get_tk_widget().pack(side=tk.RIGHT, padx=10)

# Create treeview for displaying all paths and distances
tree = ttk.Treeview(root, columns=("Path", "Distance"), show="headings")
tree.heading("Path", text="Path")
tree.heading("Distance", text="Distance")
tree.pack()

# Set specific column widths if needed
tree.column("Path", width=450)
tree.column("Distance", width=150)

# Function to update the table with all paths and distances
def update_table(paths, distances, start):
    for row in tree.get_children():
        tree.delete(row)
    for path, distance in zip(paths, distances):
        if path[0] == start:  # Only show paths that start from the selected start point
            named_path = ' -> '.join([citis_name[i] for i in path])
            tree.insert("", "end", values=(named_path, f"{distance:.2f}"))

# Function to plot the graph
def plot_graph(path, canvas, ax, title):
    ax.clear()

    # Plot locations as points
    scatter = ax.scatter(x_coordinates, y_coordinates, c='red', s=50)

    # Plot path as arrows
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        ax.annotate("", xy=(x_coordinates[end], y_coordinates[end]), xytext=(x_coordinates[start], y_coordinates[start]),
                    arrowprops=dict(arrowstyle="->", color="blue"))

    # Connect all points with dotted lines and show distances
    for i in range(num_locations):
        for j in range(i + 1, num_locations):
            x_start = x_coordinates[i]
            y_start = y_coordinates[i]
            x_end = x_coordinates[j]
            y_end = y_coordinates[j]
            distance = locations[i][j]
            ax.plot([x_start, x_end], [y_start, y_end], 'k--', alpha=0.2)
            ax.text((x_start + x_end) / 2, (y_start + y_end) / 2, f"{distance:.2f}", ha='center', va='center')
            if j == num_locations - 1:
                ax.text(x_end, y_end, citis_name[j], ha='left', va='bottom')
            ax.text(x_coordinates[i], y_coordinates[i], citis_name[i], ha='right', va='top')

    # Highlight the starting point in green
    if path:
        start_index = path[0]
        scatter.set_facecolors(['green' if i == start_index else 'red' for i in range(num_locations)])

    # Set the title of the graph
    ax.set_title(title)

    # Refresh the plot
    plt.tight_layout()
    canvas.draw()

# Initial plots
plot_graph([], canvas1, ax1, "BackTrack Algorithm")
plot_graph([], canvas2, ax2, "BackTrackUp Algorithm")

# Start the main loop
root.mainloop()
