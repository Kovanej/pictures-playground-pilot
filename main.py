
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import time

from image_processor import ImageProcessor

if __name__ == "__main__":
    foldername = "moon age"
    image_processor = ImageProcessor(
        path_to_pictures=f"C:/Users/kovar/Meine Art/animation/{foldername}",
        fps=40
    )
    image_processor.animate(
       # pictures_saved=True
    )

breakpoint_var=1
