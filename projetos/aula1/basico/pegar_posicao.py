import time
import pyautogui

print("Posicione o mouse no local desejado. Captura em 5 segundos...")
time.sleep(5)
print("Posição:", pyautogui.position())
