import flet as ft

# --- Paleta Translúcida & Neón (Estilo Mago de Oz) ---
COLOR_OFF = "#3a2e2b20"       # Sepia translúcido (Píxel Apagado)
COLOR_ON = "#10b981"        # Verde Esmeralda Neón (Píxel Encendido)
BG_DARK = "#090d16"         # Fondo oscuro estilo noche mágica

def main(page: ft.Page):
    page.title = "Editor de Sprites 8-Bits | Mago de Oz Edition"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG_DARK
    page.window.width = 780
    page.window.height = 740
    page.window.resizable = False
    page.padding = 24

    pixel_states = [0] * 64
    pixel_buttons = []

    # Display del Hexadecimal
    hex_display = ft.Text(
        value="0000000000000000",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#34d399",
        selectable=True,
        font_family="Consolas"
    )

    # Input para cargar Hexadecimal
    hex_input = ft.TextField(
        label="Código Hexadecimal",
        hint_text="Ej: FFFFFFFFFFFFFFFF",
        max_length=16,
        width=280,
        text_style=ft.TextStyle(font_family="Consolas", color="#f0fdf4"),
        border_color="#059669",
        focused_border_color="#34d399"
    )

    status_text = ft.Text(value="", color="#f87171", size=12)

    # Lógica: Matriz -> Hexadecimal (Fase 3)
    def update_hex_from_grid():
        binary_str = "".join(str(bit) for bit in pixel_states)
        hex_val = hex(int(binary_str, 2))[2:].upper().zfill(16)
        hex_display.value = hex_val
        page.update()

    # Lógica: Clic en Píxel (Fase 2)
    def toggle_pixel(e):
        idx = e.control.data
        if pixel_states[idx] == 0:
            pixel_states[idx] = 1
            e.control.bgcolor = COLOR_ON
            e.control.scale = 1.12
            e.control.rotate = 0.05
        else:
            pixel_states[idx] = 0
            e.control.bgcolor = COLOR_OFF
            e.control.scale = 1.0
            e.control.rotate = 0.0
        
        update_hex_from_grid()

    # Lógica: Hexadecimal -> Matriz (Fase 4)
    def load_hex_to_grid(e):
        raw_hex = hex_input.value.strip()
        if not raw_hex:
            status_text.value = "Ingresa una cadena hexadecimal."
            page.update()
            return

        try:
            val = int(raw_hex, 16)
            binary_str = bin(val)[2:].zfill(64)
            
            if len(binary_str) > 64:
                status_text.value = "Excede los 64 bits de capacidad."
                page.update()
                return

            status_text.value = ""
            for i in range(64):
                bit = int(binary_str[i])
                pixel_states[i] = bit
                if bit == 1:
                    pixel_buttons[i].bgcolor = COLOR_ON
                    pixel_buttons[i].scale = 1.12
                else:
                    pixel_buttons[i].bgcolor = COLOR_OFF
                    pixel_buttons[i].scale = 1.0

            hex_display.value = raw_hex.upper().zfill(16)
            page.update()

        except ValueError:
            status_text.value = "Hexadecimal no válido (Use 0-9, A-F)."
            page.update()

    def clear_grid(e):
        for i in range(64):
            pixel_states[i] = 0
            pixel_buttons[i].bgcolor = COLOR_OFF
            pixel_buttons[i].scale = 1.0
            pixel_buttons[i].rotate = 0.0
        hex_input.value = ""
        status_text.value = ""
        update_hex_from_grid()

    # Grid de Píxeles
    grid = ft.GridView(
        expand=False,
        runs_count=8,
        max_extent=42,
        spacing=6,
        run_spacing=6,
        width=390,
        height=390
    )

    emerald_border = ft.Border(
        top=ft.BorderSide(1, "#059669"),
        bottom=ft.BorderSide(1, "#059669"),
        left=ft.BorderSide(1, "#059669"),
        right=ft.BorderSide(1, "#059669"),
    )

    glass_border = ft.Border(
        top=ft.BorderSide(1, "#10b98140"),
        bottom=ft.BorderSide(1, "#10b98140"),
        left=ft.BorderSide(1, "#10b98140"),
        right=ft.BorderSide(1, "#10b98140"),
    )

    for i in range(64):
        btn = ft.Container(
            content=None,
            width=40,
            height=40,
            bgcolor=COLOR_OFF,
            border_radius=8,
            border=glass_border,
            data=i,
            on_click=toggle_pixel,
            animate=ft.Animation(200, "easeInOut"),
            animate_scale=ft.Animation(200, "bounceOut"),
            animate_rotation=ft.Animation(200, "easeInOut")
        )
        pixel_buttons.append(btn)
        grid.controls.append(btn)

    # Botones de Acción
    btn_cargar = ft.FilledButton(
        "Cargar Hex",
        icon=ft.Icons.AUTO_AWESOME_ROUNDED,
        on_click=load_hex_to_grid,
        style=ft.ButtonStyle(bgcolor="#059669"),
        width=135
    )

    btn_limpiar = ft.OutlinedButton(
        "Limpiar",
        icon=ft.Icons.DELETE_OUTLINED,
        on_click=clear_grid,
        width=135
    )

    # Layout Principal Translúcido
    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.AUTO_AWESOME, color="#34d399", size=32),
                        ft.Text("ESMERALDA SPRITE EDITOR", size=24, weight=ft.FontWeight.BOLD, color="#f0fdf4")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(color="#05966940", height=20),
                
                ft.Row(
                    controls=[
                        # Matriz de Píxeles
                        ft.Container(
                            content=grid,
                            padding=16,
                            bgcolor="#1e293b50",
                            border_radius=16,
                            border=emerald_border
                        ),
                        
                        # Panel Lateral
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("CAMINO A OZ", size=12, weight=ft.FontWeight.BOLD, color="#f0fdf4"),
                                    ft.Divider(color="#05966940", height=10),
                                    
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text("VALOR HEXADECIMAL", size=9, weight=ft.FontWeight.BOLD, color="#a7f3d0"),
                                                hex_display,
                                            ],
                                            spacing=4
                                        ),
                                        bgcolor="#02061790",
                                        padding=12,
                                        border_radius=10,
                                        border=glass_border,
                                        width=280
                                    ),
                                    
                                    ft.Container(height=4),
                                    hex_input,
                                    status_text,
                                    
                                    ft.Row(
                                        controls=[btn_cargar, btn_limpiar],
                                        spacing=10
                                    )
                                ],
                                spacing=10
                            ),
                            padding=16,
                            bgcolor="#1e293b50",
                            border_radius=16,
                            border=emerald_border
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=20
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)

# --- LINEA OBLIGATORIA PARA RENDER / DESPLIEGUE WEB ---
app = ft.app(target=main, export_asgi=True)