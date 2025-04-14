# Used for bandpass filtering.
from scipy.signal import butter, filtfilt
import pandas as pd


def bandpass_filter(input_path='/Users/griffinkeeler/PycharmProjects'
                     '/neuro-blink-refined/raw_eeg_data.csv',
                    output_path='filtered_eeg_data.csv',
                    lowcut=1.0, highcut=10.0, fs=256.0, order=4):
    """Applies a bandpass filter to the given channel. This filters the
     frequencies (hZ) into a specified range. The standard for low frequency
    filters is 1 Hz, and the standard for high frequency filters is 70 Hz."""

    df = pd.read_csv(input_path)

    # Nyquist frequency - half the sampling rate.
    nyquist = 0.5 * fs

    # Low frequency cutoff.
    low = lowcut/nyquist

    # High frequency cutoff.
    high = highcut/nyquist

    # Designs the bandpass filter.
    b, a = butter(order, [low, high], btype='band')

    channels = ['TP9', 'AF7', 'AF8', 'TP10']

    for ch in channels:
        df[ch] = filtfilt(b, a, df[ch])

    # Save filtered data to csv
    df.to_csv(output_path, index=False)

def main():
    bandpass_filter()


if __name__ == "__main__":
    main()

