# Used for bandpass filtering.
from scipy.signal import butter, filtfilt

# Applies a bandpass filter to the given channel.
# This filters the frequencies (hZ) into a specified range.
# The standard for low frequency filters is 1 Hz,
# and the standard for high frequency filters is 70 Hz.
def bandpass_filter(data, lowcut=1.0, highcut=10.0, fs=256.0, order=4):
    # Nyquist frequency - half the sampling rate.
    nyquist = 0.5 * fs

    # Low frequency cutoff.
    low = lowcut/nyquist

    # High frequency cutoff.
    high = highcut/nyquist

    # Designs the bandpass filter.
    b, a = butter(order, [low, high], btype='band')

    # Applies filter to the EEG signal twice to avoid phase delay.
    return filtfilt(b, a, data)