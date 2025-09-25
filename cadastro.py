import flet as ft
import datetime
import re
 
# --------------------------------------------------------------------------------------------------
# INTERFACE COM FLET
# --------------------------------------------------------------------------------------------------

def CadastroView(page:ft.Page):
    page.title = "Criar conta - Fábrica do Programador"
    page.theme_mode = "dark"
    page.window.width = 500
    page.window.min_width = 500
    page.window.max_width = 500
    page.window.height = 800
    page.window.min_height = 800
    page.window.max_height = 800

    state = {"step": 0}

    ano_atual = datetime.datetime.now().year
    ano_min = 1935
    ano_max = ano_atual - 5

    # Domínios permitidos de email
    email_dominios = [
        "@outlook.com", "@hotmail.com", "@live.com", "@yahoo.com", "@icloud.com",
        "@aol.com", "@bol.com.br", "@uol.com.br", "@terra.com.br", "@globo.com",
        "@ig.com.br", "@protonmail.com", "@tutanota.com", "@zoho.com", "@gmail.com",
        "@aluno.santanadeparnaiba.sp.gov.br", "@edu.santanadeparnaiba.sp.gov.br" ]

    # --------------------------------------------------------------------------------------------------
    # Função para checar força da senha
    def verificar_forca_senha(senha):
        pontos = 0
        if len(senha) >= 8:
            pontos += 1
        if re.search(r"[A-Z]", senha):  # Tem letra maiúscula
            pontos += 1
        if re.search(r"[a-z]", senha):  # Tem letra minúscula
            pontos += 1
        if re.search(r"\d", senha):     # Tem número
            pontos += 1
        if re.search(r"\W", senha):     # Tem caractere especial
            pontos += 1

        if pontos <= 2:
            return "fraca"
        elif pontos == 3 or pontos == 4:
            return "média"
        else:
            return "forte"

    # --------------------------------------------------------------------------------------------------
    # Campos
    nome_field = ft.TextField(label="Nome completo", width=400)
    dia = ft.TextField(label="Dia", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    mes = ft.Dropdown(
        label="Mês", width=150,
        options=[ft.dropdown.Option(m) for m in [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]]
    )
    ano = ft.TextField(label="Ano", width=100, keyboard_type=ft.KeyboardType.NUMBER)

    genero_label = ft.Text("Gênero", weight="bold")
    genero = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="F", label="Feminino"),
            ft.Radio(value="M", label="Masculino"),
            ft.Radio(value="O", label="Outro"),
            ft.Radio(value="N", label="Prefiro não dizer"),
        ])
    )

    email = ft.TextField(label="E-mail", width=400)
    senha = ft.TextField(label="Senha", width=400, password=True, can_reveal_password=True)
    senha_conf = ft.TextField(label="Confirmar senha", width=400, password=True, can_reveal_password=True)
    telefone = ft.TextField(label="Telefone", width=400)

    # Máscara automática do telefone
    def formatar_telefone(e):
        valor = telefone.value.strip()
        numeros = "".join(filter(str.isdigit, valor))
        if len(numeros) > 11:
            numeros = numeros[:11]

        if len(numeros) >= 2:
            telefone.value = f"({numeros[:2]})"
            if len(numeros) >= 7:
                telefone.value += numeros[2:7]
                if len(numeros) > 7:
                    telefone.value += "-" + numeros[7:]
            else:
                telefone.value += numeros[2:]
        else:
            telefone.value = numeros
        telefone.update()

    telefone.on_change = formatar_telefone

    # --------------------------------------------------------------------------------------------------
    # Telas
    def tela_nome():
        return ft.Column(
            [
                ft.Text("Passo 1 de 5"),
                nome_field,
                ft.ElevatedButton("Próximo", on_click=lambda e: avancar())
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True
        )

    def tela_data_genero():
        return ft.Column(
            [
                ft.Text("Passo 2 de 5"),
                ft.Row([dia, mes, ano], alignment=ft.MainAxisAlignment.CENTER),
                genero_label,
                genero,
                ft.Row([
                    ft.TextButton("Voltar", on_click=lambda e: voltar()),
                    ft.ElevatedButton("Próximo", on_click=lambda e: avancar())
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True
        )

    def tela_email():
        return ft.Column(
            [
                ft.Text("Passo 3 de 5"),
                email,
                ft.Row([
                    ft.TextButton("Voltar", on_click=lambda e: voltar()),
                    ft.ElevatedButton("Próximo", on_click=lambda e: avancar())
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True
        )

    def tela_senha():
        return ft.Column(
            [
                ft.Text("Passo 4 de 5"),
                senha,
                senha_conf,
                ft.Row([
                    ft.TextButton("Voltar", on_click=lambda e: voltar()),
                    ft.ElevatedButton("Próximo", on_click=lambda e: avancar())
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True
        )

    def tela_telefone():
        return ft.Column(
            [
                ft.Text("Passo 5 de 5"),
                telefone,
                ft.Row([
                    ft.TextButton("Voltar", on_click=lambda e: voltar()),
                    ft.ElevatedButton("Criar conta", on_click=lambda e: criar_conta())
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True
        )

    telas = [tela_nome, tela_data_genero, tela_email, tela_senha, tela_telefone]
    container = ft.Container(
        content=telas[0](),
        padding=20,
        alignment=ft.alignment.center
    )

    # --------------------------------------------------------------------------------------------------
    # Funções de navegação
    def avancar():
        # Validação do nome
        if state["step"] == 0:
            nome_digitado = nome_field.value.strip()
            if nome_digitado == "":
                page.open(ft.SnackBar(ft.Text("Digite o nome!", color="White"), bgcolor="RED"))
                page.update()
                return
            if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome_digitado):
                page.open(ft.SnackBar(ft.Text("Nome inválido! Use apenas letras.", color="White"), bgcolor="RED"))
                page.update()
                return
            if len(nome_digitado) < 10:
                page.open(ft.SnackBar(ft.Text("Mínimo 10 caracteres!", color="White"), bgcolor="RED"))
                page.update()
                return
            state["nome"] = nome_digitado

        # Data de nascimento e gênero
        if state["step"] == 1:
            try:
                dia_int = int(dia.value)
                if mes.value == "Fevereiro":
                    if not 1 <= dia_int <= 29:
                        page.open(ft.SnackBar(ft.Text("Dia inválido para Fevereiro!", color="White"), bgcolor="RED"))
                        page.update()
                        return
                else:
                    if not 1 <= dia_int <= 30:
                        page.open(ft.SnackBar(ft.Text("Dia inválido! Use 1-30.", color="White"), bgcolor="RED"))
                        page.update()
                        return
            except ValueError:
                page.open(ft.SnackBar(ft.Text("Dia inválido!", color="White"), bgcolor="RED"))
                page.update()
                return

            try:
                ano_int = int(ano.value)
                if ano_int < ano_min or ano_int > ano_max:
                    page.open(ft.SnackBar(ft.Text(f"Ano deve ser entre {ano_min} e {ano_max}!", color="White"), bgcolor="RED"))
                    page.update()
                    return
            except ValueError:
                page.open(ft.SnackBar(ft.Text("Digite um ano válido!", color="White"), bgcolor="RED"))
                page.update()
                return

            if genero.value is None:
                page.open(ft.SnackBar(ft.Text("Informe seu gênero!", color="White"), bgcolor="RED"))
                page.update()
                return

        # Email
        if state["step"] == 2:
            if not any(email.value.lower().endswith(d) for d in email_dominios):
                page.open(ft.SnackBar(ft.Text("Email inválido! Use um domínio permitido.", color="White"), bgcolor="RED"))
                page.update()
                return

        # Senha
        if state["step"] == 3:
            if senha.value.strip() == "":
                page.open(ft.SnackBar(ft.Text("Digite a senha!", color="White"), bgcolor="RED"))
                page.update()
                return
            if senha_conf.value.strip() == "":
                page.open(ft.SnackBar(ft.Text("Confirme a senha!", color="White"), bgcolor="RED"))
                page.update()
                return
            if len(senha.value) < 8:
                page.open(ft.SnackBar(ft.Text("Senha muito curta! Mínimo 8 caracteres.", color="White"), bgcolor="RED"))
                page.update()
                return
            if not re.search(r"[A-Z]", senha.value):
                page.open(ft.SnackBar(ft.Text("A senha precisa ter pelo menos 1 letra maiúscula.", color="White"), bgcolor="RED"))
                page.update()
                return
            if not re.search(r"[a-z]", senha.value):
                page.open(ft.SnackBar(ft.Text("A senha precisa ter pelo menos 1 letra minúscula.", color="White"), bgcolor="RED"))
                page.update()
                return
            if not re.search(r"\d", senha.value):
                page.open(ft.SnackBar(ft.Text("A senha precisa ter pelo menos 1 número.", color="White"), bgcolor="RED"))
                page.update()
                return
            if not re.search(r"\W", senha.value):
                page.open(ft.SnackBar(ft.Text("A senha precisa ter pelo menos 1 símbolo.", color="White"), bgcolor="RED"))
                page.update()
                return
            if senha.value != senha_conf.value:
                page.open(ft.SnackBar(ft.Text("As senhas não coincidem!", color="White"), bgcolor="RED"))
                page.update()
                return

            forca = verificar_forca_senha(senha.value)
            if forca == "fraca":
                page.open(ft.SnackBar(ft.Text("Senha FRACA: aumente a complexidade.", color="White"), bgcolor="RED"))
            elif forca == "média":
                page.open(ft.SnackBar(ft.Text("Senha MÉDIA: já serve, mas pode melhorar.", color="White"), bgcolor="ORANGE"))
            else:
                page.open(ft.SnackBar(ft.Text("Senha FORTE: excelente!", color="White"), bgcolor="GREEN"))
            page.update()

        # Telefone
        if state["step"] == 4:
            numeros = "".join(filter(str.isdigit, telefone.value))
            if len(numeros) != 11:
                page.open(ft.SnackBar(ft.Text("Telefone deve ter 11 números!", color="White"), bgcolor="RED"))
                page.update()
                return
            if not numeros.isdigit():
                page.open(ft.SnackBar(ft.Text("Telefone inválido! Apenas números.", color="White"), bgcolor="RED"))
                page.update()
                return

        if state["step"] < len(telas) - 1:
            state["step"] += 1
            container.content = telas[state["step"]]()
            page.update()

    def voltar():
        if state["step"] > 0:
            state["step"] -= 1
            container.content = telas[state["step"]]()
            page.update()

    # --------------------------------------------------------------------------------------------------
    # Criar conta (com revalidação final)
    def criar_conta():
        # Revalidar senha
        if senha.value.strip() == "" or senha_conf.value.strip() == "":
            page.open(ft.SnackBar(ft.Text("Senha ou confirmação não preenchida!", color="White"), bgcolor="RED"))
            page.update()
            return
        if len(senha.value) < 8 or senha.value != senha_conf.value:
            page.open(ft.SnackBar(ft.Text("Senha inválida ou não coincide.", color="White"), bgcolor="RED"))
            page.update()
            return
        if not re.search(r"[A-Z]", senha.value) or not re.search(r"[a-z]", senha.value) or not re.search(r"\d", senha.value) or not re.search(r"\W", senha.value):
            page.open(ft.SnackBar(ft.Text("Senha deve ter maiúscula, minúscula, número e símbolo.", color="White"), bgcolor="RED"))
            page.update()
            return

        # Revalidar telefone
        numeros = "".join(filter(str.isdigit, telefone.value))
        if len(numeros) != 11 or not numeros.isdigit():
            page.open(ft.SnackBar(ft.Text("Telefone inválido! Apenas 11 números.", color="White"), bgcolor="RED"))
            page.update()
            return

        # Se tudo passou:
        page.open(ft.SnackBar(ft.Text("Conta criada com sucesso!", color="White"), bgcolor="GREEN"))
        page.update()
        return

    # --------------------------------------------------------------------------------------------------

    return ft.View(
        route="/cadastro",
        controls=[
            ft.Column(
            [container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

