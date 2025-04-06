import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
    # Open the video file
    webcam = cv2.VideoCapture(0)
    fig, ax1 = plt.subplots()

    im1 = ax1.imshow([[0]])
    ax1.set_aspect('auto')  # Prevent square distortion

    def update(frame_num):
        ret, frame = webcam.read()
        if not ret:
            return im1,
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for matplotlib
        im1.set_data(frame)

        return im1, 

    ani = animation.FuncAnimation(fig, update, interval=30, blit=True, cache_frame_data=False)

    plt.axis('off')
    plt.show()
    webcam.release()

if __name__ == "__main__":
    main()
