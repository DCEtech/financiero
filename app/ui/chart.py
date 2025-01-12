import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from database import current_savings 
from flet_route import Params, Basket

def chart(page: ft.Page, params: Params, basket: Basket):

    username = getattr(basket, "username", "Not found")

    page.title = f"Financiero gráfico histórico de ahorro del usuario {username}"
    page.scroll = "adaptive"

    user_info_button = ft.ElevatedButton("Volver a información de usuario", on_click=lambda _: page.go("/login/user_info"))
    
    years_months = {}
    savings = []

    savings, years_months = current_savings(username)

    print(savings)
    print(years_months)

    ahorro_total = savings[-1] if savings else 0

    tittle_app = ft.Text(value=f"Gráfico de ahorro acumulado {ahorro_total:.2f} €", size=40, weight="bold")

    x_labels = []
    for year, months in years_months.items():
        for month in months:
            x_labels.append(f"{month}/{year}")
    
    print(x_labels)
    print(savings)
    
    fig, ax = plt.subplots(figsize = (12, 6))
    fig.patch.set_facecolor("#212121")  
    ax.set_facecolor("#212121")
    ax.plot(x_labels, savings, marker='o', linestyle='-', color='lime')

    ax.set_xlabel("Mes/Año", fontsize=12, fontweight = "bold" ,  color= "white")
    ax.set_ylabel("Ahorros (€)", fontsize=12, fontweight = "bold" ,  color= "white", labelpad = 20)
    ax.yaxis.label.set_rotation(0)
    ax.yaxis.set_label_position("left")
    ax.yaxis.tick_left()
    ax.yaxis.set_label_coords(-0.1, 0.5)
    ax.set_ylim(0, 10000)
    ax.tick_params(axis='y', colors='white', labelsize=10, labelrotation=0)
    ax.set_yticks(range(0, 10001, 500))
    ax.tick_params(axis='x', colors='white', labelsize=10, labelrotation=45)
    ax.xaxis.label.set_color("white")
    ax.spines['bottom'].set_color("white")
    ax.spines['left'].set_color("white")
    ax.spines['top'].set_color("#212121")
    ax.spines['right'].set_color("#212121")
    
    fig.tight_layout()

    text_nodata = ft.Text(value="No hay datos para mostrar", size=20, weight="bold")

    if ahorro_total == 0:
        chart_container = ft.Container(
            ft.Column(
                [
                ft.Row([text_nodata])
                ]                
            )
        )
    else: 
        chart_container = ft.Container(
            content=MatplotlibChart(fig, expand=True),
            border_radius=ft.border_radius.all(15),   
            bgcolor="#212121", 
            padding=10)

  
    content = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [user_info_button],
                    alignment="start"
                ),
                ft.Container(
                    content=tittle_app,
                    padding=ft.padding.only(bottom=40)
                ),
                ft.Row(
                    [chart_container],  
                    expand=True,
                    alignment="center",
                    wrap=True
                ),
            ],
            alignment="center", 
            horizontal_alignment="center",  
            spacing=20,  
            scroll="adaptive"
        ),
        padding=ft.padding.only(top=10, left=40, right=40),  
        alignment=ft.alignment.center,  
        expand=True
    )

    return ft.View("/chart", controls=[content])

    
