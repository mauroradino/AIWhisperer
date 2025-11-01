from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

agente_memoria = Agent(
    name="AgenteMemoria",
    instructions="Sos un asistente que recuerda la conversacion previa. Usa la memoria para dar mejores respuestas.",
)
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
        print(result.final_output)
test_3()    