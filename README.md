
# Melina - Ferramenta de Geração de Relatórios para Pentests

## Introdução

Melina é uma ferramenta criada para simplificar a geração de relatórios, especialmente voltada para pentests e outras aplicações técnicas. Ela permite a integração de Markdown com LaTeX, oferecendo uma solução eficaz para quem prefere evitar o formato DOCX. Melina é ideal para quem busca uma ferramenta simples e direta para a criação de relatórios em PDF.

Para informações mais completas e detalhadas peço que leia a postagem [Melina - Ferramenta de Geração de Relatórios para Pentests](https://0tax00.github.io/posts/Melina/)

## Recursos

- **Geração Automática de PDF**: Crie seu conteúdo em Markdown, faça o upload e obtenha um relatório em PDF.
- **Template Customizável**: Utiliza o template Eisvogel para garantir relatórios visivelmente atraentes e bem estruturados.
- **Integração de Imagens e Códigos**: Suporte para inclusão de imagens e blocos de código diretamente no documento Markdown.
- **Fácil Configuração**: Conte com a facilidade de configuração via Docker, sem necessidade de instalações complexas.

## Instalação

### Pré-requisitos

- Docker instalado no seu sistema.

### Configuração com Docker

1. **Clonar o repositório e construir a imagem Docker:**

```sh
git clone https://github.com/0tax00/Melina.git
cd Melina
sudo docker build -t melina .
sudo docker run -d -p 80:80 melina:latest /bin/bash
```

2. **Utilizar imagem pré-fabricada do Docker Hub:**

```sh
sudo docker run -d -p 80:80 otax03/melina:latest /bin/bash
```

### Atenção: Gerenciamento de Credenciais e Secrets

Ao configurar e utilizar a ferramenta, é crucial implementar práticas robustas de segurança para proteger informações sensíveis e garantir a integridade do sistema. Aqui estão os pontos críticos onde informações sensíveis são utilizadas:

1. **Senha de Administração do CouchDB:**
- As senhas do administrador para CouchDB são definidas no Dockerfile. Altere essas senhas para garantir a segurança do banco de dados:

 ```Dockerfile
 echo "couchdb couchdb/adminpass password teste" | debconf-set-selections
echo "couchdb couchdb/adminpass_again password teste" | debconf-set-selections
 ```

2. **Credenciais de Conexão CouchDB no Flask:**
- O código Flask conecta-se ao CouchDB usando credenciais explicitamente codificadas. É importante substituir essas credenciais hardcoded por métodos mais seguros como variáveis de ambiente:

```python
couch = couchdb.Server('http://admin:teste@127.0.0.1:5984/')
```
3. **Secret Flask:**
 - `app.secret_key` é usado para manter as sessões seguras. Nunca utilize chaves hardcoded em um ambiente de produção. Em vez disso, configure essa chave via variáveis de ambiente ou arquivos de configuração externos:

```python
app.secret_key = 'teste'
```

### Acesso

Após a instalação, acesse a interface web através de `localhost:80` ou `127.0.0.1`.

## Uso

1. **Upload de Relatório**:
   - Acesse `http://127.0.0.1/upload_relatorio` para fazer upload do arquivo Markdown formatado de acordo com o template fornecido.

2. **Consulta de Relatórios**:
   - Visite `http://127.0.0.1/consulta_relatorios` para visualizar ou baixar relatórios gerados.

3. **Gerenciamento de Vulnerabilidades**:
   - Acesse `http://127.0.0.1/vulnerabilities` para adicionar e consultar vulnerabilidades identificadas.

![Melina](/template/Melina.gif)

Template: [template.md](/template/template.md)

## Desenvolvimento

Melina surgiu em um momento de necessidade durante a eWPTX e a jogabilidade de Elden Ring(porque eu não sou dev e foi mais dificil fazer isso do que derrotar a Malenia e o Radagon). A ferramenta foi projetada para ser minimalista, porém eficiente, eliminando as complexidades desnecessárias que frequentemente sobrecarregam outras ferramentas do mercado.

## Contribuições

Contribuições são bem-vindas. Para contribuir, você pode abrir issues ou enviar pull requests através do repositório no GitHub.

Para mais informações e suporte me mande um e-mail mateusgodinho0102@gmail.com o/, por favor lembre-se que esse é apenas um projeto pequeno então não venha com 30 pedras na mão.
