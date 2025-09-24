import flet as ft

def HomeView(page:ft.Page):
    text = ft.Text("Home", size=30,color="yellow")
    botao = ft.ElevatedButton("Voltar", on_click= lambda _:page.go("/"),bgcolor="WHITE",color="BLACK")
    
    
    
    return ft.View(
        route="/home",
        controls=[
            ft.Row([text],alignment="center"),
            ft.Row([botao],alignment="center")
        ],
        vertical_alignment="center",
        horizontal_alignment="center"
    )