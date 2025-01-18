import flet as ft
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from update import handle_event_login
from flet_route import Params, Basket
import threading

dialog = None

def login(page: ft.Page, params: Params, basket: Basket): 
   
    page.title = "Financiero Login"  
    page.scroll = "adaptive"

    def close_dialog():
        if dialog:
            dialog.open = False
        page.update()

    def update_dialog(text):
        global dialog 
        if dialog: 
            dialog.open = False 
        dialog = ft.AlertDialog(title=ft.Text(text))
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        threading.Timer(2, close_dialog).start()

    def handle_button_login(e):
        event = e.control.text.lower()
        username = login_field.value
        password = password_field.value

        result = handle_event_login(event, username, password)

        if result.get("error"):
            login_success = result["error"]
            update_dialog(login_success)
            page.update()
        elif result.get("success"):  
            basket.username = username
            login_success = result["success"]
            update_dialog(login_success)
            page.go("/login/user_info")

    def handle_button_create_user(e):
        event = e.control.text.lower()
        username = login_field.value
        password = password_field.value

        result = handle_event_login(event, username, password)

        if result.get("error"):
            login_success = result["error"]
            update_dialog(login_success)
            page.update()
        elif result.get("success"):  
            login_success = result["success"]
            update_dialog(login_success)

            
    tittle_app = ft.Text(value="Financiero", size=30, weight="bold")
 
    text_login = ft.Text(value="Usuario", size=20, weight="bold")
    login_field = ft.TextField(hint_text="Ingrese su usuario", keyboard_type=ft.KeyboardType.TEXT,
    max_lines = 1, width=300, height=50, border_radius=10, content_padding=10)

    text_password = ft.Text(value="Contraseña", size=20, weight="bold")
    password_field = ft.TextField(hint_text="Ingrese su contraseña", password=True, keyboard_type=ft.KeyboardType.TEXT,
    max_lines = 1, width=300, height=50, border_radius=10, content_padding=10) 

    login_button = ft.Button(text="Iniciar sesión", on_click=handle_button_login)
    register_button = ft.Button(text="Registrarse", on_click=handle_button_create_user)

    login_advice = ft.Text(value="Si no está registrado, introduzca un usuario y contraseña para añadir sus datos al sistema.", size=14) 

    content =  ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=tittle_app,
                    padding=ft.padding.only(bottom=40),
                ),
                ft.Row(
                    [text_login, login_field],
                    alignment="center",
                    vertical_alignment="center",
                    spacing=50,
                    wrap=True
                ),
                ft.Row(
                    [text_password, password_field],
                    alignment="center",
                    vertical_alignment="center",
                    spacing=15,
                    wrap=True
                ),
                login_button,
                register_button,
                login_advice
            ],
            alignment="center",  
            horizontal_alignment="center",  
            spacing=20,
            scroll="adaptive"
        ),
        padding=ft.padding.only(top=100, left=20, right=20),  
        alignment=ft.alignment.center,  
        expand=True
    )
    
    return ft.View("/", controls=[content])