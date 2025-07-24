

import requests

url = "http://127.0.0.1:5000/perguntar"

def exibir_menu():
    print("\n🧠 Bem-vindo ao ChatBot do Programa Jovem Programador!")
    print("-------------------------------------------------------")
    print("Escolha uma opção:")
    print("[1] Fazer perguntas")
    print("[0] Sair do sistema")
    print("-------------------------------------------------------")

while True:
    exibir_menu()
    escolha = input("Digite sua opção: ")

    if escolha == '0':
        print("\n👋 Encerrando o sistema. Até logo!")
        break

    elif escolha == '1':
        print("\n🔎 Modo de perguntas ativado!")
        print("ℹ️ Digite 'menu' para voltar ao menu ou 'encerrar' para sair do sistema.\n")

        while True:
            pergunta = input("Faça sua pergunta:\n> ").strip().lower()

            if pergunta in ['menu', 'sair']:
                print("\n🔙 Retornando ao menu principal...\n")
                break
            elif pergunta == 'encerrar':
                print("\n👋 Encerrando o sistema. Até logo!")
                exit()

            if not pergunta:
                print("⚠️ Por favor, digite uma pergunta válida.")
                continue

            resposta = requests.post(url, json={"pergunta": pergunta})

            if resposta.status_code == 200:
                print("\n💬 Resposta da IA:\n" + resposta.json()["resposta"])
            else:
                print("❌ Erro:", resposta.status_code, resposta.text)

    else:
        print("❗ Opção inválida. Digite 1 para perguntas ou 0 para sair.")
