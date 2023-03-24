
import cv2
import imageio
import os
import matplotlib.pyplot as plt
import numpy as np
import time


class ImageProcessor(object):

    def __init__(self, path_to_pictures: str, fps: int = 25):

        self.path_to_pictures = f"{path_to_pictures}"
        self.images = self._load_the_pictures()
        self.images_without_watermark = None
        self.edited_images = list()
        self._remove_the_open_ai_watermark()
        self.fps = fps

    def animate(self, pictures_saved: bool = False):
        if not pictures_saved:
            self._save_the_pictures()
        self._save_the_video()

    def _save_the_video(self):

        os.chdir("./anim")
        out = cv2.VideoWriter("project.avi", cv2.VideoWriter_fourcc(*'DIVX'), 15,
                              (self.edited_images[0].shape[0], self.edited_images[0].shape[1]))
        for i in range(len(self.edited_images)):
            out.write(self.edited_images[i])
        out.release()
        self._save_the_gif()

    def _save_the_gif(self):
        output_file = 'output.gif'
        imageio.mimsave(output_file, self.edited_images, fps=self.fps)

    def _save_the_pictures(self):
        for img_ind in range(len(self.images_without_watermark)):
            img_prev = self.images_without_watermark[img_ind]
            if img_ind < len(self.images_without_watermark) - 1:
                img_next = self.images_without_watermark[img_ind + 1]
            else:
                img_next = self.images_without_watermark[0]
            for step in range(self.fps + 1):
                img_now = (1 - step / self.fps) * img_prev + step / self.fps * img_next + (
                            np.random.rand(img_prev.shape[0], img_prev.shape[1], img_prev.shape[2]) - 1 / 2) / 3
                img_now = np.where(img_now > 1, 1, np.where(img_now < 0, 0, img_now))
                self.edited_images.append(img_now)
                # plt.imsave(fname=f"anim/{img_ind}_{step}.png", arr=img_now)
                # plt.pause(1)
                # plt.close()

    def _remove_the_open_ai_watermark(self):
        self.images_without_watermark = [image[0:943, 0:943, :] for image in self.images]

    def _load_the_pictures(self):
        os.chdir(self.path_to_pictures)
        images = [plt.imread(img_dir) for img_dir in os.listdir() if ".png" in img_dir]
        return images
