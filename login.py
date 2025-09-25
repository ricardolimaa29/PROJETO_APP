import flet as ft
       
def LoginView(page: ft.Page):
    page.title = "Fabrica de programadores"
    page.theme_mode= "dark"
    ft.Text
    page.window.min_height = 900
    page.window.min_width = 500
    page.window.max_height = 900
    page.window.max_width = 500
    page.window.width = 500
    page.window.height = 900
    
    def verificar_login(e):
            if entrada_email.value == "admin" and entrada_senha.value == "1234":
                    mensagem.value = "Login realizado com sucesso!"
                    mensagem.color = ft.Colors.GREEN
            else:
                    mensagem.value = "Usuário ou senha incorretos."
                    mensagem.color = ft.Colors.RED
            page.update()




    botao_personalizado = ft.ElevatedButton(
            "Entrar",width=150,
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
            "Cadastrar",bgcolor=None
            
            )
        
    titulo = ft.Text("Login", size=30)
    criar = ft.Text("Não tem um conta?",size= 15)
    entrada_email = ft.TextField(label="E-mail", width=300,border_color="WHITE")
    entrada_senha = ft.TextField(label="Senha", password=True, width=300,border_color="WHITE")
    mensagem = ft.Text(size=16)
    
    return ft.View(controls=[
        ft.Row([titulo],alignment="center"),
        ft.Row([entrada_email], alignment="center"),
        ft.Row([entrada_senha], alignment="center"),
        ft.Row([botao_personalizado,], alignment="center"),
        ft.Row([criar,botao_cadastro], alignment="center"),
        ft.Row([mensagem], alignment="center")
    ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        expand=True,
)
