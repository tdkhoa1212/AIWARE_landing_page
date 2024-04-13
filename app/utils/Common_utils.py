import numpy as np
import math
from scipy.ndimage import gaussian_filter

def calculate_rms(values):
    values = np.asarray(values) 
    rms_value = np.sqrt(np.mean(np.square(values)))
    return rms_value

def moving_average(signal, window_size=11):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='valid')

def Gaussian(signal, window_size=11):
    return gaussian_filter(signal, sigma=window_size)

def preprocess_signals(data, technique, axis, filter):
    apart_data = data[:, :, 0] if axis == 'horizontal' else data[:, :, 1]
    
    # Processing the signals based on technique
    if technique == 'Magnitude':
        processed_data = np.concatenate((apart_data), axis=None)  # Assuming concatenation along a flat structure
    elif technique == 'RMS':
        processed_data = np.array([calculate_rms(i) for i in apart_data])
    else:
        raise ValueError(f"Unknown technique: {technique}")

    # Applying the requested filter
    if filter == 'none':
        return processed_data
    elif filter == 'gaussian':
        return Gaussian(processed_data)
    elif filter == 'moving-average':
        return moving_average(processed_data)
    else:
        raise ValueError(f"Unknown filter: {filter}")

    return processed_data
    
def predict_time(data, nor=20):
    '''
    INPUT =========================================
    data: - type: numpy.ndarray
          - dtype: float32
          - shape: 1D (for example: (1802,))
    nor: length of normal data

    OUTPUT =======================================
    fpt: - type: int
         - value: an integer value in N indicating the First Passage Time
    '''

    normal = data[:nor]
    mean_normal = normal.mean()
    std_normal = normal.std()

    limit_up = mean_normal + 3 * std_normal
    limit_down = mean_normal - 3 * std_normal

    # Find where data exceeds limits
    exceed_indices = np.where((data > limit_up) | (data < limit_down))[0]

    # Find the first sequence of 3 consecutive out-of-limit points
    if len(exceed_indices) > 2:
        consecutive_counts = np.diff(exceed_indices) == 1
        first_consecutive_idx = np.where(consecutive_counts[:-1] & consecutive_counts[1:])[0]

        if first_consecutive_idx.size > 0:
            fpt = exceed_indices[first_consecutive_idx[0]]
            return fpt

    # If no such point exists, return 0 or an appropriate default value
    return 0
    