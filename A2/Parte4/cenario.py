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

NOME_ALUNO = "Cristian Alves da Silva"
MATRICULA_ALUNO = "119211092"

MENSAGEM_BASE = "".join(format(ord(char), '08b') for char in NOME_ALUNO)

ultimo_digito = int(MATRICULA_ALUNO[-1])
GERADOR_PESSOAL = ""
NOME_GERADOR = ""

if ultimo_digito in [0, 1, 2]:
    GERADOR_PESSOAL = "11000000000000101"
    NOME_GERADOR = "CRC-16/MODBUS"
elif ultimo_digito in [3, 4, 5]:
    GERADOR_PESSOAL = "11000000000010001"
    NOME_GERADOR = "CRC-16/ARC"
elif ultimo_digito in [6, 7]:
    GERADOR_PESSOAL = "11001100000001001"
    NOME_GERADOR = "CRC-16/MAXIM"
else:
    GERADOR_PESSOAL = "10001000000100001"
    NOME_GERADOR = "CRC-16/CCITT-FALSE"

CRC_BASE = calcular_crc_manual(MENSAGEM_BASE, GERADOR_PESSOAL)

print("--- Cenário Personalizado Definido ---")
print(f"Nome do Aluno: {NOME_ALUNO}")
print(f"Matrícula: {MATRICULA_ALUNO} (Último Dígito: {ultimo_digito})")
print(f"Gerador Escolhido: {NOME_GERADOR} ({GERADOR_PESSOAL})")
print(f"\nMensagem Base em bits (M(x)):\n{MENSAGEM_BASE}")
print(f"\nCRC da Mensagem Base:\n{CRC_BASE}")