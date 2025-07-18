import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

SAMPLE_RATE = 44100
BIT_DURATION = 1.0
FREQ_LOW = 440
FREQ_HIGH = 880

def detect_frequency(audio_segment, sample_rate=SAMPLE_RATE):
    fft = np.fft.fft(audio_segment)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)

    magnitude = np.abs(fft[:len(fft)//2])
    freqs_positive = freqs[:len(freqs)//2]

    peak_idx = np.argmax(magnitude)
    detected_freq = abs(freqs_positive[peak_idx])

    return detected_freq

def frequency_to_bit(frequency, threshold=(FREQ_LOW + FREQ_HIGH)/2):
    return '1' if frequency > threshold else '0'

def decode_manchester(audio_signal, num_bits, sample_rate=SAMPLE_RATE):
    samples_per_bit = int(sample_rate * BIT_DURATION)
    decoded_bits = ""

    for i in range(num_bits):
        start_idx = i * samples_per_bit
        end_idx = start_idx + samples_per_bit

        if end_idx > len(audio_signal):
            print(f"Áudio curto demais para {num_bits} bits esperados.")
            break

        mid_point = start_idx + samples_per_bit // 2

        # Diminuindo a margem para 1/16
        margin = samples_per_bit // 16

        # Primeira metade
        first_half = audio_signal[start_idx + margin : mid_point - margin]
        freq1 = detect_frequency(first_half, sample_rate)
        state1 = frequency_to_bit(freq1)

        # Segunda metade
        second_half = audio_signal[mid_point + margin : end_idx - margin]
        freq2 = detect_frequency(second_half, sample_rate)
        state2 = frequency_to_bit(freq2)

        if state1 == '1' and state2 == '0':
            bit = '1'
        elif state1 == '0' and state2 == '1':
            bit = '0'
        else:
            bit = '?'  # Erro na transição

        print(f"Bit {i}: freq1={freq1:.1f}Hz, freq2={freq2:.1f}Hz -> {bit}")
        decoded_bits += bit

    return decoded_bits

def main():
    arquivo = 'dados_8_44100hz.wav'
    audio, sr = sf.read(arquivo)

    # Se áudio for estéreo, pega só um canal
    if len(audio.shape) > 1:
        audio = audio[:, 0]
        print("Áudio estéreo detectado. Usando apenas o canal esquerdo.")

    # Plot do sinal para análise visual
    plt.figure(figsize=(12, 3))
    plt.plot(audio)
    plt.title("Sinal de áudio do arquivo")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.show()

    num_bits_esperados = 8
    mensagem_decodificada = decode_manchester(audio, num_bits_esperados, sample_rate=sr)

    print(f"Mensagem decodificada: {mensagem_decodificada}")

if __name__ == "__main__":
    main()

