import json # Importei uma Biblioteca para ser compatível trabalhar com arquivos .JSON
import os # Importei uma biblioteca onde ele interage com diversos Sistemas Operacionais (Linux, MacIos, Windows, etc.)

ARQUIVO_USUARIOS = "usuarios.json"

cursos_disponiveis = [
    {"id": 1, "nome": "Introdução à Programação com Python"}, # Para todos os Cursos, segue o ID (para a seleção) e o nome
    {"id": 2, "nome": "Lógica de Programação"},
    {"id": 3, "nome": "Boas Práticas de Segurança Digital"}
]

# Onde vai salvar e carregar os diferentes usuários do arquivo .JSON
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

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
def cadastrar_usuario(): # Contendo todas as diferentes etapas para cadastrar um novo usuário, pedindo algumas credenciais para a identificação do mesmo
    print("\n--- Cadastro de Usuário ---")
    nome = entrada_segura("Nome: ")
    idade = int(entrada_segura("Idade: "))
    email = entrada_segura("E-mail: ")
    nivel = entrada_segura("Nível de Conhecimento (Iniciante, Intermediário, Avançado): ")
    senha = entrada_segura("Crie uma senha de acesso: ") # Pede que o usuário crie uma senha para as demais situações

    regioes_validas = ["Iguatemi", "Engenheiro Marsilac", "Municípios da região Itapetininga"] # Adicionei 3 regiões para cadastrar o usuário (3 regiões com o menor acesso a internet do estado de SP)
    print("Regiões disponíveis:") 
    for i, reg in enumerate(regioes_validas, 1):
        print(f"{i}. {reg}")

    while True:
        escolha = entrada_segura("Escolha a região (1-3): ")
        if escolha in ["1", "2", "3"]:
            regiao = regioes_validas[int(escolha)-1] 
            break
        else:
            print("Opção inválida. Tente novamente.") 

    usuario = { # Estrutura que os dados vão ficar no arquivo .JSON
        "nome": nome,
        "idade": idade,
        "email": email,
        "nivel": nivel,
        "regiao": regiao,
        "cursos": [],
        "senha": senha  
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

def listar_cursos():
    print("\n--- Cursos Disponíveis ---")
    for curso in cursos_disponiveis: 
        print(f"{curso['id']} - {curso['nome']}")

# Inscreve o usuário em um curso escolhido
def inscrever_usuario():
    usuarios = carregar_usuarios() # Função responsável por carregar os usuários
    if not usuarios:
        print("Nenhum usuário cadastrado.") # Verificação para ver se não tem usuários inscritos
        return

    listar_usuarios()
    indice = int(entrada_segura("Digite o número do usuário que deseja inscrever: ")) - 1 # Responsável por mostrar a lista de usuários incritos e solicitar a escolha
    if indice < 0 or indice >= len(usuarios): # Verifica se o usuário escolhido realmente existe
        print("Usuário inválido.")
        return

    # Solicita a senha do usuário para garantir que ele está se inscrevendo
    senha_digitada = entrada_segura("Digite sua senha para confirmar a inscrição: ")

    if senha_digitada != usuarios[indice]["senha"]:
        print("Senha incorreta! Inscrição não realizada.")
        return

    listar_cursos() # Lista os cursos e solicita a escolha
    curso_id = int(entrada_segura("Digite o ID do curso para se inscrever: ")) # Função de repetição onde ele irá listar os cursos com seus IDs até não ter mais nenhum curso (apenas 3 no momento)

    curso = next((c for c in cursos_disponiveis if c['id'] == curso_id), None) # Busca o curso pelo ID dele
    if not curso:
        print("Curso inválido.")
        return

    if curso_id not in usuarios[indice]['cursos']: # Processo simples para que o usuário se inscreva em um curso existente
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
        print("Nenhum usuário para gerar estatísticas.") # Exibe essa mensagem se não tiver nenhum usuário cadastrado para gerar o relatório
        return

    idades = [u['idade'] for u in usuarios]
    media_idade = sum(idades) / len(idades) # Onde é gerada e calculada a média das idades do alunos cadastrados
    print(f"Média de idade dos usuários: {media_idade:.2f} anos") # Monstra a média das idades

    contador_cursos = {} # Analisa e descobre qual é o curso "mais popular" entre os 3
    for usuario in usuarios:
        for curso_id in usuario['cursos']:
            contador_cursos[curso_id] = contador_cursos.get(curso_id, 0) + 1 # Cada curso começa com um contador "0", quando ele for escolhido será adicionado "1"

    if contador_cursos:
        mais_popular = max(contador_cursos, key=contador_cursos.get) # Encontra o curso que tiver mais inscrições
        nome_curso = next((c['nome'] for c in cursos_disponiveis if c['id'] == mais_popular), "") # Busca o nome do curso mais popular
        print(f"Curso mais popular: {nome_curso} ({contador_cursos[mais_popular]} inscrições)") # Exibe a mensagem com o nome do curso e quantas inscrições ele tem
    else:
        print("Nenhum curso escolhido ainda.")

    # Parte responsável por mostrar a região que mais foi escolhida
    contador_regioes = {} 
    regioes_idades = {} 

    # Intera para todos os usuários cadastrados no programa
    for u in usuarios:
        regiao = u.get("regiao") # obtem a região do usuário usando .get (evita erros)
        if regiao:
            contador_regioes[regiao] = contador_regioes.get(regiao, 0) + 1 
            regioes_idades.setdefault(regiao, []).append(u["idade"]) 

    if contador_regioes:
        regiao_mais_comum = max(contador_regioes, key=contador_regioes.get) # Mostra qual a região que mais tem usuários cadastrados
        media_regiao = sum(regioes_idades[regiao_mais_comum]) / len(regioes_idades[regiao_mais_comum]) # Faz a média das idades
        print(f"Região mais escolhida: {regiao_mais_comum} ({contador_regioes[regiao_mais_comum]} usuários)") 
        print(f"Média de idade dos usuários dessa região: {media_regiao:.2f} anos") 
    else:
        print("Nenhuma região cadastrada ainda.")

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
            senha = entrada_segura("Digite a senha para acessar os dados dos usuários: ") # Adiciona um simples método de segurança pedindo uma senha específica para listar os usuários
            if senha == "12345": # Somente com esse senha o Admin poderá acessar a lista de usuários
                listar_usuarios()
            else:
                print("Senha incorreta! Acesso negado.")
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

def verificar_login():  # Adicionei uma função onde somente exibirá as demais opções se colocado o login e senha corretos
    print("=== Login de Administrador ===")
    login = entrada_segura("Login: ") 
    senha = entrada_segura("Senha: ")

    if login != "Admin" or senha != "123321": # Defini o login e senha para a entrada do sistema
        print("Erro: Login ou senha incorretos. Encerrando o programa.")
        exit()  # Caso o Login e senha estiver errado, exibirá esse erro e com isso, encerra o programa

if __name__ == "__main__":
    verificar_login()  
    menu()
