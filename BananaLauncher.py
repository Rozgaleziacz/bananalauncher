import tkinter as tk
from tkinter import ttk
import random
import math
import pygame
import webbrowser
import json
import os
import subprocess
from PIL import Image, ImageTk
import threading
try:
    from pypresence import Presence
    DISCORD_RPC_AVAILABLE = True
except ImportError:
    DISCORD_RPC_AVAILABLE = False

pygame.mixer.init()

# Discord RPC
DISCORD_APP_ID = "1456600376777117899"
rpc_client = None

def init_discord_rpc():
    global rpc_client
    if DISCORD_RPC_AVAILABLE:
        try:
            rpc_client = Presence(DISCORD_APP_ID)
            rpc_client.connect()
            print("[✓] Discord RPC connected")
            update_discord_rpc("Idle in Launcher")
        except Exception as e:
            print(f"[!] Discord RPC connection failed: {e}")
            print(f"[!] Make sure Discord is running and the app ID is correct")
            rpc_client = None
    else:
        print("[!] pypresence not installed. Install with: pip install pypresence")

def update_discord_rpc(status, version=None):
    if rpc_client:
        try:
            if version:
                rpc_client.update(state=status, details=f"Version: {version}", large_image="banana", large_text="Banana Launcher")
            else:
                rpc_client.update(state=status, large_image="banana", large_text="Banana Launcher")
            print(f"[RPC] Updated: {status}" + (f" ({version})" if version else ""))
        except Exception as e:
            print(f"[!] RPC update failed: {e}")

def close_discord_rpc():
    global rpc_client
    if rpc_client:
        try:
            rpc_client.close()
        except Exception:
            pass

# Global state
auth_user = None
auth_token = None
auth_uuid = None
selected_version = None

# Auth file
auth_file = "auth_cache.json"

# Microsoft OAuth config - replace with your Azure App's Client ID if you have one.
# The default below is the official Minecraft client id and often returns "unauthorized_client".
CLIENT_ID = "00000000402b5328"
REDIRECT_URI = "https://login.live.com/oauth20_desktop.srf"

# OAuth PKCE helpers
oauth_state = None
oauth_code_verifier = None

def load_auth():
    global auth_user, auth_token, auth_uuid
    try:
        if os.path.exists(auth_file):
            with open(auth_file, 'r') as f:
                data = json.load(f)
                auth_user = data.get('name')
                auth_token = data.get('token')
                auth_uuid = data.get('uuid')
    except Exception:
        pass

def save_auth(username, token=None, uuid=None):
    try:
        data = {'name': username}
        if token:
            data['token'] = token
        if uuid:
            data['uuid'] = uuid
        with open(auth_file, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass

def logout():
    global auth_user, auth_token, auth_uuid
    auth_user = None
    auth_token = None
    auth_uuid = None
    if os.path.exists(auth_file):
        os.remove(auth_file)
    update_auth_display()

def update_auth_display():
    global auth_user
    if auth_user:
        auth_label.config(text=f"✅ {auth_user}", fg="#90EE90")
        auth_btn.config(text="Logout", command=logout)
    else:
        auth_label.config(text="Not authorized", fg="#FFB6C1")
        auth_btn.config(text="Login", command=login_choice)

def set_username():
    """Simple username input (offline)"""
    global auth_user
    dialog = tk.Toplevel(root)
    dialog.title("Set Username (Offline)")
    dialog.geometry("350x150")
    dialog.configure(bg="#111111")
    
    tk.Label(dialog, text="Enter Minecraft username:", bg="#111111", fg="#FFD400", font=("Segoe UI", 10, "bold")).pack(pady=10)
    
    entry = tk.Entry(dialog, font=("Courier", 10), width=30)
    entry.pack(padx=10, pady=5)
    entry.focus()
    
    def submit():
        username = entry.get().strip()
        if username and len(username) >= 3:
            global auth_user
            auth_user = username
            save_auth(auth_user)
            update_auth_display()
            dialog.destroy()
    
    tk.Button(dialog, text="Submit", command=submit, bg="#FFD400", fg="black", font=("Segoe UI", 9, "bold")).pack(pady=10)
    dialog.transient(root)
    dialog.grab_set()

def login_choice():
    """Open offline username dialog"""
    set_username()

def authorize():
    """Legacy placeholder (offline mode only)"""
    pass

console_window = None
console_text = None

def log_to_console(message):
    """Thread-safe logging to console window"""
    global console_text
    # Ensure console exists so logs are visible
    if not console_text:
        try:
            create_console()
        except Exception:
            pass

    if console_text:
        # keep the widget in normal state so selection works; typing is blocked by bindings
        console_text.insert("end", message + "\n")
        console_text.see("end")
        console_text.update()

def create_console():
    """Create console window"""
    global console_window, console_text
    
    console_window = tk.Toplevel(root)
    console_window.title("🍌 Launch Console 🍌")
    console_window.geometry("600x400")
    console_window.configure(bg="#0f0f0f")
    
    # Use a normal text widget so users can select text; block key presses to prevent edits
    console_text = tk.Text(console_window, bg="#111111", fg="#90EE90", font=("Courier", 9), state="normal")
    console_text.pack(fill="both", expand=True, padx=5, pady=5)

    # Prevent typing into the console while still allowing selection and copying
    console_text.bind("<Key>", lambda e: "break")
    console_text.bind("<<Paste>>", lambda e: "break")

    scrollbar = tk.Scrollbar(console_window)
    scrollbar.pack(side="right", fill="y")
    console_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=console_text.yview)

    # Copy helpers and context menu
    def copy_selection(event=None):
        try:
            text = console_text.get("sel.first", "sel.last")
        except tk.TclError:
            text = console_text.get("1.0", "end")
        root.clipboard_clear()
        root.clipboard_append(text)
        return "break"

    def copy_all():
        text = console_text.get("1.0", "end")
        root.clipboard_clear()
        root.clipboard_append(text)

    menu = tk.Menu(console_window, tearoff=0)
    menu.add_command(label="Copy Selection", command=copy_selection)
    menu.add_command(label="Copy All", command=copy_all)

    console_text.bind("<Control-c>", copy_selection)
    console_text.bind("<Control-C>", copy_selection)
    def show_menu(event):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            try:
                menu.grab_release()
            except Exception:
                pass

    console_text.bind("<Button-3>", show_menu)

    # Release any existing modal grabs so console can receive clicks/focus
    try:
        root.grab_release()
    except Exception:
        pass

    console_window.focus_force()
    console_text.focus_set()

def play_minecraft_thread():
    """Download and launch Minecraft in background thread"""
    global selected_version, auth_user, auth_token, auth_uuid
    
    try:
        log_to_console(f"[*] Starting launcher for {selected_version}...")
        
        import minecraft_launcher_lib.install as install
        import minecraft_launcher_lib.command as command
        import minecraft_launcher_lib
        
        mc_dir = os.path.join(os.getcwd(), "minecraft")
        log_to_console(f"[*] Minecraft directory: {mc_dir}")
        log_to_console(f"[*] Downloading from: https://launcher.mojang.com")
        
        # Download if needed
        log_to_console(f"[*] Installing version {selected_version}...")
        log_to_console(f"[*] This may take a while (downloading ~200-500MB)...")
        status_label.config(text=f"⏳ Installing {selected_version}...", fg="#FFD400")
        
        install.install_minecraft_version(selected_version, mc_dir)
        log_to_console(f"[✓] Version {selected_version} downloaded and ready")
        
        # Get launch command
        log_to_console(f"[*] Preparing launch command...")
        # Provide authenticated token/uuid when available, otherwise use offline demo token
        if auth_token and auth_uuid:
            options = {
                "username": auth_user,
                "uuid": auth_uuid,
                "token": auth_token,
            }
        else:
            options = {
                "username": auth_user,
                "uuid": "00000000-0000-0000-0000-000000000000",
                "token": "demo_token",
            }
        
        cmd = command.get_minecraft_command(selected_version, mc_dir, options)
        log_to_console(f"[*] Command created, launching Minecraft...")
        
        # Launch
        log_to_console(f"[*] Launching Minecraft {selected_version}...")
        status_label.config(text=f"✅ Launching {selected_version}...", fg="#90EE90")
        update_discord_rpc(f"Launching minecraft", selected_version)
        subprocess.Popen(cmd)
        log_to_console(f"[✓] Minecraft launched!")
        update_discord_rpc(f"Playing minecraft", selected_version)
        
    except Exception as e:
        error_msg = str(e)
        log_to_console(f"[✗] ERROR: {error_msg}")
        import traceback
        log_to_console(traceback.format_exc())
        status_label.config(text=f"❌ Error: {str(e)[:50]}", fg="#FF6B6B")

def play_minecraft():
    """Download and launch Minecraft"""
    global selected_version, auth_user, console_window
    
    if not selected_version:
        status_label.config(text="❌ Select a version first", fg="#FF6B6B")
        return
    
    if not auth_user:
        status_label.config(text="❌ Set username first", fg="#FF6B6B")
        return
    
    # Create console window
    if not console_window:
        create_console()
    else:
        console_window.lift()
    
    status_label.config(text=f"⏳ Launching {selected_version}...", fg="#FFD400")
    log_to_console(f"\n{'='*50}\n[START] Play button clicked\n{'='*50}")
    
    # Run in background thread to prevent UI freeze
    thread = threading.Thread(target=play_minecraft_thread, daemon=True)
    thread.start()

# Setup root window
root = tk.Tk()
root.title("🍌 Banana Launcher 🍌")
root.state("zoomed")

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

# Canvas
canvas = tk.Canvas(root, bg="#0f0f0f", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# --- Logo at Top ---
try:
    logo_img = Image.open("banana_launcher_logo.png")
    logo_width, logo_height = logo_img.size
except FileNotFoundError:
    print("⚠️  banana_launcher_logo.png not found.")
    logo_img = Image.new('RGB', (120, 120), (255, 215, 50))
    logo_width, logo_height = 120, 120

logo_pulse = 0

logo_tk_global = ImageTk.PhotoImage(logo_img)
logo_id = canvas.create_image(screen_w // 2, 80, anchor="center", image=logo_tk_global)

def animate_logo():
    global logo_tk_global, logo_pulse, logo_id

    logo_pulse = (logo_pulse + 0.08) % (2 * 3.14159)
    scale = 1.0 + 0.08 * math.sin(logo_pulse)

    new_width = int(logo_width * scale)
    new_height = int(logo_height * scale)
    resized = logo_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    logo_tk_global = ImageTk.PhotoImage(resized)
    canvas.itemconfig(logo_id, image=logo_tk_global)

    root.after(50, animate_logo)

animate_logo()

# --- Music Frame (top right) ---
music_frame = tk.Frame(canvas, bg="#111111", highlightbackground="#FFD400", highlightthickness=2, width=200, height=120)
music_frame.pack_propagate(False)
canvas.create_window(screen_w - 210, 10, anchor="nw", window=music_frame)

PLAYLIST = [
    ("banany.mp3", "Bananowa Piosenka"),
    ("banany2.mp3", "BANANA!"),
    ("banany3.mp3", "I'm A Banana")
]

music_index = 0
is_playing = False

def play_music():
    global is_playing, music_index
    try:
        pygame.mixer.music.load(PLAYLIST[music_index][0])
        pygame.mixer.music.play(-1)
        is_playing = True
        song_label.config(text=PLAYLIST[music_index][1])
    except:
        song_label.config(text="Song not found")

def stop_music():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False

def next_song():
    global music_index
    music_index = (music_index + 1) % len(PLAYLIST)
    play_music()

def set_volume(val):
    pygame.mixer.music.set_volume(float(val))

song_label = tk.Label(music_frame, text="— no music —", bg="#111111", fg="#FFD400", wraplength=180, justify="right", font=("Segoe UI", 9, "bold"))
song_label.pack(padx=8, pady=(6, 4))

controls = tk.Frame(music_frame, bg="#111111")
controls.pack(pady=4)

tk.Button(controls, text="▶", command=play_music, bg="#FFD400", fg="black", width=3, relief="flat").pack(side="left", padx=2)
tk.Button(controls, text="⏸", command=stop_music, bg="#FFD400", fg="black", width=3, relief="flat").pack(side="left", padx=2)
tk.Button(controls, text="⏭", command=next_song, bg="#FFD400", fg="black", width=3, relief="flat").pack(side="left", padx=2)

volume = tk.Scale(music_frame, from_=0, to=1, resolution=0.01, orient="horizontal", command=set_volume, bg="#111111", fg="#FFD400", troughcolor="#FFD400", highlightthickness=0, length=180)
volume.set(0.4)
volume.pack(padx=6, pady=(4, 6))

# --- Auth Frame (bottom left) ---
auth_frame = tk.Frame(canvas, bg="#111111", highlightbackground="#FFD400", highlightthickness=2, width=200, height=110)
auth_frame.pack_propagate(False)
canvas.create_window(10, screen_h - 120, anchor="nw", window=auth_frame)

auth_label = tk.Label(auth_frame, text="Not authorized", bg="#111111", fg="#FFB6C1", font=("Segoe UI", 9, "bold"))
auth_label.pack(padx=8, pady=(8, 4), fill="x")

auth_btn = tk.Button(auth_frame, text="Set Username", command=set_username, bg="#FFD400", fg="black", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=6)
auth_btn.pack(padx=6, pady=(4, 8), fill="x")

# --- Play Frame (bottom center) ---
play_frame = tk.Frame(canvas, bg="#111111", highlightbackground="#FFD400", highlightthickness=2, width=350, height=180)
play_frame.pack_propagate(False)
canvas.create_window(screen_w // 2 - 175, screen_h - 190, anchor="nw", window=play_frame)

tk.Label(play_frame, text="Select Version:", bg="#111111", fg="#FFD400", font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))

version_var = tk.StringVar()
versions = ["1.20.1", "1.20", "1.19.2", "1.18.2", "1.17.1", "1.16.5"]
version_combo = ttk.Combobox(play_frame, textvariable=version_var, values=versions, state="readonly", width=30, font=("Segoe UI", 9))
version_combo.pack(pady=5)
version_combo.set(versions[0])

def on_version_change(event):
    global selected_version
    selected_version = version_var.get()
    update_discord_rpc("Selecting version...", selected_version)

version_combo.bind("<<ComboboxSelected>>", on_version_change)

try:
    play_img = Image.open("join.png").resize((100, 100))
    play_tk_img = ImageTk.PhotoImage(play_img)
    play_btn = tk.Button(play_frame, image=play_tk_img, command=play_minecraft, bg="#0f0f0f", relief="flat", bd=0)
    play_btn.image = play_tk_img
except FileNotFoundError:
    play_btn = tk.Button(play_frame, text="PLAY", command=play_minecraft, bg="#FFD400", fg="black", font=("Segoe UI", 14, "bold"), padx=20, pady=10)

play_btn.pack(pady=10)

button_frame = tk.Frame(play_frame, bg="#111111")
button_frame.pack(pady=5, fill="x", padx=10)

status_label = tk.Label(play_frame, text="Ready to play", bg="#111111", fg="#FFD400", font=("Segoe UI", 8), wraplength=330)
status_label.pack(pady=5)

def open_github():
    webbrowser.open("https://github.com/Rozgaleziacz/bananalauncher")

download_btn = tk.Button(button_frame, text="📥 Download", command=open_github, bg="#00B4D8", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=10)
download_btn.pack(side="left", padx=5)

load_auth()
update_auth_display()
init_discord_rpc()

def on_closing():
    close_discord_rpc()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
