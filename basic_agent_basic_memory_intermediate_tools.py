#######################
# Agente Basico De IA #
# Agente              #
#######################

# Importacion para el ambiente
from dotenv import load_dotenv

# Importacion para el LLM
from groq import Groq

# Importacion para el manejo de sistema
import os

# Importacion para el uso de formato JSON
import json

# Importacion para el manejo de fechas y zonas horarias
from datetime import datetime
from zoneinfo import ZoneInfo

# Importacion para el manejo memoria y herramientas#
from basic_memory import BasicMemory
from intermediate_tools import IntermediateTools



# Cargar variables de entorno #
load_dotenv()

# Inicializar el cliente de Groq con la clave de API
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Captura la hora actual en la zona horaria de Guatemala
now = datetime.now(ZoneInfo("America/Guatemala"))

# Inicializar herramientas y memoria #
MEMORY_MAX_MESSAGES = 10
memory = BasicMemory(max_messages=MEMORY_MAX_MESSAGES)


SYSTEM_PROMPT = f"""
Eres un asistente que habla en español, también puede hablar en inglés y alemán y responde de manera muy breve y concisa.
 
Herramientas:
- Cuentas con una herramienta llamada consultar_tipo_cambio_api, la cual te da el tipo de cambio actual
para cualquier moneda. 
- Al llamar a esta herramienta, la moneda es obligatoria.
- Cuentas también con herramientas del Banco Mundial para consultar por país: PIB, inflación, desempleo,
población, PIB per cápita, exportaciones, importaciones, deuda externa, inversión extranjera directa
y consumo de los hogares.
- Al llamar a estas herramientas, el código del país es obligatorio.
- La respuesta que de estas herramientas debes regresarla tal cual, considerando que es correcta.
"""
 
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "consultar_tipo_cambio_api",
            "description": (
                "Llama a esta funcion para consultar el tipo de cambio de una moneda "
                "respecto al quetzal de Guatemala. "
                "Se debe enviar como argumento el codigo de la moneda que se desea consultar."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "moneda": {
                        "type": "string",
                        "description": "Codigo de la moneda que se desea consultar, por ejemplo USD"
                    }
                },
                "required": ["moneda"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_pib_api",
            "description": "Llama a esta funcion para consultar el PIB de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_inflacion_api",
            "description": "Llama a esta funcion para consultar la inflación de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_desempleo_api",
            "description": "Llama a esta funcion para consultar el desempleo de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_poblacion_api",
            "description": "Llama a esta funcion para consultar la población de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_pib_per_capita_api",
            "description": "Llama a esta funcion para consultar el PIB per cápita de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_exportaciones_api",
            "description": "Llama a esta funcion para consultar las exportaciones de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_importaciones_api",
            "description": "Llama a esta funcion para consultar las importaciones de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_deuda_externa_api",
            "description": "Llama a esta funcion para consultar la deuda externa de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_inversion_extranjera_api",
            "description": "Llama a esta funcion para consultar la inversión extranjera directa de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_consumo_hogares_api",
            "description": "Llama a esta funcion para consultar el consumo de los hogares de un país.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pais": {
                        "type": "string",
                        "description": "Codigo del pais que se desea consultar, por ejemplo GT"
                    }
                },
                "required": ["pais"]
            }
        }
    }
]
 
print("Agente Basico De IA")
 
def process_response(client:Groq, memory_messages: list[dict], user_text:str):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(memory_messages)
    messages.append({"role": "user", "content": user_text})
    
    while True:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=TOOLS
        )
 
        msg = resp.choices[0].message
        
        # Si no hay llamados a herramientas, entonces ya regresamos la respuesta
        if not getattr(msg, "tool_calls", None):
            return msg.content or ""
        
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [tc.model_dump() for tc in msg.tool_calls]
        })
        
        tools = IntermediateTools()
 
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")
            
            if name == "consultar_tipo_cambio_api":
                result = tools.consultar_tipo_cambio_api(
                    moneda=args["moneda"]
                )
            elif name == "consultar_pib_api":
                result = tools.consultar_pib_api(
                    pais=args["pais"]
                )
            elif name == "consultar_inflacion_api":
                result = tools.consultar_inflacion_api(
                    pais=args["pais"]
                )
            elif name == "consultar_desempleo_api":
                result = tools.consultar_desempleo_api(
                    pais=args["pais"]
                )
            elif name == "consultar_poblacion_api":
                result = tools.consultar_poblacion_api(
                    pais=args["pais"]
                )
            elif name == "consultar_pib_per_capita_api":
                result = tools.consultar_pib_per_capita_api(
                    pais=args["pais"]
                )
            elif name == "consultar_exportaciones_api":
                result = tools.consultar_exportaciones_api(
                    pais=args["pais"]
                )
            elif name == "consultar_importaciones_api":
                result = tools.consultar_importaciones_api(
                    pais=args["pais"]
                )
            elif name == "consultar_deuda_externa_api":
                result = tools.consultar_deuda_externa_api(
                    pais=args["pais"]
                )
            elif name == "consultar_inversion_extranjera_api":
                result = tools.consultar_inversion_extranjera_api(
                    pais=args["pais"]
                )
            elif name == "consultar_consumo_hogares_api":
                result = tools.consultar_consumo_hogares_api(
                    pais=args["pais"]
                )
            else:
                print(f"Se intentó llamar a una herramienta desconocida {name}")
                result = {"error": f"Herramienta desconocida: {name}"}
                
            # Agregar a los mensajes el resultado del llamado de la herramienta
            # Esto lo recibirá el modelo al continuar la iteración
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False)
            })
 
while True:
 
    user_text = input("Tú: ").strip()
    if not user_text:
        continue
 
    if user_text.lower() in ("exit","salir"):
        print("Hasta luego!")
        break
 
    assistant_text = process_response(client, memory.messages(), user_text)
    print(f"Agente: {assistant_text}")
 
    # Actualizar la memoria #
    memory.add("user",user_text)
    memory.add("assistant", assistant_text)