import cv2
import mediapipe as mp
import pygame
from patternRecognizer import patternRecorgnizer

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

pygame.mixer.init()

p = patternRecorgnizer()

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

            # Detect finger taps
            index_tap = p.recognize_finger_tap_for_flute(hand_landmarks, hand_label, "Index")
            middle_tap = p.recognize_finger_tap_for_flute(hand_landmarks, hand_label, "Middle")
            ring_tap = p.recognize_finger_tap_for_flute(hand_landmarks, hand_label, "Ring")
            pinky_tap = p.recognize_finger_tap_for_flute(hand_landmarks, hand_label, "Pinky")

            # Display the detected gestures on the frame
            gestures = [index_tap, middle_tap, ring_tap, pinky_tap]
            for i, gesture in enumerate(gestures):
                if gesture != "Unknown Gesture":
                    text_position = 30 + i * 30
                    if gesture[0] == "R":
                        text_position += 120
                    cv2.putText(frame, gesture, (10, text_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Perform actions based on detected gestures
            if index_tap != "Unknown Gesture":
                play_sound("prueba")  # Replace with appropriate sound
            if middle_tap != "Unknown Gesture":
                play_sound("prueba")  # Replace with appropriate sound
            if ring_tap != "Unknown Gesture":
                play_sound("prueba")  # Replace with appropriate sound
            if pinky_tap != "Unknown Gesture":
                play_sound("prueba")  # Replace with appropriate sound

    # Display the frame with hand landmarks
    cv2.imshow("Hand Gesture Recognition", frame)

    # Exit the loop if the 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII for 'Esc'
        break

# Release resources and close windows
vid.release()
cv2.destroyAllWindows()