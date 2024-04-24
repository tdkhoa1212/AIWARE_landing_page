import numpy as np
import math
from scipy.ndimage import gaussian_filter
from scipy.stats import skew
from scipy import fftpack, signal, stats

def calculate_fft_magnitude_at_dominant_frequency(signal):
    fft = fftpack.fft(signal)
    dominant_frequency_magnitude = np.max(np.abs(fft))
    return dominant_frequency_magnitude

def calculate_total_psd(signal):
    fft = fftpack.fft(signal)
    psd = np.abs(fft) ** 2
    total_psd = np.sum(psd) / len(signal)
    return total_psd

def calculate_spectral_centroid(signal):
    fft = fftpack.fft(signal)
    magnitude_spectrum = np.abs(fft)
    freqs = fftpack.fftfreq(len(signal))
    spectral_centroid = np.sum(magnitude_spectrum * freqs) / np.sum(magnitude_spectrum)
    return spectral_centroid

def calculate_spectral_flatness(signal):
    fft = fftpack.fft(signal)
    magnitude_spectrum = np.abs(fft)
    spectral_flatness = np.exp(np.mean(np.log(magnitude_spectrum + 1e-10))) / np.mean(magnitude_spectrum)
    return spectral_flatness

def calculate_spectral_roll_off(signal, roll_off_fraction=0.85):
    fft = fftpack.fft(signal)
    magnitude_spectrum = np.abs(fft)
    freqs = fftpack.fftfreq(len(signal))
    total_energy = np.sum(magnitude_spectrum)
    cumulative_energy = np.cumsum(magnitude_spectrum)
    idx = np.where(cumulative_energy >= roll_off_fraction * total_energy)[0][0]
    return freqs[idx]

def calculate_rms(values):
    values = np.asarray(values) 
    rms_value = np.sqrt(np.mean(np.square(values)))
    return rms_value

def moving_average(signal, window_size=11):
    return np.convolve(signal, np.ones(window_size)/window_size, mode='valid')

def Gaussian(signal, window_size=11):
    return gaussian_filter(signal, sigma=window_size)

def Zero_crossing_Rate(signal):
    zero_crossings = np.where(np.diff(np.sign(signal)))[0]
    zcr = len(zero_crossings) / signal.size
    return zcr

def preprocess_signals(data, technique, axis, filter):
    apart_data = data[:, :, 0] if axis == 'horizontal' else data[:, :, 1]
    
    # Processing the signals based on technique
    if technique == 'RMS':
        processed_data = np.array([calculate_rms(i) for i in apart_data])
    elif technique == 'P2P':
        processed_data = np.array([np.ptp(i) for i in apart_data])
    elif technique == 'STD':
        processed_data = np.array([np.std(i) for i in apart_data])
    elif technique == 'Skewness':
        processed_data = np.array([skew(i) for i in apart_data])
    elif technique == 'ZCR':
        processed_data = np.array([Zero_crossing_Rate(i) for i in apart_data])

    elif technique == 'FFT':
        processed_data = np.array([calculate_fft_magnitude_at_dominant_frequency(i) for i in apart_data])
    elif technique == 'PSD':
        processed_data = np.array([calculate_total_psd(i) for i in apart_data])
    elif technique == 'SC':
        processed_data = np.array([calculate_spectral_centroid(i) for i in apart_data])
    elif technique == 'SF':
        processed_data = np.array([calculate_spectral_flatness(i) for i in apart_data])
    elif technique == 'SR':
        processed_data = np.array([calculate_spectral_roll_off(i) for i in apart_data])

    else:
        raise ValueError(f"Unknown technique: {technique}")

    # Applying the requested filter
    if filter == 'none':
        return processed_data
    elif filter == 'Gaussian':
        return Gaussian(processed_data)
    elif filter == 'Moving-average':
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
    