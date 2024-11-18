import numpy as np
import matplotlib.pyplot as plt

# Parameters
f1 = 1000  # Frequency of first signal (Hz)
f2 = 1010  # Frequency of second signal (Hz)
fs = 50000  # Sampling frequency (samples per second)
duration = 0.2  # Duration of the signal (seconds)

# Time vector
t = np.linspace(0, duration, int(fs * duration))

# Signals
signal1 = np.sin(2 * np.pi * f1 * t)
signal2 = np.sin(2 * np.pi * f2 * t)

# Combined signal (resulting beat frequency)
combined_signal = signal1 + signal2

# Envelope (positive values of the low-frequency oscillation)
envelope = 2 * np.abs(np.cos(np.pi * (f2 - f1) * t))

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(18, 12))

# Plot component signals
axs[0].plot(t, combined_signal, color='navy', alpha=0.7, linewidth=1)
axs[0].plot(t, envelope, color='red', linewidth=2, label='Envelope')
axs[0].set_ylabel('Amplitude',fontsize=30)
axs[0].set_xlabel('Time (s)',fontsize=30)
axs[0].tick_params(axis='both', which='major', labelsize=25)
axs[0].tick_params(axis='both', which='minor', labelsize=25)
axs[0].set_title('Resulting Beat Frequency from Combined High-Frequency Signals', fontsize=30, fontweight='bold', pad=20)
axs[0].grid(True, linestyle='--', alpha=0.6)


axs[1].plot(t, signal1, label=f'{f1} Hz Component')
axs[1].plot(t, signal2, label=f'{f2} Hz Component')
axs[1].set_title('Component Signals', fontsize=30, fontweight='bold', pad=20)
axs[1].set_xlabel('Time (s)',fontsize=30)
axs[1].set_ylabel('Amplitude',fontsize=30)
axs[1].tick_params(axis='both', which='major', labelsize=25)
axs[1].tick_params(axis='both', which='minor', labelsize=25)
axs[1].grid(True, linestyle='--', alpha=0.6)
axs[1].set_xlim(0, 0.02)  # Zoom into the first 0.2 seconds for this subplot

# # Plot individual components in separate subplots
# axs[2].plot(t, signal2, label=f'{f2} Hz Component')
# axs[2].set_title('1.01 kHz Component Signal', fontsize=30, fontweight='bold')
# axs[2].set_xlabel('Time (s)',fontsize=30)
# axs[2].set_ylabel('Amplitude',fontsize=30)
# axs[2].tick_params(axis='both', which='major', labelsize=20)
# axs[2].tick_params(axis='both', which='minor', labelsize=20)
# axs[2].grid(True, linestyle='--', alpha=0.6)

# Add a single legend just below the last subplot
handles, labels = [], []
for ax in axs:
    handle, label = ax.get_legend_handles_labels()
    handles.extend(handle)
    labels.extend(label)
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=30)

# Increase the padding between subplots and center the subplots in the figure
plt.tight_layout(pad=5.0)
# plt.subplots_adjust(top=2, bottom=0.1)

# Save the resulting plot with the correct dimensions
fig.savefig('beat.png', bbox_inches='tight')

plt.tight_layout()
plt.show()

