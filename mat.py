import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def syracuse_steps(n):
    steps = 0
    max_value = n
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        max_value = max(max_value, n)
        steps += 1
    return steps, max_value

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel('Nombre')
ax1.set_ylabel('Nombre d\'étapes', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Altitude maximale', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

steps_list = []
max_values = []

n_max = 10000000000000000
current_number = 1

def update(frame):
    global current_number, steps_list, max_values
    
    steps, max_value = syracuse_steps(current_number)
    
    steps_list.append(steps)
    max_values.append(max_value)
    
    ax1.clear()
    ax2.clear()
    
    ax1.set_xlabel('Nombre')
    ax1.set_ylabel('Nombre d\'étapes', color='tab:blue')
    ax1.plot(range(1, len(steps_list) + 1), steps_list, color='tab:blue', label='Nombre d\'étapes')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    ax2.set_ylabel('Altitude maximale', color='tab:red')
    ax2.plot(range(1, len(max_values) + 1), max_values, color='tab:red', label='Altitude maximale')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    ax1.set_title(f"Conjecture de Syracuse: Analyse jusqu'au nombre {current_number}")
    
    current_number += 1
    return ax1, ax2

ani = FuncAnimation(fig, update, frames=range(1, n_max + 1), repeat=False)

plt.tight_layout()
plt.show()
