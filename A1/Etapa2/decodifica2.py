import numpy as np
import soundfile as sf

def detect_frequency(audio_segment, sample_rate=44100):
    fft = np.fft.fft(audio_segment)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
    magnitude = np.abs(fft[:len(fft)//2])
    freqs_positive = freqs[:len(freqs)//2]
    peak_idx = np.argmax(magnitude)
    detected_freq = abs(freqs_positive[peak_idx])
    return detected_freq

def frequency_to_bit(frequency, threshold=660):
    return '1' if frequency > threshold else '0'

def decode_nrz(audio_signal, num_bits, sample_rate=44100, debug=False):
    samples_per_bit = int(sample_rate * 1.0)  # 1 segundo por bit
    decoded_bits = ""
    
    if debug:
        print("Decodificando NRZ:")
    
    for i in range(num_bits):
        start_idx = i * samples_per_bit
        end_idx = start_idx + samples_per_bit
        if end_idx > len(audio_signal):
            if debug:
                print(f"Aviso: áudio muito curto para {num_bits} bits")
            break
        
        mid_start = start_idx + samples_per_bit // 4
        mid_end = end_idx - samples_per_bit // 4
        segment = audio_signal[mid_start:mid_end]
        
        freq = detect_frequency(segment, sample_rate)
        bit = frequency_to_bit(freq)
        decoded_bits += bit
        
        if debug:
            print(f"Bit {i}: freq={freq:.1f}Hz -> '{bit}'")
    
    return decoded_bits

# --- Execução principal ---

if __name__ == "__main__":
    arquivo = "dados_8_44100hz.wav"
    print(f"Lendo arquivo: {arquivo}")
    audio_signal, samplerate = sf.read(arquivo)
    
    # Ajuste o número de bits conforme seu gráfico (15 bits no seu caso)
    num_bits = 15
    
    decoded_message = decode_nrz(audio_signal, num_bits, sample_rate=samplerate, debug=True)
    print(f"Mensagem decodificada NRZ: {decoded_message}")
