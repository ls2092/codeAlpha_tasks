import numpy as np
from music21 import converter, instrument, note, chord, stream
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

# Step 1: Load and Preprocess Data
def get_notes():
    notes = []
    midi = converter.parse('example.mid')  # <-- Use any small MIDI file here

    parts = instrument.partitionByInstrument(midi)

    if parts:  # If multiple instruments
        notes_to_parse = parts.parts[0].recurse()
    else:
        notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))

    return notes

# Step 2: Prepare Sequences
def prepare_sequences(notes, n_vocab):
    sequence_length = 100
    pitchnames = sorted(set(item for item in notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    for i in range(0, len(notes) - sequence_length, 1):
        seq_in = notes[i:i + sequence_length]
        seq_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in seq_in])
        network_output.append(note_to_int[seq_out])

    n_patterns = len(network_input)

    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    network_input = network_input / float(n_vocab)
    network_output = np.eye(n_vocab)[network_output]

    return network_input, network_output

# Step 3: Create the Model
def create_model(network_input, n_vocab):
    model = Sequential()
    model.add(LSTM(256, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(256))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model

# Step 4: Generate Music
def generate_music(model, network_input, pitchnames, n_vocab):
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    start = np.random.randint(0, len(network_input)-1)
    pattern = network_input[start]
    pattern = pattern.reshape(1, pattern.shape[0], pattern.shape[1])

    prediction_output = []

    for note_index in range(200):
        prediction = model.predict(pattern, verbose=0)
        index = np.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)

        pattern = np.append(pattern[:,1:,:], [[ [index / float(n_vocab)] ]], axis=1)

    return prediction_output

# Step 5: Create a MIDI file
def create_midi(prediction_output):
    offset = 0
    output_notes = []

    for pattern in prediction_output:
        # if pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp='output.mid')

# Step 6: Run Everything
def main():
    notes = get_notes()
    n_vocab = len(set(notes))
    network_input, network_output = prepare_sequences(notes, n_vocab)
    model = create_model(network_input, n_vocab)

    print("Training model... (might take a few minutes)")
    model.fit(network_input, network_output, epochs=20, batch_size=64)

    print("Generating music...")
    pitchnames = sorted(set(item for item in notes))
    prediction_output = generate_music(model, network_input, pitchnames, n_vocab)

    print("Saving music to output.mid...")
    create_midi(prediction_output)
    print("Done! 🎵")

if __name__ == '__main__':
    main()
