import flet as ft
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CONFIG = os.path.join(BASE_DIR, "configuracoes.json")


def carregar_configuracoes():
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, dict):
            print("JSON inválido: o arquivo precisa ter formato de dicionário.")
            return {}

        return dados

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {ARQUIVO_CONFIG}")
        return {}

    except json.JSONDecodeError as erro:
        print(f"Erro ao ler JSON: {erro}")
        return {}

    except Exception as erro:
        print(f"Erro inesperado: {erro}")
        return {}


CONFIGURACOES = carregar_configuracoes()


def main(page: ft.Page):
    page.title = "Configurador de Inversores"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 700
    page.padding = 0
    page.spacing = 0

    link_atual = {"url": ""}

    def obter_link_configuracao():
        if not dd_inversor.value or not dd_configuracao.value:
            return ""

        grupo = CONFIGURACOES.get(dd_inversor.value, {})
        dados = grupo.get(dd_configuracao.value, {})

        if isinstance(dados, dict):
            return dados.get("link", "")

        return ""

    def atualizar_linha_link():
        url = obter_link_configuracao()
        link_atual["url"] = url

        if url:
            texto_link.value = url
            texto_link.color = ft.Colors.BLUE_700
            botao_abrir_link.disabled = False
        else:
            texto_link.value = "Nenhum link disponível para esta configuração."
            texto_link.color = ft.Colors.GREY_700
            botao_abrir_link.disabled = True

        page.update()

    imagem_topo = ft.Container(
        #padding=15,
        #alignment=ft.alignment.center,
        content=ft.Image(
            src="images/topo01.png",
          #  width=2000,
            height=70,
            fit=ft.ImageFit.COVER,
            
            #border_radius=12,
        ),
    )

    dd_inversor = ft.Dropdown(
        label="Modelo do Inversor",
        width=220,
        options=[ft.dropdown.Option(nome) for nome in sorted(CONFIGURACOES.keys())],
    )

    dd_configuracao = ft.Dropdown(
        label="Configuração",
        width=260,
        options=[],
    )

    botao_mostrar = ft.ElevatedButton(
        text="Mostrar",
        icon=ft.Icons.SEARCH,
    )

    texto_link = ft.Text(
        "Nenhum link disponível para esta configuração.",
        selectable=True,
        color=ft.Colors.GREY_700,
        size=14,
    )

    def abrir_link(e):
        if link_atual["url"]:
            page.launch_url(link_atual["url"])

    botao_abrir_link = ft.TextButton(
        text="abrir link",
        on_click=abrir_link,
        disabled=True,
    )

    resultado = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def adicionar_secao(titulo, itens, separador="="):
        if not itens:
            return

        linhas = []
        for item in itens:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                linhas.append(ft.Text(f"{item[0]} {separador} {item[1]}"))
            else:
                linhas.append(ft.Text(str(item)))

        resultado.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column(
                        [
                            ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
                            *linhas,
                        ]
                    ),
                )
            )
        )

    def adicionar_observacoes(lista):
        if not lista:
            return

        resultado.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column(
                        [
                            ft.Text("OBSERVAÇÕES", size=18, weight=ft.FontWeight.BOLD),
                            *[ft.Text(f"• {obs}") for obs in lista],
                        ]
                    ),
                )
            )
        )

    def ao_mudar_inversor(e):
        dd_configuracao.value = None
        dd_configuracao.options = []
        resultado.controls.clear()

        modelo = dd_inversor.value

        if not modelo:
            atualizar_linha_link()
            return

        grupo = CONFIGURACOES.get(modelo, {})
        if not isinstance(grupo, dict):
            resultado.controls.append(
                ft.Text("Estrutura inválida para esse modelo.", color=ft.Colors.RED)
            )
            atualizar_linha_link()
            return

        nomes = list(grupo.keys())
        dd_configuracao.options = [ft.dropdown.Option(nome) for nome in nomes]
        atualizar_linha_link()

    def ao_mudar_configuracao(e):
        atualizar_linha_link()

    dd_inversor.on_change = ao_mudar_inversor
    dd_configuracao.on_change = ao_mudar_configuracao

    def mostrar_configuracao(e):
        resultado.controls.clear()

        if not dd_inversor.value:
            resultado.controls.append(
                ft.Text("Escolha um modelo de inversor.", color=ft.Colors.RED)
            )
            page.update()
            return

        if not dd_configuracao.value:
            resultado.controls.append(
                ft.Text("Escolha uma configuração.", color=ft.Colors.RED)
            )
            page.update()
            return

        grupo = CONFIGURACOES.get(dd_inversor.value, {})
        dados = grupo.get(dd_configuracao.value)

        if not isinstance(dados, dict):
            resultado.controls.append(
                ft.Text("Configuração inválida.", color=ft.Colors.RED)
            )
            page.update()
            return

        resultado.controls.append(
            ft.Text(
                f"{dd_inversor.value} - {dd_configuracao.value}",
                size=24,
                weight=ft.FontWeight.BOLD,
            )
        )
        resultado.controls.append(ft.Divider())

        adicionar_secao("LIGAÇÕES", dados.get("ligacoes", []), "→")
        adicionar_secao("PARÂMETROS", dados.get("parametros", []), "=")
        adicionar_secao("MOTOR", dados.get("motor", []), "=")
        adicionar_observacoes(dados.get("observacoes", []))

        atualizar_linha_link()
        page.update()

    botao_mostrar.on_click = mostrar_configuracao

    linha_codigo = ft.Container(
        padding=15,
        content=ft.Row(
            [dd_inversor, dd_configuracao, botao_mostrar],
            wrap=True,
            spacing=15,
        ),
    )

    linha_link = ft.Container(
        padding=15,
        content=ft.Row(
            [
                ft.Text("Desenho da Aplicação:", size=12, weight=ft.FontWeight.BOLD),
                texto_link,
                botao_abrir_link,
            ],
            wrap=True,
            spacing=12,
        ),
    )

    area_resultado = ft.Container(
        expand=True,
        padding=15,
        content=resultado,
    )

    rodape = ft.Row(
        [
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.ORANGE_800,
                padding=5,
                content=ft.Text(
                    "Metaltex ",
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
            )
        ]
    )

    page.add(
        ft.Column(
            expand=True,
            spacing=0,
            controls=[
                imagem_topo,
                linha_codigo,
                
                area_resultado,
                linha_link,
                rodape,
            ],
        )
    )


ft.app(target=main)