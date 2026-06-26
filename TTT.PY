def main(page: ft.Page):
    page.title = "Metaltex - Guia de Seleção Inversor"
    page.window_width = 720
    page.window_top = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_maximizable = False
    page.scroll = ft.ScrollMode.AUTO

    resultado = ft.Text(
        size=20,
        color="#0A2D42",
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )
    resultado2 = ft.Text(size=13, color="black", text_align=ft.TextAlign.CENTER)
    resultado3 = ft.Text(size=11, color="red", text_align=ft.TextAlign.CENTER)
    resultado4 = ft.Text(size=11, color="black", text_align=ft.TextAlign.CENTER)
    resultado5 = ft.Text(size=11, color="black", text_align=ft.TextAlign.CENTER)
    resultado7 = ft.Text(size=12, color="red", text_align=ft.TextAlign.CENTER)