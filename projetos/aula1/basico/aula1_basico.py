# Aula 1 — Python Power Up | versão básica
# Jornada Python Impressionador
# Adaptação de estudo: Anthony Freitas
#
# Instale: pip install pyautogui pandas
# IMPORTANTE: ajuste as coordenadas para a sua tela antes de executar.

import time
import pandas as pd
import pyautogui

URL_SISTEMA = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"
EMAIL = "seu-email@exemplo.com"
SENHA = "sua-senha"
ARQUIVO = "produtos_exemplo.csv"

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True

# 1. Entrar no sistema
pyautogui.press("win")
pyautogui.write("chrome")
pyautogui.press("enter")
time.sleep(2)
pyautogui.write(URL_SISTEMA)
pyautogui.press("enter")
time.sleep(3)

# 2. Fazer login — ajuste os pontos com pegar_posicao.py
pyautogui.click(x=685, y=451)
pyautogui.write(EMAIL)
pyautogui.press("tab")
pyautogui.write(SENHA)
pyautogui.press("enter")
time.sleep(3)

# 3. Importar a base
tabela = pd.read_csv(ARQUIVO)

# 4 e 5. Cadastrar cada produto e repetir até o fim
for linha in tabela.index:
    pyautogui.click(x=653, y=294)  # ajuste para o primeiro campo
    campos = ["codigo", "marca", "tipo", "categoria", "preco_unitario", "custo"]
    for campo in campos:
        pyautogui.write(str(tabela.loc[linha, campo]))
        pyautogui.press("tab")

    obs = tabela.loc[linha, "obs"]
    if not pd.isna(obs):
        pyautogui.write(str(obs))
    pyautogui.press("tab")
    pyautogui.press("enter")
    pyautogui.scroll(5000)

print(f"Cadastro finalizado: {len(tabela)} produtos processados.")
