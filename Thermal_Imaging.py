import time
import board
import busio
import adafruit_mlx90640
import numpy as np
import matplotlib.pyplot as plt

# Set up I2C communication
i2c = busio.I2C(board.SCL, board.SDA)
mlx = adafruit_mlx90640.MLX90640(i2c)

# Print the detected serial number
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

# Set the refresh rate (if needed, adjust to prevent retries)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ

# Initialize a frame buffer to store the thermal data
frame = [0] * 768

# Set up the figure for displaying the thermal image
fig, ax = plt.subplots(figsize=(8, 6))  # Create a single subplot

# Plot the thermal image
im = ax.imshow(np.zeros((24, 32)), cmap='inferno', vmin=20, vmax=40)
ax.set_title("Thermal Image from MLX90640")
fig.colorbar(im, ax=ax)  # Add color bar

# Enable interactive mode for real-time updates
plt.ion()

while True:
    try:
        # Read a frame of thermal data from the sensor
        mlx.getFrame(frame)
    except ValueError:
        # Retry if there's an issue with reading the frame
        continue

    # Convert the flat frame into a 2D array (24x32)
    frame_2d = np.reshape(frame, (24, 32))

    # Update the thermal image
    im.set_data(frame_2d)

    # Redraw the plots
    plt.draw()
    plt.pause(0.01)  # Pause to allow the plot to update
