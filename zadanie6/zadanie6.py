# Author: Kamil Kornatowski
# Author: Adrian Paczewski

# face landmark detection reference: http://dlib.net/face_landmark_detection.py.html

# Program uses the dlib library for face and landmark detection,
# along with OpenCV for video rendering, to detect closed eyes in a video.

# Download the pre-trained shape predictor model from
# (http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
# and extract the file to the script's directory or provide the correct path in the code.

# pip install numpy
# pip install opencv-python
# pip install dlib

import cv2  # for video rendering
import dlib  # for face and landmark detection
import numpy as np  # for mathematical operations on arrays

# initialize dlib's face detector and face landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# Calculates the center of mass for a given set of eye landmarks.
def calculate_eye_center(eye_landmarks):
    """
        calculate_eye_center.
            Parameters:
                eye_landmarks (list): List of dlib points representing eye landmarks.
            Return:
                eye_center (tuple): Tuple representing the calculated eye center.
    """
    eye_center = np.mean([(point.x, point.y) for point in eye_landmarks], axis=0).astype(int)
    return eye_center


# Detects if the eyes are closed based on the vertical difference
# between the centers of mass of the left and right eye.
def detect_eyes_closed(shape):
    """
        calculate_eye_center.
            Parameters:
                shape: dlib shape object representing facial landmarks.
            Return:
                eyes_closed (boolean): Boolean indicating whether the eyes are closed.
    """
    # Set left and right eye landmarks
    left_eye_landmarks = shape.parts()[36:42]
    right_eye_landmarks = shape.parts()[42:48]

    # Calculate centers of mass
    left_eye_center = calculate_eye_center(left_eye_landmarks)
    right_eye_center = calculate_eye_center(right_eye_landmarks)

    # Calculate vertical difference
    vertical_diff = left_eye_center[1] - right_eye_center[1]

    return vertical_diff >= -5


# Displays the result on the frame.
def display_result(frame, face, eyes_closed):
    """
        display_result.
            Parameters:
                frame: Current video frame.
                face: dlib rectangle object representing the detected face.
                eyes_closed: Boolean indicating whether the eyes are closed.
    """
    # Mark face on the screen.
    cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (255, 0, 0), 2)

    # Check if eyes are closed.
    if eyes_closed:
        cv2.putText(frame, "Eyes Closed", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "Eyes Open", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# Main function for detecting closed eyes in a video.
def detect_closed_eyes(video_path):
    """
            calculate_eye_center.
                Parameters:
                    video_path: Path to the video file.
                Return:
                    Displays the video, press 'q' to exit the video window.
        """
    cap = cv2.VideoCapture(video_path)
    cv2.namedWindow('Closed Eyes Detection', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Closed Eyes Detection', 1080, 1920)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Face detection
        faces = detector(gray)
        for face in faces:
            shape = predictor(gray, face)

            eyes_closed = detect_eyes_closed(shape)
            display_result(frame, face, eyes_closed)

        cv2.imshow('Closed Eyes Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path = "test_video.mp4"
    detect_closed_eyes(video_path)
