import flet as ft
import time
import threading

def main(page: ft.Page):
    # Configurações para mobile
    page.title = "Meu App"
    page.window.width = 400
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = ft.Colors.BLACK

    # ========== CONFIGURAÇÃO DA IMAGEM ==========
    # Altere o caminho da imagem aqui:
    IMAGEM_LOGO = "LOGO.jpg.png"  # Coloque o caminho da sua imagem
    # ============================================

    # Tela de carregamento
    def CarregamentoView():
        return ft.Container(
            width=400,
            height=700,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_700, ft.Colors.BLACK]
            ),
            content=ft.Column(
                [
                    # Container da imagem - CENTRALIZADA
                    ft.Container(
                        content=ft.Image(
                            src=IMAGEM_LOGO,  # Sua imagem aqui
                            width=200,        # Largura da imagem
                            height=200,       # Altura da imagem
                            fit=ft.ImageFit.CONTAIN,
                            error_content=ft.Icon(ft.Icons.IMAGE, size=100, color=ft.Colors.WHITE),
                        ),
                        margin=ft.margin.only(bottom=30),
                        alignment=ft.alignment.center,
                    ),
                    
                    # Texto do app
                    ft.Text(
                        "Meu Aplicativo",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Versão
                    ft.Text(
                        "Versão 1.0",
                        size=14,
                        color=ft.Colors.GREY_400,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.Container(height=40),
                    
                    # Indicador de progresso
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.ProgressRing(
                                    width=60,
                                    height=60,
                                    stroke_width=5,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "Inicializando...",
                                    size=16,
                                    color=ft.Colors.WHITE70,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                    
                    ft.Container(height=50),
                    
                    # Loading animado
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(
                                    width=15,
                                    height=15,
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=10,
                                    animate=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
                                ) for _ in range(3)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        )

    # Função para remover o loading após um tempo
    def remover_loading():
        time.sleep(3)  # Tempo de exibição do loading (3 segundos)
        
        # Remove a tela de loading
        page.clean()
        
        # Adiciona a tela principal do app
        tela_principal = ft.Container(
            width=400,
            height=700,
            bgcolor=ft.Colors.BLUE_800,
            content=ft.Column(
                [
                    ft.Container(height=100),
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=80, color=ft.Colors.GREEN),
                    ft.Container(height=20),
                    ft.Text(
                        "App Carregado!",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Bem-vindo a Fábrica de Programadores",
                        size=16,
                        color=ft.Colors.WHITE70,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=40),
                    ft.ElevatedButton(
                        "Começar",
                        on_click=lambda e: print("App iniciado!"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN,
                            color=ft.Colors.WHITE,
                            padding=20,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        )
        
    # Adiciona a tela de loading
  
    page.update()

    # Inicia a thread para remover o loading após o tempo definido
    threading.Thread(target=remover_loading, daemon=True).start()
 
    return ft.View(
        route = "/carregamento",
        controls=[
        CarregamentoView
    ],
        vertical_alignment="center",
        horizontal_alignment="center"
)
