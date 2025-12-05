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


agente_memoria = Agent(
    name="AgenteMemoria",
    instructions="Sos un asistente que recuerda la conversacion previa. Usa la memoria para dar mejores respuestas. Tenes una herramienta llamada 'add_product' para agregar usuarios a la base, usala en caso de que el usuario te lo pida",
    model="gpt-4", 
    tools=[add_product]
)
#print(agente_memoria.model)
conversation_history = []
def test_3():
    global conversation_history
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "salir"]:
            break
        conversation_history.append({"role": "user", "content": user_input})
        result = Runner.run_sync(agente_memoria, conversation_history)
        conversation_history.append({"role": "assistant", "content": result.final_output})
        print(conversation_history)
        print(result.final_output)
test_3()    