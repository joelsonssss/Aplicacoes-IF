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

        # Garante que o JSON carregado seja um dicionário
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
    page.window_width = 500
    page.window_height = 700
    page.padding = 0
    page.spacing = 0

    # Armazena o link atualmente selecionado
    # Foi usado um dicionário para poder alterar o valor dentro das funções internas
    link_atual = {"url": ""}

    def obter_link_configuracao():
        """
        Retorna o link da configuração selecionada no momento.

        Fluxo:
        - Verifica se há um inversor e uma configuração escolhidos.
        - Busca os dados no dicionário CONFIGURACOES.
        - Se existir um campo 'link', retorna esse valor.
        - Caso contrário, retorna string vazia.
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

        Se houver link:
        - mostra a URL em azul
        - habilita o botão para abrir o link

        Se não houver link:
        - mostra mensagem padrão
        - desabilita o botão
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

    # Imagem de topo da aplicação
    imagem_topo = ft.Container(
        alignment=ft.alignment.bottom_left,
        content=ft.Image(
            src="images/topo01.png",
            height=70,
            fit=ft.ImageFit.COVER,
        ),
    )

    # Dropdown para selecionar o modelo do inversor
    # As opções são montadas com base nas chaves do JSON carregado
    dd_inversor = ft.Dropdown(
        label="Modelo do Inversor",
        width=220,
        dense=True,
        content_padding=ft.padding.symmetric(vertical=6, horizontal=12),
        text_style=ft.TextStyle(size=14),
        label_style=ft.TextStyle(size=14),
        options=[ft.dropdown.Option(nome) for nome in sorted(CONFIGURACOES.keys())],
    )

    # Dropdown para selecionar o tipo de configuração
    # Inicialmente vazio, pois depende do inversor escolhido
    dd_configuracao = ft.Dropdown(
        label="Configuração",
        width=260,
        options=[],
    )

    # Botão que dispara a exibição da configuração selecionada
    botao_mostrar = ft.ElevatedButton(
        text="Mostrar",
        icon=ft.Icons.SEARCH,
    )

    # Texto que mostra o link da aplicação/desenho
    texto_link = ft.Text(
        "Nenhum link disponível para esta configuração.",
        selectable=True,
        color=ft.Colors.GREY_700,
        size=14,
    )

    def abrir_link(e):
        """
        Abre o link atual no navegador, se houver URL válida.
        """
        if link_atual["url"]:
            page.launch_url(link_atual["url"])

    # Botão para abrir o link da configuração
    botao_abrir_link = ft.TextButton(
        text="abrir link",
        on_click=abrir_link,
        disabled=True,
    )

    # Coluna onde serão exibidos os resultados da configuração escolhida
    resultado = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def adicionar_secao(titulo, itens, separador="="):
        """
        Adiciona uma seção formatada na área de resultados.

        Parâmetros:
        - titulo: nome da seção que aparecerá no card
        - itens: lista de itens da seção
        - separador: símbolo usado entre campo e valor

        Comportamento:
        - Se o item for lista/tupla com dois elementos, exibe como:
          campo separador valor
        - Caso contrário, exibe o item como texto simples
        """
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
        """
        Adiciona um card específico para observações.

        Cada observação é exibida com marcador '•'.
        """
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
        """
        Evento executado quando o usuário troca o modelo do inversor.

        Ações:
        - limpa a configuração anterior
        - limpa a área de resultados
        - busca as configurações do inversor selecionado
        - preenche o dropdown de configuração
        - atualiza a linha do link
        """
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
        """
        Evento executado quando o usuário troca a configuração.

        Aqui a função apenas atualiza a área do link,
        pois o conteúdo detalhado só será mostrado ao clicar em 'Mostrar'.
        """
        atualizar_linha_link()

    # Associa os eventos aos dropdowns
    dd_inversor.on_change = ao_mudar_inversor
    dd_configuracao.on_change = ao_mudar_configuracao

    def mostrar_configuracao(e):
        """
        Exibe na tela os dados da configuração selecionada.

        Validações:
        - exige que o modelo do inversor esteja selecionado
        - exige que a configuração esteja selecionada
        - verifica se os dados da configuração são válidos

        Se estiver tudo certo:
        - mostra título
        - mostra seções de ligações, parâmetros, motor e observações
        - atualiza a linha do link
        """
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

        # Título principal do resultado
        resultado.controls.append(
            ft.Text(
                f"{dd_inversor.value} - {dd_configuracao.value}",
                size=24,
                weight=ft.FontWeight.BOLD,
            )
        )
        resultado.controls.append(ft.Divider())

        # Monta as seções de acordo com as chaves do JSON
        adicionar_secao("LIGAÇÕES", dados.get("ligacoes", []), "→")
        adicionar_secao("PARÂMETROS", dados.get("parametros", []), "=")
        adicionar_secao("MOTOR", dados.get("motor", []), "=")
        adicionar_observacoes(dados.get("observacoes", []))

        atualizar_linha_link()
        page.update()

    # Associa o botão Mostrar à função de exibição
    botao_mostrar.on_click = mostrar_configuracao

    # Linha com os controles de seleção
    linha_codigo = ft.Container(
        padding=15,
        alignment=ft.alignment.center,
        content=ft.Row(
            [dd_inversor, dd_configuracao, botao_mostrar],
            wrap=True,
            spacing=15,
        ),
    )

    # Linha que mostra o link da aplicação/desenho
    linha_link = ft.Container(
        padding=15,
        alignment=ft.alignment.center,
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

    # Área principal onde os resultados aparecem
    area_resultado = ft.Container(
        expand=True,
        padding=15,
        alignment=ft.alignment.center,
        content=resultado,
    )

    # Rodapé da aplicação
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

    # Monta a página final na ordem visual
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


# Inicia a aplicação Flet chamando a função principal
ft.app(target=main)