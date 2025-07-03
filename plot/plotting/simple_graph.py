import matplotlib.pyplot as plt

# Define nodes and their (x, y) positions
positions = {
    'A': (0, 0),
    'B': (1, 1),
    'C': (2, 0),
    'D': (1, -1)
}

# Define edges as pairs of nodes
edges = [
    ('A', 'B'),
    ('B', 'C'),
    ('A', 'D'),
    ('C', 'D')
]

# Create the plot
fig, ax = plt.subplots()

# Plot edges
for edge in edges:
    x0, y0 = positions[edge[0]]
    x1, y1 = positions[edge[1]]
    ax.plot([x0, x1], [y0, y1], 'k-', lw=2)

# Plot nodes
for node, (x, y) in positions.items():
    ax.scatter(x, y, s=300, c='skyblue', edgecolors='black', zorder=3)
    ax.text(x, y, node, fontsize=12, ha='center', va='center', zorder=4)

# Clean up axes
ax.set_aspect('equal')
ax.axis('off')
plt.title("Simple Loop-Free Graph with Matplotlib")
plt.show()