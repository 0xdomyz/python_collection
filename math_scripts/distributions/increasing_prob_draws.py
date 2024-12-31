import numpy as np
import matplotlib.pyplot as plt

def generate_probabilities(n, p, steepness):
    ranks = np.arange(1, n + 1)
    probabilities = np.exp(-steepness * (ranks - 1))
    probabilities /= probabilities.sum()  # Normalize to sum to 1
    probabilities *= p / 100  # Scale to ensure total probability sums to p%
    return probabilities

n = 100  # Total number of items
p = 20  # Percentage to draw
steepness_values = [0.01, 0.05, 0.1, 0.5]  # Different steepness values to compare

plt.figure(figsize=(12, 8))

for steepness in steepness_values:
    probabilities = generate_probabilities(n, p, steepness)
    plt.plot(np.arange(1, n + 1), probabilities, label=f'Steepness {steepness}')

plt.xlabel('Rank')
plt.ylabel('Probability Density')
plt.title('Probability Density Distribution for Different Steepness Values')
plt.legend()
plt.grid(True)
plt.show()