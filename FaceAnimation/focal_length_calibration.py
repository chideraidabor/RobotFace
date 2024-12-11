import cv2

# Load the reference image
ref_image = cv2.imread("reference_object.jpg")

# Convert to grayscale
gray = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Known measurements
KNOWN_DISTANCE = 63.5  # cm (distance at which the image was captured)
KNOWN_WIDTH = 17.8  # cm (real-world width of your face)

# Initialize face width in pixels
face_width_pixels = 0

for (x, y, w, h) in faces:
    # Assume the first detected face is the reference
    face_width_pixels = w
    cv2.rectangle(ref_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    break

# Display the detected face
cv2.imshow("Detected Face", ref_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

if face_width_pixels > 0:
    # Calculate the focal length
    focal_length = (face_width_pixels * KNOWN_DISTANCE) / KNOWN_WIDTH
    print(f"Focal Length: {focal_length:.2f} pixels")
else:
    print("No face detected!")
