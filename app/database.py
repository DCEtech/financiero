import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError
import bcrypt
from datetime import datetime
import time

load_dotenv()

now = datetime.now
year =  now().year
month = now().month

mongo_uri = str(os.getenv("MONGODB_URI"))
db_name = str(os.getenv("DB_NAME"))

while True:
  try:
    client = MongoClient(mongo_uri)
    mydb =  client[db_name]
    client.server_info() 
  except ConnectionFailure as _:
    print("Error connecting to MongoDB: Retrying...")
    time.sleep(5)
  else:
    print("Sucssesfull conexion to MongoDB")
    if "users" not in mydb.list_collection_names():
      mycol = mydb.create_collection("users")
    else:
      mycol = mydb["users"]
      mycol.create_index('username', unique=True)
    break

def create_user(username, password):
  try:

    if not username and not password:
      return {"error": "El nombre de usuario y la contraseña no pueden estar vacíos."}
    if not username: 
      return {"error": "El nombre de usuario no puede estar vacío."}
    if not password: 
      return {"error": "La contraseña no puede estar vacía."}
    
    password_hash  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
      "username": username,
      "password_hash": password_hash,
      "financial_data": [
      ]
    }
    mycol.insert_one(user)
    return {"success": f"Usuario {username} registrado exitosamente."}

  except  DuplicateKeyError:
    print(f"Error: User name already exists.")
    return{"error": f"El usuario {username} ya está registrado."}
  except  PyMongoError as e:
    print(f"Error: {e}")
    return {"error": "Error al registrar usuario."}

def delete_user(username):
  try:

    mycol.delete_one({"username": username})
    return {"success": f"Usuario {username} eliminado exitosamente."}

  except PyMongoError as e:
    print(f"Error: {e}")
    return {"error": "Error al eliminar usuario."}

def authentication_user(username, password):

  try:

    user = mycol.find_one({"username": username})
    if user: 
      password_hash  = user["password_hash"] 

      if user and bcrypt.checkpw(password.encode('utf-8'), password_hash):
        user_sesion = username
        print(f"User session set for: {user_sesion}") 
        return {"success": f"Bienvenido a Financiero {username}"}
    else:
      return {"error": "Usuario o contraseña incorrectos."}
  
  except PyMongoError as e:
        print(f"Database error: {e}")
        return False
  except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
def insert_financial_data(username, income, savings, expenses):
  try: 
    
    user = mycol.find_one({"username": username})

    if "," in str(income) or "," in str(savings) or "," in str(expenses): 
      return {"error": "Utilize . para valores decimales."}
    
    if "." in str(income): 
      entero , decimal = str(income).split(".")
      if len(decimal) > 2:
        return {"error": "El valor decimal no puede tener más de 2 dígitos."}
      
    if "." in str(savings):
      entero , decimal = str(savings).split(".")
      if len(decimal) > 2:
        return {"error": "El valor decimal no puede tener más de 2 dígitos."}
    
    if "." in str(expenses): 
      entero , decimal = str(expenses).split(".")
      if len(decimal) > 2:
        return {"error": "El valor decimal no puede tener más de 2 dígitos."}
      
    if income == "":
      return {"error": "Los ingresos no pueden estar vacios."}
    
    
    if float(income) < float(savings) + float(expenses):
      return {"error":"Los ingresos no pueden ser menores que la suma de ahorro y gasto."}

    excedent = float(income) - float(savings) - float(expenses)

    income = float(income)
    savings = float(savings)
    expenses = float(expenses)
    excedent = float(excedent)

    income_decimal = f"{income:.2f}"
    savings_decimal = f"{savings:.2f}"
    expenses_decimal = f"{expenses:.2f}"
    excedent_decimal = f"{excedent:.2f}"
    
    new_data = {
      "income": income_decimal,
      "savings": savings_decimal,
      "expenses": expenses_decimal,
      "excedent": excedent_decimal,
      "month": month,
      "year": year
    }

    item_exist = [data for data in user["financial_data"] if data["month"] == new_data["month"] and data["year"] == new_data["year"]]
    if any(item_exist):
      return {"error": "Ya existe un registro para este mes y año."}
    else:
      mycol.update_one(
        {"username": username},
        {"$push":{"financial_data": new_data}}
      )
      print("Financial data inserted successfully.")
      return {"success": "Informacion añadida correctamente"}
        
  except PyMongoError as e:
    print(f"Error inserting financial data: {e}")
    return {"error": "Error al insertar datos financieros."}

def delete_financial_data(username, month, year):
  try: 

    user =  mycol.find_one({"username": username})

    update_financial_data = [data for data in user["financial_data"] if not ((data["month"] == month) & (data["year"] == year))] 

    if len(update_financial_data) != len(user["financial_data"]):
      mycol.update_one(
        {"username": username},
        {"$set": {"financial_data": update_financial_data}})
      print("Financial data deleted successfully.")
      return {"success": "Informacion eliminada correctamente"}
    else: 
      return {"error": "No se ha podido realizar la operacion."}
  except  PyMongoError as e:
    print(f"Error deleting financial data: {e}")

def update_financial_data(username, income, savings, expenses, month, year):
    try: 
        user = mycol.find_one({"username": username})

        if "," in str(income) or "," in str(savings) or "," in str(expenses): 
          return {"error": "Utilice . para valores decimales."}

        if "." in str(income):
          entero, decimal = str(income).split(".")
          if len(decimal) > 2:
            return {"error": "El valor decimal no puede tener más de 2 dígitos."}

        if "." in str(savings):
          entero, decimal = str(savings).split(".")
          if len(decimal) > 2:
            return {"error": "El valor decimal no puede tener más de 2 dígitos."}

        if "." in str(expenses):
          entero, decimal = str(expenses).split(".")
          if len(decimal) > 2:
            return {"error": "El valor decimal no puede tener más de 2 dígitos."}

        if float(income) < float(savings) + float(expenses):
          return {"error": "Los ingresos no pueden ser menores que la suma de ahorro y gasto."}
        
        excedent = float(income) - float(savings) - float(expenses)

        income = float(income)
        savings = float(savings)
        expenses = float(expenses)
        excedent = float(excedent)

        income_decimal = f"{income:.2f}"
        savings_decimal = f"{savings:.2f}"
        expenses_decimal = f"{expenses:.2f}"
        excedent_decimal = f"{excedent:.2f}"

        for check in user["financial_data"]:
            if check["month"] == month and check["year"] == year:
              check["income"] = income_decimal
              check["savings"] = savings_decimal
              check["expenses"] = expenses_decimal
              check["excedent"] = excedent_decimal
              break
      
        mycol.update_one(
          {"username": username},
          {"$set": {"financial_data": user["financial_data"]}}
        )

        print("Financial data updated successfully.")
        return {"success": "Información actualizada correctamente."}

    except PyMongoError as e:
        print(f"Error updating financial data: {e}")
        return {"error": "No se ha podido realizar la operación."}

def data_info(username, month, year):
  try: 
    user =  mycol.find_one({"username": username})
    financial_data = []

    data = user["financial_data"]

    print(f"all financial {data}")

    for data in user["financial_data"]:
      if data["month"] == month and data["year"] == year:
        financial_data.append(data)
    
    print(f"financial_data {financial_data}")
    return financial_data

  except PyMongoError as e:
    print(f"Error getting financial data: {e}")

def years_months_data(username):
  try: 

    user =  mycol.find_one({"username": username})
    bidimensional_data = {}

    for data in user["financial_data"]:
      year = data["year"]
      month = data["month"]

      if year not in bidimensional_data:
        bidimensional_data[year] = []
      
      if month not in bidimensional_data[year]:
        bidimensional_data[year].append(month)

    return bidimensional_data
  
  except PyMongoError as e:
    print(f"Error get months: {e}")
    return {}

def current_savings(username):
  try:
    user =  mycol.find_one({"username": username})
    financial_data = user.get("financial_data", []) 

    bidimensional_data = {}
    
    for data in financial_data: 
      year = data["year"]
      month = data["month"]

      if year not in bidimensional_data:
        bidimensional_data[year] = []
      if month not in bidimensional_data[year]:
        bidimensional_data[year].append(month)

    sum_savings = []
    total = 0

    for data in financial_data:
      savings = float(data.get("savings", 0))
      total += float(savings)
      sum_savings.append(total)

    return sum_savings, bidimensional_data
  except PyMongoError as e:
    print(f"Error getting current savings: {e}")
  