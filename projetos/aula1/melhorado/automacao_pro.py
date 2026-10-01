"""Python Power Up Pro — evolução do projeto da Aula 1.
Interface local para configurar e acompanhar uma automação RPA com PyAutoGUI.
Desenvolvido por Anthony Freitas como estudo da Jornada Python Impressionador.
"""
import threading
import time
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25
CAMPOS = ["codigo", "marca", "tipo", "categoria", "preco_unitario", "custo", "obs"]

class PowerUpPro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Power Up Pro | Anthony Freitas")
        self.geometry("820x650")
        self.minsize(760, 590)
        self.stop_requested = False
        self.csv_path = tk.StringVar(value=str(Path(__file__).with_name("produtos_exemplo.csv")))
        self.url = tk.StringVar(value="https://dlp.hashtagtreinamentos.com/python/intensivao/login")
        self.email = tk.StringVar(value="")
        self.senha = tk.StringVar(value="")
        self.dry_run = tk.BooleanVar(value=True)
        self.x_campo = tk.IntVar(value=653)
        self.y_campo = tk.IntVar(value=294)
        self._build()

    def _build(self):
        wrap = ttk.Frame(self, padding=18); wrap.pack(fill="both", expand=True)
        ttk.Label(wrap, text="Python Power Up Pro", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(wrap, text="Automação RPA • Aula 1 • Jornada Python Impressionador").pack(anchor="w", pady=(0,14))

        cfg=ttk.LabelFrame(wrap,text="Configuração",padding=12); cfg.pack(fill="x")
        self._row(cfg,"Arquivo CSV",self.csv_path,0, browse=True)
        self._row(cfg,"URL do sistema",self.url,1)
        self._row(cfg,"E-mail",self.email,2)
        self._row(cfg,"Senha",self.senha,3, password=True)
        xy=ttk.Frame(cfg); xy.grid(row=4,column=1,sticky="w",pady=5)
        ttk.Label(cfg,text="Primeiro campo (x / y)").grid(row=4,column=0,sticky="w")
        ttk.Entry(xy,textvariable=self.x_campo,width=8).pack(side="left")
        ttk.Entry(xy,textvariable=self.y_campo,width=8).pack(side="left",padx=6)
        ttk.Button(xy,text="Capturar em 3s",command=self.capture_position).pack(side="left")
        ttk.Checkbutton(cfg,text="Modo de teste (não digita nem clica)",variable=self.dry_run).grid(row=5,column=1,sticky="w",pady=5)
        cfg.columnconfigure(1,weight=1)

        actions=ttk.Frame(wrap); actions.pack(fill="x",pady=12)
        self.start_btn=ttk.Button(actions,text="▶ Iniciar automação",command=self.start); self.start_btn.pack(side="left")
        ttk.Button(actions,text="■ Parar",command=self.stop).pack(side="left",padx=8)
        ttk.Button(actions,text="Validar CSV",command=self.validate_csv).pack(side="left")
        self.status=ttk.Label(actions,text="Pronto"); self.status.pack(side="right")

        self.progress=ttk.Progressbar(wrap,mode="determinate"); self.progress.pack(fill="x",pady=(0,10))
        box=ttk.LabelFrame(wrap,text="Log da execução",padding=8); box.pack(fill="both",expand=True)
        self.logbox=tk.Text(box,height=15,state="disabled",font=("Consolas",10)); self.logbox.pack(fill="both",expand=True)
        ttk.Label(wrap,text="Segurança: mover o mouse para um canto da tela aciona o FAILSAFE do PyAutoGUI.").pack(anchor="w",pady=(8,0))

    def _row(self,parent,label,var,row,browse=False,password=False):
        ttk.Label(parent,text=label).grid(row=row,column=0,sticky="w",pad=(0,10),pady=5)
        fr=ttk.Frame(parent); fr.grid(row=row,column=1,sticky="ew",pady=5)
        ttk.Entry(fr,textvariable=var,show="*" if password else "").pack(side="left",fill="x",expand=True)
        if browse: ttk.Button(fr,text="Selecionar",command=self.pick_csv).pack(side="left",padx=(8,0))

    def log(self,msg):
        self.logbox.configure(state="normal"); self.logbox.insert("end",f"{time.strftime('%H:%M:%S')}  {msg}\n"); self.logbox.see("end"); self.logbox.configure(state="disabled")

    def pick_csv(self):
        f=filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if f: self.csv_path.set(f)

    def capture_position(self):
        self.log("Posicione o mouse no primeiro campo. Captura em 3 segundos...")
        def cap():
            time.sleep(3); pos=pyautogui.position(); self.x_campo.set(pos.x); self.y_campo.set(pos.y); self.log(f"Posição capturada: {pos.x}, {pos.y}")
        threading.Thread(target=cap,daemon=True).start()

    def load_csv(self):
        tabela=pd.read_csv(self.csv_path.get())
        faltando=[c for c in CAMPOS if c not in tabela.columns]
        if faltando: raise ValueError("Colunas ausentes: " + ", ".join(faltando))
        return tabela

    def validate_csv(self):
        try:
            t=self.load_csv(); messagebox.showinfo("CSV válido",f"{len(t)} produtos encontrados.\nColunas obrigatórias presentes.")
        except Exception as e: messagebox.showerror("CSV inválido",str(e))

    def start(self):
        if not self.dry_run.get() and (not self.email.get() or not self.senha.get()):
            messagebox.showwarning("Dados de acesso","Informe e-mail e senha ou use o modo de teste."); return
        self.stop_requested=False; self.start_btn.config(state="disabled")
        threading.Thread(target=self.run_automation,daemon=True).start()

    def stop(self):
        self.stop_requested=True; self.log("Parada solicitada pelo usuário.")

    def run_automation(self):
        try:
            tabela=self.load_csv(); total=len(tabela); self.progress["maximum"]=total; self.progress["value"]=0
            self.status.config(text="Executando..."); self.log(f"Base validada: {total} produtos.")
            if self.dry_run.get(): self.log("MODO DE TESTE ativo: nenhuma ação será enviada ao computador.")
            else:
                webbrowser.open(self.url.get()); self.log("Navegador aberto. Aguardando carregamento..."); time.sleep(4)
                pyautogui.click(685,451); pyautogui.write(self.email.get()); pyautogui.press("tab"); pyautogui.write(self.senha.get()); pyautogui.press("enter"); time.sleep(4)
            for n,(_,r) in enumerate(tabela.iterrows(),1):
                if self.stop_requested: self.log("Execução interrompida."); break
                self.log(f"[{n}/{total}] {r['codigo']} • {r['marca']} • {r['tipo']}")
                if not self.dry_run.get():
                    pyautogui.click(self.x_campo.get(),self.y_campo.get())
                    for c in CAMPOS[:-1]: pyautogui.write(str(r[c])); pyautogui.press("tab")
                    if not pd.isna(r['obs']): pyautogui.write(str(r['obs']))
                    pyautogui.press("tab"); pyautogui.press("enter"); pyautogui.scroll(5000)
                self.progress["value"]=n
            else: self.log("Automação concluída com sucesso.")
            self.status.config(text="Pronto")
        except pyautogui.FailSafeException:
            self.log("FAILSAFE acionado. Automação interrompida."); self.status.config(text="Interrompido")
        except Exception as e:
            self.log(f"ERRO: {e}"); self.status.config(text="Erro")
        finally: self.start_btn.config(state="normal")

if __name__ == "__main__":
    PowerUpPro().mainloop()
