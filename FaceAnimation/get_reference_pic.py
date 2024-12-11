import cv2

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

print("Press 's' to save the reference image.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting.")
        break

    cv2.imshow("Reference Capture", frame)

    # Press 's' to save the image
    if cv2.waitKey(1) & 0xFF == ord("s"):
        cv2.imwrite("reference_object.jpg", frame)
        print("Reference image saved as 'reference_object.jpg'.")
        break

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
