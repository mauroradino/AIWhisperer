from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import requests
load_dotenv()

@function_tool
def obtener_info_simpsons(nombre_personaje: str) -> str:
    characters_data = requests.get("https://thesimpsonsapi.com/api/characters")
    if characters_data.status_code == 200:
        characters = characters_data.json()
        for character in characters:
            if character["name"].lower() == nombre_personaje.lower():
                return f"{character['name']}: {character['description']}"
        return "Personaje no encontrado."
    else:
        return "Error al obtener datos de Los Simpsons."


agente_simpsons = Agent(
    name="SimpAgent", 
    instructions="Sos un experto en la serie Los Simpsons. Responde preguntas relacionadas con personajes de la serie",
    handoff_description="Sos un agente especializado en Los Simpsons.",
    tools=[obtener_info_simpsons])

@function_tool
def obtener_info_pokemon(nombre_pokemon: str) -> str:
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon.lower()}")
    if response.status_code == 200:
        data = response.json()
        tipos = [tipo['type']['name'] for tipo in data['types']]
        habilidades = [habilidad['ability']['name'] for habilidad in data['abilities']]
        return f"{data['name'].title()}: Tipos: {', '.join(tipos)}. Habilidades: {', '.join(habilidades)}."
    else:
        return "Pokemon no encontrado."


agente_pokemon = Agent(
    name="PokemonAgent",
    instructions="Sos un experto en pokemon. Tenes una herramienta para obtener informacion de los pokemon.",
    handoff_description="Sos un agente especializado en pokemon",
    tools=[obtener_info_pokemon]
    )
agente_maestro = Agent(
    name="MaestroAgent", 
    instructions="Sos el coordinador de un equipo de maestros. Tenes que delegar preguntas a otros agentes segun su especialidad. Si la pregunta es matematica, preguntale al agente de matematicas. Si la pregunta es traduccion, preguntale al agente de traduccion. Responde en el mismo idioma en que te pregunten.",
    handoffs = [agente_simpsons, agente_pokemon]
)

def test_2():
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "salir"]:
            break
        result = Runner.run_sync(agente_maestro, user_input)
        print(result.final_output)

test_2()