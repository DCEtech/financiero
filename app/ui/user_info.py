import flet as ft
import threading
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from update import handle_event_insert, handle_event_get_data, handle_event_update_data, handle_event_del_data
from update import handle_event_del_user
from database import years_months_data
from flet_route import Params, Basket
from datetime import datetime

dialog = None
stop_refresh = False

def data_update(username, page):
    global year_select, month_select, stop_refresh
    last_years = None
    last_months = None

    print(last_months, last_years)

    def refresh():
        nonlocal last_years, last_months  

        while not stop_refresh:
            try:

                historical_data = years_months_data(username)

                new_years = [ft.dropdown.Option(str(year)) for year in historical_data.keys()]
                new_months = []

                if new_years:
                    default_year = int(new_years[0].key)
                    new_months = [ft.dropdown.Option(str(month)) for month in historical_data.get(default_year, [])]
                
                print(historical_data)

                if new_years != last_years or new_months != last_months:
                  
                    last_years = new_years
                    last_months = new_months

                    year_select.options = new_years
                    month_select.options = new_months

                    year_select.update()
                    month_select.update()
                print(year_select, month_select)
 
            except Exception as e:
                print(f"Error refreshing dropdowns: {e}")

            time.sleep(2)

    threading.Thread(target=refresh, daemon=True).start()   

def force_refresh_dropdowns(username):
    global year_select, month_select
    try:
        historical_data = years_months_data(username)
        new_years = [ft.dropdown.Option(str(year)) for year in historical_data.keys()]
        new_months = []

        if new_years:
            default_year = int(new_years[0].key)
            new_months = [ft.dropdown.Option(str(month)) for month in historical_data.get(default_year, [])]
        
        year_select.options = new_years
        month_select.options = new_months
        year_select.value = new_years[0].key if new_years else None

        year_select.update()
        month_select.update()

    except Exception as e:
        print(f"Error refreshing dropdowns: {e}")
             
def stop_data_update():
    global stop_refresh
    stop_refresh = True

def user_info(page: ft.Page, params: Params, basket: Basket):
    
    username = getattr(basket, "username", "Not found")
    
    global year_select, month_select

    date = datetime.now().strftime("%m-%Y")

    page.title = f"Financiero informacion del usuario {username}"  
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

    tittle_app = ft.Text(value=f"Informacion financiera de {username}", size=30, weight="bold")

    def handle_button_add_info(e):
        event = e.control.text.lower()
        ingresos = ingresos_field.value  
        gastos = gastos_field.value 
        ahorro = ahorro_field.value 
        result = handle_event_insert(event, username, ingresos, gastos, ahorro)

        if result.get("error"):
            add_result = result["error"]
            update_dialog(add_result)
        elif result.get("success"):
            add_result = result["success"]
            update_dialog(add_result)
            force_refresh_dropdowns(username)
            year_select.value = None
            year_select.value = None
            year_select.update()
            month_select.update()

    def update_months(selected_year):

        month_select.options.clear()
        selected_months = historical_data.get(selected_year, [])
        month_select.options.extend([ft.dropdown.Option(str(month)) for month in selected_months])
        month_select.update()
    
    def handle_button_click_get_data(e):
        event = e.control.text.lower()

        if not year_select.value and not month_select.value:
            update_dialog("Seleccione año y mes.")
        elif not year_select.value: 
            update_dialog("Seleccione un año.")
        elif not month_select.value:
            update_dialog("Seleccione un mes.")
        else:
            month = int(month_select.value)
            year = int(year_select.value)
            financial_data = handle_event_get_data(event, username, month, year)
            data = financial_data[0]
            print("financial_data:", data)
            ingresos_field.value = data.get("income")
            gastos_field.value = data.get("expenses")
            ahorro_field.value = data.get("savings")
            excedente_field.value = data.get("excedent")
            text_date.value = f"{month}-{year}"
            force_refresh_dropdowns(username)
            year_select.value = None
            month_select.value = None
            year_select.update()
            month_select.update()
            page.update()
    
    def handle_button_click_update_data(e):
        event = e.control.text.lower()
        
        if not year_select.value and not month_select.value:
            update_dialog("Seleccione año y mes.")
        elif not year_select.value: 
            update_dialog("Seleccione un año.")
        elif not month_select.value:
            update_dialog("Seleccione un mes.")

        ingresos = ingresos_field.value
        gastos = gastos_field.value
        ahorro = ahorro_field.value
        mes = int(month_select.value)
        año = int(year_select.value)
        result = handle_event_update_data(event, username, ingresos, ahorro, gastos, mes, año)
        text_date.value = f"{mes}-{año}"

        if result.get("error"):
            text_update = result["error"]
            update_dialog(text_update)
            
        elif result.get("success"):
            text_update = result["success"]
            ingresos_field.value = ""
            gastos_field.value = ""
            ahorro_field.value = ""
            excedente_field.value = ""
            year_select.value = None
            month_select.value = None
            year_select.update()
            month_select.update()
            update_dialog(text_update)
    
    def handle_button_click_del_data(e):
        event = e.control.text.lower()
        if not year_select.value and not month_select.value:
            update_dialog("Seleccione año y mes.")
        elif not year_select.value: 
            update_dialog("Seleccione un año.")
        elif not month_select.value:
            update_dialog("Seleccione un mes.")
        
        mes = int(month_select.value)
        año = int(year_select.value)
        text_date.value = f"{mes}-{año}"
        result = handle_event_del_data(event, username, mes, año)

        if result.get("error"):
            text_del = result["error"]
            update_dialog(text_del)

        elif result.get("success"):
            text_date.value = date
            text_del = result["success"]
            ingresos_field.value = ""
            gastos_field.value = ""
            ahorro_field.value = ""
            excedente_field.value = ""
            year_select.value = None
            month_select.value = None
            year_select.update()
            month_select.update()
            force_refresh_dropdowns(username)
            update_dialog(text_del) 
    
    def handle_button_click_del_user(e):
        event = e.control.text.lower()
        result = handle_event_del_user(event, username)
        if result.get("error"):
            text_del = result["error"]
            update_dialog(text_del)
        elif result.get("success"):
            text_del = result["success"]
            update_dialog(text_del)
            stop_data_update()
            page.go("/")
         
    def handle_button_login(e):
        stop_data_update()
        page.go("/")

    def handle_button_chart(e):
        stop_data_update()
        page.go("/login/chart")


    text_ingresos = ft.Text(value="Ingresos", size=20, weight="bold")
    ingresos_field = ft.TextField(hint_text="Introduzca ingresos", keyboard_type=ft.KeyboardType.TEXT,
    max_lines = 1, width=300, height=50, border_radius=10, content_padding=10)

    text_gastos = ft.Text(value="Gastos", size=20, weight="bold")
    gastos_field = ft.TextField(hint_text="Introduzca gastos", keyboard_type=ft.KeyboardType.TEXT,
    max_lines = 1, width=300, height=50, border_radius=10, content_padding=10)

    text_ahorro = ft.Text(value="Ahorro", size=20, weight="bold")
    ahorro_field = ft.TextField(hint_text="Introduzca ahorro", keyboard_type=ft.KeyboardType.TEXT,
    max_lines = 1, width=300, height=50, border_radius=10)

    text_excedente = ft.Text(value="Excedente", size=20, weight="bold")
    excedente_field = ft.TextField(hint_text="Excedente generado automaticamente", keyboard_type=ft.KeyboardType.TEXT,
    max_lines = 1, width=300, height=50, border_radius=10)

    chart_button = ft.Button("Grafico de ahorro", on_click = handle_button_chart)
    add_button = ft.Button(text="Añadir informacion", on_click = handle_button_add_info)
    data_button = ft.Button(text="Visualizar datos", on_click = handle_button_click_get_data)
    update_button = ft.Button(text="Actualizar datos", on_click = handle_button_click_update_data)
    del_button = ft.Button(text="Borrar datos", on_click = handle_button_click_del_data)

    exit_button = ft.ElevatedButton("Cerrar sesión", on_click = handle_button_login)
    delete_user_button = ft.ElevatedButton("Eliminar usuario", on_click = handle_button_click_del_user)

    
    historical_data = years_months_data(username)

    years = [ft.dropdown.Option(str(year)) for year in historical_data.keys()]
    months = []

    if years: 
        default_year = int(years[0].key)
        months = [ft.dropdown.Option(str(month)) for month in historical_data.get(default_year)]
    
    text_year = ft.Text(value = "Año", size=20, weight="bold")
    year_select = ft.Dropdown(
    width=100,
    options=years,
    on_change=lambda e: update_months(int(e.control.value)))
    
    text_month = ft.Text (value = "Mes", size=20, weight="bold")
    month_select = ft.Dropdown(
    width=100,
    options=months)

    data_update(username, page)
    
    text_date = ft.Text(value=date, size=30, weight="bold")

    content = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [exit_button, delete_user_button],
                    alignment="start",  
                    vertical_alignment="center"
                ),
                ft.Container(
                    content=tittle_app,
                    padding=ft.padding.only(bottom=40)
                ),
                ft.Row(
                    [text_date],
                    alignment="center",
                    vertical_alignment="center",
                    spacing=60
                ),
                ft.Row(
                    [text_ingresos, ingresos_field],
                    alignment="center",
                    vertical_alignment="center",
                    spacing=64,
                    wrap=True
                ),
                ft.Row(
                    [text_gastos, gastos_field],
                    alignment="center",
                    vertical_alignment="center",
                    spacing=80,
                    wrap=True
                ),
                ft.Row(
                    [text_ahorro, ahorro_field],
                    alignment="center",
                    vertical_alignment="center",
                    spacing=77,
                    wrap=True
                ),
                ft.Row(
                    [text_excedente, excedente_field],
                    alignment="center",
                    vertical_alignment="center",
                    spacing=50,
                    wrap=True
                ),
                ft.Row(
                    [text_month, month_select, text_year, year_select, data_button, update_button, del_button],
                    alignment="center",
                    vertical_alignment="center",
                    spacing=20,
                    wrap=True 
                ),
                ft.Row(
                    [add_button, chart_button], 
                    alignment="center",
                    vertical_alignment="center",
                    spacing=20
                ),
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


    return ft.View("/user_info", controls = [content])

