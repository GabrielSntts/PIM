import json
import os

ARQUIVO_USUARIOS = "usuarios.json"

# Cursos que estão disponíveis na plataforma
cursos_disponiveis = [
    {"id": 1, "nome": "Introdução à Programação com Python"},
    {"id": 2, "nome": "Lógica de Programação"},
    {"id": 3, "nome": "Boas Práticas de Segurança Digital"}
]

# Onde vai salver e carregar os diferentes usuários do arquivo .JSON
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

# Aqui ele vai salvar os usuários em um arquivo .JSON
def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

# Uma função "auxiliar" para a entrada segura dos dados (além de tentar evitar os erros de input)
def entrada_segura(mensagem):
    try:
        return input(mensagem)
    except (EOFError, OSError):
        print("\nErro de entrada detectado. Encerrando programa.")
        exit()

# Nessa parte, cadastra um novo usuário
def cadastrar_usuario():
    print("\n--- Cadastro de Usuário ---")
    nome = entrada_segura("Nome: ")
    idade = int(entrada_segura("Idade: "))
    email = entrada_segura("E-mail: ")
    nivel = entrada_segura("Nível de Conhecimento (Iniciante, Intermediário, Avançado): ")

    usuario = {
        "nome": nome,
        "idade": idade,
        "email": email,
        "nivel": nivel,
        "cursos": []
    }

    usuarios = carregar_usuarios()
    usuarios.append(usuario)
    salvar_usuarios(usuarios)
    print("Usuário cadastrado com sucesso!")

# Nesta etapa, o programa vai listar os usuários novos e os que ja foram cadastrados anteriormente
def listar_usuarios():
    print("\n--- Lista de Usuários ---")
    usuarios = carregar_usuarios()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. Nome: {usuario['nome']}, Idade: {usuario['idade']}, Email: {usuario['email']}, Cursos inscritos: {len(usuario['cursos'])}")

# Parte responsável por listar os diferentes cursos disponíveis
def listar_cursos():
    print("\n--- Cursos Disponíveis ---")
    for curso in cursos_disponiveis:
        print(f"{curso['id']} - {curso['nome']}")

# Inscreve o usuário em um curso escolhido 
def inscrever_usuario():
    usuarios = carregar_usuarios()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    listar_usuarios()
    indice = int(entrada_segura("Digite o número do usuário que deseja inscrever: ")) - 1
    if indice < 0 or indice >= len(usuarios):
        print("Usuário inválido.")
        return

    listar_cursos()
    curso_id = int(entrada_segura("Digite o ID do curso para se inscrever: "))

    curso = next((c for c in cursos_disponiveis if c['id'] == curso_id), None)
    if not curso:
        print("Curso inválido.")
        return

    if curso_id not in usuarios[indice]['cursos']:
        usuarios[indice]['cursos'].append(curso_id)
        salvar_usuarios(usuarios)
        print("Inscrição realizada com sucesso!")
    else:
        print("Usuário já está inscrito neste curso.")

# Gerar as estatísticas básicas solicitadas, como a moda, média e mediana
def gerar_estatisticas():
    print("\n--- Estatísticas da Plataforma ---")
    usuarios = carregar_usuarios()
    if not usuarios:
        print("Nenhum usuário para gerar estatísticas.")
        return

    idades = [u['idade'] for u in usuarios]
    media_idade = sum(idades) / len(idades)
    print(f"Média de idade dos usuários: {media_idade:.2f} anos")

    contador_cursos = {}
    for usuario in usuarios:
        for curso_id in usuario['cursos']:
            contador_cursos[curso_id] = contador_cursos.get(curso_id, 0) + 1

    if contador_cursos:
        mais_popular = max(contador_cursos, key=contador_cursos.get)
        nome_curso = next((c['nome'] for c in cursos_disponiveis if c['id'] == mais_popular), "")
        print(f"Curso mais popular: {nome_curso} ({contador_cursos[mais_popular]} inscrições)")
    else:
        print("Nenhum curso escolhido ainda.")

# Menu principal com as diferentes opções para os usuários
def menu():
    while True:
        print("\n=== SafeLearn - Aprendizado seguro com um futuro garantido! ===")
        print("1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("3. Listar Cursos")
        print("4. Inscrever Usuário em Curso")
        print("5. Gerar Estatísticas")
        print("0. Sair")
        opcao = entrada_segura("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            listar_cursos()
        elif opcao == "4":
            inscrever_usuario()
        elif opcao == "5":
            gerar_estatisticas()
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
