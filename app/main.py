import flet as ft
from flet_route import Routing, path
from ui import login, user_info, chart

def main(page: ft.Page):

    app_routes = [
        path(url = "/", clear = True, view = login),
        path(url = "/login/user_info", clear = True, view = user_info),
        path(url = "/login/chart", clear = True, view = chart)
    ]

    Routing(page = page, app_routes= app_routes)

    page.go(page.route)

ft.app(target=main)