import flet as ft


def LoginView(page:ft.Page):
    page.title = " Teste"
    page.window.width = 500
    page.window.height = 900
    page.vertical_alignment ="center"
    page.horizontal_alignment = "center"
    page.theme_mode = "dark"
    page.fonts={"Poppins":"fonts\Poppins-Bold.ttf",
               "Poppins2":"fonts\Poppins-Light.ttf",
               "Poppins3":"fonts\Poppins-Regular.ttf"}

    titulo = ft.Text("Login",size=30,font_family="Poppins")
    nome = ft.TextField(label="Usuario",width=300,
                        
                        focused_border_color=ft.Colors.YELLOW_200)
    senha = ft.TextField(label="Senha",width=300,
                         
                         focused_border_color=ft.Colors.YELLOW_200,
                         can_reveal_password=True,
                         password=True)
    botao = ft.ElevatedButton("Entrar",icon=ft.Icons.OPEN_IN_BROWSER,bgcolor=ft.Colors.GREEN,color="WHITE",style=ft.ButtonStyle(ft.Text(font_family="Poppins")),width=150,on_click=lambda _: page.go("/home"))
    botao_cad = ft.ElevatedButton("Cadastrar",icon=ft.Icons.EXIT_TO_APP,bgcolor=ft.Colors.BLUE,color="WHITE",style=ft.ButtonStyle(ft.Text(font_family="Poppins3")),width=150,on_click=lambda _: page.go("/cadastro"))
    return ft.View(
            route="/",
            controls=[
                ft.Row([titulo],alignment="center"),
                ft.Row([nome],alignment="center"),
                ft.Row([senha],alignment="center"),
                ft.Row([botao,botao_cad],alignment="center")
            ],
            vertical_alignment="center",
            horizontal_alignment="center"
        )