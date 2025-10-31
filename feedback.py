import flet as ft

avaliacao_enviada = 0

# ---------- Função para criar estrelas ----------
def criar_estrelas(on_change):
    stars = []                  # Lista que vai armazenar os botões de estrela
    rating = {"nota": 0}        # Dicionário para guardar a nota selecionada

    def on_click_star(e):
        rating["nota"] = e.control.data  # Atualiza a nota com a estrela clicada
        for s in stars:
            # ✅ Se a estrela estiver dentro da nota selecionada, fica âmbar
            # ❌ Se não, fica cinza
            s.icon = "star" if s.data <= rating["nota"] else "star_outline"
            s.icon_color = ft.Colors.AMBER_400 if s.data <= rating["nota"] else ft.Colors.GREY_400
        on_change(rating["nota"])  # Atualiza a interface que mostra o número de estrelas
        e.page.update()             # Atualiza a tela

    for i in range(1, 6):
        star = ft.IconButton(
            icon="star_outline",        # Começa vazia (cinza)
            icon_color=ft.Colors.GREY_400, # Cor inicial cinza
            icon_size=55,
            data=i,                     # Guarda o número da estrela
            tooltip=f"{i} estrela{'s' if i > 1 else ''}",
            on_click=on_click_star,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )
        stars.append(star)

    return stars, rating



# ---------- Tela de Feedback ----------
def feedback_view(page: ft.Page):
    global avaliacao_enviada

    page.title = "Feedback"
    page.window.width = 500
    page.window.height = 800
    page.window.min_width = 500
    page.window.min_height = 800
    page.window.max_width = 500
    page.window.max_height = 800
    page.padding = 0
    
    
    # ---------- Funções ----------
    def voltar_home(e):
        page.go("/home")

    def on_rating_change(nota):
        nota_text.value = f"{nota} estrela{'s' if nota > 1 else ''}"
        page.update()

    def enviar_click(e=None):
        global avaliacao_enviada

        if rating["nota"] == 0:
            page.open(
                ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ERROR_OUTLINE, color="white"),
                        ft.Text("Selecione uma avaliação antes de enviar!", color="white")
                    ]),
                    bgcolor=ft.Colors.RED_600,
                    duration=3000
                )
            )
        else:
            avaliacao_enviada = rating["nota"]
            page.open(
                ft.SnackBar(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="white"),
                        ft.Text("Sua mensagem foi enviada com sucesso!", color="white")
                    ]),
                    bgcolor=ft.Colors.GREEN_600,
                    duration=3000
                )
            )
            comentario.value = ""
            rating["nota"] = 0
            for s in stars:
                s.icon = ft.Icons.STAR_OUTLINE
            nota_text.value = ""
        page.update()

    def mudar_tema(e=None):
        page.theme_mode = (
            ft.ThemeMode.LIGHT
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        aplicar_tema()

    def aplicar_tema():
        if page.theme_mode == ft.ThemeMode.DARK:
            page.bgcolor = ft.Colors.BLUE_500
            texto_avaliacao.color = ft.Colors.WHITE
            texto_avaliacaoo.color = ft.Colors.WHITE70
            nota_text.color = ft.Colors.AMBER_400
        else:
            page.bgcolor = ft.Colors.BLUE_100
            texto_avaliacao.color = ft.Colors.BLACK
            texto_avaliacaoo.color = ft.Colors.BLACK54
            nota_text.color = ft.Colors.AMBER_800
        page.update()

    # ---------- Elementos ----------
    logo = ft.Image(
        src="LOGO.jpg.png",
        width=210,
        height=160,
        fit=ft.ImageFit.CONTAIN
    )

    texto_avaliacaoo = ft.Text(
        "O feedback do aluno serve para avaliar como foi seu dia em aula, identificar se está tudo bem e receber sugestões que possam contribuir para as atividades em sala. Dessa forma, busca-se promover uma maior aproximação entre aluno e professor, fortalecendo a harmonia no ensino.",
        size=13,
        weight="bold",
        text_align=ft.TextAlign.JUSTIFY,
        width=400,
    )

    texto_avaliacao = ft.Text(
        "Como você avalia o App ",
        size=19,
        weight="bold",
        text_align=ft.TextAlign.CENTER,
    )

    nota_text = ft.Text(
        "",
        size=14,
        weight="bold",
        color=ft.Colors.AMBER_400,
        opacity=0.20,
    )

    stars, rating = criar_estrelas(on_rating_change)

    estrela_row = ft.Row(
        controls=stars,
        alignment=ft.MainAxisAlignment.CENTER
    )

    comentario = ft.TextField(
        label="Conte-nos sua experiência (opcional)",
        multiline=True,
        min_lines=3,
        max_lines=6,
        width=360
    )

    conteudo = ft.Column(
        [
            logo,
            texto_avaliacaoo,
            texto_avaliacao,
            estrela_row,
            nota_text,
            comentario,
            ft.ElevatedButton(
                "Enviar",
                icon=ft.Icons.SEND,
                on_click=enviar_click,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                width=180,
                height=50
            ),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    card_color = ft.Colors.BLUE_700 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_300

    return ft.View(
        route="/feedback",
        controls=[
            ft.AppBar(
                title=ft.Text("Feedback", size=20, weight=ft.FontWeight.BOLD, color="white"),
                bgcolor=card_color,
                center_title=True,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    icon_color="white",
                    tooltip="Voltar",
                    on_click=voltar_home,
                ),
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="TEMA", icon=ft.Icons.WB_SUNNY_OUTLINED, on_click=mudar_tema),
                            ft.PopupMenuItem(text="FEEDBACK", icon=ft.Icons.FEEDBACK, on_click=lambda e: print("Feedback")),
                            ft.PopupMenuItem(text="ACESSIBILIDADE", icon=ft.Icons.ACCESSIBILITY, on_click=lambda e: print("Acessibilidade")),
                            ft.PopupMenuItem(text="CONFIGURAÇÕES", icon=ft.Icons.SETTINGS_OUTLINED, on_click=lambda e: print("Configurações")),
                            ft.PopupMenuItem(text="SUPORTE", icon=ft.Icons.HELP_OUTLINE_ROUNDED, on_click=lambda e: print("Suporte")),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(text="SAIR", icon=ft.Icons.CLOSE_ROUNDED, on_click=lambda e: print("Sair")),
                        ]
                    ),
                ],
            ),
            ft.Container(
                content=conteudo,
                expand=True,
                alignment=ft.alignment.center,
                padding=20,
            ),
        ],
    )


# ---------- Função principal ----------
def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.views.append(feedback_view(page))
    page.update()


    return ft.View(
    route="/feedback",
    controls=[       ft.Container(
            content=feedback_view,
            alignment=ft.alignment.center,
            expand=True,
        )],
    vertical_alignment="center",
    horizontal_alignment="center",
        )
