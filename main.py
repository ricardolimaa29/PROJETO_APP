import flet as ft
from home import HomeView
from login import LoginView
from cadastro import CadastroView
from notificação import View_notificacao

# CRIAR UM BOTAO PARA INSERIR UM SITE DE PORTFOLIO PARA CADA DEV COM AS INFORMAÇÕES E O LINK PARA GIT

def main(page: ft.Page):
    page.title = "Area do Aluno"
    page.window.width = 500
    page.window.height = 800
    
    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(LoginView(page))
        elif page.route == "/home":
            page.views.append(HomeView().get_view(page))
        elif page.route == "/cadastro":
            page.views.append(CadastroView(page))
        elif page.route == "/notificacao":
            page.views.append(View_notificacao(page))    
        

        page.update()

   
    page.on_route_change = route_change
    page.go("/")  

ft.app(target=main)
