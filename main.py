import flet as ft
import json
import os


# Define a pasta onde está este arquivo .py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define o caminho completo do arquivo de configurações JSON
ARQUIVO_CONFIG = os.path.join(BASE_DIR, "configuracoes.json")


def carregar_configuracoes():
    """
    Lê o arquivo configuracoes.json e retorna seu conteúdo como dicionário.
    Se ocorrer erro de arquivo ausente, JSON inválido ou outro problema,
    retorna um dicionário vazio.
    """
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


# Carrega as configurações uma única vez ao iniciar o programa
CONFIGURACOES = carregar_configuracoes()


def main(page: ft.Page):
    """
    Função principal da aplicação Flet.
    Monta a interface gráfica, cria os controles e define os eventos.
    """
    page.title = "Configurador de Inversores"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 700
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.GREY_100

    # Armazena o link atualmente selecionado
    link_atual = {"url": ""}

    def obter_link_configuracao():
        """
        Retorna o link da configuração selecionada no momento.
        """
        if not dd_inversor.value or not dd_configuracao.value:
            return ""

        grupo = CONFIGURACOES.get(dd_inversor.value, {})
        dados = grupo.get(dd_configuracao.value, {})

        if isinstance(dados, dict):
            return dados.get("link", "")

        return ""

    def atualizar_linha_link():
        """
        Atualiza a área visual do link na interface.
        """
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

    def abrir_link(e):
        """
        Abre o link atual no navegador, se houver URL válida.
        """
        if link_atual["url"]:
            page.launch_url(link_atual["url"])

    imagem_topo = ft.Container(
        alignment=ft.alignment.bottom_left,
        content=ft.Image(
            src="images/topo01.png",
            height=70,
            fit=ft.ImageFit.COVER,
        ),
    )

    dd_inversor = ft.Dropdown(
        label="IF ",
        width=112,
        dense=True,
        content_padding=ft.padding.symmetric(vertical=4, horizontal=8),
        text_style=ft.TextStyle(size=15),
        label_style=ft.TextStyle(size=17),
        options=[ft.dropdown.Option(nome) for nome in sorted(CONFIGURACOES.keys())],
    )

    dd_configuracao = ft.Dropdown(
        label="Aplicação",
        width=175,
        dense=True,
        content_padding=ft.padding.symmetric(vertical=4, horizontal=8),
        text_style=ft.TextStyle(size=15),
        label_style=ft.TextStyle(size=17),
        options=[],
    )

    botao_mostrar = ft.ElevatedButton(
        text="Buscar",
        icon=ft.Icons.SEARCH,
        height=40,
        bgcolor=ft.Colors.ORANGE_800,
        color="#F7F8F3",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
        ),
    )

    texto_link = ft.Text(
        "Nenhum link disponível para esta configuração.",
        selectable=True,
        color=ft.Colors.GREY_700,
        size=14,
        text_align=ft.TextAlign.CENTER,
    )

    botao_abrir_link = ft.TextButton(
        text="abrir link",
        width=90,
        height=32,
        on_click=abrir_link,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.ORANGE_800,
            color="#F7F8F3",
            shape=ft.RoundedRectangleBorder(radius=5),
        ),
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
        page.update()

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
        padding=6,
        content=ft.Row(
            [dd_inversor, dd_configuracao, botao_mostrar],
            wrap=False,
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ),
    )

    linha_link = ft.Container(
        padding=4,
        alignment=ft.alignment.center,
        content=ft.Row(
            [
                texto_link,
                botao_abrir_link,
            ],
            wrap=True,
            spacing=6,
            run_spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    area_resultado = ft.Container(
        expand=True,
        padding=4,
        content=resultado,
    )

    rodape = ft.Row(
        [
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.ORANGE_800,
                padding=4,
                content=ft.Text(
                    "Metaltex",
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
            )
        ]
    )

    conteudo_app = ft.Container(
        width=400,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                imagem_topo,
                linha_codigo,
                area_resultado,
                linha_link,
                rodape,
            ],
        ),
    )

    def ajustar_layout(e=None):
        largura_disponivel = page.width if page.width else 400
        largura_final = min(max(largura_disponivel - 12, 280), 400)
        conteudo_app.width = largura_final
        page.update()

    page.on_resize = ajustar_layout

    page.add(
        ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[conteudo_app],
        )
    )

    ajustar_layout()


ft.app(target=main)