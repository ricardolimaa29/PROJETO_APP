import flet as ft

def main(page: ft.Page):
    # ---------- CONFIGURAÇÕES DE TELA ----------
    page.window.width = 500
    page.window.height = 800
    page.window.min_width = 400
    page.window.min_height = 600
    page.window.max_width = 600
    page.window.max_height = 900
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Configurações do App"

    # Estado das configurações
    config = {
        "notifications": True,
        "sounds": False,
        "privacy_mode": False,
        "analytics": True
    }

    # Referências para os controles
    switches = {}

    def alternar_tema(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK 
            else ft.ThemeMode.DARK
        )
        # Recarregar a página para aplicar o novo tema
        page.views.clear()
        page.views.append(configuracoes_view())
        page.update()

    def toggle_notificacoes(e):
        config["notifications"] = e.control.value
        mostrar_snackbar(f"Notificações {'ativadas' if e.control.value else 'desativadas'}", "info")

    def toggle_sons(e):
        config["sounds"] = e.control.value
        mostrar_snackbar(f"Sons {'ativados' if e.control.value else 'desativados'}", "info")

    def toggle_privacidade(e):
        config["privacy_mode"] = e.control.value
        mostrar_snackbar(f"Modo privacidade {'ativado' if e.control.value else 'desativado'}", "info")

    def toggle_analytics(e):
        config["analytics"] = e.control.value
        mostrar_snackbar(f"Análise de uso {'ativada' if e.control.value else 'desativada'}", "info")

    def resetar_configuracoes(e):
        # Resetar configurações
        config.update({
            "notifications": True,
            "sounds": False,
            "privacy_mode": False,
            "analytics": True
        })
        
        # Atualizar os controles usando as referências armazenadas
        if 'notificacoes' in switches:
            switches['notificacoes'].value = config["notifications"]
        if 'sons' in switches:
            switches['sons'].value = config["sounds"]
        if 'privacidade' in switches:
            switches['privacidade'].value = config["privacy_mode"]
        if 'analytics' in switches:
            switches['analytics'].value = config["analytics"]
        
        mostrar_snackbar("Configurações restauradas com sucesso!", "success")
        page.update()

    def limpar_cache(e):
        mostrar_snackbar("Cache limpo com sucesso! 45MB liberados.", "success")

    def exportar_dados(e):
        mostrar_snackbar("Dados exportados com sucesso!", "success")

    def mostrar_info_app(e):
        mostrar_snackbar("App v2.1.0 • Desenvolvido com Flet", "info")

    def mostrar_snackbar(mensagem, tipo):
        cores = {
            "success": ft.Colors.GREEN_600,
            "info": ft.Colors.BLUE_600,
            "warning": ft.Colors.ORANGE_600,
            "error": ft.Colors.RED_600
        }
        
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(mensagem, color="white"),
                bgcolor=cores.get(tipo, ft.Colors.BLUE_600),
                duration=2000
            )
        )

    def configuracoes_view():
        # Cores baseadas no tema
        if page.theme_mode == ft.ThemeMode.DARK:
            bg_color = ft.Colors.BLUE_GREY_900
            surface_color = ft.Colors.BLUE_GREY_800
            card_color = ft.Colors.BLUE_700
            text_color = ft.Colors.WHITE
            divider_color = ft.Colors.BLUE_GREY_600
        else:
            bg_color = ft.Colors.BLUE_50
            surface_color = ft.Colors.WHITE
            card_color = ft.Colors.BLUE_300
            text_color = ft.Colors.BLACK
            divider_color = ft.Colors.BLUE_GREY_200

        app_bar = ft.AppBar(
            title=ft.Text("Configurações", size=24, weight="bold", color="white"),
            bgcolor=card_color,
            center_title=True,
            actions=[
                ft.IconButton(
                    ft.Icons.INFO_OUTLINE,
                    icon_color="white",
                    tooltip="Sobre o app",
                    on_click=mostrar_info_app
                )
            ]
        )

        # Switches de configuração
        switch_notificacoes = ft.Switch(
            value=config["notifications"],
            active_color=ft.Colors.BLUE_600,
            on_change=toggle_notificacoes
        )

        switch_sons = ft.Switch(
            value=config["sounds"],
            active_color=ft.Colors.BLUE_600,
            on_change=toggle_sons
        )

        switch_privacidade = ft.Switch(
            value=config["privacy_mode"],
            active_color=ft.Colors.BLUE_600,
            on_change=toggle_privacidade
        )

        switch_analytics = ft.Switch(
            value=config["analytics"],
            active_color=ft.Colors.BLUE_600,
            on_change=toggle_analytics
        )

        # Armazenar referências dos switches
        switches['notificacoes'] = switch_notificacoes
        switches['sons'] = switch_sons
        switches['privacidade'] = switch_privacidade
        switches['analytics'] = switch_analytics

        # Seção de Preferências
        secao_preferencias = ft.Card(
            elevation=3,
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PALETTE, color=ft.Colors.BLUE_600),
                        title=ft.Text("Tema do App", weight="bold", color=text_color),
                        subtitle=ft.Text("Aparência visual da aplicação", color=text_color),
                        trailing=ft.IconButton(
                            ft.Icons.BRIGHTNESS_4,
                            icon_color=ft.Colors.BLUE_600,
                            on_click=alternar_tema,
                            tooltip="Alternar tema claro/escuro"
                        )
                    ),
                    ft.Divider(color=divider_color),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color=ft.Colors.BLUE_600),
                        title=ft.Text("Notificações", weight="bold", color=text_color),
                        subtitle=ft.Text("Receber notificações push", color=text_color),
                        trailing=switch_notificacoes
                    ),
                    ft.Divider(color=divider_color),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.VOLUME_UP, color=ft.Colors.BLUE_600),
                        title=ft.Text("Sons do App", weight="bold", color=text_color),
                        subtitle=ft.Text("Efeitos sonoros e feedback", color=text_color),
                        trailing=switch_sons
                    ),
                ]),
                padding=10
            )
        )

        # Seção de Privacidade
        secao_privacidade = ft.Card(
            elevation=3,
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PRIVACY_TIP, color=ft.Colors.BLUE_600),
                        title=ft.Text("Modo Privacidade", weight="bold", color=text_color),
                        subtitle=ft.Text("Limitar coleta de dados", color=text_color),
                        trailing=switch_privacidade
                    ),
                    ft.Divider(color=divider_color),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.BLUE_600),
                        title=ft.Text("Análise de Uso", weight="bold", color=text_color),
                        subtitle=ft.Text("Compartilhar dados para melhorias", color=text_color),
                        trailing=switch_analytics
                    ),
                ]),
                padding=10
            )
        )

        # Seção de Dados
        secao_dados = ft.Card(
            elevation=3,
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.STORAGE, color=ft.Colors.BLUE_600),
                        title=ft.Text("Limpar Cache", weight="bold", color=text_color),
                        subtitle=ft.Text("Liberar 45MB de espaço", color=text_color),
                        trailing=ft.ElevatedButton(
                            "Limpar",
                            icon=ft.Icons.CLEANING_SERVICES,
                            on_click=limpar_cache,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE
                            )
                        )
                    ),
                    ft.Divider(color=divider_color),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.FILE_DOWNLOAD, color=ft.Colors.BLUE_600),
                        title=ft.Text("Exportar Dados", weight="bold", color=text_color),
                        subtitle=ft.Text("Backup das suas configurações", color=text_color),
                        trailing=ft.ElevatedButton(
                            "Exportar",
                            icon=ft.Icons.SAVE_ALT,
                            on_click=exportar_dados,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE
                            )
                        )
                    ),
                ]),
                padding=10
            )
        )

        # Botões de ação
        botoes_acao = ft.Row(
            [
                ft.ElevatedButton(
                    "Restaurar Padrões",
                    icon=ft.Icons.RESTORE,
                    on_click=resetar_configuracoes,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.ORANGE_600,
                        color=ft.Colors.WHITE,
                        padding=20
                    ),
                    expand=True
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Layout principal
        conteudo_principal = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Configurações do App", 
                           size=28, 
                           weight="bold", 
                           color=text_color,
                           text_align=ft.TextAlign.CENTER),
                    ft.Divider(color=divider_color),
                    ft.Text("Preferências", size=18, weight="bold", color=text_color),
                    secao_preferencias,
                    ft.Text("Privacidade", size=18, weight="bold", color=text_color),
                    secao_privacidade,
                    ft.Text("Dados e Armazenamento", size=18, weight="bold", color=text_color),
                    secao_dados,
                    botoes_acao,
                ],
                spacing=20,
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            padding=20,
            expand=True
        )
        

        return ft.View(
            route="/config",
            controls=[
                app_bar,
                conteudo_principal,
            ],
            bgcolor=bg_color
        )

    # Inicializar a view
    page.views.append(configuracoes_view())
    page.update()

