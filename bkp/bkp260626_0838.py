import flet as ft
import json


# =====================================================
# CARREGA JSON
# =====================================================

with open("configuracoes.json", "r", encoding="utf-8") as arquivo:
    CONFIGURACOES = json.load(arquivo)


# =====================================================
# APP
# =====================================================

def main(page: ft.Page):

    page.title = "Configurador de Inversores"
    page.window_width = 900
    page.window_height = 900
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    # -----------------------------
    # UI
    # -----------------------------

    titulo = ft.Text(
        "CONFIGURADOR DE INVERSORES",
        size=30,
        weight=ft.FontWeight.BOLD
    )

    dd_inversor = ft.Dropdown(
        label="Modelo do Inversor",
        width=250
    )

    dd_config = ft.Dropdown(
        label="Configuração",
        width=300
    )

    btn = ft.ElevatedButton(
        "GERAR",
        icon=ft.Icons.SETTINGS
    )

    resultado = ft.Column(scroll=ft.ScrollMode.AUTO)

    # -----------------------------
    # CARREGA INVERSORES
    # -----------------------------

    for inv in CONFIGURACOES.keys():
        dd_inversor.options.append(ft.dropdown.Option(inv))

    # -----------------------------
    # TROCA INVERSOR
    # -----------------------------

    def mudou_inversor(e):
        dd_config.options.clear()
        dd_config.value = None

        if dd_inversor.value:
            for cfg in CONFIGURACOES[dd_inversor.value].keys():
                dd_config.options.append(ft.dropdown.Option(cfg))

        page.update()

    dd_inversor.on_change = mudou_inversor

    # -----------------------------
    # GERAR CONFIGURAÇÃO
    # -----------------------------

    def gerar(e):

        resultado.controls.clear()

        if not dd_inversor.value or not dd_config.value:
            return

        dados = CONFIGURACOES[dd_inversor.value][dd_config.value]

        # CABEÇALHO
        resultado.controls.append(
            ft.Text(
                f"{dd_inversor.value} - {dd_config.value}",
                size=28,
                weight=ft.FontWeight.BOLD
            )
        )

        resultado.controls.append(ft.Divider())

        # =================================================
        # LIGAÇÕES
        # =================================================

        resultado.controls.append(
            ft.Text("LIGAÇÕES", size=22, weight=ft.FontWeight.BOLD)
        )

        for item in dados.get("ligacoes", []):
            resultado.controls.append(
                ft.Text(f"{item[0]} → {item[1]}")
            )

        resultado.controls.append(ft.Divider())

        # =================================================
        # PARÂMETROS
        # =================================================

        resultado.controls.append(
            ft.Text("PARÂMETROS", size=22, weight=ft.FontWeight.BOLD)
        )

        for item in dados.get("parametros", []):
            resultado.controls.append(
                ft.Text(f"{item[0]} = {item[1]}")
            )

        resultado.controls.append(ft.Divider())

        # =================================================
        # MOTOR (AGORA NO JSON)
        # =================================================

        resultado.controls.append(
            ft.Text("MOTOR", size=22, weight=ft.FontWeight.BOLD)
        )

        for item in dados.get("motor", []):
            resultado.controls.append(
                ft.Text(f"{item[0]} = {item[1]}")
            )

        resultado.controls.append(ft.Divider())

        # =================================================
        # OBSERVAÇÕES
        # =================================================

        resultado.controls.append(
            ft.Text("OBSERVAÇÕES", size=22, weight=ft.FontWeight.BOLD)
        )

        for obs in dados.get("observacoes", []):
            resultado.controls.append(ft.Text(f"• {obs}"))

        page.update()

    btn.on_click = gerar

    # -----------------------------
    # LAYOUT
    # -----------------------------

    page.add(
        titulo,

        ft.Row([
            dd_inversor,
            dd_config,
            btn
        ]),

        ft.Divider(),

        resultado
    )


ft.app(target=main)
