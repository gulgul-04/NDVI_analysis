import numpy as np

def calculate_valid_fractions(valid_pixels, total_pixels):
    fractions = np.array(valid_pixels) / np.array(total_pixels)
    return fractions

def assign_weights(fractions):
    def get_weight(f):
        if f > 0.80:
            return 5
        elif f > 0.65:
            return 4
        elif f > 0.55:
            return 3
        elif f > 0.40:
            return 2
        elif f > 0.30:
            return 1
        else:
            return 0
    weights = np.array([get_weight(f) for f in fractions])
    return weights
