import cv2
import os
import time

def video_split(video_path, name):
    # Directory to save the frames
    output_folder = os.path.join("/home/pi/parul_hack/face_detect/dataset", name)
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break  # End of video

        # Save each frame as an image
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        print(f"Saved: {frame_filename}")
        frame_count += 1

    video_capture.release()
    print(f"All frames saved to folder: {output_folder}")

def record_video(output_file, duration=30, fps=30, frame_width=640, frame_height=480):
    # Open the default camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the camera.")
        return

    # Set the frame size
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    # Start recording
    start_time = time.time()
    print(f"Recording started. Duration: {duration} seconds")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Write the frame to the video file
        out.write(frame)

        # Display the recording frame (optional)
        cv2.imshow('Recording...', frame)

        # Stop recording after the specified duration
        if time.time() - start_time > duration:
            print("Recording finished.")
            break

        # Press 'q' to stop recording manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Recording stopped manually.")
            break

    # Release the camera and close the window
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Prompt user for a name
    name = input("Enter the name for the dataset folder: ").strip()

    # Record the video
    video_filename = f"/home/pi/parul_hack/face_detect/{name}.mp4"
    record_video(video_filename, duration=30)

    # Split the video into frames and save them
    video_split(video_filename, name)