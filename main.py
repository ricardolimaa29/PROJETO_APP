import flet as ft
from Carregamento import CarregamentoView
from home import HomeView
from login import LoginView
from cadastro import CadastroView
from perfil import PerfilView
from testeaulassss import aulasView
from notificação import View_notificacao
from suporte import suporte_view

# CRIAR UM BOTAO PARA INSERIR UM SITE DE PORTFOLIO PARA CADA DEV COM AS INFORMAÇÕES E O LINK PARA GIT

def main(page: ft.Page):
    page.title = "Area do Aluno"
    page.window.width = 500
    page.window.height = 800
    
    def route_change(e):
        page.views.clear()
        if page.route == "/login":
            page.views.append(LoginView(page))
        elif page.route == "/home":
            page.views.append(HomeView(page))
        elif page.route == "/cadastro":
            page.views.append(CadastroView(page))    
        elif page.route == "/perfil":
            page.views.append(PerfilView(page)) 
        elif page.route == "/":
            page.views.append(CarregamentoView(page)) 
        elif page.route == "/aulasView":
            page.views.append(aulasView(page)) 
        elif page.route == "/notificação":
            page.views.append(View_notificacao(page)) 
        elif page.route == "/suporte":
            page.views.append(suporte_view(page))
        page.update()

   
    page.on_route_change = route_change
    page.go("/")  

ft.app(target=main)

