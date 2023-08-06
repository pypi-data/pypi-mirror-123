import numpy as np
from projectaile.data.loader import LOADER


@LOADER
def image_loader(img_path):
    # Test whether any of the image libraries exist
    
    loader_lib = None
    
    loaders = ['cv2', 'PIL', 'skimage', 'matplotlib', 'numpy']
    
    loader_func = None
    
    for loader in loaders:
        try:
            loader_lib = __import__(loader)
        except Exception as e:
            pass
        
        if loader_lib:
            print(f'Reading Using {loader_lib.__name__}')
            break
        
    if loader_lib.__name__ == 'cv2':
        loader_func = loader_lib.imread
    elif loader_lib.__name__ == 'skimage':
        loader_func = loader_lib.io.imread
    elif loader_lib.__name__ == 'matplotlib':
        loader_func = loader_lib.pyplot.imread
    elif loader_lib.__name__ == 'PIL':
        loader_func = loader_lib.Image.open
    elif loader_lib.__name__ == 'numpy':
        loader_func = loader_lib.fromfile
        
    if loader_lib.__name__ == 'numpy':
        img_path = open(img_path, 'r')
        
    img = loader_func(img_path)
    
    if len(img.shape) == 0:
        return f'Image Not Found At Path : {img_path}'
    
    return img