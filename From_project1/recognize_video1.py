from imutils.video import VideoStream, FPS
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
import time
from datetime import datetime
import pandas as pd

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detector", required=True,
                help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,
                help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-r", "--recognizer", required=True,
                help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
                help="path to label encoder")
ap.add_argument("-f", "--folder", required=True,
                help="path to attendance records folder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

classNames = ["unknown"]
names_and_time = []

def mark_attendance(name, probability):
    capture_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    details = {
        "Student's Name": name,
        "Time": capture_time,
        "Face Probability": str(round(probability * 100, 3)) + "%"
    }
    names_and_time.append(details)
    classNames.append(name)
    
def save_attendance_records(records, path):
    records = pd.DataFrame(records)
    if not os.path.exists(path):
        print("Creating Folder!")
        os.makedirs(path)
    file_name = "Attendance_Records_" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".csv"
    print(file_name)
    print(path)
    full_path = os.path.join(path, file_name)
    print(full_path)
    records.to_csv(full_path)
        

print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"], "res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(args["recognizer"], "rb").read())
le = pickle.loads(open(args["le"], "rb").read())

# initialize the video stream then allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

#start the FPS throughput estimator
fps = FPS().start()

# loop over the frames from the video stream
while True:
    frame = vs.read()
    
    # resize the frame to have a width of 600 pixels ( while maintaining the aspect
    # ratio), and then grab the image dimensions
    frame = imutils.resize(frame, width=600)
    (h, w) = frame.shape[:2]
    
    # construct a blob from the image
    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)
    
    # apply OpenCV's deep learning-based face detector to localize faces in the
    # input image
    detector.setInput(imageBlob)
    detections = detector.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections
        if confidence > args["confidence"]:
            print("confidence: ", confidence, args["confidence"])
            # compute the (x, y) -coordinates of the bounding box for the face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI
            face = frame[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue

            # construct a blob for the face ROI, then pass the blob through the face
            # embedding model to obtain the 128-d quantification of the face
            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            # perform classification to recognize the face
            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]
            print(le.classes_)
            if proba < 0.6:
                print("Prior Name: ", name)
                name = "unknown"
            print("Probability Measured: ", proba)
            print("Name Gained: ", name)
            if name not in classNames:
                mark_attendance(name, proba)

            # draw the bounding box of the face along with the associated probability
            text = "{}: {:.2f}%".format(name, proba * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            if name != "unknown":
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0 , 255, 0), 2)
                cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    
    fps.update()

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(10) & 0xFF
    if key == 27:
            break
            
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
if len(names_and_time):
    print(f"[INFO] Students Found: {names_and_time}")
    save_attendance_records(names_and_time, args["folder"])
else:
    print(f"[INFO] No Student Found!")
cv2.destroyAllWindows()
vs.stop()

