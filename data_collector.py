import os
import cv2
import time
import uuid

IMAGE_PATH = "CollectedImages"
labels = ['Namaste', 'Yes']
number_of_images = 5

# Create necessary directories
for label in labels:
    img_path = os.path.join(IMAGE_PATH, label)
    os.makedirs(img_path, exist_ok=True)

# Open camera once to avoid delay
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set camera properties for smoother capture
cap.set(cv2.CAP_PROP_FPS, 30)  # Set FPS to 30
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

for label in labels:
    print(f"Collecting images for '{label}' in 3 seconds...")

    # Countdown before starting to capture
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    print("Starting capture...")

    for imgnum in range(number_of_images):
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            continue

        # Save the image
        imagename = os.path.join(IMAGE_PATH, label, f"{label}.{uuid.uuid1()}.jpg")
        cv2.imwrite(imagename, frame)

        # Display the frame with a small delay
        cv2.imshow('frame', frame)
        time.sleep(0.5)  # Reduced delay for smoother capture

        # Press 'q' to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print(f"Finished collecting images for '{label}'")

# Release camera and close window properly
cap.release()
cv2.destroyAllWindows()
