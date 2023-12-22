import cv2
from bluemoon.extras.interrogate import default_interrogator as default_interrogator_photo
from bluemoon.extras.wd14tagger import default_interrogator as default_interrogator_anime
from bluemoon.utils.logly import logly

img = cv2.imread('./test_imgs/red_box.jpg')[:, :, ::-1].copy()
logly.info(default_interrogator_photo(img))
img = cv2.imread('./test_imgs/miku.jpg')[:, :, ::-1].copy()
logly.info(default_interrogator_anime(img))
