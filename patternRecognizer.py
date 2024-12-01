class patternRecorgnizer:

    def recognize_finger_tap_for_flute(self, hand_landmarks, hand_label, finger_name):
        """
        Recognizes tapping gestures for a specific finger and determines the hand (left or right).
        
        :param hand_landmarks: Hand landmarks from MediaPipe.
        :param hand_label: Label indicating "Left" or "Right" hand.
        :param finger_name: Name of the finger to detect ("Index", "Middle", "Ring", "Pinky").
        :return: Gesture name (e.g., "Index Tap") or "Unknown Gesture".
        """
        # Finger landmark indices based on MediaPipe hand model
        finger_landmarks = {
            "Index": [5, 6, 7, 8],  # MCP, PIP, DIP, TIP for index finger
            "Middle": [9, 10, 11, 12],  # MCP, PIP, DIP, TIP for middle finger
            "Ring": [13, 14, 15, 16],  # MCP, PIP, DIP, TIP for ring finger
            "Pinky": [17, 18, 19, 20],  # MCP, PIP, DIP, TIP for pinky finger
        }

        if finger_name not in finger_landmarks:
            return "Unknown Gesture"

        mcp, pip, dip, tip = finger_landmarks[finger_name]

        # Get landmark positions for the specified finger
        mcp_pos = hand_landmarks.landmark[mcp]
        pip_pos = hand_landmarks.landmark[pip]
        dip_pos = hand_landmarks.landmark[dip]
        tip_pos = hand_landmarks.landmark[tip]
        palm_base = hand_landmarks.landmark[0]  # Wrist base

        # Detect tapping motion (TIP lower than PIP and DIP, TIP near palm)
        if finger_name == "Pinky":
            is_tapping = (
                ((tip_pos.y > pip_pos.y and  # TIP below PIP
                tip_pos.y > mcp_pos.y) or (tip_pos.x - dip_pos.x == 0)) and
                pip_pos.y < palm_base.y
            )
        elif finger_name == "Middle" or finger_name == "Ring":
            is_tapping = (
                tip_pos.y > pip_pos.y and  # TIP below PIP
                tip_pos.y > dip_pos.y and  # TIP below DIP
                tip_pos.y > mcp_pos.y and
                pip_pos.y < palm_base.y    # PIP above palm base
            )
        else:
            is_tapping = (
                tip_pos.y > pip_pos.y and  # TIP below PIP
                tip_pos.y > dip_pos.y and  # TIP below DIP
                tip_pos.y < mcp_pos.y and
                pip_pos.y < palm_base.y    # PIP above palm base
            )

        # Ensure hand-specific actions (optional)
        if is_tapping:
            return f"{hand_label} {finger_name} Tap"

        return "Unknown Gesture"


    # def recognize_gesture(self, hand_landmarks, hand_label):
    #     # Get the coordinates for key landmarks (index positions for simplicity)
    #     thumb_tip = hand_landmarks.landmark[4]
    #     index_tip = hand_landmarks.landmark[8]
    #     middle_tip = hand_landmarks.landmark[12]
    #     ring_tip = hand_landmarks.landmark[16]
    #     pinky_tip = hand_landmarks.landmark[20]
    #     palm_base = hand_landmarks.landmark[0]

    #     index_pip = hand_landmarks.landmark[6]
    #     middle_pip = hand_landmarks.landmark[10]
    #     ring_pip = hand_landmarks.landmark[14]
    #     pinky_pip = hand_landmarks.landmark[18]

    #     thumb_up = (
    #         (thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y and thumb_tip.y < ring_tip.y and thumb_tip.y < pinky_tip.y and thumb_tip.y < palm_base.y) and 
    #         (index_tip.x >= index_pip.x and middle_tip.x >= middle_pip.x and ring_tip.x >= ring_pip.x and pinky_tip.x >= pinky_pip.x)
    #     )
    #     # Check if the thumb is extended and all other fingers are curled (Thumbs Up gesture)
    #     if thumb_up:
    #         return "Thumbs Up"
    #     return "Unknown Gesture"
    
    
    # # Function to recognize the "index finger tap" gesture based on landmarks
    # def recognize_index_tap(self, hand_landmarks, hand_label):
    #     index_mcp = hand_landmarks.landmark[5]
    #     index_pip = hand_landmarks.landmark[6]  # Proximal interphalangeal joint
    #     index_dip = hand_landmarks.landmark[7]
    #     index_tip = hand_landmarks.landmark[8]
    #     palm_base = hand_landmarks.landmark[0]  # Wrist base (for simplicity)

    #     idx_tap = (
    #         (index_tip.y > index_pip.y and index_tip.y > index_dip.y and index_pip.y < palm_base.y) and
    #         (index_tip.x > index_dip.x)    
    #     )
    #     # Detect if the index finger tip has moved close to the palm base
    #     if idx_tap and self.recognize_gesture(hand_landmarks, 0) != "Thumbs Up":  # Finger tip is lower than PIP joint (curled position)
    #         return "Index Tap"
    #     return "Unknown Gesture"
    
    # def recognize_middle_tap(self, hand_landmarks, hand_label):
    #     middle_mcp = hand_landmarks.landmark[9]
    #     middle_pip = hand_landmarks.landmark[10]
    #     middle_dip = hand_landmarks.landmark[11]
    #     middle_tip = hand_landmarks.landmark[12]

    #     palm_base = hand_landmarks.landmark[0]

    #     middle_tap = (
    #         (middle_tip.y > middle_pip.y and middle_tip.y > middle_dip.y and middle_pip.y < palm_base.y) and
    #         (middle_tip.x > middle_dip.x)
    #     )
    #     if middle_tap:
    #         return "Middel Tap"
    #     return "Unknown Gesture"
        