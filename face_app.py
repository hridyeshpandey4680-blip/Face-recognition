import sys
import os

# --- STEP 1: AUTOMATIC ENVIRONMENT SETUP ---
try:
    import face_recognition
    import face_recognition_models
    import cv2
    import numpy as np
except ImportError:
    print("Setting up the core environment... This may take 1-2 minutes. Please wait...")
    os.system(f'"{sys.executable}" -m pip install --upgrade pip')
    os.system(f'"{sys.executable}" -m pip install cmake')
    os.system(f'"{sys.executable}" -m pip install face-recognition-models')
    os.system(f'"{sys.executable}" -m pip install face_recognition opencv-python numpy')
    print("Setup completed successfully! Initializing the application...")

# --- STEP 2: GLOBAL IMPORTS ---
import cv2
import numpy as np
import face_recognition

# --- STEP 3: CORE APPLICATION LOGIC ---
print("Loading Advanced Biometric Models...")

# --- AUTHORIZED DATABASE SETUP ---
persons_data = [("pandey.jpg", "HRIDYESH KUMAR PANDEY")]
known_face_encodings = [face_recognition.face_encodings(face_recognition.load_image_file(img))[0] for img, _ in persons_data]
known_face_names = [name for _, name in persons_data]

# Camera Configuration
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Set standard width
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set standard height

# Named Window Configuration (Resizable Mode)
window_name = 'INTELLIGENT BIOMETRIC DASHBOARD'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 640, 480) 

# --- CUSTOM GRAPHICS UTILITY FUNCTION ---
def draw_modern_corners(img, top, right, bottom, left, color, thickness=2, length=15):
    """Draws sleek, high-tech HUD corner brackets around the detected target face"""
    # Top-Left Corner
    cv2.line(img, (left, top), (left + length, top), color, thickness)
    cv2.line(img, (left, top), (left, top + length), color, thickness)
    # Top-Right Corner
    cv2.line(img, (right, top), (right - length, top), color, thickness)
    cv2.line(img, (right, top), (right, top + length), color, thickness)
    # Bottom-Left Corner
    cv2.line(img, (left, bottom), (left + length, bottom), color, thickness)
    cv2.line(img, (left, bottom), (left, bottom - length), color, thickness)
    # Bottom-Right Corner
    cv2.line(img, (right, bottom), (right - length, bottom), color, thickness)
    cv2.line(img, (right, bottom), (right, bottom - length), color, thickness)

print("Biometric Core Engine Active. Press 'q' to terminate application.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
        
    height, width, _ = frame.shape
    
    # UI State Initialization (Default - Scanning Mode)
    status_text = "SYSTEM STATUS: SCANNING BIO-DATA..."
    panel_color = (238, 238, 0)   # Neon Cyan / Aqua
    text_color = (255, 255, 255)  # Crisp White
    
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
        # Default Security Flag for Non-Matches
        status_text = "ACCESS DENIED | UNKNOWN SUBJECT"
        panel_color = (0, 0, 255)    # High-Alert Red
        text_color = (255, 255, 255)
        
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            status_text = f"ACCESS GRANTED | {name} (VERIFIED)"
            panel_color = (0, 255, 0) # Secure Smart Green
            text_color = (0, 255, 0)
        
        # 1. Render modern target corner frames
        draw_modern_corners(frame, top, right, bottom, left, panel_color, thickness=3, length=15)
        
        # 2. Render an elegant alpha tint box within the target frame
        overlay = frame.copy()
        cv2.rectangle(overlay, (left, top), (right, bottom), panel_color, -1)
        cv2.addWeighted(overlay, 0.1, frame, 0.9, 0, frame)

    # --- MODERN BOTTOM HUD INTERFACE PANEL ---
    panel_height = 50 
    hud_overlay = frame.copy()
    cv2.rectangle(hud_overlay, (0, height - panel_height), (width, height), (10, 10, 10), -1)
    cv2.addWeighted(hud_overlay, 0.6, frame, 0.4, 0, frame)
    
    # Render HUD panel divider rule
    cv2.line(frame, (0, height - panel_height), (width, height - panel_height), panel_color, 2)
    
    # Status Text Formatting and Positioning
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5  
    font_thickness = 1
    text_size = cv2.getTextSize(status_text, font, font_scale, font_thickness)[0]
    
    # Calculate geometric alignment for absolute center within the HUD panel
    x_pos = (width - text_size[0]) // 2
    y_pos = (height - panel_height) + ((panel_height + text_size[1]) // 2)
    
    # Drop shadow implementation for enhanced text readability
    cv2.putText(frame, status_text, (x_pos + 1, y_pos + 1), font, font_scale, (0, 0, 0), font_thickness)
    cv2.putText(frame, status_text, (x_pos, y_pos), font, font_scale, text_color, font_thickness)
        
    # Render Output Stream
    cv2.imshow(window_name, frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()