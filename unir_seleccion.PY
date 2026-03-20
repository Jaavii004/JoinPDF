import sys
import os
import time
import tempfile
import subprocess
import atexit
from pypdf import PdfWriter, PdfReader
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Configuración Global de Estética
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Globales para gestión de limpieza
LOCK_FILE = os.path.join(tempfile.gettempdir(), "joinpdf_v2_core.lock")
ARGS_FILE = os.path.join(tempfile.gettempdir(), "joinpdf_v2_queue.txt")

def cleanup_lock():
    """Asegura que el lock se borre al salir del proceso maestro."""
    try:
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE, "r") as f:
                content = f.read().strip()
                if content == str(os.getpid()):
                    os.remove(LOCK_FILE)
    except: pass

class App(ctk.CTk):
    """Clase principal de la aplicación (oculta por defecto)."""
    def __init__(self):
        super().__init__()
        self.withdraw()

class SplashWindow(ctk.CTkToplevel):
    """Ventana de carga inicial mientras se recopilan los archivos."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Unir PDF")
        self.geometry("350x160")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.winfo_screenheight() // 2) - (160 // 2)
        self.geometry(f"+{x}+{y}")
        self.label = ctk.CTkLabel(self, text="Recopilando archivos...", font=("Inter", 16, "bold"))
        self.label.pack(pady=(25, 5))
        self.sub = ctk.CTkLabel(self, text="Esperando al sistema...", font=("Inter", 12))
        self.sub.pack()
        self.progress = ctk.CTkProgressBar(self, width=280)
        self.progress.pack(pady=20)
        self.progress.start()
        self.update()

    def set_status(self, text):
        self.sub.configure(text=text)
        self.update()

def is_process_running(pid):
    """Comprueba si un proceso con el PID dado está en ejecución en Windows."""
    try:
        output = subprocess.check_output(f'tasklist /fi "PID eq {pid}"', shell=True).decode(errors='ignore')
        return f" {pid} " in output or f'"{pid}"' in output # Búsqueda más precisa del PID
    except: return False

def collect_arguments(root, args):
    """Gestiona la comunicación entre instancias (Master/Slave) para recolectar archivos."""
    if not args: return []
    
    # 1. Validar si ya hay un Maestro VIVO
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                master_pid = int(f.read().strip())
            if is_process_running(master_pid):
                # 
                for _ in range(50):
                    try:
                        with open(ARGS_FILE, "a", encoding="utf-8") as f:
                            for arg in args: f.write(arg + "\n")
                        break
                    except: time.sleep(0.1)
                sys.exit(0)
            else:
                # El proceso maestro murió, limpiar lock
                os.remove(LOCK_FILE)
                if os.path.exists(ARGS_FILE): os.remove(ARGS_FILE)
        except: pass

    try:
        # 2. INTENTO SER MAESTRA (Lock persistente)
        with open(LOCK_FILE, "x") as f:
            f.write(str(os.getpid()))
        atexit.register(cleanup_lock)
        
        splash = SplashWindow(root)
        with open(ARGS_FILE, "w", encoding="utf-8") as f:
            for arg in args: f.write(arg + "\n")
        
        # 3. Recolección Dinámica (Paciencia Maestra)
        last_size = os.path.getsize(ARGS_FILE)
        start_time = time.time()
        last_change = time.time()
        
        while time.time() - start_time < 7.0: # Espera máx 7s
            time.sleep(0.3)
            splash.update()
            
            current_size = os.path.getsize(ARGS_FILE)
            if current_size > last_size:
                last_size = current_size
                last_change = time.time()
            
            # Decidir si tenemos lo suficiente para avanzar
            with open(ARGS_FILE, "r", encoding="utf-8") as f:
                count = len([l for l in f.readlines() if l.strip()])
            
            if count >= 2 and (time.time() - last_change > 1.2):
                break
            
            status = f"Buscando selección... {int(time.time()-start_time)}s" if count < 2 else f"Capturados {count} archivos..."
            splash.set_status(status)

        with open(ARGS_FILE, "r", encoding="utf-8") as f:
            collected = list(dict.fromkeys([line.strip() for line in f.readlines() if line.strip()]))
        
        splash.destroy()
        return collected

    except (FileExistsError, PermissionError):
        # Doble comprobación: alguien se nos adelantó
        sys.exit(0)
    except Exception:
        cleanup_lock()
        return args

class ProgressWindow(ctk.CTkToplevel):
    def __init__(self, parent, total_files):
        super().__init__(parent)
        self.title("Unir PDF")
        self.geometry("420x220")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (420 // 2)
        y = (self.winfo_screenheight() // 2) - (220 // 2)
        self.geometry(f"+{x}+{y}")
        self.label = ctk.CTkLabel(self, text=f"Uniendo {total_files} archivos...", font=("Inter", 15, "bold"))
        self.label.pack(pady=(30, 10))
        self.progress = ctk.CTkProgressBar(self, width=320)
        self.progress.set(0)
        self.progress.pack(pady=10)
        self.status = ctk.CTkLabel(self, text="Inicializando...", font=("Inter", 12))
        self.status.pack(pady=10)

    def update_progress(self, value, text, status_text):
        self.progress.set(value)
        self.label.configure(text=text)
        self.status.configure(text=status_text)
        self.update()

def main():
    args = sys.argv[1:]
    if not args: return
    root = App()
    
    archivos = collect_arguments(root, args)
    if not archivos: 
        root.destroy()
        return

    pdfs = [f for f in archivos if f.lower().endswith('.pdf')]
    if len(pdfs) < 2:
        messagebox.showwarning("Unir PDF", "Selecciona al menos 2 archivos PDF.")
        root.destroy()
        return

    pdfs.sort()
    root.update()
    
    output_path = filedialog.asksaveasfilename(
        parent=root,
        title="Guardar como...",
        initialfile="Fusion_PDF.pdf",
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not output_path:
        root.destroy()
        return

    progress_win = ProgressWindow(root, len(pdfs))
    try:
        merger = PdfWriter()
        for i, pdf in enumerate(pdfs):
            progress_win.update_progress((i+1)/len(pdfs), f"Procesando {i+1} de {len(pdfs)}", os.path.basename(pdf))
            with open(pdf, 'rb') as f:
                merger.append(PdfReader(f))

        progress_win.update_progress(0.95, "Finalizando...", "Escribiendo PDF...")
        with open(output_path, "wb") as f:
            merger.write(f)
        merger.close()
        progress_win.destroy()
        messagebox.showinfo("Unir PDF", "¡Todo listo! Fusión completada con éxito.")
    except Exception as e:
        if 'progress_win' in locals(): progress_win.destroy()
        messagebox.showerror("Error", str(e))
    finally:
        root.destroy()

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_lock()

