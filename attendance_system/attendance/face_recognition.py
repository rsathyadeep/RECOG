import cv2
import numpy as np
from attendance.models import Student, Attendance
import face_recognition




def mark_attendance_from_camera():
    # Load all student face encodings
    students = Student.objects.all()
    known_encodings = [face_recognition.face_encodings(face_recognition.load_image_file(student.photo.path))[0] for student in students]
    known_names = [student.name for student in students]

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access the camera.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare captured face to known faces
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            if True in matches:
                matched_index = matches.index(True)
                name = known_names[matched_index]
                student = students[matched_index]

                # Mark attendance
                Attendance.objects.create(student=student)
                print(f"Attendance marked for {name}.")
            else:
                print("Unknown face detected. Please register.")

        cv2.imshow('Recognize Face', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit
            break

    cap.release()
    cv2.destroyAllWindows()


def register_new_user(name):
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    print("Press 's' to save the image and register the user, 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access the camera.")
            break

        cv2.imshow('Register Face', frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Save image and register
            # Detect face
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            if len(face_locations) == 1:  # Ensure only one face is captured
                face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                
                # Save the user data
                student = Student(name=name)
                student.save()
                
                # Save photo
                img_path = f'media/photos/{student.student_id}.jpg'
                cv2.imwrite(img_path, frame)
                student.photo = img_path
                student.face_encoding = face_encoding.tobytes()
                student.save()

                print(f"User {name} registered successfully!")
                break
            else:
                print("No face detected or multiple faces detected. Try again.")

        elif key == ord('q'):  # Quit
            break

    cap.release()
    cv2.destroyAllWindows()


def capture_and_mark_attendance():
    # Load pre-trained model for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    student_id = "12345"
    try:
        student = Student.objects.get(student_id=student_id)
        Attendance.objects.create(student=student)
        print(f"Marked attendance for {student.name}")
    except ObjectDoesNotExist:
        print(f"No student found with ID {student_id}")

    # Load student images and encode them
    def get_encoded_faces():
        encoded_faces = {}
        for student in Student.objects.all():
            img_path = student.photo.path
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Placeholder for encoding logic
            encoded_faces[student.student_id] = img  # Replace with real encodings
        return encoded_faces

    face_encodings = get_encoded_faces()

    # Start webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Recognize and match faces here (placeholder logic)
            student_id = "12345"  # Replace with matching logic
            student = Student.objects.get(student_id=student_id)
            Attendance.objects.create(student=student)
            print(f"Marked attendance for {student.name}")

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


