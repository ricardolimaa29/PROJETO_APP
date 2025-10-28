import flet as ft
import webbrowser
       
def LoginView(page: ft.Page):
    page.title = "Fabrica de programadores"
    page.theme_mode= "dark"
    page.window.min_height = 900
    page.window.min_width = 500
    page.window.max_height = 900
    page.window.max_width = 500
    page.window.width = 500
    page.window.height = 900
    

    botao_personalizado = ft.ElevatedButton(
            "Entrar",width=150,on_click=lambda _:page.go("/home"),
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.HOVERED: ft.Colors.WHITE,
                    ft.ControlState.FOCUSED: ft.Colors.GREEN,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                },
                bgcolor={ft.ControlState.FOCUSED: ft.Colors.PINK_200, "": ft.Colors.GREEN},
                padding={ft.ControlState.HOVERED: 20},
                overlay_color=ft.Colors.TRANSPARENT,
                elevation={"pressed": 0, "": 1},
                animation_duration=500,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.GREEN),
                    ft.ControlState.HOVERED: ft.BorderSide(2, ft.Colors.GREEN),
                },
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                },
            ),
        )
    
    botao_cadastro = ft.ElevatedButton(
            "Cadastrar",bgcolor=None,on_click=lambda _:page.go("/cadastro")
    )
    
    def login_google():
        # URL do Google OAuth para seleção de conta
        google_oauth_url = (
            "https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?"
            "response_type=code&"
            "client_id=YOUR_CLIENT_ID&"  # Você precisa substituir pelo seu Client ID
            "redirect_uri=YOUR_REDIRECT_URI&"  # Você precisa substituir pelo seu Redirect URI
            "scope=email%20profile&"
            "access_type=offline&"
            "prompt=select_account"
        )
        
        # URL alternativa mais simples (abre a página de login do Google)
        simple_google_url = "https://accounts.google.com/AccountChooser?continue=https://www.google.com&hl=pt-BR"
        
        # Abre a página de seleção de conta do Google
        webbrowser.open(simple_google_url)
        mensagem.value = "Abrindo seleção de conta Google..."
        mensagem.color = ft.Colors.BLUE
        page.update()
    
    # Botão de login com Google usando Container
    botao_google_container = ft.Container(
        content=ft.Row([
            ft.Image(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/768px-Google_%22G%22_logo.svg.png",
                width=20,
                height=20,
            ),
            ft.Text("Entrar com Google", color=ft.Colors.BLACK, size=14),
        ], alignment="center", spacing=10),
        width=300,
        height=40,
        border_radius=4,
        bgcolor=ft.Colors.WHITE,
        alignment=ft.alignment.center,
        on_click=lambda e: login_google(),
    )
        
    titulo = ft.Text("Login", size=30)
    criar = ft.Text("Não tem um conta?",size= 15)
    entrada_email = ft.TextField(label="E-mail", width=300,border_color="WHITE")
    entrada_senha = ft.TextField(label="Senha", password=True, width=300,border_color="WHITE")
    mensagem = ft.Text(size=16)
    
    # Divisor "ou"
    divisor_ou = ft.Row([
        ft.Container(ft.Divider(height=1, color=ft.Colors.GREY_600), expand=True),
        ft.Text(" ou ", color=ft.Colors.GREY_400, size=12),
        ft.Container(ft.Divider(height=1, color=ft.Colors.GREY_600), expand=True),
    ], alignment="center", vertical_alignment="center")
    
    return ft.View(
        route = "/",
        controls=[
            ft.Row([titulo],alignment="center"),
            ft.Row([entrada_email], alignment="center"),
            ft.Row([entrada_senha], alignment="center"),
            ft.Row([botao_personalizado], alignment="center"),
            ft.Row([divisor_ou], alignment="center"),
            ft.Row([botao_google_container], alignment="center"),
            ft.Row([criar, botao_cadastro], alignment="center"),
            ft.Row([mensagem], alignment="center")
        ],
        vertical_alignment="center",
        horizontal_alignment="center"
    )
