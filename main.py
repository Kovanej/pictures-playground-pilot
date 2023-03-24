
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import time

from image_processor import ImageProcessor

if __name__ == "__main__":
    foldername = "strangers_2"
    image_processor = ImageProcessor(
        path_to_pictures=f"C:/Users/kovar/Meine Art/animation/{foldername}",
        steps=25, fps=25
    )
    image_processor.animate(
       # pictures_saved=True
    )

breakpoint_var=1
