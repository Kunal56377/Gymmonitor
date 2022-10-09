from PIL import Image, ImageTk
import cv2
import tkinter as tk
from tkinter import Menu
import customtkinter as ck
from datetime import datetime
import pandas as pd
import numpy as np
import pickle
import mediapipe as mp
mp.drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


window = tk.Tk()
window.geometry("1000x1500")
window.title("Gym Monitor")
ck.set_appearance_mode("dark")


classLabel = ck.CTkLabel(window, height=40, width=120, text_font=(
    "Arial", 20), text_color="black", padx=10)
classLabel.place(x=10, y=1)
classLabel.configure(text='STAGE')
counterLabel = ck.CTkLabel(window, height=40, width=120, text_font=(
    "Arial", 20), text_color="black", padx=10)
counterLabel.place(x=160, y=1)
counterLabel.configure(text='REPS')
probLabel = ck.CTkLabel(window, height=40, width=120, text_font=(
    "Arial", 20), text_color="black", padx=10)
probLabel.place(x=300, y=1)
probLabel.configure(text='PROB')
classBox = ck.CTkLabel(window, height=40, width=120, text_font=(
    "Arial", 20), text_color="white", fg_color="blue")
classBox.place(x=10, y=41)
classBox.configure(text='0')
counterBox = ck.CTkLabel(window, height=40, width=120, text_font=(
    "Arial", 20), text_color="white", fg_color="blue")
counterBox.place(x=160, y=41)
counterBox.configure(text='0')
probBox = ck.CTkLabel(window, height=40, width=120, text_font=(
    "Arial", 20), text_color="white", fg_color="blue")
probBox.place(x=300, y=41)
probBox.configure(text='0')
flag = 0
destoyflg = 1
frame = tk.Frame(height=500, width=700)
frame.place(x=10, y=90)
lmain = tk.Label(frame)
lmain.place(x=0, y=0)
lmain1 = ''
frame1 = ''
frame2 = ''
lmain2 = ''
Function = ''


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle


def reset_counter():
    global counter
    counter = 0


button = ck.CTkButton(window, text='RESET', command=reset_counter, height=40,
                      width=120, text_font=("Arial", 20), text_color="white", fg_color="blue")


button.place(x=10, y=600)


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.8)
cap = cv2.VideoCapture(0)
current_stage = ''

counter = 0
bodylang_prob = np.array([0, 0])
bodylang_class = ''


def excesize():

    global flag
    global current_stage
    global counter
    global bodylang_class
    global bodylang_prob
    # global flag
    global lmain1
    global frame1
    global frame
    global lmain
    image = ''
    if flag == 1:
        # frame = tk.Frame(height=600, width=700)
        # frame.place(x=10, y=90)
        # lmain = tk.Label(frame)
        # lmain.place(x=0, y=0)

        #cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            landmarks = results.pose_landmarks.landmark
        except:
            pass

        try:
            # Calculate Left anchle
            hipL = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            kneeL = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ancleL = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            # Calculate Right  anchle
            hipR = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            kneeR = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ancleR = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            angle1 = calculate_angle(hipL, kneeL, ancleL)
            angle2 = calculate_angle(hipR, kneeR, ancleR)
            angle = (angle1 + angle2)/2
            # Visualize angle
            cv2.putText(image, str(angle),
                        tuple(np.multiply(hipR, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                        255, 255), 2, cv2.LINE_AA
                        )
            if (angle <= 160 and angle > 95) and current_stage != 'UP':
                bodylang_prob = angle
                print("started")
                current_stage = "UP"
                bodylang_class = "UP"
            if angle <= 95 and current_stage == 'UP':
                bodylang_prob = angle
                current_stage = "DOWN"
                bodylang_class = "DOWN"
                counter += 1
                print(counter)

            cv2.putText(image, str(angle),
                        tuple(np.multiply(hipR, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                        255, 255), 2, cv2.LINE_AA
                        )
        except:
            pass
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(
                                      color=(106, 13, 173), thickness=4, circle_radius=5),
                                  mp_drawing.DrawingSpec(color=(255, 102, 0), thickness=5, circle_radius=10))

    if flag == 2:
        # frame.destroy()
        # frame = tk.Frame(height=600, width=700)
        # frame.place(x=10, y=90)
        # lmain = tk.Label(frame)
        # lmain.place(x=0, y=0)
        Function = "Pushup"
        # if flag == 1:
        #     global frame1
        #     frame1.pack_forget()

        if flag != 2:
            flag = 2
            # flag = 1

            # frame2 = tk.Frame(height=500, width=700)
            # frame2.place(x=10, y=90)
            # lmain2 = tk.Label(frame2)
            # lmain2.place(x=0, y=0)
            # lmain.imgtk = np.NAN
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            landmarks = results.pose_landmarks.landmark
        except:
            pass

        try:
            shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hipL = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            # Calculate Right  anchle
            hipR = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            angle_left = calculate_angle(shoulderL, elowL, wristL)
            angle_right = calculate_angle(shoulderR, elowR, wristR)

            angle_left1 = calculate_angle(shoulderL, elowL, hipL)
            angle_right1 = calculate_angle(shoulderR, elowR, hipR)

            angle_SEW = (angle_left + angle_right)/2
            angle_SEH = (angle_left1 + angle_right1)/2

            # Visualize angle
            cv2.putText(image, str(angle_SEW),
                        tuple(np.multiply(elowR, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                        255, 255), 2, cv2.LINE_AA
                        )

            cv2.putText(image, str(angle_SEH),
                        tuple(np.multiply(hipR, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                        255, 255), 2, cv2.LINE_AA
                        )

            if (angle_SEW <= 160 and angle_SEW > 95 and angle_SEH <= 40) and current_stage != 'UP':
                bodylang_prob = angle_SEW
                print("started")
                current_stage = "UP"
                bodylang_class = "UP"
            if angle_SEW <= 90 and current_stage == 'UP':
                # print(angle)
                bodylang_prob = angle_SEW
                current_stage = "DOWN"
                bodylang_class = "DOWN"
                counter += 1
                print(counter)

        except:
            pass

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(
                                      color=(106, 13, 173), thickness=4, circle_radius=5),
                                  mp_drawing.DrawingSpec(color=(255, 102, 0), thickness=5, circle_radius=10))

    if flag == 3:
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            landmarks = results.pose_landmarks.landmark
        except:
            pass

        try:
            shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hipL = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            # Calculate Right  anchle
            hipR = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            angle_left = calculate_angle(wristL, elowL, shoulderL)
            angle_right = calculate_angle(wristR, elowR, shoulderR)

            angle_left1 = calculate_angle(shoulderL, elowL, hipL)
            angle_right1 = calculate_angle(shoulderR, elowR, hipR)

            angle_SEH = (angle_left1 + angle_right1)/2
            angle_SEW = (angle_left + angle_right)/2

            # Visualize angle
            cv2.putText(image, str(angle_SEW),
                        tuple(np.multiply(elowR, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                        255, 255), 2, cv2.LINE_AA
                        )

            cv2.putText(image, str(angle_SEH),
                        tuple(np.multiply(hipR, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                        255, 255), 2, cv2.LINE_AA
                        )

            if (angle_SEH <= 40 and angle_SEW < 160):
                bodylang_prob = angle_SEH
                current_stage = "started"
                bodylang_class = "Started"
                start = datetime.now()
                counter = counter + 1
            else:
                if start != 0 and current_stage == 'started':
                    current_stage = 'end'
                    bodylang_class = "end"
                    bodylang_prob = angle_SEH
                    counter = (datetime.now() - start).total_seconds()

        except:
            pass

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(
                                      color=(106, 13, 173), thickness=4, circle_radius=5),
                                  mp_drawing.DrawingSpec(color=(255, 102, 0), thickness=5, circle_radius=10))

    if flag == 4:
        # frame = tk.Frame(height=600, width=700)
        # frame.place(x=10, y=90)
        # lmain = tk.Label(frame)
        # lmain.place(x=0, y=0)
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            landmarks = results.pose_landmarks.landmark
        except:
            pass

        try:
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)

            # Visualize angle
            cv2.putText(image, str(angle),
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                        255, 255), 2, cv2.LINE_AA
                        )

            if angle > 160:
                current_stage = "down"
                bodylang_class = "down"
                bodylang_prob = angle
            if angle < 30 and current_stage == 'down':
                current_stage = "up"
                bodylang_class = "down"
                bodylang_prob = angle
                counter += 1
                print(counter)
        except:
            pass

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(
                                      color=(106, 13, 173), thickness=4, circle_radius=5),
                                  mp_drawing.DrawingSpec(color=(255, 102, 0), thickness=5, circle_radius=10))

    img = image
    imgarr = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(imgarr)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, excesize)
    counterBox.configure(text=counter)
    probBox.configure(text=bodylang_prob)
    classBox.configure(text=current_stage)


def show_squat():
    global flag
    if flag == 0:
        flag = 1
        excesize()
    flag = 1


def show_push():
    global flag
    if flag == 0:
        flag = 2
        excesize()
    flag = 2


def show_plank():
    global flag
    if flag == 0:
        flag = 3
        excesize()
    flag = 3


def show_bicep():
    global flag
    if flag == 0:
        flag = 4
        excesize()
    flag = 4


menubar = Menu()
menubar.add_command(label="Squat", command=show_squat)
menubar.add_command(label="Pushup", command=show_push)
menubar.add_command(label="Plank", command=show_plank)
menubar.add_command(label="Bicep Curl", command=show_bicep)


window.config(menu=menubar)
# detect()
window.mainloop()
