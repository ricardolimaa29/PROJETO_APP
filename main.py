import flet as ft
from home import HomeView
from login import LoginView
from cadastro import CadastroView

def main(page: ft.Page):
    page.title = "Area do Aluno"
    page.window.width = 500
    page.window.height = 800
    page.theme_mode = "dark"

    
    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(LoginView(page))
        elif page.route == "/home":
            page.views.append(HomeView(page))
        elif page.route == "/cadastro":
            page.views.append(CadastroView(page))

        page.update()

   
    page.on_route_change = route_change
    page.go("/")  

ft.app(target=main)
