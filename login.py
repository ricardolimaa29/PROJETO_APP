import flet as ft
import json
import os

def LoginView(page: ft.Page):
    page.title = "Fábrica de Programadores"
    page.theme_mode= "dark"
    page.window.min_height = 900
    page.window.min_width = 500
    page.window.max_height = 900
    page.window.max_width = 500
    page.window.width = 500
    page.window.height = 900

    mensagem = ft.Text(size=16)

    entrada_email = ft.TextField(label="E-mail", width=300, border_color="WHITE")
    entrada_senha = ft.TextField(label="Senha", password=True, width=300, border_color="WHITE")

    def entrar(e):
        email_digitado = entrada_email.value.strip().lower()
        senha_digitada = entrada_senha.value.strip()

        if not os.path.exists("usuarios.json"):
            mensagem.value = "Nenhum usuário cadastrado."
            page.update()
            return

        with open("usuarios.json", "r") as f:
            dados = json.load(f)

        for u in dados["usuarios"]:
            if u["email"].lower() == email_digitado:
                # Para teste, não usamos senha ainda
                # Se quiser, pode comparar senha_digitada == u["senha"]
                with open("session.json", "w") as sf:
                    json.dump(u, sf, indent=4)
                page.go("/home")
                return

        mensagem.value = "E-mail ou senha inválidos."
        page.update()

    botao_entrar = ft.ElevatedButton(
        "Entrar", width=150, on_click=entrar
    )

    botao_cadastro = ft.ElevatedButton(
        "Cadastrar", bgcolor=None, on_click=lambda _: page.go("/cadastro")
    )

    titulo = ft.Text("Login", size=30)
    criar = ft.Text("Não tem uma conta?", size=15)

    return ft.View(
        route="/login",
        controls=[
            ft.Row([titulo], alignment="center"),
            ft.Row([entrada_email], alignment="center"),
            ft.Row([entrada_senha], alignment="center"),
            ft.Row([botao_entrar], alignment="center"),
            ft.Row([criar, botao_cadastro], alignment="center"),
            ft.Row([mensagem], alignment="center")
        ],
        vertical_alignment="center",
        horizontal_alignment="center"
    )
