import flet as ft
import json
import os

# =====================================================
# CAMINHO DO JSON
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CONFIG = os.path.join(BASE_DIR, "configuracoes.json")

# =====================================================
# CARREGA JSON
# =====================================================
def carregar_configuracoes():
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, dict):
            print(f"JSON inválido: esperado dicionário em {ARQUIVO_CONFIG}")
            return {}

        print(f"JSON carregado com sucesso: {ARQUIVO_CONFIG}")
        print(f"Modelos encontrados: {list(dados.keys())}")
        return dados

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {ARQUIVO_CONFIG}")
        return {}

    except json.JSONDecodeError as e:
        print(f"Erro ao ler JSON: {ARQUIVO_CONFIG} | {e}")
        return {}

    except Exception as e:
        print(f"Erro inesperado ao carregar configurações: {e}")
        return {}


CONFIGURACOES = carregar_configuracoes()

# =====================================================
# APP
# =====================================================
def main(page: ft.Page):
    page.title = "Configurador de Inversores"
    page.window_width = 900
    page.window_height = 900
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    titulo = ft.Text(
        "CONFIGURADOR DE INVERSORES",
        size=30,
        weight=ft.FontWeight.BOLD,
    )

    info_arquivo = ft.Text(
        f"Arquivo JSON: {ARQUIVO_CONFIG}",
        size=12,
        color=ft.Colors.GREY_700,
    )

    dd_inversor = ft.Dropdown(
        label="Modelo do Inversor",
        width=260,
        options=[ft.dropdown.Option(inv) for inv in sorted(CONFIGURACOES.keys())],
    )

    dd_config = ft.Dropdown(
        label="Configuração",
        width=320,
        options=[],
    )

    btn = ft.ElevatedButton(
        "GERAR",
        icon=ft.Icons.SETTINGS,
    )

    resultado = ft.Column(
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def adicionar_secao(titulo_secao, itens, separador="="):
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
                            ft.Text(
                                titulo_secao,
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
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
                            ft.Text(
                                "OBSERVAÇÕES",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            *[ft.Text(f"• {obs}") for obs in lista],
                        ]
                    ),
                )
            )
        )

    # =====================================================
    # QUANDO ESCOLHE O INVERSOR
    # =====================================================
    def mudou_inversor(e):
        dd_config.value = None
        dd_config.options = []
        resultado.controls.clear()

        inversor_escolhido = dd_inversor.value
        print(f"Inversor escolhido: {inversor_escolhido}")

        if not inversor_escolhido:
            resultado.controls.append(
                ft.Text("Selecione um modelo de inversor.")
            )
            page.update()
            return

        grupo = CONFIGURACOES.get(inversor_escolhido, {})

        if not isinstance(grupo, dict):
            resultado.controls.append(
                ft.Text(
                    "Estrutura inválida para o inversor selecionado.",
                    color=ft.Colors.RED,
                )
            )
            page.update()
            return

        lista_cfg = list(grupo.keys())
        print(f"Configurações encontradas para {inversor_escolhido}: {lista_cfg}")

        dd_config.options = [ft.dropdown.Option(cfg) for cfg in lista_cfg]

        if lista_cfg:
            resultado.controls.append(
                ft.Text(
                    f"Configurações carregadas: {', '.join(lista_cfg)}",
                    color=ft.Colors.GREEN,
                )
            )
        else:
            resultado.controls.append(
                ft.Text(
                    "Nenhuma configuração encontrada para esse inversor.",
                    color=ft.Colors.RED,
                )
            )

        page.update()

    dd_inversor.on_change = mudou_inversor

    # =====================================================
    # GERAR
    # =====================================================
    def gerar(e):
        resultado.controls.clear()

        if not CONFIGURACOES:
            resultado.controls.append(
                ft.Text(
                    "Nenhuma configuração foi carregada do arquivo JSON.",
                    color=ft.Colors.RED,
                )
            )
            page.update()
            return

        if not dd_inversor.value:
            resultado.controls.append(
                ft.Text(
                    "Selecione um modelo de inversor.",
                    color=ft.Colors.RED,
                )
            )
            page.update()
            return

        if not dd_config.value:
            resultado.controls.append(
                ft.Text(
                    "Selecione uma configuração.",
                    color=ft.Colors.RED,
                )
            )
            page.update()
            return

        grupo = CONFIGURACOES.get(dd_inversor.value, {})
        if not isinstance(grupo, dict):
            resultado.controls.append(
                ft.Text(
                    "Estrutura inválida no JSON para o modelo selecionado.",
                    color=ft.Colors.RED,
                )
            )
            page.update()
            return

        dados = grupo.get(dd_config.value)
        if not isinstance(dados, dict):
            resultado.controls.append(
                ft.Text(
                    "Configuração não encontrada ou inválida.",
                    color=ft.Colors.RED,
                )
            )
            page.update()
            return

        resultado.controls.append(
            ft.Text(
                f"{dd_inversor.value} - {dd_config.value}",
                size=28,
                weight=ft.FontWeight.BOLD,
            )
        )

        resultado.controls.append(ft.Divider())

        adicionar_secao("LIGAÇÕES", dados.get("ligacoes", []), "→")
        adicionar_secao("PARÂMETROS", dados.get("parametros", []), "=")
        adicionar_secao("MOTOR", dados.get("motor", []), "=")
        adicionar_observacoes(dados.get("observacoes", []))

        if not any([
            dados.get("ligacoes"),
            dados.get("parametros"),
            dados.get("motor"),
            dados.get("observacoes"),
        ]):
            resultado.controls.append(
                ft.Text(
                    "A configuração foi encontrada, mas está sem dados para exibir.",
                    color=ft.Colors.ORANGE,
                )
            )

        page.update()

    btn.on_click = gerar

    page.add(
        titulo,
        info_arquivo,
        ft.Row(
            [
                dd_inversor,
                dd_config,
                btn,
            ],
            wrap=True,
        ),
        ft.Divider(),
        resultado,
    )

ft.app(target=main)