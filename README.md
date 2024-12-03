# README: AI Squat Counter 

## Overview

This Python project implements a **real-time AI squat counter** using MediaPipe, OpenCV, and CVZone. It tracks body movements through pose detection, calculates knee angles, and counts valid squats based on the detected angles. The system adapts dynamically to the user's camera orientation and provides accurate results in real-time.

---

## Features

1. **Pose Detection**:  
   - Leverages MediaPipe’s **BlazePose** model for accurate keypoint tracking.  
   - Tracks 33 keypoints on the human body using **Convolutional Neural Networks (CNNs)** and **Graph Neural Networks (GNNs)**.  
   - Dynamically determines which side of the body to analyze based on keypoint visibility.  

2. **Knee Angle Calculation**:  
   - Detects keypoints at the hip, knee, and ankle for both legs: landmarks 23, 24, 25, 26, 27, and 28.  
   - Calculates angles using **arctangent functions** for precise detection of squats.  

3. **Dynamic and Adaptive**:  
   - Works seamlessly with either side of the body facing the camera.  
   - Provides a progress bar and real-time squat count on the screen.  

4. **Real-Time Performance**:  
   - Efficient implementation ensures smooth operation without heavy computational demands.  

---

## How It Works

1. **Pose Detection with BlazePose**:  
   - The detector uses a **Single Shot Detection (SSD)** method to locate the human body and create a bounding box.  
   - The bounding box is resized to a 256x256 image and fed into an estimator, which uses heatmaps to predict keypoint locations.  
   - Outputs a list of landmarks with coordinates and visibility scores.  

2. **Knee Angle Calculation**:  
   - Using landmarks at the hip, knee, and ankle, the system calculates the knee angle using the formula:
     \[
     \text{angle} = \arctan\left(\frac{y_2 - y_1}{x_2 - x_1}\right) - \arctan\left(\frac{y_3 - y_2}{x_3 - x_2}\right)
     \]  
   - The side with the higher visibility score (left or right) is used for squat detection.  

3. **Squat Validation**:  
   - A squat is considered valid when the knee angle is at least 95 degrees.  
   - The system counts a squat when the user transitions between standing and squatting positions.  

4. **Dynamic Visualization**:  
   - Keypoints are displayed on the video feed for real-time feedback.  
   - A progress bar tracks how deep the user squats.  

---

## How to Set Up

1. Install Python and required libraries:
   ```bash
   pip install opencv-python-headless numpy cvzone
2. Connect a webcam to your computer.
3. Run the script: python squat_counter.py
4. Position yourself so the webcam can see your full body.

---

## Limitations

1. Single-User Tracking:
   Current implementation tracks only one person at a time.

2. Lighting Sensitivity:
  Detection accuracy decreases in poorly lit environments.

3. Hardware Dependency:
  Performance may vary based on the quality of the camera and system processing power.

4. Angle Precision:
   Minor inaccuracies may occur due to noise in keypoint detection.

---

## Future Improvements

1. Multi-Person Tracking:
  Extend to track multiple users simultaneously for group fitness.

2. Lighting Robustness:
  Add preprocessing to handle poor lighting conditions and noisy backgrounds.

3. Advanced Feedback:
  Integrate AI models for real-time form correction and exercise advice.

4. Broader Applications:
  Adapt for other exercises like lunges, push-ups, or movements used in physical therapy and sports.

---

## Key Learnings

1. Integration:
   Learned to combine OpenCV, MediaPipe, and CVZone for real-time AI applications.
2. Pose Estimation:
   Gained expertise in using BlazePose for landmark detection.
3. Collaboration:
   Improved teamwork and project management skills during development.
4. AI Applications:
   Demonstrated the potential of low-cost AI tools for fitness and health analytics.

---

## Acknowledgments

1. Google MediaPipe:
    For providing the BlazePose model and pose detection tools.
2. OpenCV: 
    For video capture and image processing.
3. CVZone: 
    For simplifying the integration of MediaPipe with OpenCV.
