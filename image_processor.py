
import cv2
import imageio
import os
import matplotlib.pyplot as plt
import numpy as np
import time


class ImageProcessor(object):

    def __init__(self, path_to_pictures: str, steps: int, fps: int = 25):

        self.path_to_pictures = f"{path_to_pictures}"
        self.images = self._load_the_pictures()
        self.images_without_watermark = None
        self.edited_images = list()
        self._remove_the_open_ai_watermark()
        self.fps = fps
        self.steps = steps

    def animate(self, pictures_saved: bool = False):
        if not pictures_saved:
            self._save_the_pictures()
        self._save_the_video()
        self._save_the_gif()

    def _save_the_video(self):

        if "anim" not in os.listdir():
            os.mkdir("./anim")
        os.chdir("./anim")
        with imageio.get_writer('output.mp4', fps=self.fps) as writer:
            for image in self.edited_images:
                writer.append_data(image)

    def _save_the_gif(self, resolution: int = 320):
        output_file = 'output.gif'
        images_resized = [cv2.resize(image, (resolution, resolution)) for image in self.edited_images]
        imageio.mimsave(output_file, images_resized, fps=self.fps)

    def _save_the_pictures(self):
        for img_ind in range(len(self.images_without_watermark)):
            img_prev = self.images_without_watermark[img_ind]
            if img_ind < len(self.images_without_watermark) - 1:
                img_next = self.images_without_watermark[img_ind + 1]
            else:
                img_next = self.images_without_watermark[0]
            img1 = img_prev[:, :, 0]
            img2 = img_next[:, :, 0]
            # flow = cv2.calcOpticalFlowFarneback(img1, img2, None, 0.8, 10, 30, 10, 5, 2)
            for step in range(self.steps + 1):
                t = step / self.steps
                img_now = (1 - t) * img_prev + t * img_next + (
                        np.random.rand(img_prev.shape[0], img_prev.shape[1], img_prev.shape[2]) - 1 / 2
                ) / (2 - np.random.rand() * t)
                img_now = np.where(img_now > 1, 1, np.where(img_now < 0, 0, img_now))
                # flow_t = (1 - t) * flow  # Scale the flow vectors by t
                # warped_img = cv2.remap(img_prev, flow_t, None, cv2.INTER_LINEAR)
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
