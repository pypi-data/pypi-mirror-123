import cv2
from .preprocess import preprocess



@preprocess()
def resize(inp, w=None, h=None, keep_ar=False, interpolation=cv2.INTER_AREA):
    h_inp, w_inp = inp.shape[:2]
    update_params = False
    if keep_ar:
        width, height = target_size
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        elif height is None:
            r = width / float(w)
            dim = (width, int(h * r))
        target_size = dim
        keep_ar = False
        update_params = True
                    
    out = cv2.resize(inp, target_size, interpolation=interpolation)