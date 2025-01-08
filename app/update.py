from database import create_user, authentication_user, insert_financial_data, update_financial_data
from database import delete_financial_data, data_info, delete_user 

def handle_event_login(event, username, password):
    if event.lower() == "iniciar sesión":
        result = authentication_user(username, password)
        return result
    elif event.lower() == "registrarse":
        result = create_user(username, password)
        return result

def handle_event_insert(event, username, ingresos, ahorro, gastos):
    if event.lower() == "añadir informacion":

        gastos = gastos if gastos else 0.00
        ahorro = ahorro if ahorro else 0.00

        result = insert_financial_data(username, ingresos, gastos, ahorro)
    return result 

def handle_event_get_data(event, username, month, year):
    if event.lower() == "visualizar datos":
        result = data_info(username, month, year)
        return result

def handle_event_update_data(event, username, income, savings, expenses, month, year):
    if event.lower() == "actualizar datos":

        expenses = expenses if expenses else 0.00
        savings = savings if savings else 0.00
        expenses = expenses if expenses else 0.00
        
        result = update_financial_data(username, income, savings, expenses, month, year)
    return result

def handle_event_del_data(event, username, month, year):
    if event.lower() == "borrar datos":
        result = delete_financial_data(username, month, year)
    return result

def handle_event_del_user(event, username):
    if event.lower() == "eliminar usuario":
        result = delete_user(username)
    return result