import cv2
import time
from imutils import video
from typing import Iterable

from darcyai.input.input_stream import InputStream
from darcyai.stream_data import StreamData
from darcyai.utils import validate_not_none, timestamp

class CameraStream(InputStream):
    """
    A class for reading from a camera.
    """


    def __init__(self,
                 use_pi_camera:bool=False,
                 video_device:str=None,
                 video_width:int=640,
                 video_height:int=480,
                 flip_frames:bool=False,
                 fps:int=30):
        """
        Initializes a new instance of the CameraStream class.
        :param use_pi_camera: A boolean indicating whether or not to use the Raspberry Pi camera.
        :param video_device: The video device to use.
        :param video_width: The width of the video stream.
        :param video_height: The height of the video stream.
        :param flip_frames: A boolean indicating whether or not to flip the frames.
        :param fps: The frames per second to stream.
        """
        if not use_pi_camera:
            validate_not_none(video_device, "video_device is required")

        self.__use_pi_camera = use_pi_camera
        self.__video_device = video_device
        self.__frame_width = video_width
        self.__frame_height = video_height
        self.__flip_frames = flip_frames
        self.__fps = fps

        self.__vs = None
        self.__stopped = True


    def __initialize_video_camera_stream(self) -> video.VideoStream:
        """
        Initializes the video camera stream.
        :return: The video camera stream.
        """
        if not self.__use_pi_camera:
            vs = video.VideoStream(src=self.__video_device, resolution=(self.__frame_width, self.__frame_height), framerate=20).start()
        else:
            vs = video.VideoStream(usePiCamera=True, resolution=(self.__frame_width, self.__frame_height), framerate=20).start()

        test_frame = vs.read()
        counter = 0
        while test_frame is None:
            if counter == 10:
                raise Exception("Could not initialize video stream")

            # Give the camera unit a few seconds to start
            print("Waiting for camera unit to start...")
            counter += 1
            time.sleep(1)
            test_frame = vs.read()

        return vs


    def stop(self) -> None:
        """
        Stops the stream.
        :return: None
        """
        if not self.__vs is None:
            self.__vs.stop()
            self.__vs = None

        self.__stopped = True


    def stream(self) -> Iterable[StreamData]:
        """
        Streams the video.
        :return: an iterator that yields data from camera
        """
        if self.__vs is None:
            self.__vs = self.__initialize_video_camera_stream()
        
        self.__stopped = False

        while not self.__stopped:
            time.sleep(1 / self.__fps)

            frame = self.__vs.read()

            if self.__flip_frames:
                frame = cv2.flip(frame, 1)

            yield(StreamData(frame, timestamp()))
