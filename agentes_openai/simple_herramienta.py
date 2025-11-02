from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import json
load_dotenv()


@function_tool
def add_product(name:str, price:str, description:str) -> str:
    json_data = []
    with open("datos.json", "r") as file:
        content = json.load(file)
        if content:
            json_data.append(content)
    with open("datos.json", "w") as file:
        json_data.append(f'{{"name": "{name}", "price": {price}, "description": "{description}"}}')
        file.write(",\n".join(json_data))
    return "Producto agregado exitosamente."

agent = Agent(name="Assistant", instructions="Sos un asistente que ayuda a agregar productos a una base de datos JSON. Tenes que darle a la herramienta 'add_product' el nombre, el precio y la descripcion del producto", tools=[add_product])


def test_1():
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "salir"]:
            break
        result = Runner.run_sync(agent, user_input)
        print(result.final_output)


test_1()        