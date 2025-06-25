import soundfile as sf
import numpy as np

def detect_frequency(audio_segment, sample_rate=44100):
    fft = np.fft.fft(audio_segment)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
    magnitude = np.abs(fft[:len(fft)//2])
    freqs_positive = freqs[:len(freqs)//2]
    peak_idx = np.argmax(magnitude)
    return abs(freqs_positive[peak_idx])

def frequency_to_bit(frequency, threshold=660):
    return '1' if frequency > threshold else '0'

def decode_nrz(audio_signal, num_bits, sample_rate=44100, bit_duration=1.0):
    samples_per_bit = int(sample_rate * bit_duration)
    decoded_bits = ""
    for i in range(num_bits):
        start_idx = i * samples_per_bit
        end_idx = start_idx + samples_per_bit
        if end_idx > len(audio_signal):
            break
        segment = audio_signal[start_idx:end_idx]
        freq = detect_frequency(segment, sample_rate)
        bit = frequency_to_bit(freq)
        decoded_bits += bit
    return decoded_bits

audio_signal, samplerate = sf.read("dados_ar.wav")
num_bits = 15  # ajuste se souber outro valor

decoded_message = decode_nrz(audio_signal, num_bits, samplerate)
print(f"Mensagem decodificada NRZ: {decoded_message}")
