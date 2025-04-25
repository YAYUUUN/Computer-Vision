import cv2
import mediapipe as mp
import pygame
from patternRecognizer import patternRecorgnizer

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

pygame.mixer.init()

def play_sound(nombre):
    nombre = nombre + ".mp3"
    pygame.mixer.music.load(nombre)
    pygame.mixer.music.play()

vid = cv2.VideoCapture(0)


# Start the hand gesture detection loop
while vid.isOpened():
    # Read the frame from the webcam
    ret, frame = vid.read()
    
    if not ret:
        break

    # Flip the frame horizontally for a more natural user experience
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB (MediaPipe requires RGB input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get the landmarks
    results = hands.process(rgb_frame)

    # If hand landmarks are detected
    if results.multi_hand_landmarks:
        # hand_label = results.multi_handedness.classification[0].label  # "Left" or "Right"
        # if hand_label == "right":
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            hand_label = handedness.classification[0].label  # "Left" or "Right"

    # Display the frame with hand landmarks
    cv2.imshow("Hand Gesture Recognition", frame)

    # Exit the loop if the 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII for 'Esc'
        break

# Release resources and close windows
vid.release()
cv2.destroyAllWindows()