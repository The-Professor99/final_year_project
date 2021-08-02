from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import numpy as np
import pandas as pd
import csv
import sys

# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--prototxt", required=True,
#                 help="path to Caffe 'deploy' prototxt file")
# ap.add_argument("-m", "--model", required=True,
#                 help="path to Caffe pre-trained model")
# ap.add_argument("-c", "--confidence", type=float, default=0.5,
#                 help="minimum probability to filter weak detections")
# ap.add_argument("-o", "--output", required=True,
#                 help="path to output directory")
# args = vars(ap.parse_args())


#load OpenCV's haar cascade for face detection from disk
def capture_biometrics(name, mat_no):
    
    print("Starting")
    prototxt_file = "../constants/deploy.prototxt.txt" # make sure these initializations are present before continuing
    model_file = "../constants/res10_300x300_ssd_iter_140000.caffemodel"
    confidence_used = 0.85
    output_folder = "../changes/datasets" # make sure these initializations are present before continuing
    
    student_details = []

    student_details.append({
        "Name of the Student": name,
        "Matriculation Number": mat_no
    })
    
    students_data_file = "Students_data.csv"
    if not os.path.exists(students_data_file):
        print("Yeah creating...")
        with open(students_data_file, "w+") as f:
            outputWriter = csv.writer(f)
            outputWriter.writerow(['Name of the Student', 'Matriculation Number'])
            pass

    record = pd.read_csv(students_data_file)
    status = name in list(record["Name of the Student"])
    print(status)

    if not status:
        student_details = pd.DataFrame(student_details)
        student_details.to_csv("Students_data.csv", mode="a", index=False, header=False)
    else:
        confirm = input("User Detail already taken!, Continue or Go back(y/N): ")
        if confirm != "y":
            print("[ERROR] Exiting Application")
            sys.exit(-1)
            
            
    output_folder = os.path.join(output_folder, name)
    print("Output folder", output_folder)
    
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(prototxt_file, model_file)

    print("Path: ", output_folder)
    path = output_folder
    if not os.path.exists(path):
        print("Non-Existent path")
        os.makedirs(path)
        
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    total = 0
    
    while True:
        frame = vs.read()
        orig = frame.copy()
        frame = imutils.resize(frame, width=400)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123))

        # pass the blob through the network and obtain the detections and predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]
            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence < confidence_used:
                continue
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the bounding box of the face along with the associated
            # probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                (255, 0, 0), 2)
            cv2.putText(frame, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10) & 0xFF

        if key == ord("k"):
            print(key)
            p = os.path.sep.join([output_folder, "{}.png".format(str(total).zfill(5))])
            print("z_fill: ", p)
            cv2.imwrite(p, orig)
            total += 1
        elif key == ord("q"):
            break
            
    print("[INFO] {} face images stored".format(total))
    print("[INFO] saving user's information...")
    # with open("./students_data/school_information.csv", "r+") as file_object:

    cv2.destroyAllWindows()
    vs.stop()
    
capture_biometrics("Eze Ihechi Festus", "uj/2014/3n/sl")