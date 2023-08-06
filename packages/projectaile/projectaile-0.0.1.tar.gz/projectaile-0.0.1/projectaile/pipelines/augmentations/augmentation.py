from functools import wraps
import random

# base augmentation method
def augmentation(config, apply_on_target=False):
    if config:
        # assign config vars to the function and use them
        # otherwise use defaults
        prob = config['apply_probability']
        
    def decor(func):
        func.__apply_prob__ = prob
        func.__callable_type__ = 'augmentation'
        func.__apply_on_target__ = apply_on_target
        @wraps(func)
        def wrapper(x, y, *args, **kwargs):
            if random.random() < prob:
                x = func(x, *args, **kwargs)
                if apply_on_target:
                    y = func(y, *args, **kwargs)
            return x, y
        return wrapper
    return decor