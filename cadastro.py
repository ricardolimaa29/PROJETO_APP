import flet as ft
import datetime
import re
import json
import os

def CadastroView(page: ft.Page):
    page.title = "Criar conta - Fábrica do Programador"
    page.theme_mode = "dark"
    page.window.width = 500
    page.window.height = 900
    page.window.min_width = 500
    page.window.min_height = 900
    page.window.max_width = 500
    page.window.max_height = 900

    state = {"step": 0}
    ano_atual = datetime.datetime.now().year
    ano_min = 1935
    ano_max = ano_atual - 5

    email_dominios = [
        "@outlook.com", "@hotmail.com", "@live.com", "@yahoo.com", "@icloud.com",
        "@aol.com", "@bol.com.br", "@uol.com.br", "@terra.com.br", "@globo.com",
        "@ig.com.br", "@protonmail.com", "@tutanota.com", "@zoho.com", "@gmail.com",
        "@aluno.santanadeparnaiba.sp.gov.br", "@edu.santanadeparnaiba.sp.gov.br", "@fabrica.santanadeparnaiba.sp.gov.br"
    ]

    # --- Função para verificar força da senha ---
    def verificar_forca_senha(senha):
        pontos = 0
        if len(senha) >= 8: pontos += 1
        if re.search(r"[A-Z]", senha): pontos += 1
        if re.search(r"[a-z]", senha): pontos += 1
        if re.search(r"\d", senha): pontos += 1
        if re.search(r"\W", senha): pontos += 1

        if pontos <= 2: return "fraca"
        elif pontos <= 4: return "média"
        else: return "forte"

    # --- Campos ---
    nome_field = ft.TextField(label="Nome completo", width=400)
    dia = ft.TextField(label="Dia", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    mes = ft.Dropdown(
        label="Mês", width=150,
        options=[ft.dropdown.Option(m) for m in [
            "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
            "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
        ]]
    )
    ano = ft.TextField(label="Ano", width=100, keyboard_type=ft.KeyboardType.NUMBER)
    genero = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="F", label="Feminino"),
        ft.Radio(value="M", label="Masculino"),
        ft.Radio(value="O", label="Outro"),
        ft.Radio(value="N", label="Prefiro não dizer"),
    ]))
    email = ft.TextField(label="E-mail", width=400)
    senha = ft.TextField(label="Senha", width=400, password=True, can_reveal_password=True)
    senha_conf = ft.TextField(label="Confirmar senha", width=400, password=True, can_reveal_password=True)
    telefone = ft.TextField(label="Telefone", width=400)

    # --- Máscara telefone ---
    def formatar_telefone(e):
        valor = telefone.value.strip()
        numeros = "".join(filter(str.isdigit, valor))
        if len(numeros) > 11: numeros = numeros[:11]

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

    # --- Telas ---
    def tela_nome():
        return ft.Column([ft.Text("Passo 1 de 5"), nome_field,
                          ft.ElevatedButton("Próximo", on_click=lambda e: avancar())],
                         alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def tela_data_genero():
        return ft.Column([
            ft.Text("Passo 2 de 5"),
            ft.Row([dia, mes, ano], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Gênero", weight="bold"),
            genero,
            ft.Row([ft.TextButton("Voltar", on_click=lambda e: voltar()),
                    ft.ElevatedButton("Próximo", on_click=lambda e: avancar())],
                   alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def tela_email():
        return ft.Column([ft.Text("Passo 3 de 5"), email,
                          ft.Row([ft.TextButton("Voltar", on_click=lambda e: voltar()),
                                  ft.ElevatedButton("Próximo", on_click=lambda e: avancar())],
                                 alignment=ft.MainAxisAlignment.CENTER)],
                         alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def tela_senha():
        return ft.Column([ft.Text("Passo 4 de 5"), senha, senha_conf,
                          ft.Row([ft.TextButton("Voltar", on_click=lambda e: voltar()),
                                  ft.ElevatedButton("Próximo", on_click=lambda e: avancar())],
                                 alignment=ft.MainAxisAlignment.CENTER)],
                         alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def tela_telefone():
        return ft.Column([ft.Text("Passo 5 de 5"), telefone,
                          ft.Row([ft.TextButton("Voltar", on_click=lambda e: voltar()),
                                  ft.ElevatedButton("Criar conta", on_click=lambda e: criar_conta())],
                                 alignment=ft.MainAxisAlignment.CENTER)],
                         alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    telas = [tela_nome, tela_data_genero, tela_email, tela_senha, tela_telefone]
    container = ft.Container(content=telas[0](), padding=20, alignment=ft.alignment.center)

    # --- Navegação ---
    def avancar():
        if state["step"] == 0:
            nome_digitado = nome_field.value.strip()
            if not nome_digitado or len(nome_digitado) < 10 or not re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome_digitado):
                page.open(ft.SnackBar(ft.Text("Nome inválido!", color="White"), bgcolor="RED"))
                page.update()
                return
            state["nome"] = nome_digitado
        elif state["step"] == 1:
            try:
                dia_int = int(dia.value)
                ano_int = int(ano.value)
                if mes.value == "Fevereiro" and not 1 <= dia_int <= 29:
                    raise ValueError
                elif mes.value != "Fevereiro" and not 1 <= dia_int <= 30:
                    raise ValueError
                if ano_int < ano_min or ano_int > ano_max:
                    raise ValueError
            except:
                page.open(ft.SnackBar(ft.Text("Data inválida!", color="White"), bgcolor="RED"))
                page.update()
                return
            if genero.value is None:
                page.open(ft.SnackBar(ft.Text("Informe seu gênero!", color="White"), bgcolor="RED"))
                page.update()
                return
        elif state["step"] == 2:
            if not any(email.value.lower().endswith(d) for d in email_dominios):
                page.open(ft.SnackBar(ft.Text("Email inválido!", color="White"), bgcolor="RED"))
                page.update()
                return
        elif state["step"] == 3:
            if senha.value.strip() == "" or senha_conf.value.strip() == "" or senha.value != senha_conf.value:
                page.open(ft.SnackBar(ft.Text("Senhas inválidas!", color="White"), bgcolor="RED"))
                page.update()
                return
        elif state["step"] == 4:
            numeros = "".join(filter(str.isdigit, telefone.value))
            if len(numeros) != 11:
                page.open(ft.SnackBar(ft.Text("Telefone deve ter 11 números!", color="White"), bgcolor="RED"))
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

    # --- Criar conta ---
    def criar_conta():
        usuario = {
            "nome": nome_field.value.strip(),
            "data_nascimento": f"{dia.value}/{mes.value}/{ano.value}",
            "genero": genero.value,
            "email": email.value.strip(),
            "senha": senha.value.strip(),  # agora salvo a senha
            "telefone": telefone.value.strip(),
            "imagem_personalizada": "",
            "imagem_base": "fem.jpeg" if genero.value=="F" else "masc.jpeg" if genero.value=="M" else "outro.jpeg"
        }

        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r") as f:
                dados = json.load(f)
        else:
            dados = {"usuarios": []}

        dados["usuarios"].append(usuario)
        with open("usuarios.json", "w") as f:
            json.dump(dados, f, indent=4)

        page.open(ft.SnackBar(ft.Text("Conta criada com sucesso! Faça login.", color="White"), bgcolor="GREEN"))
        page.update()
        page.go("/login")  # direciona para login

    # --- Header ---
    voltar_button = ft.IconButton(icon="ARROW_BACK", icon_color="WHITE", tooltip="Voltar", on_click=lambda e: page.go("/login"))
    header = ft.Row(controls=[voltar_button], alignment="start")

    return ft.View(
        route="/cadastro",
        controls=[ft.Column([header, container], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)],
        vertical_alignment="center",
        horizontal_alignment="center",
    )



