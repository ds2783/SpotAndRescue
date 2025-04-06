import board
import busio
import time
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ROTATION_VECTOR
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Initialize I2C and BNO08X sensor
i2c = busio.I2C(board.D1, board.D0)
bno = BNO08X_I2C(i2c, address=0x4b)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

# Set up the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the plot limits (flipped X and Y axes)
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([-1.5, 1.5])

# Set axis labels to reflect flipped axes
ax.set_xlabel('Y')
ax.set_ylabel('X')
ax.set_zlabel('Z')

# Define the 3D cube vertices and faces
def create_cube():
    # Vertices of a cube centered at (0, 0, 0) with side length 1
    vertices = np.array([[-0.5, -0.5, -0.5],
                         [ 0.5, -0.5, -0.5],
                         [ 0.5,  0.5, -0.5],
                         [-0.5,  0.5, -0.5],
                         [-0.5, -0.5,  0.5],
                         [ 0.5, -0.5,  0.5],
                         [ 0.5,  0.5,  0.5],
                         [-0.5,  0.5,  0.5]])
    # List of cube faces, where each face is defined by a list of vertex indices
    faces = [[0, 1, 2, 3],  # front
             [4, 5, 6, 7],  # back
             [0, 1, 5, 4],  # bottom
             [1, 2, 6, 5],  # right
             [2, 3, 7, 6],  # top
             [3, 0, 4, 7]]  # left
    return vertices, faces

# Function to apply quaternion rotation to the cube vertices
def rotate_cube(vertices, quat_i, quat_j, quat_k, quat_real):
    # Convert the quaternion into a rotation matrix
    q0 = quat_real
    q1 = quat_i
    q2 = quat_j
    q3 = quat_k

    # Create a rotation matrix from the quaternion
    rot_matrix = np.array([
        [1 - 2 * (q2**2 + q3**2), 2 * (q1*q2 - q0*q3), 2 * (q1*q3 + q0*q2)],
        [2 * (q1*q2 + q0*q3), 1 - 2 * (q1**2 + q3**2), 2 * (q2*q3 - q0*q1)],
        [2 * (q1*q3 - q0*q2), 2 * (q2*q3 + q0*q1), 1 - 2 * (q1**2 + q2**2)]
    ])

    # Rotate the vertices using the rotation matrix
    rotated_vertices = np.dot(vertices, rot_matrix.T)

    # Flip the X and Y coordinates of the rotated vertices
    rotated_vertices[:, [0, 1]] = rotated_vertices[:, [1, 0]]

    return rotated_vertices

# Plotting function to draw the cube
def plot_cube(vertices, faces):
    # Clear the previous plot
    ax.cla()

    # Set the plot limits (flipped X and Y axes)
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])

    # Plot the cube faces, but make the top face (index 1) red
    for i, face in enumerate(faces):
        verts = [vertices[face]]
        # If the face is the top face (index 1), make it red
        if i == 3:
            ax.add_collection3d(Poly3DCollection(verts, facecolors='red', linewidths=1, edgecolors='b', alpha=0.5))
        else:
            ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='b', alpha=0.1))

    # Set axis labels to reflect flipped axes
    ax.set_xlabel('Y')
    ax.set_ylabel('X')
    ax.set_zlabel('Z')

    # Display the plot
    plt.draw()
    plt.pause(0.01)

# Main loop to read quaternion and update plot
while True:
    # time.sleep(0.005)

    print("Rotation Vector Quaternion:")
    quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member

    # Create cube and apply rotation
    vertices, faces = create_cube()
    rotated_vertices = rotate_cube(vertices, quat_i, quat_j, quat_k, quat_real)

    # Plot the rotated cube with the top face in red
    plot_cube(rotated_vertices, faces)
