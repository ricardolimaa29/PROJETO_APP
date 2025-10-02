import flet as ft
import re

def perfil(page: ft.Page):
    page.title = "Perfil"
    page.theme_mode = "dark"
    # Configurações de tamanho de janela (mantidas)
    page.window.width = 500
    page.window.min_width = 500
    page.window.max_width = 500
    page.window.height = 900
    page.window.min_height = 900
    page.window.max_height = 900
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"

    # Domínios de email válidos conforme solicitado
    VALID_DOMAINS = [
        "@outlook.com", "@hotmail.com", "@live.com", "@yahoo.com",
        "@icloud.com", "@aol.com", "@bol.com.br", "@uol.com.br",
        "@terra.com.br", "@globo.com", "@ig.com.br", "@protonmail.com",
        "@tutanota.com", "@zoho.com", "@gmail.com"
    ]

    # Função auxiliar para mostrar as mensagens de snackbar
    def show_snackbar(message, color="RED"):
        page.open(ft.SnackBar(
            ft.Text(message, color="White"),
            bgcolor=color,
            duration=3000
        ))

    # ----------------------------
    # Imagem de perfil
    # ----------------------------
    # Nota: 'perfil_default.png' precisa estar disponível no mesmo diretório
    foto = ft.Image(
        src="perfil_default.png",
        fit=ft.ImageFit.COVER,
        width=120,
        height=120
    )

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
            icon="CAMERA_ALT",
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
            ft.Container(
                content=botao_alterar,
                alignment=ft.alignment.top_left,
                padding=5,
            ),
        ],
        width=120,
        height=120,
    )

    # ----------------------------
    # Campos de texto
    # ----------------------------
    nome_field = ft.TextField("Nome ficticio", label="NOME", read_only=True, border_color="grey", focused_border_color="white")
    email_field = ft.TextField("email@gmail.com", label="EMAIL", read_only=True, border_color="grey", focused_border_color="white")
    nascimento_field = ft.TextField("01/01/2000", label="DATA DE NASCIMENTO", read_only=True, border_color="grey", focused_border_color="white")
    telefone_field = ft.TextField("(11) 99999-9999", label="TELEFONE (Apenas 11 números)", read_only=True, border_color="grey", focused_border_color="white")

    # ----------------------------
    # Funções dos botões
    # ----------------------------
    def habilitar_edicao(e):
        nome_field.read_only = False
        email_field.read_only = False
        telefone_field.read_only = False
        editar_button.visible = False
        atualizar_button.visible = True
        page.update()

    def atualizar_perfil(e):
        nome = nome_field.value.strip()
        email = email_field.value.strip().lower()
        telefone_formatado = telefone_field.value.strip()
        
        # 1. Validação do NOME (apenas letras, espaços e min. 10 caracteres)
        
        # 1.1. Verifica se contém apenas letras e espaços
        if not re.fullmatch(r"^[A-Za-zÀ-ÿ\s]+$", nome):
            show_snackbar("Nome inválido! Use apenas letras e espaços (sem números ou caracteres especiais).", color="RED")
            page.update()
            return

        # 1.2. Verifica o tamanho mínimo
        if len(nome) < 10:
            show_snackbar(f"Nome inválido! Deve ter no mínimo 10 caracteres.", color="RED")
            page.update()
            return
            
        # 2. Validação do TELEFONE
        # Remove caracteres de formatação ((, ), -, espaço)
        telefone_limpo = re.sub(r'[\(\)\-\s]', '', telefone_formatado) 
        
        if not telefone_limpo.isdigit():
            show_snackbar("Telefone inválido! Apenas números são permitidos.", color="RED")
            page.update()
            return
            
        if len(telefone_limpo) != 11:
            show_snackbar(f"Telefone inválido! Deve conter exatamente 11 números (DDI + 9 dígitos), mas tem {len(telefone_limpo)}.", color="RED")
            page.update()
            return

        # 3. Validação do EMAIL (domínios válidos)
        is_email_valid = False
        
        # Verifica se o email termina com um dos domínios válidos
        for domain in VALID_DOMAINS:
            if email.endswith(domain):
                is_email_valid = True
                break
        
        if not is_email_valid:
            # Checa se o email tem um formato básico (algo@algo.algo)
            if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                 show_snackbar("Email inválido! O formato não é reconhecido.", color="RED")
            else:
                show_snackbar("Email inválido! O domínio (@...) não está na lista de domínios permitidos.", color="RED")
            page.update()
            return
                
        
        # Se todas as validações passarem:
        
        # Atualiza os campos como somente leitura
        nome_field.read_only = True
        email_field.read_only = True
        telefone_field.read_only = True
        
        # Atualiza a visibilidade dos botões
        editar_button.visible = True
        atualizar_button.visible = False
        
        # Mensagem de sucesso
        show_snackbar("Perfil atualizado com sucesso!", color="GREEN")
        
        page.update()
        
    # ----------------------------
    # Botões de Ação
    # ----------------------------
    editar_button = ft.ElevatedButton("Editar Perfil", on_click=habilitar_edicao)
    # Note que o 'on_click' do botão 'Atualizar' agora chama a função com as validações
    atualizar_button = ft.ElevatedButton("Atualizar Perfil", on_click=atualizar_perfil, visible=False)

    # ----------------------------
    # Botão de voltar (seta)
    # ----------------------------
    voltar_button = ft.IconButton(
        icon="ARROW_BACK",
        icon_color="YELLOW",
        tooltip="Voltar",
        on_click=lambda e: page.go("/home"),
    )

    header = ft.Row(
        controls=[voltar_button],
        alignment="start"
    )

    # ----------------------------
    # Layout final
    # ----------------------------
    page.add(
        ft.Column(
            controls=[
                header,
                ft.Container(height=20), # Espaçamento
                foto_stack,
                nome_field,
                email_field,
                nascimento_field,
                telefone_field,
                ft.Row([editar_button, atualizar_button], alignment="center"),
            ],
            horizontal_alignment="center",
            alignment="start",
            spacing=20
        )
    )

ft.app(target=perfil)