import random

# Função de verificação. Retorna True se o erro foi detectado, False caso contrário.
def verificar_crc(quadro_corrompido: str, gerador_bits: str) -> bool:
    resto = calcular_crc_manual(quadro_corrompido, gerador_bits)
    # Se o resto for uma string de zeros, o erro NÃO foi detectado.
    return not all(bit == '0' for bit in resto)

# Preparação do quadro original
QUADRO_TRANSMITIDO = MENSAGEM_BASE + CRC_BASE
testes = []

print("--- Iniciando 10 Testes com Erros Aleatórios de Rajada ---")

# 10 Testes com erros de rajada aleatórios
for i in range(10):
    tamanho_rajada = random.randint(1, 17)
    posicao_erro = random.randint(0, len(MENSAGEM_BASE) - tamanho_rajada)
    padrao_erro_rajada = '1' * tamanho_rajada
    erro_completo = ('0' * posicao_erro) + padrao_erro_rajada + ('0' * (len(QUADRO_TRANSMITIDO) - posicao_erro - tamanho_rajada))
    quadro_corrompido = xor_bits(QUADRO_TRANSMITIDO, erro_completo)
    detectado = verificar_crc(quadro_corrompido, GERADOR_PESSOAL)
    testes.append({
        "Teste #": i + 1,
        "Tipo de Erro": f"Rajada de {tamanho_rajada} bits",
        "Posição": posicao_erro,
        "Detectado?": "Sim" if detectado else "NÃO (Ponto Cego!)"
    })

# Teste 11: O Ponto Cego Garantido para o relatório
posicao_erro_cego = 10
erro_ponto_cego = ('0' * posicao_erro_cego) + GERADOR_PESSOAL + ('0' * (len(QUADRO_TRANSMITIDO) - posicao_erro_cego - len(GERADOR_PESSOAL)))
quadro_corrompido_cego = xor_bits(QUADRO_TRANSMITIDO, erro_ponto_cego)
detectado_cego = verificar_crc(quadro_corrompido_cego, GERADOR_PESSOAL)
testes.append({
    "Teste #": "11 (Especial)",
    "Tipo de Erro": "Padrão do Gerador G(x)",
    "Posição": posicao_erro_cego,
    "Detectado?": "Sim" if detectado_cego else "NÃO (Ponto Cego!)"
})

# --- Impressão do Relatório ---
print("\n--- Relatório Final dos Testes de Erro ---")
print("-" * 60)
print(f"{'Teste #':<15} | {'Tipo de Erro':<25} | {'Detectado?':<15}")
print("-" * 60)
for teste in testes:
    print(f"{str(teste['Teste #']):<15} | {teste['Tipo de Erro']:<25} | {teste['Detectado?']:<15}")
print("-" * 60)