# -*- coding: utf-8 -*-

#Created by MediaPipe

import cv2
import mediapipe as mp
import time
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

# For static images:
with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    min_detection_confidence=0.5) as pose:
    image = cv2.imread('test.jpg')  #Insert your Image Here
    image_height, image_width, _  = image.shape
    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # Draw pose landmarks on the image.
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imwrite(r'test.png', annotated_image)

# For webcam input:
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("/content/drive/MyDrive/Old Man Down/Real-TimeActionRecognition files/FallDataset/Home_01/Videos/video (23).avi")

# Get video file's dimensions
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Creates output video file
codec = cv2.VideoWriter_fourcc(*'MJPG')
writer = cv2.VideoWriter("/content/drive/MyDrive/Old Man Down/Real-TimePose/video23_pose.avi", codec, 30, (frame_width,frame_height))


#For Video input:
prevTime = 0
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      break

    # Convert the BGR image to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
    #cv2.imshow('BlazePose', image) # Uncomment to show if running local

    writer.write(image)

    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
writer.release()