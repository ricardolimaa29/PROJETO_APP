import flet as ft

def suporte_view(page: ft.Page):
    page.title = "Suporte"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.min_height = 900
    page.window.min_width = 500
    page.window.max_height = 900
    page.window.max_width = 500
    page.window.width = 500
    page.window.height = 900
    page.padding = 0
    page.window.center()

    # ---------- Inputs ----------
    envidas = ft.TextField(label="Nome de usuário", width=360)
    mensagem = ft.TextField(
        label="Mensagem",
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=360,
    )

    # ---------- Função Enviar ----------
    def enviar_click(e):
      if envidas.value.strip() and mensagem.value.strip():
        page.open( ft.SnackBar(
            content=ft.Text("Enviado com sucesso!", color="white"),
            bgcolor="green"
        ))
        # Limpar os campos após envio
        envidas.value = ""
        mensagem.value = ""
      else:
        page.open( ft.SnackBar(
            content=ft.Text("Preencha todos os campos!", color="white"),
            bgcolor="red"
        ))
        page.open = True
        page.update()

    # ---------- Layout ----------
    conteudo = ft.Column(
        [
            ft.Text("SUPORTE", size=30, weight="bold"),
            envidas,
            mensagem,
            ft.ElevatedButton("Enviar", on_click=enviar_click, width=300),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


 
    
    
    return ft.View(
    route="/suporte",
    controls=[       ft.Container(
            content=conteudo,
            alignment=ft.alignment.center,
            expand=True,
        )],
    vertical_alignment="center",
    horizontal_alignment="center",
        )
