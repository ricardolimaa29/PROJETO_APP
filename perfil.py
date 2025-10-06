import flet as ft
import re

def main(page: ft.Page):
    page.title = "Tela de Perfil"
    page.theme_mode = "dark"

    # Forçar janela em proporção 9:16 (tipo celular)
    page.window.width = 500
    page.window.min_width = 500
    page.window.max_width = 5000
    page.window.height = 800
    page.window.min_height = 800
    page.window.max_height = 800
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"

    VALID_DOMAINS = [
        "@outlook.com", "@hotmail.com", "@live.com", "@yahoo.com",
        "@icloud.com", "@aol.com", "@bol.com.br", "@uol.com.br",
        "@terra.com.br", "@globo.com", "@ig.com.br", "@protonmail.com",
        "@tutanota.com", "@zoho.com", "@gmail.com"
    ]

    def show_snackbar(message, color="RED"):
        page.open(ft.SnackBar(
            ft.Text(message, color="White"),
            bgcolor=color,
            duration=3000
        ))

    # Foto de perfil
    foto = ft.Image(src="perfil_default.png", fit=ft.ImageFit.COVER, width=120, height=120)

    foto_container = ft.Container(
        content=foto,
        width=120,
        height=120,
        border_radius=60,
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )

    def foto_escolhida(e: ft.FilePickerResultEvent):
        if e.files:
            caminho = e.files[0].path
            foto.src = caminho
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
            style=ft.ButtonStyle(
                bgcolor={"": "#2196F3"},
                shape=ft.CircleBorder()
            ),
        ),
        width=40,
        height=40,
        alignment=ft.alignment.center,
    )

    foto_stack = ft.Stack(
        controls=[
            foto_container,
            ft.Container(content=botao_alterar, alignment=ft.alignment.top_left, padding=5),
        ],
        width=120,
        height=120,
    )

    # Função para estilizar campos translúcidos
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
            bgcolor=ft.Colors.WHITE38,   # branco translúcido
            border_radius=0,
            padding=10,
            width=400,
        )

    nome_field = campo_personalizado("NOME", "Nome Fictício")
    email_field = campo_personalizado("EMAIL", "email@gmail.com")
    nascimento_field = campo_personalizado("DATA DE NASCIMENTO", "01/01/2000")
    telefone_field = campo_personalizado("TELEFONE", "(11) 99999-9999")

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

        # Validação do nome
        if not re.fullmatch(r"^[A-Za-zÀ-ÿ\s]+$", nome):
            show_snackbar("Nome inválido! Use apenas letras e espaços.")
            return
        if len(nome) < 10:
            show_snackbar("Nome inválido! Deve ter no mínimo 10 caracteres.")
            return

        # Validação telefone
        telefone_limpo = re.sub(r'[\(\)\-\s]', '', telefone_formatado)
        if not telefone_limpo.isdigit() or len(telefone_limpo) != 11:
            show_snackbar("Telefone inválido! Deve conter 11 números.")
            return

        # Validação email
        if not any(email.endswith(domain) for domain in VALID_DOMAINS):
            show_snackbar("Email inválido! Domínio não permitido.")
            return

        # Salvar
        for campo in [nome_field, email_field, telefone_field]:
            campo.content.read_only = True
        editar_button.visible = True
        atualizar_button.visible = False
        show_snackbar("Perfil atualizado com sucesso!", color="GREEN")
        page.update()

    editar_button = ft.ElevatedButton("Editar Perfil", on_click=habilitar_edicao,bgcolor="white",color="black",width=100)
    atualizar_button = ft.ElevatedButton("Atualizar Perfil", on_click=atualizar_perfil, visible=False,bgcolor="white",color="black",width=100)

    voltar_button = ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="YELLOW", tooltip="Voltar")
    header = ft.Row([voltar_button], alignment="start")

    return ft.View(
        route="/perfil",
        controls=[
    page.add(
        ft.Stack(
            expand=True,
            controls=[
                ft.Image(
                    src="Tecnologia 9_16.jpg",
                    expand=True,              # ocupa todo espaço disponível
                    fit=ft.ImageFit.COVER,    # cobre toda a tela
                ),
                ft.Column(
                    controls=[
                        header,
                        ft.Container(height=20),
                        foto_stack,
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
            ]
        )
    )
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )
