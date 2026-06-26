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
            return json.load(arquivo)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {ARQUIVO_CONFIG}")
        return {}
    except json.JSONDecodeError:
        print(f"Erro ao ler JSON: {ARQUIVO_CONFIG}")
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

    titulo = ft.Text(
        "CONFIGURADOR DE INVERSORES",
        size=30,
        weight=ft.FontWeight.BOLD,
    )

    dd_inversor = ft.Dropdown(
        label="Modelo do Inversor",
        width=260,
        enable_filter=True,
    )

    dd_config = ft.Dropdown(
        label="Configuração",
        width=320,
        enable_filter=True,
    )

    btn = ft.ElevatedButton(
        "GERAR",
        icon=ft.Icons.SETTINGS,
    )

    resultado = ft.Column(
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
    )

    for inv in sorted(CONFIGURACOES.keys()):
        dd_inversor.options.append(ft.dropdown.Option(inv))

    def adicionar_secao(titulo_secao, itens, separador="="):
        if not itens:
            return

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
                            *[
                                ft.Text(f"{item[0]} {separador} {item[1]}")
                                for item in itens
                            ],
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
                            *[
                                ft.Text(f"• {obs}")
                                for obs in lista
                            ],
                        ]
                    ),
                )
            )
        )

    def mudou_inversor(e):
        dd_config.options.clear()
        dd_config.value = None

        if dd_inversor.value and dd_inversor.value in CONFIGURACOES:
            for cfg in CONFIGURACOES[dd_inversor.value].keys():
                dd_config.options.append(ft.dropdown.Option(cfg))

        page.update()

    dd_inversor.on_change = mudou_inversor

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

        dados = CONFIGURACOES[dd_inversor.value][dd_config.value]

        resultado.controls.append(
            ft.Text(
                f"{dd_inversor.value} - {dd_config.value}",
                size=28,
                weight=ft.FontWeight.BOLD,
            )
        )

        resultado.controls.append(ft.Divider())

        adicionar_secao(
            "LIGAÇÕES",
            dados.get("ligacoes", []),
            "→",
        )

        adicionar_secao(
            "PARÂMETROS",
            dados.get("parametros", []),
            "=",
        )

        adicionar_secao(
            "MOTOR",
            dados.get("motor", []),
            "=",
        )

        adicionar_observacoes(
            dados.get("observacoes", [])
        )

        page.update()

    btn.on_click = gerar

    page.add(
        titulo,
        ft.Row(
            [
                dd_inversor,
                dd_config,
                btn,
            ]
        ),
        ft.Divider(),
        resultado,
    )

ft.app(target=main)