# raspar_site.py
import requests
from bs4 import BeautifulSoup

urls = [
    'https://www.jovemprogramador.com.br/',
    'https://www.jovemprogramador.com.br/hackathon/',
    'https://www.jovemprogramador.com.br/duvidas.php',
]

conteudo_total = ""
print("🔎 Iniciando raspagem inteligente do site...")

for url in urls:
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove partes indesejadas como menus, rodapés e scripts
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()

        conteudo = soup.body.get_text(separator='\n', strip=True)
        conteudo_total += f"\n\n--- Conteúdo da página: {url} ---\n\n{conteudo}"
        print(f"✔️ Página '{url}' raspada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao raspar {url}: {e}")

with open("conteudo_site.txt", "w", encoding="utf-8") as f:
    f.write(conteudo_total)

print("\n✅ Raspagem concluída. Conteúdo limpo salvo em 'conteudo_site.txt'.")
