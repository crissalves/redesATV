import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# Configurações globais
SAMPLE_RATE = 44100
BIT_DURATION = 0.05
FREQ_LOW = 440
FREQ_HIGH = 880

# === Funções ===

def generate_tone(frequency, duration, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(2 * np.pi * frequency * t)
    window = np.hanning(len(tone))
    return tone * window

def encode_nrz(data_bits):
    audio_signal = np.array([])
    for bit in data_bits:
        freq = FREQ_HIGH if bit == '1' else FREQ_LOW
        tone = generate_tone(freq, BIT_DURATION)
        audio_signal = np.concatenate([audio_signal, tone])
    return audio_signal

def encode_manchester(data_bits):
    audio_signal = np.array([])
    for bit in data_bits:
        if bit == '1':
            tone1 = generate_tone(FREQ_HIGH, BIT_DURATION / 2)
            tone2 = generate_tone(FREQ_LOW, BIT_DURATION / 2)
        else:
            tone1 = generate_tone(FREQ_LOW, BIT_DURATION / 2)
            tone2 = generate_tone(FREQ_HIGH, BIT_DURATION / 2)
        audio_signal = np.concatenate([audio_signal, tone1, tone2])
    return audio_signal

def detect_frequency(audio_segment, sample_rate=SAMPLE_RATE):
    fft = np.fft.fft(audio_segment)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
    magnitude = np.abs(fft[:len(fft)//2])
    freqs_positive = freqs[:len(freqs)//2]
    peak_idx = np.argmax(magnitude)
    return abs(freqs_positive[peak_idx])

def frequency_to_bit(frequency, threshold=660):
    return '1' if frequency > threshold else '0'

def decode_nrz(audio_signal, num_bits):
    samples_per_bit = int(SAMPLE_RATE * BIT_DURATION)
    decoded_bits = ""
    for i in range(num_bits):
        start_idx = i * samples_per_bit
        end_idx = start_idx + samples_per_bit
        if end_idx > len(audio_signal):
            break
        segment = audio_signal[start_idx:end_idx]
        freq = detect_frequency(segment)
        decoded_bits += frequency_to_bit(freq)
    return decoded_bits

def decode_manchester(audio_signal, num_bits):
    samples_per_bit = int(SAMPLE_RATE * BIT_DURATION)
    decoded_bits = ""
    for i in range(num_bits):
        start_idx = i * samples_per_bit
        end_idx = start_idx + samples_per_bit
        if end_idx > len(audio_signal):
            break
        mid = start_idx + samples_per_bit // 2
        first_half = audio_signal[start_idx + samples_per_bit//8 : mid - samples_per_bit//8]
        second_half = audio_signal[mid + samples_per_bit//8 : end_idx - samples_per_bit//8]
        freq1 = detect_frequency(first_half)
        freq2 = detect_frequency(second_half)
        state1 = frequency_to_bit(freq1)
        state2 = frequency_to_bit(freq2)
        if state1 == '1' and state2 == '0':
            decoded_bits += '1'
        elif state1 == '0' and state2 == '1':
            decoded_bits += '0'
        else:
            decoded_bits += '?'  # erro
    return decoded_bits

def adicionar_ruido(audio_signal, snr_db=-3):
    """
    Adiciona ruído gaussiano ao sinal
    
    Args:
        audio_signal: Sinal original
        snr_db: Relação sinal-ruído em dB
    
    Returns:
        array: Sinal com ruído
    """
    signal_power = np.mean(audio_signal ** 2)
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear
    noise = np.random.normal(0, np.sqrt(noise_power), len(audio_signal))
    return audio_signal + noise

def contar_erros(bits_originais, bits_decodificados):
    erros = 0
    for o, d in zip(bits_originais, bits_decodificados):
        if o != d:
            erros += 1
    return erros

# === Execução com um único valor de ruído (Exemplo do notebook) ===

original_bits = "00111000"
snr = -3

print("\nEtapa 3: Teste pontual com ruído SNR = -3 dB")
clean_signal = encode_nrz(original_bits)
noisy_signal = adicionar_ruido(clean_signal, snr)
decoded = decode_nrz(noisy_signal, len(original_bits))

print(f"  Original:     {original_bits}")
print(f"  Decodificado: {decoded}")
print(f"  Correto:      {original_bits == decoded}\n")

# === Análise completa com gráfico ===

original_bits = "110101000100010" * 10
num_bits = len(original_bits)
snr_values = np.arange(5, -20, -1)

errors_nrz = []
errors_manchester = []

for snr in snr_values:
    # NRZ
    sinal_nrz = encode_nrz(original_bits)
    sinal_nrz_ruido = adicionar_ruido(sinal_nrz, snr)
    decodificado_nrz = decode_nrz(sinal_nrz_ruido, num_bits)
    erros_nrz = contar_erros(original_bits, decodificado_nrz)
    errors_nrz.append(erros_nrz)

    # Manchester
    sinal_manchester = encode_manchester(original_bits)
    sinal_manchester_ruido = adicionar_ruido(sinal_manchester, snr)
    decodificado_manchester = decode_manchester(sinal_manchester_ruido, num_bits)
    erros_manchester = contar_erros(original_bits, decodificado_manchester)
    errors_manchester.append(erros_manchester)

    print(f"SNR={snr} dB | Erros NRZ: {erros_nrz} | Erros Manchester: {erros_manchester}")

# Gráfico
plt.plot(snr_values, errors_nrz, label='NRZ', marker='o')
plt.plot(snr_values, errors_manchester, label='Manchester', marker='x')
plt.xlabel('SNR (dB)')
plt.ylabel('Número de erros')
plt.title('Erros de decodificação vs SNR')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
