import time
import tracemalloc
import os
from crc import Calculator, Crc16
import matplotlib.pyplot as plt
import platform

def xor_bits(a, b):
    resultado = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            resultado += '0'
        else:
            resultado += '1'
    return resultado

def calcular_crc_manual(dados_bits: str, gerador_bits: str) -> str:
    n = len(gerador_bits)
    r = n - 1
    mensagem_aumentada = list(dados_bits + '0' * r)
    for i in range(len(dados_bits)):
        if mensagem_aumentada[i] == '1':
            janela_atual = "".join(mensagem_aumentada[i : i + n])
            resultado_xor = xor_bits(janela_atual, gerador_bits)
            for j in range(n):
                mensagem_aumentada[i + j] = resultado_xor[j]
    resto = "".join(mensagem_aumentada[-r:])
    return resto

calculator_lib = Calculator(Crc16.MODBUS)
tamanhos_bytes = [1500, 3000, 6000, 16000]
gerador_modbus_bits = "11000000000000101"
resultados = []

for tamanho in tamanhos_bytes:
    mensagem_bytes = os.urandom(tamanho)
    mensagem_bits = "".join(format(byte, '08b') for byte in mensagem_bytes)
    
    # Medição da Implementação Manual
    tracemalloc.start()
    start_time_manual = time.perf_counter()
    crc_manual = calcular_crc_manual(mensagem_bits, gerador_modbus_bits)
    end_time_manual = time.perf_counter()
    mem_atual_manual, mem_pico_manual = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tempo_manual = end_time_manual - start_time_manual
    
    # Medição da Biblioteca
    tracemalloc.start()
    start_time_lib = time.perf_counter()
    crc_lib = calculator_lib.checksum(mensagem_bytes)
    end_time_lib = time.perf_counter()
    mem_atual_lib, mem_pico_lib = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tempo_lib = end_time_lib - start_time_lib
    
    resultados.append({
        "tamanho": tamanho,
        "tempo_manual": tempo_manual,
        "mem_pico_manual": mem_pico_manual / 1024,
        "tempo_lib": tempo_lib,
        "mem_pico_lib": mem_pico_lib / 1024
    })

print("--- Resultados Finais ---")
for res in resultados:
    print(res)

# Geração dos Gráficos
tamanhos = [r['tamanho'] for r in resultados]
tempos_manual = [r['tempo_manual'] for r in resultados]
tempos_lib = [r['tempo_lib'] for r in resultados]
mems_manual = [r['mem_pico_manual'] for r in resultados]
mems_lib = [r['mem_pico_lib'] for r in resultados]

# Gráfico 1: Tempo de Execução
plt.figure(figsize=(10, 5))
plt.plot(tamanhos, tempos_manual, marker='o', label='Implementação Manual')
plt.plot(tamanhos, tempos_lib, marker='o', label='Biblioteca Otimizada (crc)')
plt.title('Tempo de Execução vs. Tamanho da Mensagem')
plt.xlabel('Tamanho da Mensagem (bytes)')
plt.ylabel('Tempo de Execução (segundos)')
plt.legend()
plt.grid(True)
plt.show()

# Gráfico 2: Pico de Memória
plt.figure(figsize=(10, 5))
plt.plot(tamanhos, mems_manual, marker='o', label='Implementação Manual')
plt.plot(tamanhos, mems_lib, marker='o', label='Biblioteca Otimizada (crc)')
plt.title('Pico de Memória vs. Tamanho da Mensagem')
plt.xlabel('Tamanho da Mensagem (bytes)')
plt.ylabel('Pico de Memória (KiB)')
plt.legend()
plt.grid(True)
plt.show()

# Informações da Máquina
print("\n--- Informações da Máquina ---")
print(f"Processador: {platform.processor()}")
print(f"Sistema Operacional: {platform.system()} {platform.release()}")