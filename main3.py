import flet as ft
import json


# =====================================================
# CARREGA O JSON
# =====================================================

with open("configuracoes.json", "r", encoding="utf-8") as arquivo:
    CONFIGURACOES = json.load(arquivo)


# =====================================================
# APLICAÇÃO
# =====================================================

def main(page: ft.Page):

    page.title = "Configurador de Inversores"
    page.window_width = 1200
    page.window_height = 900
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT
    # -------------------------------------------------
    # TÍTULO
    # -------------------------------------------------

    titulo = ft.Text(
        "CONFIGURADOR DE INVERSORES",
        size=30,
        weight=ft.FontWeight.BOLD
    )

    # -------------------------------------------------
    # DROPDOWNS
    # -------------------------------------------------

    dd_inversor = ft.Dropdown(
        label="Modelo do Inversor",
        width=250
    )

    dd_config = ft.Dropdown(
        label="Tipo de Configuração",
        width=300
    )

    # -------------------------------------------------
    # DADOS MOTOR
    # -------------------------------------------------

    txt_kw = ft.TextField(
        label="Potência (kW)",
        width=180
    )

    txt_corrente = ft.TextField(
        label="Corrente (A)",
        width=180
    )

    txt_freq = ft.TextField(
        label="Frequência (Hz)",
        width=180
    )

    txt_rpm = ft.TextField(
        label="RPM",
        width=180
    )

    # -------------------------------------------------
    # ÁREA DE RESULTADO
    # -------------------------------------------------

    resultado = ft.Column(
        spacing=8,
        scroll=ft.ScrollMode.AUTO
    )

    # -------------------------------------------------
    # CARREGA INVERSORES
    # -------------------------------------------------

    for inversor in CONFIGURACOES.keys():
        dd_inversor.options.append(
            ft.dropdown.Option(inversor)
        )

    # -------------------------------------------------
    # TROCA INVERSOR
    # -------------------------------------------------

    def mudou_inversor(e):

        dd_config.options.clear()
        dd_config.value = None

        if dd_inversor.value:

            for configuracao in CONFIGURACOES[
                dd_inversor.value
            ].keys():

                dd_config.options.append(
                    ft.dropdown.Option(configuracao)
                )

        page.update()

    dd_inversor.on_change = mudou_inversor

    # -------------------------------------------------
    # GERA CONFIGURAÇÃO
    # -------------------------------------------------

    def gerar(e):

        resultado.controls.clear()

        if not dd_inversor.value:
            return

        if not dd_config.value:
            return

        dados = CONFIGURACOES[
            dd_inversor.value
        ][
            dd_config.value
        ]

        # ==========================================
        # CABEÇALHO
        # ==========================================

        resultado.controls.append(
            ft.Text(
                f"{dd_inversor.value} - {dd_config.value}",
                size=28,
                weight=ft.FontWeight.BOLD
            )
        )

        resultado.controls.append(ft.Divider())

        # ==========================================
        # PARÂMETROS
        # ==========================================

        resultado.controls.append(
            ft.Text(
                "PARÂMETROS",
                size=22,
                weight=ft.FontWeight.BOLD
            )
        )

        for parametro, valor in dados["parametros"]:

            resultado.controls.append(
                ft.Container(
                    content=ft.Text(
                        f"{parametro} = {valor}",
                        size=16
                    ),
                    padding=3
                )
            )

        # ==========================================
        # DADOS MOTOR
        # ==========================================

        if any([
            txt_kw.value,
            txt_corrente.value,
            txt_freq.value,
            txt_rpm.value
        ]):

            resultado.controls.append(ft.Divider())

            resultado.controls.append(
                ft.Text(
                    "DADOS DO MOTOR",
                    size=22,
                    weight=ft.FontWeight.BOLD
                )
            )

            if txt_kw.value:
                resultado.controls.append(
                    ft.Text(
                        f"P2.01 = {txt_kw.value} kW"
                    )
                )

            if txt_corrente.value:
                resultado.controls.append(
                    ft.Text(
                        f"P2.03 = {txt_corrente.value} A"
                    )
                )

            if txt_freq.value:
                resultado.controls.append(
                    ft.Text(
                        f"P2.04 = {txt_freq.value} Hz"
                    )
                )

            if txt_rpm.value:
                resultado.controls.append(
                    ft.Text(
                        f"P2.05 = {txt_rpm.value} RPM"
                    )
                )

        # ==========================================
        # LIGAÇÕES
        # ==========================================

        resultado.controls.append(ft.Divider())

        resultado.controls.append(
            ft.Text(
                "LIGAÇÕES",
                size=22,
                weight=ft.FontWeight.BOLD
            )
        )

        for terminal, descricao in dados["ligacoes"]:

            resultado.controls.append(
                ft.Text(
                    f"{terminal} → {descricao}",
                    size=16
                )
            )

        # ==========================================
        # OBSERVAÇÕES
        # ==========================================

        resultado.controls.append(ft.Divider())

        resultado.controls.append(
            ft.Text(
                "OBSERVAÇÕES",
                size=22,
                weight=ft.FontWeight.BOLD
            )
        )

        for obs in dados["observacoes"]:

            resultado.controls.append(
                ft.Text(
                    f"• {obs}",
                    size=16
                )
            )

        page.update()

    # -------------------------------------------------
    # BOTÃO
    # -------------------------------------------------

    btn_gerar = ft.ElevatedButton(
        text="GERAR CONFIGURAÇÃO",
        icon=ft.Icons.SETTINGS,
        height=50,
        on_click=gerar
    )

    # -------------------------------------------------
    # LAYOUT
    # -------------------------------------------------

    page.add(

        titulo,

        ft.Divider(),

        ft.Row(
            [
                dd_inversor,
                dd_config,
                btn_gerar
            ]
        ),

        ft.Divider(),

        ft.Text(
            "Dados do Motor (Opcional)",
            size=18,
            weight=ft.FontWeight.BOLD
        ),

        ft.Row(
            [
                txt_kw,
                txt_corrente,
                txt_freq,
                txt_rpm
            ]
        ),

        ft.Divider(),

        resultado
    )


# =====================================================
# INICIA APP
# =====================================================

ft.app(target=main)