import flet as ft


def CadastroView(page:ft.Page):
    titulo = ft.Text("Cadastro",size=30,color="YELLOW")
    nome = ft.TextField(label="Digite seu nome",width=300,color="white",focused_border_color="green")
    senha = ft.TextField(label="Digite sua senha",width=300,color="white",focused_border_color="green")
    conf_senha = ft.TextField(label="Confirme sua senha",width=300,color="white",focused_border_color="green")
    botao = ft.ElevatedButton("Cadastrar", on_click=lambda _:page.go("/home"),width=150,bgcolor="Green",color="WHITE")
    voltar = ft.ElevatedButton("Voltar", on_click=lambda _:page.go("/"),width=150,bgcolor="RED",color="WHITE")
    
    return ft.View(
        route="/cadastro",
        controls=[
            ft.Row([titulo],alignment="center"),
            ft.Row([nome],alignment="center"),
            ft.Row([senha],alignment="center"),
            ft.Row([conf_senha],alignment="center"),
            ft.Row([voltar,botao],alignment="center"),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )