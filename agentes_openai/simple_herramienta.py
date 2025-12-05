from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import json
load_dotenv()


@function_tool
def add_product(name:str, price:str, description:str) -> str:
    try:
        try:
            with open("datos.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        new_product = {
            "name": name,
            "price": price,
            "description": description
        }
        data.append(new_product)
        with open("datos.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        return "Producto agregado exitosamente."
    except Exception as e:
        return f"Error al agregar el producto: {e}"

agent = Agent(name="Assistant", instructions="Sos un asistente que ayuda a agregar productos a una base de datos JSON. Tenes que darle a la herramienta 'add_product' el nombre, el precio y la descripcion del producto", tools=[add_product])


def test_1():
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "salir"]:
            break
        result = Runner.run_sync(agent, user_input)
        print(result.final_output)


test_1()        