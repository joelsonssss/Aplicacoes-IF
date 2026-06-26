import flet as ft
import json
import os

# =====================================================
# JSON
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CONFIG = os.path.join(BASE_DIR, "configuracoes.json")


def carregar_configuracoes():
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Erro ao carregar JSON:", e)
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

    titulo = ft.Text(
        "CONFIGURADOR DE INVERSORES",
        size=28,
        weight=ft.FontWeight.BOLD,
    )

    # ----------------------------
    # DROPDOWNS
    # ----------------------------

    dd_inversor = ft.Dropdown(
        label="Modelo do Inversor",
        width=260,
    )

    dd_config = ft.Dropdown(
        label="Configuração",
        width=320,
    )

    btn = ft.ElevatedButton("GERAR")

    resultado = ft.Column(scroll=ft.ScrollMode.AUTO)

    # =====================================================
    # CARREGA INVERSORES
    # =====================================================

    for inv in CONFIGURACOES.keys():
        dd_inversor.options.append(ft.dropdown.Option(inv))

    # =====================================================
    # AO MUDAR INVERSOR
    # =====================================================

    def mudou_inversor(e):
        dd_config.options.clear()
        dd_config.value = None

        inv = dd_inversor.value

        if inv in CONFIGURACOES:
            for cfg in CONFIGURACOES[inv].keys():
                # 🔥 IMPORTANTE: value = cfg (garante chave correta)
                dd_config.options.append(
                    ft.dropdown.Option(text=cfg, key=cfg)
                )

        page.update()

    dd_inversor.on_change = mudou_inversor

    # =====================================================
    # FUNÇÕES UI
    # =====================================================

    def secao(titulo, itens, simbolo="="):
        if not itens:
            return

        resultado.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column(
                        [
                            ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
                            *[
                                ft.Text(f"{i[0]} {simbolo} {i[1]}")
                                for i in itens
                            ],
                        ]
                    ),
                )
            )
        )

    def obs(lista):
        if not lista:
            return

        resultado.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column(
                        [
                            ft.Text("OBSERVAÇÕES", size=18, weight=ft.FontWeight.BOLD),
                            *[ft.Text("• " + o) for o in lista],
                        ]
                    ),
                )
            )
        )

    # =====================================================
    # GERAR
    # =====================================================

    def gerar(e):
        resultado.controls.clear()

        inv = dd_inversor.value
        cfg = dd_config.value

        # ----------------------------
        # VALIDAÇÕES
        # ----------------------------

        if not CONFIGURACOES:
            resultado.controls.append(ft.Text("JSON não carregado!", color="red"))
            page.update()
            return

        if not inv:
            resultado.controls.append(ft.Text("Selecione o inversor!", color="red"))
            page.update()
            return

        if not cfg:
            resultado.controls.append(ft.Text("Selecione a configuração!", color="red"))
            page.update()
            return

        # ----------------------------
        # PEGAR DADOS COM SEGURANÇA
        # ----------------------------

        dados = CONFIGURACOES.get(inv, {}).get(cfg)

        if not dados:
            resultado.controls.append(
                ft.Text("Configuração não encontrada no JSON!", color="red")
            )
            page.update()
            return

        # ----------------------------
        # TÍTULO
        # ----------------------------

        resultado.controls.append(
            ft.Text(f"{inv} - {cfg}", size=24, weight=ft.FontWeight.BOLD)
        )

        resultado.controls.append(ft.Divider())

        # ----------------------------
        # SEÇÕES
        # ----------------------------

        secao("LIGAÇÕES", dados.get("ligacoes", []), "→")
        secao("PARÂMETROS", dados.get("parametros", []))
        secao("MOTOR", dados.get("motor", []))

        obs(dados.get("observacoes", []))

        page.update()

    btn.on_click = gerar

    # =====================================================
    # UI
    # =====================================================

    page.add(
        titulo,
        ft.Row([dd_inversor, dd_config, btn]),
        ft.Divider(),
        resultado,
    )


ft.app(target=main)