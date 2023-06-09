import cv2
import threading
import time
import sys
sys.path.append("./")
from src.libs.utils.config import Path
from src.libs.utils.face_mesh import FaceMesh
from src.libs.detection.drowsiness import Drowsiness

# Only for testing, we need to use it in another class, not implemented yet 
from src.libs.utils.gaze import Gaze


class VideoRecorder():  
    # Video class based on openCV 
    def __init__(self,
                 fps=6,
                 fourcc="MJPG",
                 device_index=-1,
                 frame_counts=1,
                 frameSize=(640,480),
                 video_filename=Path.VIDEO_FILE_NAME.value):
        """
        Args:
            fps (int): Frames per second.
            fourcc (str): Four character code.
            device_index (int): -1: Default device.
            frame_counts (int): Number of frames to record.
            frameSize (tuple): Size of the frame.
            video_filename (str): Output file path.
        """
        self.open = True
        # fps should be the minimum constant rate at which the camera can
        self.fps = fps
        # capture images (with no decrease in speed over time; 
        # testing is required)               
        self.fourcc = fourcc
        self.device_index = device_index
        self.frame_counts = frame_counts
        # video formats and sizes also depend and vary according to the camera 
        # used    
        self.frameSize = frameSize 
        
        self.path = Path.PATH_VIDEO_RECORDING.value
        self.video_filename = self.path + video_filename
        
        self.video_cap = cv2.VideoCapture(self.device_index)
        if not self.video_cap.isOpened():
            raise ValueError("Unable to open video source", device_index)
        
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, 
                                         self.video_writer, 
                                         self.fps, 
                                         self.frameSize)
        self.width = self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.start_time = time.time()
    
    
    def record(self)->None:
        """
        Video starts being recorded and saved to a video file.
        """
        # counter = 1
        timer_start = time.time()
        timer_current = 0
        
        cv2.namedWindow("video_frame", cv2.WINDOW_NORMAL)
        
        face_mesh = FaceMesh()
        drw = Drowsiness()
        
        # We do not use the Gaze class here, but we can use it in the future in
        # another class, like the Drowsiness class with EAR
        gz = Gaze()

        while self.open:
            ret, video_frame = self.video_cap.read()
            if ret:
                
                # NOTE: compute face landmarks
                landmarks = face_mesh.compute_face_landmarks(video_frame)
                # Comment the next line to not plot the face mesh
                face_mesh.plot_face_mesh(video_frame, landmarks)
                
                
                if landmarks:
                    landmarks = landmarks[0]
                    # NOTE: compute face landmarks, and detect drowsiness
                    video_frame = drw.detect_drowsiness(video_frame, landmarks)
                    video_frame = drw.plot_text(video_frame)
                    
                    # NOTE! The Gazes class is not implemented to handle 
                    # distraction detection, but it can only compute the gaze 
                    # direction.
                    # We need to implement a class to handle distraction 
                    # detection, o we don't call it here, but we can use it in 
                    # the future in another class, like the Drowsiness class 
                    # with EAR
                    gz.compute_gaze(video_frame, landmarks)
                    
                    
                    # NOTE! Here we can add image processing with deep learning 
                    # models to detect driver's distraction
                # video_frame = cv2.flip(video_frame, 1)
                cv2.imshow('video_frame', video_frame)
                
                # Write the frame to the current video file
                self.video_out.write(video_frame)
                # print str(counter) + " " + str(self.frame_counts) + " frames written " + str(timer_current)
                self.frame_counts += 1
                # counter += 1
                # timer_current = time.time() - timer_start
                # time.sleep(0.16)
                # gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('video_frame', gray)
                cv2.waitKey(1)
            else:
                break
                # 0.16 delay -> 6 fps

    
    def stop(self)->None:
        """
        Finishes the video recording therefore the thread too
        """
        if self.open==True:
            self.open=False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()
        pass
    
    
    def start(self)->None:
        """
        Launches the video recording function using a thread
        """
        video_thread = threading.Thread(target=self.record)
        video_thread.start()
        
    
    def get_frame(self):
        """
        Alternative function of record to capture video using a gui with tkinter

        Returns:
            _type_: _description_
        """
        face_mesh = FaceMesh()
        drw = Drowsiness()
        
        # We do not use the Gaze class here, but we can use it in the future in
        # another class, like the Drowsiness class with EAR
        gz = Gaze()
        if self.video_cap.isOpened():
            ret, video_frame = self.video_cap.read()
            if ret:
                # NOTE: compute face landmarks
                landmarks = face_mesh.compute_face_landmarks(video_frame)
                # Comment the next line to not plot the face mesh
                # face_mesh.plot_face_mesh(video_frame, landmarks)
                
                if landmarks:
                    landmarks = landmarks[0]
                    # NOTE: compute face landmarks, and detect drowsiness
                    video_frame = drw.detect_drowsiness(video_frame, landmarks)
                    video_frame = drw.plot_text(video_frame)
                    
                    # NOTE! The Gazes class is not implemented to handle 
                    # distraction detection, but it can only compute the gaze 
                    # direction.
                    # We need to implement a class to handle distraction 
                    # detection, o we don't call it here, but we can use it in 
                    # the future in another class, like the Drowsiness class 
                    # with EAR
                    gz.compute_gaze(video_frame, landmarks)
                    
                    
                    # NOTE! Here we can add image processing with deep learning 
                    # models to detect driver's distraction
                # video_frame = cv2.flip(video_frame, 1)
                #cv2.imshow('video_frame', video_frame)
                
                # Write the frame to the current video file
                self.video_out.write(video_frame)
                # print str(counter) + " " + str(self.frame_counts) + " frames written " + str(timer_current)
                self.frame_counts += 1
                # counter += 1
                # timer_current = time.time() - timer_start
                # time.sleep(0.16)
                # gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('video_frame', gray)
                cv2.waitKey(1)
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)