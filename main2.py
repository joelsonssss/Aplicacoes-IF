import flet as ft

# =====================================================
# BANCO DE CONFIGURAÇÕES
# =====================================================

CONFIGURACOES = {

    "IF10": {

        "3 FIOS": {

            "parametros": [
                ["P101", "3"],
                ["P102", "1"],
                ["P317", "8"],
                ["P329", "2"],
            ],

            "ligacoes": [
                ["FWD", "Botão Liga NO"],
                ["S1", "Botão Desliga NC"],
                ["REV", "Botão Reversão NO (Opcional)"],
            ],

            "observacoes": [
                "Botão Liga NO ligado no borne FWD",
                "Botão Desliga NC ligado no borne S1",
                "Botão Reversão NO ligado no borne REV (Opcional)"
            ]
        }
    },

    "IF20": {

        "3 FIOS": {

            "parametros": [
                ["P5.11", "2"],
                ["P5.00", "1"],
                ["P5.01", "2"],
                ["P5.02", "3"],
            ],

            "ligacoes": [
                ["FWD + GND", "Botão Liga NA"],
                ["S1 + GND", "Botão Desliga NF"],
            ],

            "observacoes": [
                "FWD + GND = Botão Liga NA",
                "S1 + GND = Botão Desliga NF"
            ]
        },

        "UP / DOWN": {

            "parametros": [
                ["P0.02", "1"],
                ["P0.04", "1"],
                ["P0.10", "Valor Hz Inicial"],
                ["P0.23", "1"],
                ["P5.00", "1"],
                ["P5.01", "2"],
                ["P5.02", "6"],
                ["P5.03", "7"],
                ["P5.12", "Pulso em Hz"],
            ],

            "ligacoes": [
                ["FWD + GND", "Botão Liga"],
                ["REV + GND", "Botão Reversão"],
                ["S1 + GND", "Mais Velocidade"],
                ["S2 + GND", "Menos Velocidade"],
            ],

            "observacoes": [
                "S1 incrementa velocidade",
                "S2 decrementa velocidade",
                "Definir frequência inicial em P0.10"
            ]
        }
    },

    "IF30": {
        "3 FIOS": {

            "parametros": [
                ["EXEMPLO", "0"]
            ],

            "ligacoes": [
                ["EXEMPLO", "CONFIGURAR"]
            ],

            "observacoes": [
                "Adicionar parâmetros do IF30"
            ]
        }
    }
}


# =====================================================
# FUNÇÃO PRINCIPAL
# =====================================================

def main(page: ft.Page):

    page.title = "Gerador de Configuração de Inversores"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1300
    page.window_height = 900
    page.scroll = ft.ScrollMode.AUTO

    titulo = ft.Text(
        "GERADOR DE CONFIGURAÇÃO DE INVERSORES",
        size=28,
        weight=ft.FontWeight.BOLD
    )

    subtitulo = ft.Text(
        "Selecione o modelo e a configuração desejada."
    )

    resultado_titulo = ft.Text(
        "",
        size=22,
        weight=ft.FontWeight.BOLD
    )

    # ==================================
    # DROPDOWN INVERSOR
    # ==================================

    dd_inversor = ft.Dropdown(
        width=250,
        label="Modelo do Inversor",
        options=[
            ft.dropdown.Option("IF10"),
            ft.dropdown.Option("IF20"),
            ft.dropdown.Option("IF30"),
        ]
    )

    # ==================================
    # DROPDOWN CONFIGURAÇÃO
    # ==================================

    dd_configuracao = ft.Dropdown(
        width=300,
        label="Tipo de Configuração",
        options=[]
    )

    # ==================================
    # TABELA PARÂMETROS
    # ==================================

    tabela_parametros = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Parâmetro")),
            ft.DataColumn(ft.Text("Valor")),
        ],
        rows=[]
    )

    # ==================================
    # TABELA LIGAÇÕES
    # ==================================

    tabela_ligacoes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Terminal")),
            ft.DataColumn(ft.Text("Descrição")),
        ],
        rows=[]
    )

    # ==================================
    # OBSERVAÇÕES
    # ==================================

    lista_observacoes = ft.Column()

    # ==================================
    # AO TROCAR INVERSOR
    # ==================================

    def atualizar_configuracoes(e):

        dd_configuracao.options.clear()

        if dd_inversor.value:

            configs = CONFIGURACOES[dd_inversor.value]

            for nome in configs.keys():
                dd_configuracao.options.append(
                    ft.dropdown.Option(nome)
                )

        dd_configuracao.value = None

        page.update()

    dd_inversor.on_change = atualizar_configuracoes

    # ==================================
    # GERAR CONFIGURAÇÃO
    # ==================================

    def gerar_configuracao(e):

        tabela_parametros.rows.clear()
        tabela_ligacoes.rows.clear()
        lista_observacoes.controls.clear()

        if not dd_inversor.value:
            return

        if not dd_configuracao.value:
            return

        dados = CONFIGURACOES[
            dd_inversor.value
        ][
            dd_configuracao.value
        ]

        resultado_titulo.value = (
            f"{dd_inversor.value} - {dd_configuracao.value}"
        )

        # parâmetros

        for parametro, valor in dados["parametros"]:

            tabela_parametros.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(parametro)),
                        ft.DataCell(ft.Text(valor)),
                    ]
                )
            )

        # ligações

        for terminal, descricao in dados["ligacoes"]:

            tabela_ligacoes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(terminal)),
                        ft.DataCell(ft.Text(descricao)),
                    ]
                )
            )

        # observações

        for obs in dados["observacoes"]:

            lista_observacoes.controls.append(
                ft.Text(f"• {obs}")
            )

        page.update()

    # ==================================
    # BOTÃO
    # ==================================

    btn_gerar = ft.ElevatedButton(
        text="GERAR CONFIGURAÇÃO",
        icon=ft.Icons.SETTINGS,
        height=50,
        on_click=gerar_configuracao
    )

    # ==================================
    # LAYOUT
    # ==================================

    page.add(

        titulo,
        subtitulo,

        ft.Divider(),

        ft.Row(
            [
                dd_inversor,
                dd_configuracao,
                btn_gerar,
            ]
        ),

        ft.Divider(),

        resultado_titulo,

        ft.Text(
            "PARÂMETROS",
            size=20,
            weight=ft.FontWeight.BOLD
        ),

        tabela_parametros,

        ft.Divider(),

        ft.Text(
            "LIGAÇÕES",
            size=20,
            weight=ft.FontWeight.BOLD
        ),

        tabela_ligacoes,

        ft.Divider(),

        ft.Text(
            "OBSERVAÇÕES",
            size=20,
            weight=ft.FontWeight.BOLD
        ),

        lista_observacoes,
    )


ft.app(target=main)