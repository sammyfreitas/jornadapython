# Aula 1 — Python Power Up

Projeto de estudo da **Jornada Python Impressionador (28/09/26 a 01/10/26)**.

## Básico
Reproduz a lógica ensinada na aula: abrir sistema, login, importar CSV, cadastrar produto e repetir.

## Melhorado — Python Power Up Pro
Evolução de Anthony Freitas com interface Tkinter, validação de CSV, modo de teste, progresso, logs, captura de coordenadas e interrupção segura.

## Instalação
```bash
pip install -r requirements.txt
python automacao_pro.py
```

> O PyAutoGUI controla mouse e teclado do computador. Teste primeiro com o modo de teste ativado e não publique credenciais no repositório.


## Instalação local
Use o mesmo Python que executará o projeto:

```powershell
& "C:\Program Files\Python312\python.exe" -m pip install --upgrade pip
& "C:\Program Files\Python312\python.exe" -m pip install pandas pyautogui
```

Ou, na versão melhorada:

```powershell
& "C:\Program Files\Python312\python.exe" -m pip install -r melhorado\requirements.txt
```

A demonstração web (`demo-pro/index.html`) não executa PyAutoGUI: ela reproduz a interface e o fluxo para que o visitante possa experimentar o projeto no GitHub Pages.
