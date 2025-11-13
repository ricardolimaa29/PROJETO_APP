import json
from pathlib import Path
import flet as ft

# Arquivo de configurações ao lado deste módulo
SETTINGS_FILE = Path(__file__).resolve().parent / "app_settings.json"


def _read_settings():
    """Lê o arquivo de configurações JSON."""
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Erro ao ler configurações: {e}")
    return {}


def _write_settings(data: dict):
    """Escreve configurações no arquivo JSON."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
        return False


def read_theme():
    """Retorna o tema salvo: 'dark' ou 'light'. Retorna None se não configurado."""
    s = _read_settings()
    t = s.get("theme")
    if t in ("dark", "light"):
        return t
    return None


def write_theme(mode: str):
    """Persiste o modo de tema. mode deve ser 'dark' ou 'light'."""
    if mode not in ("dark", "light"):
        return False
    s = _read_settings()
    s["theme"] = mode
    return _write_settings(s)


def apply_theme(page: ft.Page):
    """Aplica o tema persistido na página.
    
    Se o tema foi salvo, aplica dark ou light. Se não, não altera nada.
    """
    t = read_theme()
    if t == "dark":
        page.theme_mode = ft.ThemeMode.DARK
        page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    elif t == "light":
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
 



import json
import os
from pathlib import Path
import flet as ft

# Configurações do tema
def read_theme():
    try:
        config_path = Path("app_settings.json")
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("theme", "dark")
        return "dark"
    except Exception:
        return "dark"

def write_theme(theme_mode):
    try:
        config_path = Path("app_settings.json")
        # Lê configuração existente ou cria nova
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {}
        
        config["theme"] = theme_mode
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar tema: {e}")

def apply_theme(page):
    try:
        theme_mode = read_theme()
        if theme_mode == "light":
            page.theme_mode = "light"
        else:
            page.theme_mode = "dark"
        page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        page.update()
    except Exception as e:
        print(f"Erro ao aplicar tema: {e}")

# Configurações do tamanho da fonte
def read_font_size():
    try:
        config_path = Path("app_settings.json")
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("font_scale", 1.0)
        return 1.0
    except Exception:
        return 1.0

def write_font_size(font_scale):
    try:
        config_path = Path("app_settings.json")
        # Lê configuração existente ou cria nova
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {}
        
        config["font_scale"] = font_scale
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar tamanho da fonte: {e}")

# Sistema de observadores para atualização em tempo real
font_size_listeners = []

def add_font_size_listener(callback):
    """Adiciona um callback para ser notificado quando o tamanho da fonte mudar"""
    font_size_listeners.append(callback)

def remove_font_size_listener(callback):
    """Remove um callback da lista de observadores"""
    if callback in font_size_listeners:
        font_size_listeners.remove(callback)

def notify_font_size_changed():
    """Notifica todos os observadores que o tamanho da fonte mudou"""
    for listener in font_size_listeners:
        try:
            listener()
        except Exception as e:
            print(f"Erro ao notificar observador de fonte: {e}")