import flet as ft
import json
import os
from pathlib import Path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CONFIG = os.path.join(BASE_DIR, "configuracoes.json")
CONTADOR_ARQUIVO = Path(BASE_DIR) / "contador_acessos.txt"


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


def registrar_acesso():
    """
    Lê o contador de acessos do arquivo, soma 1 e grava de volta.
    Retorna o total atualizado ou None em caso de erro.
    """
    try:
        if CONTADOR_ARQUIVO.exists():
            valor = int(
                CONTADOR_ARQUIVO.read_text(encoding="utf-8").strip() or "0"
            )
        else:
            valor = 0

        valor += 1
        CONTADOR_ARQUIVO.write_text(str(valor), encoding="utf-8")
        return valor
    except Exception as erro:
        print(f"Erro ao registrar acesso: {erro}")
        return None


CONFIGURACOES = carregar_configuracoes()


def main(page: ft.Page):
    page.title = "Aplicações IF"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.GREY_100

    # Só força tamanho em desktop; em Android/iOS/Web deixa adaptar
    if page.platform in (
        ft.PagePlatform.WINDOWS,
        ft.PagePlatform.MACOS,
        ft.PagePlatform.LINUX,
    ):
        page.window_width = 0
        page.window_height = 0

    # Conta acesso toda vez que uma nova sessão é iniciada
    total_acessos = registrar_acesso()
    print("Total de acessos:", total_acessos)

    link_aplicacao = {"url": ""}
    link_manual = {"url": ""}

    def obter_links_aplicacao():
        """
        Retorna os links (aplicação e manual) da configuração selecionada.
        """
        if not dd_inversor.value or not dd_configuracao.value:
            return {"link": "", "manual": ""}

        grupo = CONFIGURACOES.get(dd_inversor.value, {})
        dados = grupo.get(dd_configuracao.value, {})

        if isinstance(dados, dict):
            return {
                "link": dados.get("link", ""),
                "manual": dados.get("manual", ""),
            }

        return {"link": "", "manual": ""}

    def atualizar_linha_link():
        """
        Atualiza os botões de aplicação e manual conforme a configuração selecionada.
        """
        links = obter_links_aplicacao()

        link_aplicacao["url"] = (
            links["link"].strip() if isinstance(links["link"], str) else ""
        )
        botao_aplicacao.disabled = not bool(link_aplicacao["url"])
        botao_aplicacao.visible = bool(link_aplicacao["url"])

        link_manual["url"] = (
            links["manual"].strip() if isinstance(links["manual"], str) else ""
        )
        botao_manual.disabled = not bool(link_manual["url"])
        botao_manual.visible = bool(link_manual["url"])

        page.update()

    def abrir_aplicacao(e):
        """
        Abre o link da aplicação no navegador, se houver URL válida.
        """
        if link_aplicacao["url"]:
            page.launch_url(link_aplicacao["url"])

    def abrir_manual(e):
        """
        Abre o manual da aplicação no navegador, se houver URL válida.
        """
        if link_manual["url"]:
            page.launch_url(link_manual["url"])

    imagem_topo = ft.Container(
        alignment=ft.alignment.bottom_left,
        content=ft.Image(
            src="images/topo01.png",
            height=70,
            fit=ft.ImageFit.COVER,
        ),
    )

    dd_texto01 = ft.Text(
        "Defina Inversor e Aplicação",
        size=15,
        color=ft.Colors.ORANGE_800,
        text_align=ft.TextAlign.CENTER,
    )

    dd_inversor = ft.Dropdown(
        label="IF",
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

    botao_aplicacao = ft.TextButton(
        text="Detalhes",
        width=90,
        height=32,
        disabled=True,
        on_click=abrir_aplicacao,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.ORANGE_800,
            color="#F7F8F3",
            shape=ft.RoundedRectangleBorder(radius=5),
        ),
    )

    botao_manual = ft.TextButton(
        text="Manual",
        width=90,
        height=32,
        disabled=True,
        visible=False,
        on_click=abrir_manual,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.ORANGE_800,
            color="#F7F8F3",
            shape=ft.RoundedRectangleBorder(radius=5),
        ),
    )

    # Coluna principal de resultado com scroll e expand
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

        observacoes_filtradas = [obs for obs in lista if str(obs).strip()]
        if not observacoes_filtradas:
            return

        resultado.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column(
                        [
                            ft.Text("OBSERVAÇÕES", size=18, weight=ft.FontWeight.BOLD),
                            *[ft.Text(f"• {obs}") for obs in observacoes_filtradas],
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
        nomes = [n for n in nomes if n != "manual_url"]
        dd_configuracao.options = [ft.dropdown.Option(nome) for nome in nomes]
        atualizar_linha_link()
        page.update()

    def ao_mudar_configuracao(e):
        atualizar_linha_link()

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
                ft.Text(
                    "Escolha uma Aplicação.",
                    color=ft.Colors.RED,
                    size=18,
                )
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

    dd_inversor.on_change = ao_mudar_inversor
    dd_configuracao.on_change = ao_mudar_configuracao
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
            [botao_aplicacao, botao_manual],
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

    # Rodapé com texto + contador centralizado
    rodape_texto = ft.Text(
        f"Metaltex – Ferramenta oficial de aplicações IF © 2026. "
        f"Todos os direitos reservados. Versão 1.0   "
        f"Acessos: {total_acessos if total_acessos is not None else '--'}",
        color=ft.Colors.WHITE,
        size=9,
        text_align=ft.TextAlign.CENTER,
    )

    rodape = ft.Container(
        expand=False,
        bgcolor=ft.Colors.ORANGE_800,
        padding=4,
        content=ft.Row(
            [rodape_texto],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    conteudo_app = ft.Container(
        width=400,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    [
                        imagem_topo,
                        dd_texto01,
                        linha_codigo,
                        area_resultado,
                        linha_link,
                    ],
                    spacing=0,
                    expand=True,
                ),
                rodape,
        ],
    ),
)
    def ajustar_layout(e=None):
        largura_disponivel = page.width or 400
        # mais flexível para celulares e PCs
        largura_final = max(largura_disponivel - 24, 260)
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
    atualizar_linha_link()


ft.app(target=main, assets_dir="assets")