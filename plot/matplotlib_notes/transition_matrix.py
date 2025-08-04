fig, ax = plt.subplots(figsize=(6, 5))

# Show the matrix as an image
cax = ax.imshow(df.values, cmap='Blues')

# Add colorbar
fig.colorbar(cax, label='Transition %')

# Set axis labels
ax.set_xticks(range(len(df.columns)))
ax.set_yticks(range(len(df.index)))
ax.set_xticklabels(df.columns)
ax.set_yticklabels(df.index)
ax.set_xlabel("To State")
ax.set_ylabel("From State")
ax.set_title("State Transition Matrix (%)")

# Annotate each cell with the percentage
for i in range(len(df.index)):
    for j in range(len(df.columns)):
        ax.text(j, i, f"{df.iloc[i, j]:.1f}%", ha='center', va='center', color='black')

plt.tight_layout()
plt.show()