# Used for streaming EEG data via bluetooth.
from pylsl import StreamInlet, resolve_streams
from time import sleep

print("Looking for EEG streams...")

# Gives the stream time to initialize.
sleep(5)

# Finds all active LSL (Lab Streaming Layer) streams.
streams = resolve_streams()

# Loops through each stream 's' in 'streams'.
# if s.type() is EEG, 'next' gets the first match.
eeg_streams = next(s for s in streams if s.type() == 'EEG')

# Connects the code to the EEG data stream.
inlet = StreamInlet(eeg_streams)

print("Streaming EEG data...")

# Channel lists for storing sample and timestamp values.
tp9_raw_data, tp9_timestamp = [], []

tp10_raw_data, tp10_timestamp = [], []

af7_raw_data, af7_timestamp = [], []

af8_raw_data, af8_timestamp = [], []

# Main data collection loop.
while True:
    # Pulls sample and timestamp from the EEG data stream.
    sample, timestamp = inlet.pull_sample()

    # Samples for each channel.
    tp9 = sample[0]
    af7 = sample[1]
    af8 = sample[2]
    tp10 = sample[3]

    # Outputs the data, rounded to the second decimal place.
    print(f"TP9: {tp9:.2f} | AF7: {af7:.2f} | "
          f"AF8: {af8:.2f} | TP10: {tp10:.2f}")

    # Optional delay for data collection.
    sleep(0)

    # Adds samples and timestamps to the corresponding channel list.
    tp9_raw_data.append(tp9)
    tp9_timestamp.append(timestamp)

    af7_raw_data.append(af7)
    af7_timestamp.append(timestamp)

    af8_raw_data.append(af8)
    af8_timestamp.append(timestamp)

    tp10_raw_data.append(tp10)
    tp10_timestamp.append(timestamp)
