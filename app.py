# app.py
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Chave GEMINI_API_KEY não encontrada no arquivo .env!")

genai.configure(api_key=GEMINI_API_KEY)

# Otimização: Carrega o contexto uma única vez ao iniciar a API
try:
    with open("conteudo_site.txt", "r", encoding="utf-8") as f:
        conteudo_site_global = f.read()
    print("✅ Contexto do site carregado na memória.")
except FileNotFoundError:
    print("⚠️ ATENÇÃO: Arquivo 'conteudo_site.txt' não encontrado. Rode 'python raspar_site.py' primeiro.")
    conteudo_site_global = ""

app = Flask(__name__)

@app.route('/')
def home():
    return "API do Jovem Programador (versão melhorada) no ar!"

@app.route('/perguntar', methods=['POST'])
def perguntar():
    data = request.get_json()
    pergunta = data.get("pergunta")
    if not pergunta:
        return jsonify({"erro": "Pergunta não fornecida."}), 400

    try:
        # Usamos um prompt robusto com regras claras.
        prompt = f"""
Você é um assistente virtual especialista no Programa Jovem Programador. Seu tom de voz é amigável e prestativo.

--- REGRAS OBRIGATÓRIAS ---
1.  **FOCO ESTRITO:** Responda usando APENAS o CONTEÚDO DE REFERÊNCIA abaixo. Não use conhecimento externo.

2.  **REGRA DA IDADE (MUITO IMPORTANTE):** O requisito é ter **16 anos ou mais**. Não existe idade máxima.
    - Se o usuário **PERGUNTAR** qual a idade (ex: "qual a idade?", "a partir de quantos anos?"), responda que a idade mínima é 16 anos.
    - Se o usuário **AFIRMAR** a própria idade (ex: "tenho 29 anos", "tenho 15 anos"), trate isso como uma verificação de elegibilidade.
        - Se a idade for 16 ou mais, responda positivamente de forma personalizada. Ex: "Com 29 anos, você atende perfeitamente ao requisito de idade! 👍"
        - Se a idade for menor que 16, responda de forma empática. Ex: "Que legal seu interesse! Para participar, é preciso ter 16 anos. Falta muito para o seu aniversário?"

3.  **PROIBIÇÃO DE ASSUNTOS EXTERNOS:** Se a pergunta não se encaixar na REGRA DA IDADE e for sobre qualquer tema não contido no texto (futebol, política, etc.), responda EXATAMENTE: 'Desculpe, minha função é responder apenas sobre o Programa Jovem Programador.'

4.  **PROATIVIDADE FOCADA:** Ao final de cada resposta, faça uma pergunta para guiar o usuário, como "Isso ajuda? Gostaria de saber sobre as cidades ou sobre o hackathon?".

5.  **FORMATAÇÃO:** Use parágrafos curtos, emojis para destacar informações importantes.

--- CONTEÚDO DE REFERÊNCIA ---
{conteudo_site_global}
--- FIM DO CONTEÚDO DE REFERÊNCIA ---

PERGUNTA DO USUÁRIO: "{pergunta}"
"""
        model = genai.GenerativeModel('gemini-1.5-flash')
        resposta = model.generate_content(prompt)
        return jsonify({"resposta": resposta.text})
    except Exception as e:
        print(f"ERRO: {e}")
        return jsonify({"erro": "Erro ao processar a pergunta", "detalhes": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
