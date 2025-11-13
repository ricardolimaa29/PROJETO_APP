import flet as ft
import json
import os
import re
from pathlib import Path
import time
import threading
from app_settings import write_theme, apply_theme

def PerfilView(page: ft.Page):
    # Aplica o tema persistido
    try:
        apply_theme(page)
    except Exception:
        page.theme_mode = "dark"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"
    page.window.center()
    # ---------- Ler dados do usuário (preferência: perfil_usuario.json) ----------
    usuario = {}

    def _perfil_json_path():
        try:
            project_root = Path(__file__).resolve().parent
        except Exception:
            project_root = Path(os.getcwd())
        return project_root / "perfil_usuario.json"

    perfil_path = _perfil_json_path()
    if perfil_path.exists():
        try:
            with open(perfil_path, "r", encoding="utf-8") as f:
                usuario = json.load(f)
        except Exception:
            usuario = {}
    elif os.path.exists("session.json"):
        with open("session.json", "r", encoding="utf-8") as f:
            usuario = json.load(f)
    elif os.path.exists("usuarios.json"):
        with open("usuarios.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            if "usuarios" in dados and len(dados["usuarios"]) > 0:
                usuario = dados["usuarios"][-1]  # pega o último cadastrado

    nome_inicial = usuario.get("nome", "Nome Fictício")
    email_inicial = usuario.get("email", "email@gmail.com")
    nascimento_inicial = usuario.get("data_nascimento", "01/01/2000")
    telefone_inicial = usuario.get("telefone", "(11) 99999-9999")
    genero = usuario.get("genero", "O")  # "F", "M" ou "O"
    foto_inicial = usuario.get("foto") or usuario.get("imagem_personalizada")

    # ---------- Imagem ----------
    if genero == "F":
        imagem_base = "fem.jpeg"
    elif genero == "M":
        imagem_base = "masc.jpeg"
    else:
        imagem_base = "outro.jpeg"

    if foto_inicial:
        imagem_base = foto_inicial

    # ---------- Funções ----------
    def voltar(e):
        page.go("/home")

    def mudar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        page.update()

    def clicou_menu(e):
        item = e.control.text
        print(f"Item clicado: {item}")

    def show_snackbar(message, color="RED"):
        page.open(ft.SnackBar(
            ft.Text(message, color="White"),
            bgcolor=color,
            duration=3000
        ))

    appbar = ft.AppBar(
    leading=ft.IconButton(
        ft.Icons.ARROW_BACK,
        on_click=lambda _:page.go('/home'),
    ), 
    title=ft.Text("DESEMPENHO", weight="bold"),  # título da AppBar
    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,  # cor de fundo
    actions=[  # ações do lado direito
        
        ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
                ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click="/suporte"),
                ft.PopupMenuItem(text="FEEDBACK", icon="FEEDBACK", on_click=("/feedback")),
                ft.PopupMenuItem(),  # separador
                ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=("/")),
            ]
        ),
    ],
    )

    # ---------- Foto de perfil e Campos ----------
    foto = ft.Image(src=imagem_base, fit=ft.ImageFit.COVER, width=110, height=110)
    
    def foto_escolhida(e: ft.FilePickerResultEvent):
        if e.files:
            caminho = e.files[0].path
            foto.src = caminho
            usuario["imagem_personalizada"] = caminho
            usuario["foto"] = caminho
            # salva também em perfil_usuario.json quando possível
            try:
                with open(perfil_path, "w", encoding="utf-8") as f:
                    json.dump(usuario, f, indent=4, ensure_ascii=False)
            except Exception:
                # fallback para session.json
                with open("session.json", "w", encoding="utf-8") as f:
                    json.dump(usuario, f, indent=4, ensure_ascii=False)
            foto.update()

    file_picker = ft.FilePicker(on_result=foto_escolhida)
    page.overlay.append(file_picker)

    botao_alterar = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.CAMERA_ALT,
            icon_size=20,
            icon_color="white",
            tooltip="Alterar foto",
            on_click=lambda _: file_picker.pick_files(
                allow_multiple=False,
                file_type=ft.FilePickerFileType.IMAGE
            ),
            style=ft.ButtonStyle(bgcolor={"": "#2196F3"}, shape=ft.CircleBorder())
        ),
        width=40, height=40, alignment=ft.alignment.center,
    )

    # container interno que segura a imagem (usado para ajustar raio/tamanho dinamicamente)
    inner_container = ft.Container(
        content=foto,
        width=110, height=110,
        border_radius=55,
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )

    foto_stack = ft.Stack(
        controls=[
            inner_container,
            ft.Container(content=botao_alterar, alignment=ft.alignment.top_left, padding=5),
        ],
        width=120, height=120,
    )

    foto_moldura = ft.Container(
        content=foto_stack,
        padding=4,
        border=ft.border.all(3, ft.Colors.WHITE),  # borda mais visível
        border_radius=66,  # valor inicial; será ajustado dinamicamente
        width=132, height=132,
        alignment=ft.alignment.center,
        bgcolor=None,  # transparente para deixar a borda e o fundo da página aparecerem
    )

    def campo_personalizado(label, valor, read_only=True):
        return ft.Container(
            content=ft.TextField(
                value=valor,
                label=label,
                read_only=read_only,
                border="none",
                bgcolor="transparent",
                text_size=18,
                color="white"
            ),
            bgcolor=ft.Colors.WHITE38,
            border_radius=0,
            padding=10,
            width=400,
        )

    nome_field = campo_personalizado("NOME", nome_inicial)
    email_field = campo_personalizado("EMAIL", email_inicial)
    nascimento_field = campo_personalizado("DATA DE NASCIMENTO", nascimento_inicial)
    telefone_field = campo_personalizado("TELEFONE", telefone_inicial)
    genero_field = campo_personalizado("GÊNERO", genero)

    def habilitar_edicao(e):
        for campo in [nome_field, email_field, telefone_field, nascimento_field, genero_field]:
            campo.content.read_only = False
        editar_button.visible = False
        atualizar_button.visible = True
        page.update()

    def atualizar_perfil(e):
        nome = nome_field.content.value.strip()
        email = email_field.content.value.strip().lower()
        telefone_formatado = telefone_field.content.value.strip()

        # Validações
        if not re.fullmatch(r"^[A-Za-zÀ-ÿ\s]+$", nome) or len(nome) < 10:
            show_snackbar("Nome inválido! Use apenas letras e espaços (min. 10 caracteres).")
            return
        telefone_limpo = re.sub(r'[\(\)\-\s]', '', telefone_formatado)
        if not telefone_limpo.isdigit() or len(telefone_limpo) != 11:
            show_snackbar("Telefone inválido! Deve conter 11 números.")
            return
        if "@" not in email:
            show_snackbar("Email inválido!")
            return

        # Salvar alterações
        usuario["nome"] = nome
        usuario["email"] = email
        usuario["telefone"] = telefone_formatado
        # salvar data de nascimento e genero se disponíveis
        try:
            usuario["data_nascimento"] = nascimento_field.content.value.strip()
        except Exception:
            pass
        try:
            usuario["genero"] = genero_field.content.value.strip()
        except Exception:
            pass

        # salvar em perfil_usuario.json (principal) e em session.json como fallback
        try:
            with open(perfil_path, "w", encoding="utf-8") as f:
                json.dump(usuario, f, indent=4, ensure_ascii=False)
        except Exception:
            with open("session.json", "w", encoding="utf-8") as f:
                json.dump(usuario, f, indent=4, ensure_ascii=False)

        for campo in [nome_field, email_field, telefone_field, nascimento_field, genero_field]:
            campo.content.read_only = True
        editar_button.visible = True
        atualizar_button.visible = False
        show_snackbar("Perfil atualizado com sucesso!", color="GREEN")
        page.update()

    editar_button = ft.ElevatedButton("Editar Perfil", on_click=habilitar_edicao, bgcolor="white", color="black", width=120)
    atualizar_button = ft.ElevatedButton("Atualizar Perfil", on_click=atualizar_perfil, visible=False, bgcolor="white", color="black", width=140)

    # --- Live-reload do perfil: monitora perfil_usuario.json, session.json e usuarios.json
    def _perfil_candidate_paths():
        try:
            project_root = Path(__file__).resolve().parent
        except Exception:
            project_root = Path(os.getcwd())
        candidates = [
            project_root / "perfil_usuario.json",
            Path(os.getcwd()) / "perfil_usuario.json",
            Path(os.getcwd()) / "session.json",
            Path(os.getcwd()) / "usuarios.json",
        ]
        # remove duplicatas mantendo ordem
        seen = set()
        out = []
        for p in candidates:
            s = str(p)
            if s not in seen:
                seen.add(s)
                out.append(p)
        return out

    def apply_profile_to_view(profile: dict):
        nonlocal usuario
        try:
            if not isinstance(profile, dict):
                return
            usuario.update(profile)
            # atualiza somente campos que não estão em edição
            if nome_field.content.read_only:
                nome_field.content.value = profile.get("nome", nome_field.content.value)
            if email_field.content.read_only:
                email_field.content.value = profile.get("email", email_field.content.value)
            if telefone_field.content.read_only:
                telefone_field.content.value = profile.get("telefone", telefone_field.content.value)
            if nascimento_field.content.read_only:
                nascimento_field.content.value = profile.get("data_nascimento", nascimento_field.content.value)
            if genero_field.content.read_only:
                genero_field.content.value = profile.get("genero", genero_field.content.value)

            foto_path = profile.get("foto") or profile.get("imagem_personalizada")
            if foto_path:
                # atualiza a imagem de perfil (tenta URL, caminho local relativo e absoluto)
                if isinstance(foto_path, str) and (foto_path.startswith("http://") or foto_path.startswith("https://")):
                    foto.src = foto_path
                else:
                    candidate = Path(foto_path)
                    if not candidate.exists():
                        candidate2 = Path(__file__).resolve().parent / foto_path
                        if candidate2.exists():
                            foto.src = str(candidate2)
                    else:
                        foto.src = str(candidate)
                try:
                    foto.update()
                except Exception:
                    pass

            page.update()
        except Exception as e:
            print(f"Erro ao aplicar perfil na view (perfil.py): {e}")

    def load_profile_from_file():
        # tenta os candidatos na ordem e retorna o primeiro perfil válido
        for path in _perfil_candidate_paths():
            try:
                if not path.exists():
                    continue
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
                if isinstance(data, dict) and "usuarios" in data and isinstance(data["usuarios"], list) and len(data["usuarios"]):
                    return data["usuarios"][-1]
            except Exception as e:
                print(f"Erro ao ler perfil em {path}: {e}")
        return {}

    watcher_started = False

    def start_profile_watcher(poll_interval: float = 1.0):
        nonlocal watcher_started
        if watcher_started:
            return
        watcher_started = True

        def watcher():
            candidate_paths = _perfil_candidate_paths()
            last_mtimes = {}
            for p in candidate_paths:
                try:
                    last_mtimes[str(p)] = p.stat().st_mtime if p.exists() else 0
                except Exception:
                    last_mtimes[str(p)] = 0
            while True:
                try:
                    time.sleep(poll_interval)
                    for p in candidate_paths:
                        try:
                            mtime = p.stat().st_mtime if p.exists() else 0
                        except Exception:
                            mtime = 0
                        key = str(p)
                        if mtime != last_mtimes.get(key, 0):
                            last_mtimes[key] = mtime
                            try:
                                page.call_later(lambda: apply_profile_to_view(load_profile_from_file()))
                            except Exception:
                                try:
                                    apply_profile_to_view(load_profile_from_file())
                                except Exception as e:
                                    print(f"Erro ao recarregar perfil pelo watcher (perfil.py): {e}")
                except Exception as e:
                    print(f"Erro no profile watcher (perfil.py): {e}")

        threading.Thread(target=watcher, daemon=True).start()

    # NAVIGATION BAR CORRIGIDA
    def mudar_tela(e):
        # Evita navegação múltipla rápida
        if page.route == "/home" and e.control.selected_index == 0:
            return
        if page.route == "/desempenho" and e.control.selected_index == 1:
            return
        if page.route == "/notificação" and e.control.selected_index == 2:
            return
        if page.route == "/perfil" and e.control.selected_index == 3:
            return

        index = e.control.selected_index
        if index == 0:
            page.go("/home")
        elif index == 1:
            page.go("/desempenho")
        elif index == 2:
            page.go("/notificação")
        elif index == 3:
            page.go("/perfil")

    navbar = ft.NavigationBar(
        selected_index=3,  # Corrigido: índice 3 para a página de perfil
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Início"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BAR_CHART_OUTLINED,
                selected_icon=ft.Icons.BAR_CHART,
                label="Desempenho"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                selected_icon=ft.Icons.NOTIFICATIONS,
                label="Notificações"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINED,
                selected_icon=ft.Icons.PERSON,
                label="Perfil"
            ),
        ],
        on_change=mudar_tela
    )

    # ---------- Return View ----------
    view = ft.View(
        route="/perfil",
        controls=[
         
            ft.Column(
                [
                    ft.Container(height=20),
                    foto_moldura,
                    nome_field,
                    email_field,
                    nascimento_field,
                    telefone_field,
                    ft.Row([editar_button, atualizar_button], alignment="center"),
                ],
                horizontal_alignment="center",
                alignment="start",
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                expand=True  # Adicionado para melhor layout
            ),
            ft.Container(  # Container para a navbar ficar fixa na parte inferior
                content=navbar,
                padding=0,
                margin=0
            )
        ],
        vertical_alignment="start",
        horizontal_alignment="center",
    )

    def on_view_loaded(e):
        # Aplica dados atuais do arquivo e inicia watcher para atualizações ao vivo
        try:
            apply_profile_to_view(load_profile_from_file())
        except Exception:
            pass
        try:
            start_profile_watcher()
        except Exception as ex:
            print(f"Não foi possível iniciar profile watcher (perfil.py): {ex}")

        # Se houver um comando de ação vindo do Home (ex.: abrir em modo edição), aplica
        try:
            action_file = Path(__file__).resolve().parent.parent / "perfil_action.json"
            if action_file.exists():
                try:
                    with open(action_file, "r", encoding="utf-8") as af:
                        cmd = json.load(af)
                    if isinstance(cmd, dict) and cmd.get("action") == "edit":
                        try:
                            habilitar_edicao(None)
                        except Exception:
                            pass
                except Exception:
                    pass
                try:
                    action_file.unlink()
                except Exception:
                    pass
        except Exception:
            pass

    view.on_load = on_view_loaded
    return view