import cv2
import json
import numpy as np

def get_face_at_point(x, y, faces):
    """Return face index if (x,y) is inside a face rectangle"""
    for i, face in enumerate(faces, 1):
        rect = face["face_rectangle"]
        if (x >= rect["left"] and x <= rect["left"] + rect["width"] and 
            y >= rect["top"] and y <= rect["top"] + rect["height"]):
            return i
    return None

def mouse_callback(event, x, y, flags, param):
    """Handle mouse clicks"""
    if event == cv2.EVENT_LBUTTONDOWN:
        face_data = param['faces']
        comparisons = param['comparisons']
        image = param['image'].copy()
        
        clicked_face = get_face_at_point(x, y, face_data)
        if clicked_face:
            # Clear previous image and redraw all faces in gray
            for i, face in enumerate(face_data, 1):
                rect = face["face_rectangle"]
                color = (128, 128, 128)  # Gray for non-selected faces
                cv2.rectangle(image, 
                            (rect["left"], rect["top"]), 
                            (rect["left"] + rect["width"], rect["top"] + rect["height"]), 
                            color, 2)
                cv2.putText(image, f"Face {i}", 
                           (rect["left"], rect["top"] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Highlight selected face in blue
            selected_face = face_data[clicked_face - 1]
            rect = selected_face["face_rectangle"]
            cv2.rectangle(image, 
                        (rect["left"], rect["top"]), 
                        (rect["left"] + rect["width"], rect["top"] + rect["height"]), 
                        (255, 0, 0), 2)  # Blue
            
            # Show comparison results for selected face
            y_offset = 30
            for comp in comparisons:
                if comp['face1']['number'] == clicked_face:
                    other_face = comp['face2']['number']
                    confidence = comp['confidence']
                    other_rect = face_data[other_face - 1]["face_rectangle"]
                    # Red for high similarity (>80%), otherwise green-red gradient
                    if confidence > 80:
                        color = (0, 0, 255)  # Pure red for high similarity
                    else:
                        green = int(255 * (confidence/100))
                        red = int(255 * (1 - confidence/100))
                        color = (0, green, red)
                    cv2.rectangle(image, 
                                (other_rect["left"], other_rect["top"]), 
                                (other_rect["left"] + other_rect["width"], 
                                 other_rect["top"] + other_rect["height"]), 
                                color, 2)
                    cv2.putText(image, f"Face {other_face}: {confidence:.1f}%", 
                              (10, y_offset), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    y_offset += 20
                elif comp['face2']['number'] == clicked_face:
                    other_face = comp['face1']['number']
                    confidence = comp['confidence']
                    other_rect = face_data[other_face - 1]["face_rectangle"]
                    # Red for high similarity (>80%), otherwise green-red gradient
                    if confidence > 80:
                        color = (0, 0, 255)  # Pure red for high similarity
                    else:
                        green = int(255 * (confidence/100))
                        red = int(255 * (1 - confidence/100))
                        color = (0, green, red)
                    cv2.rectangle(image, 
                                (other_rect["left"], other_rect["top"]), 
                                (other_rect["left"] + other_rect["width"], 
                                 other_rect["top"] + other_rect["height"]), 
                                color, 2)
                    cv2.putText(image, f"Face {other_face}: {confidence:.1f}%", 
                              (10, y_offset), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    y_offset += 20
            
            cv2.imshow("Labeled Faces", image)

# Load the image
image_path = "IMG_0020.JPG"
original_image = cv2.imread(image_path)

# Load faces from face_tokens.json
try:
    with open('face_tokens.json', 'r') as f:
        data = json.load(f)
        faces = data["faces"]
except FileNotFoundError:
    print("Error: face_tokens.json file not found")
    exit(1)

# Load comparison results
try:
    with open('face_comparison_results.json', 'r') as f:
        comparison_data = json.load(f)
        comparisons = comparison_data['comparisons']
except FileNotFoundError:
    comparisons = []

# Initial drawing of faces
image = original_image.copy()
for i, face in enumerate(faces, 1):
    rect = face["face_rectangle"]
    cv2.rectangle(image, 
                 (rect["left"], rect["top"]), 
                 (rect["left"] + rect["width"], rect["top"] + rect["height"]), 
                 (0, 255, 0), 2)
    cv2.putText(image, f"Face {i}", 
                (rect["left"], rect["top"] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Create window and set mouse callback
cv2.imshow("Labeled Faces", image)
param = {'faces': faces, 'comparisons': comparisons, 'image': original_image}
cv2.setMouseCallback("Labeled Faces", mouse_callback, param)

# Wait for key press
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        break

cv2.destroyAllWindows()
