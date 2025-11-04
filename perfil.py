import flet as ft
import json
import os
import re
from pathlib import Path

def PerfilView(page: ft.Page):
    page.theme_mode = "dark"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"

    # ---------- Ler dados do usuário (preferência: perfil_usuario.json) ----------
    usuario = {}

    def _perfil_json_path():
        try:
            base = Path(__file__).resolve().parent
            # perfil_usuario.json está na raiz do projeto (um nível acima)
            candidate = base.parent / "perfil_usuario.json"
        except Exception:
            candidate = Path(os.getcwd()) / "perfil_usuario.json"
        return candidate

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


    app_bar = ft.AppBar(
        leading=ft.IconButton(
            ft.Icons.ARROW_BACK,
            icon_color="white",
            tooltip="Voltar",
            on_click=voltar,
        ),
        leading_width=40,
        title=ft.Text("FÁBRICA DE PROGRAMADORES", weight="bold"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                    ft.PopupMenuItem(text="ACESSIBILIDADE", icon="ACCESSIBILITY", on_click=clicou_menu),
                    ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
                    ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=lambda e:page.go("/")),
                ]
            ),
        ],
    )
    # -------------------------------------------------------------

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

    foto_stack = ft.Stack(
        controls=[
            ft.Container(
                content=foto,
                width=110, height=110,
                border_radius=55,
                clip_behavior=ft.ClipBehavior.HARD_EDGE
            ),
            ft.Container(content=botao_alterar, alignment=ft.alignment.top_left, padding=5),
        ],
        width=120, height=120,
    )

    foto_moldura = ft.Container(
        content=foto_stack,
        padding=6,
        border=ft.border.all(2, ft.Colors.WHITE24),
        border_radius=70,
        width=132, height=132,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.BLACK,
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

    def habilitar_edicao(e):
        for campo in [nome_field, email_field, telefone_field]:
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

        # salvar em perfil_usuario.json (principal) e em session.json como fallback
        try:
            with open(perfil_path, "w", encoding="utf-8") as f:
                json.dump(usuario, f, indent=4, ensure_ascii=False)
        except Exception:
            with open("session.json", "w", encoding="utf-8") as f:
                json.dump(usuario, f, indent=4, ensure_ascii=False)

        for campo in [nome_field, email_field, telefone_field]:
            campo.content.read_only = True
        editar_button.visible = True
        atualizar_button.visible = False
        show_snackbar("Perfil atualizado com sucesso!", color="GREEN")
        page.update()

    editar_button = ft.ElevatedButton("Editar Perfil", on_click=habilitar_edicao, bgcolor="white", color="black", width=120)
    atualizar_button = ft.ElevatedButton("Atualizar Perfil", on_click=atualizar_perfil, visible=False, bgcolor="white", color="black", width=140)

    # ---------- Return View ----------
    return ft.View(
        route="/perfil",
        controls=[
            app_bar, 
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
                scroll=ft.ScrollMode.AUTO
            )
        ],
        vertical_alignment="start", 
        horizontal_alignment="center",
    )
