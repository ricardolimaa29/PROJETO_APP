import flet as ft
from flet import *

def TermosView(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(font_family="Poppins", color_scheme_seed=ft.Colors.INDIGO)
    page.title = "Termos e Condições"
    page.window.width = 500
    page.window.height = 800
    page.window.max_width = 500
    page.window.max_height = 800
    page.window.min_width = 500
    page.window.min_height = 800
    page.scroll = 'auto'
    page.padding = 1

    def mudar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    def voltar(e):
        page.go("/home")
        
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.ARROW_BACK, tooltip="Voltar", on_click=voltar),
        leading_width=40,
        title=ft.Text("Termos e Condições"),
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                    ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED"),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED"),
                ]
            )
        ]
    )
    
    # Função para criar seções com formatação adequada
    def criar_secao(titulo, conteudo):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD),
                    padding=ft.padding.only(bottom=8)
                ),
                conteudo
            ]),
            padding=ft.padding.only(bottom=20)
        )
    
    def criar_item_lista(texto):
        return ft.Row([
            ft.Container(
                width=8,
                height=8,
                border_radius=4,
                margin=ft.margin.only(right=8, top=6)
            ),
            ft.Text(texto, size=14, text_align=ft.TextAlign.JUSTIFY, expand=True)
        ])

    def criar_item_numerado(numero, texto):
        return ft.Row([
            ft.Text(f"{numero}.", size=14, weight=ft.FontWeight.BOLD, width=25),
            ft.Text(texto, size=14, text_align=ft.TextAlign.JUSTIFY, expand=True)
        ])

    # Conteúdo dos Termos e Condições
    termos_content = ft.Column([
        # Cabeçalho
        ft.Container(
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SECURITY),
                    title=ft.Text("Termos e Condições de Uso - App Fábrica", weight=ft.FontWeight.W_600, size=16),
                    subtitle=ft.Text("Proteção de dados e privacidade"),
                ),
            ]),
            alignment=ft.alignment.center
        ),
        ft.Divider(),
        
        # Seção I
        criar_secao(
            "I. ACEITAÇÃO DOS TERMOS",
            ft.Column([
                ft.Text("Ao acessar e utilizar este site e seus serviços, o usuário (aluno, responsável ou professor) declara ter lido, compreendido e concordado com estes Termos e Condições de Uso.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=8),
                ft.Text("Caso não concorde com algum ponto, o usuário não deve utilizar a plataforma.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY, weight=ft.FontWeight.W_500),
            ])
        ),
        
        # Seção II
        criar_secao(
            "II. DEFINIÇÕES",
            ft.Column([
                criar_item_lista("Plataforma: site ou sistema de gestão educacional do App Fábrica."),
                criar_item_lista("Usuário: aluno, pai/mãe/responsável ou professor que utiliza a plataforma."),
                criar_item_lista("Controlador: App Fábrica, responsável pelo tratamento de dados."),
                criar_item_lista("Operador: terceiros contratados que tratam dados pessoais sob orientação do controlador."),
                criar_item_lista("Dados pessoais: informações que identificam ou podem identificar o usuário."),
                criar_item_lista("LGPD: Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018)."),
            ], spacing=6)
        ),
        
        # Seção III
        criar_secao(
            "III. COLETA DE DADOS",
            ft.Column([
                ft.Text("A plataforma poderá coletar:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(height=10),
                
                ft.Text("Alunos:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(
                    content=ft.Column([
                        criar_item_lista("Nome completo, CPF, data de nascimento"),
                        criar_item_lista("Telefone e e-mail"),
                        criar_item_lista("Senha"),
                        criar_item_lista("Gênero"),
                        criar_item_lista("Notas e frequência"),
                        criar_item_lista("Fotografias e registros de atividades"),
                    ], spacing=4),
                    padding=ft.padding.only(left=16)
                ),
                
                ft.Container(height=8),
                ft.Text("Pais ou responsáveis:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(
                    content=ft.Column([
                        criar_item_lista("Nome completo, CPF, data de nascimento"),
                        criar_item_lista("Relação com o aluno"),
                        criar_item_lista("Senha"),
                        criar_item_lista("Telefone e e-mail"),
                    ], spacing=4),
                    padding=ft.padding.only(left=16)
                ),
                
                ft.Container(height=8),
                ft.Text("Professores:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(
                    content=ft.Column([
                        criar_item_lista("Nome completo"),
                        criar_item_lista("E-mail institucional"),
                        criar_item_lista("Senha"),
                    ], spacing=4),
                    padding=ft.padding.only(left=16)
                ),
                
                ft.Container(height=8),
                ft.Text("Gestão:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(
                    content=ft.Column([
                        criar_item_lista("Nome completo"),
                        criar_item_lista("E-mail institucional"),
                        criar_item_lista("Senha"),
                    ], spacing=4),
                    padding=ft.padding.only(left=16)
                ),
                
                ft.Container(height=10),
                ft.Text("Os dados são coletados somente para fins educacionais e administrativos.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY, weight=ft.FontWeight.W_500),
            ])
        ),
        
        # Seção IV
        criar_secao(
            "IV. FINALIDADE DO TRATAMENTO DE DADOS",
            ft.Column([
                ft.Text("Os dados pessoais coletados pelo App Fábrica são tratados exclusivamente para finalidades específicas, legítimas e transparentes, relacionadas à gestão educacional e administrativa da plataforma.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=10),
                ft.Text("As principais finalidades incluem:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(height=8),
                ft.Column([
                    criar_item_numerado("1", "Gestão acadêmica: realizar matrícula, registrar frequência, notas e desempenho escolar, gerar relatórios acadêmicos e históricos."),
                    ft.Container(height=6),
                    criar_item_numerado("2", "Comunicação institucional: enviar avisos, boletins, comunicados, informações pedagógicas e eventuais alertas aos alunos, pais ou responsáveis."),
                    ft.Container(height=6),
                    criar_item_numerado("3", "Autenticação e acesso à plataforma: permitir que cada usuário tenha login seguro, garantindo o uso adequado dos recursos do sistema."),
                    ft.Container(height=6),
                    criar_item_numerado("4", "Cumprimento de obrigações legais: atender a exigências de órgãos governamentais e educacionais, incluindo emissão de documentos oficiais e relatórios legais."),
                    ft.Container(height=6),
                    criar_item_numerado("5", "Segurança da informação: monitorar acessos e atividades para prevenir fraudes, uso indevido ou qualquer violação de dados pessoais."),
                ]),
                ft.Container(height=10),
                ft.Text("O tratamento dos dados é sempre realizado respeitando os princípios da LGPD, como necessidade, finalidade, transparência e segurança, garantindo que apenas as informações essenciais sejam utilizadas para cada propósito.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
            ])
        ),
        
        # Seção V
        criar_secao(
            "V. COMPARTILHAMENTO DE DADOS",
            ft.Column([
                ft.Text("O App Fábrica não compartilha, comercializa ou divulga dados pessoais dos usuários para terceiros sem a devida autorização, exceto nas seguintes situações:", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=10),
                ft.Column([
                    criar_item_numerado("1", "Cumprimento de obrigações legais ou regulatórias: quando o compartilhamento for exigido por lei, norma ou autoridade competente, como órgãos educacionais ou fiscais."),
                    ft.Container(height=6),
                    criar_item_numerado("2", "Prestadores de serviços contratados: empresas ou profissionais que realizam serviços em nome da instituição (como hospedagem de dados, processamento de pagamentos ou suporte técnico), desde que também cumpram as exigências da LGPD."),
                    ft.Container(height=6),
                    criar_item_numerado("3", "Autorização expressa do titular: quando o usuário ou seu responsável legal consentir de forma clara e específica para que seus dados sejam compartilhados."),
                    ft.Container(height=6),
                    criar_item_numerado("4", "Processos judiciais ou administrativos: quando for necessário para a defesa da instituição ou atendimento a ordens judiciais ou governamentais."),
                ]),
                ft.Container(height=10),
                ft.Text("Em todas as situações, a instituição garante que o tratamento e compartilhamento dos dados será realizado de maneira segura, transparente e limitada à finalidade específica, conforme previsto na LGPD.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
            ])
        ),
        
        # Seção VI
        criar_secao(
            "VI. DIREITOS DOS USUÁRIOS",
            ft.Column([
                ft.Text("Em conformidade com a Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709/2018), os usuários têm direitos assegurados sobre seus dados pessoais, que podem ser exercidos a qualquer momento.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=10),
                ft.Text("Esses direitos incluem:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(height=8),
                ft.Column([
                    criar_item_numerado("1", "Confirmação de tratamento: saber se seus dados pessoais estão sendo coletados e utilizados pela plataforma."),
                    ft.Container(height=6),
                    criar_item_numerado("2", "Acesso aos dados: obter cópia das informações pessoais que estão sendo tratadas."),
                    ft.Container(height=6),
                    criar_item_numerado("3", "Correção: solicitar a atualização ou retificação de dados incompletos, inexatos ou desatualizados."),
                    ft.Container(height=6),
                    criar_item_numerado("4", "Anonimização, bloqueio ou exclusão: pedir que dados desnecessários ou excessivos sejam anonimizados, bloqueados ou eliminados."),
                    ft.Container(height=6),
                    criar_item_numerado("5", "Revogação do consentimento: retirar o consentimento previamente concedido para o tratamento de seus dados."),
                    ft.Container(height=6),
                    criar_item_numerado("6", "Portabilidade: transferir seus dados pessoais para outro serviço ou fornecedor, quando aplicável."),
                    ft.Container(height=6),
                    criar_item_numerado("7", "Informações sobre compartilhamento: ser informado sobre terceiros com os quais seus dados possam ter sido compartilhados."),
                ]),
                ft.Container(height=10),
                ft.Text("Para exercer esses direitos, o usuário pode entrar em contato com a Fábrica", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=8),
                ft.Text("A instituição compromete-se a responder às solicitações de forma clara e em prazo razoável, garantindo que os direitos do titular sejam plenamente respeitados.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
            ])
        ),
        
        # Seção VII
        criar_secao(
            "VII. SEGURANÇA E ARMAZENAMENTO",
            ft.Column([
                ft.Text("O App Fábrica adota medidas técnicas, administrativas e organizacionais adequadas para proteger os dados pessoais dos usuários contra acessos não autorizados, uso indevido, alteração, divulgação ou destruição.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=10),
                ft.Text("Os dados coletados são armazenados apenas pelo período necessário para cumprir as finalidades para as quais foram coletados, respeitando as exigências legais e regulatórias aplicáveis.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=8),
                ft.Text("Após o término desse período ou quando os dados deixarem de ser necessários, eles serão devidamente eliminados ou anonimizados, garantindo que não possam mais ser identificados ou utilizados de forma indevida.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=8),
                ft.Text("A instituição se compromete a manter práticas de segurança da informação atualizadas, monitorando continuamente o sistema e treinando colaboradores, de modo a minimizar riscos e proteger a privacidade dos usuários.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
            ])
        ),
        
        # Seção VIII
        criar_secao(
            "VIII. USO DE COOKIES",
            ft.Column([
                ft.Text("A App Fábrica utiliza cookies e tecnologias semelhantes para melhorar a experiência dos usuários em sua plataforma, armazenando preferências, registrando interações e permitindo o funcionamento adequado de funcionalidades essenciais do sistema.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=10),
                ft.Text("Os cookies podem ser utilizados para:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(height=8),
                ft.Column([
                    criar_item_numerado("1", "Personalizar a navegação, lembrando preferências e ajustes do usuário;"),
                    ft.Container(height=6),
                    criar_item_numerado("2", "Garantir segurança, prevenindo acessos não autorizados e fraudes;"),
                    ft.Container(height=6),
                    criar_item_numerado("3", "Analisar o uso da plataforma, permitindo melhorias contínuas nos serviços oferecidos."),
                ]),
                ft.Container(height=10),
                ft.Text("O usuário pode, a qualquer momento, gerenciar ou desativar os cookies através das configurações de seu navegador, porém essa ação pode limitar ou impedir o acesso a certas funcionalidades da plataforma.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=8),
                ft.Text("A utilização de cookies está em conformidade com a LGPD, garantindo transparência e controle do usuário sobre suas informações.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
            ])
        ),
        
        # Seção IX
        criar_secao(
            "IX. DEVERES DOS USUÁRIOS",
            ft.Column([
                ft.Text("Os usuários da plataforma da App Fábrica têm a responsabilidade de utilizar os serviços de maneira ética, segura e adequada, comprometendo-se a:", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=10),
                ft.Column([
                    criar_item_numerado("1", "Fornecer informações verdadeiras e precisas, mantendo seus dados pessoais atualizados;"),
                    ft.Container(height=6),
                    criar_item_numerado("2", "Utilizar a plataforma de forma adequada, respeitando as regras institucionais e evitando qualquer prática que possa comprometer o sistema ou terceiros;"),
                    ft.Container(height=6),
                    criar_item_numerado("3", "Manter a confidencialidade das credenciais de acesso, como senhas e logins, não compartilhando-os com outras pessoas;"),
                    ft.Container(height=6),
                    criar_item_numerado("4", "Não divulgar ou compartilhar dados pessoais de terceiros sem a devida autorização;"),
                    ft.Container(height=6),
                    criar_item_numerado("5", "Cooperar com a instituição em situações que exijam esclarecimentos ou ajustes relacionados ao uso da plataforma e à proteção de dados pessoais."),
                ]),
                ft.Container(height=10),
                ft.Text("O descumprimento destes deveres pode acarretar restrição de acesso à plataforma e outras medidas previstas na legislação e nas políticas internas da instituição.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
            ])
        ),
        
        # Seção X
        criar_secao(
            "X. ALTERAÇÕES DOS TERMOS",
            ft.Column([
                ft.Text("O App Fábrica pode atualizar estes Termos e Condições de Uso a qualquer momento, a fim de refletir mudanças na legislação, na plataforma, nas políticas internas ou em outros aspectos relevantes para a segurança e proteção dos dados dos usuários.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=10),
                ft.Text("Toda alteração será publicada nesta mesma página, com a devida data de atualização, garantindo transparência e permitindo que o usuário tenha ciência das mudanças.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=8),
                ft.Text("O uso contínuo da plataforma após a publicação de alterações constitui aceitação expressa dos novos Termos e Condições, obrigando o usuário a cumprir as disposições atualizadas.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=8),
                ft.Text("Recomenda-se que o usuário verifique periodicamente esta página, a fim de se manter informado sobre as condições vigentes para o uso da plataforma e o tratamento de seus dados pessoais.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
            ])
        ),
        
        # Seção XI
        criar_secao(
            "XI. LEGISLAÇÃO E FORO",
            ft.Column([
                ft.Text("Estes Termos são regidos pelas leis da República Federativa do Brasil, especialmente pela Lei nº 13.709/2018 – Lei Geral de Proteção de Dados Pessoais (LGPD).", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=10),
                ft.Text("A LGPD é a legislação brasileira que regula o uso, tratamento e proteção de dados pessoais de qualquer pessoa física. Ela garante que cada indivíduo tenha controle sobre suas informações, determinando como empresas e instituições podem coletar, armazenar, compartilhar e excluir dados.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
                ft.Container(height=10),
                ft.Text("De forma prática, a LGPD estabelece que:", size=14, weight=ft.FontWeight.W_500),
                ft.Container(height=8),
                ft.Column([
                    criar_item_lista("Os dados só podem ser usados para finalidades específicas e claras;"),
                    criar_item_lista("O titular (a pessoa dona dos dados) tem direito de acesso, correção, exclusão e portabilidade de suas informações;"),
                    criar_item_lista("A instituição deve garantir segurança e proteger os dados contra acessos não autorizados;"),
                    criar_item_lista("Qualquer tratamento de dados precisa ser transparente e justificado, e o titular deve ser informado sobre como suas informações são utilizadas."),
                ], spacing=6),
                ft.Container(height=10),
                ft.Text("Caso haja qualquer disputa ou necessidade de solução judicial relacionada a estes Termos ou ao uso de dados pessoais, fica eleito o foro da comarca de [Cidade/UF da instituição], com renúncia a qualquer outro, para dirimir tais questões.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY),
            ])
        ),
        
        # Declaração final
        ft.Container(
            content=ft.Column([
                ft.Divider(),
                ft.Text("DECLARAÇÃO DE CIÊNCIA E ACEITAÇÃO", 
                       size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                ft.Text("Ao utilizar este aplicativo, você reconhece que leu e compreendeu estes Termos e Condições e concorda em estar vinculado por eles.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY, weight=ft.FontWeight.W_500),
                ft.Container(height=5),
                ft.Text("Este documento constitui instrumento formal e vinculante entre as partes.", 
                       size=14, text_align=ft.TextAlign.JUSTIFY, style=ft.TextStyle(italic=True)),
            ]),
            padding=20,
            border_radius=8,
            margin=ft.margin.only(top=10)
        ),
    ], scroll=ft.ScrollMode.ADAPTIVE)

    card_termos = ft.Card(
        content=ft.Container(
            content=termos_content,
            padding=25,
        ),
        elevation=8,
        margin=ft.margin.all(10)
    )

    # Botão de aceitação
    btn_aceitar = ft.Checkbox(label="CONCORDAR E ACEITAR OS TERMOS", value=False)

    # Rodapé
    rodape = ft.Container(
        content=ft.Column([
            ft.Container(btn_aceitar, alignment=ft.alignment.center),
            ft.Divider(),
            ft.Text(
                "Documento invalido até o momento",
                size=11,
                color=ft.Colors.GREY_600,
                italic=True,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Versão 1.0.0 | App Fábrica © 2025",
                size=11,
                text_align=ft.TextAlign.CENTER
            )
        ]),
        padding=ft.padding.only(top=20, bottom=10)
    )

    # Layout principal
    layout_principal = ft.Column([
        card_termos,
        rodape
    ])

    page.add(layout_principal)

ft.app(target=TermosView)