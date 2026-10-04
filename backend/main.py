from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

estoque = {
    "arroz 5kg": 12,
    "feijão 1kg": 8,
    "leite 1l": 25,
    "água 1l": 30,
    "café 500g": 6,
}

class ChatRequest(BaseModel):
    message: str

def consultar_estoque(produto: str):
    import unicodedata

    pergunta = unicodedata.normalize("NFKD", produto.lower())
    pergunta = "".join(
        caractere for caractere in pergunta
        if not unicodedata.combining(caractere)
    )

    respostas = []

    palavras_estoque = [
        "o que tem",
        "o que possui",
        "quais produtos",
        "lista de produtos",
        "todos os produtos",
        "estoque"
    ]

    if any(palavra in pergunta for palavra in palavras_estoque):
        return " ".join(
            f"{quantidade} unidades de {nome_produto}"
            for nome_produto, quantidade in estoque.items()
        )

    for nome_produto, quantidade in estoque.items():
        nome_normalizado = unicodedata.normalize(
            "NFKD", nome_produto.lower()
        )
        nome_normalizado = "".join(
            caractere for caractere in nome_normalizado
            if not unicodedata.combining(caractere)
        )

        nome_base = nome_normalizado.split()[0]

        if (
            nome_base in pergunta
            or nome_normalizado.replace(" ", "") in pergunta.replace(" ", "")
        ):
            respostas.append(
                f"Temos {quantidade} unidades de {nome_produto}."
            )

    if respostas:
        return " ".join(respostas)

    return "Não encontrei esse produto no estoque."

@app.get("/")
def home():
    return {"message": "Chatbot da loja funcionando!"}

@app.post("/chat")
def chat(request: ChatRequest):
    resposta_estoque = consultar_estoque(request.message)

    prompt = f"""
Você é o atendente virtual de uma loja.

Use exclusivamente as informações fornecidas abaixo para responder.
Não invente produtos, quantidades ou serviços.
Não ofereça reservas, avisos, marcas, tamanhos ou outras funcionalidades que não foram informadas.
Responda somente à pergunta do cliente, de forma curta, clara e natural.

Informação do estoque:
{resposta_estoque}

Pergunta do cliente:
{request.message}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return {"response": response.output_text}