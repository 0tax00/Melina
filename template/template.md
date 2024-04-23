---
title: Pentest
author: 
date: \LARGE 04 de Março de 2024
subject: Markdown
keywords:
  - Markdown
  - Example
subtitle: xpto
lang: en
titlepage: true
titlepage-color: DC143C
titlepage-text-color: FFFFFF
titlepage-rule-color: FFFFFF
titlepage-rule-height: 2
header-right: \textbf{xpto}
header-left: \textcolor{red}{\textbf{CONFIDENCIAL}}
book: true
classoption: oneside
code-block-font-size: \scriptsize
toc-own-page: true
---
\listoffigures

#  DECLARAÇÃO E RESPONSABILIDADE

Escreva a declaração de forma clara e concisa, utilizando linguagem simples e direta. Certifique-se de incluir todos os detalhes relevantes, como escopo do teste, objetivos, limitações, responsabilidades e confidencialidade. Ao redigir, mantenha um tom profissional e objetivo, evitando jargões técnicos desnecessários e garantindo que o documento seja facilmente compreensível para todas as partes envolvidas.

# SUMÁRIO EXECUTIVO

O Sumário Executivo deve ser redigido de forma clara e objetiva, fornecendo uma visão geral das principais descobertas e conclusões do teste realizado. Deve incluir uma breve descrição do escopo do teste, os principais resultados e recomendações para mitigar as vulnerabilidades identificadas. Mantenha o texto sucinto e focado nos pontos mais importantes, facilitando a compreensão por parte dos stakeholders e a tomada de decisões.

## ESCOPO DO TESTE

Descreva claramente os sistemas, redes ou aplicativos incluídos no escopo do teste, especificando os objetivos e limitações do mesmo. Certifique-se de definir os parâmetros do teste para evitar ambiguidades e garantir uma compreensão clara das atividades planejadas.

## RESULTADO EXECUTIVO

Apresente de forma resumida e concisa os principais resultados do teste de penetração, destacando as vulnerabilidades críticas identificadas, as áreas de maior risco e quaisquer insights relevantes para a segurança da organização. Fornecer uma visão geral dos impactos potenciais e recomendações prioritárias para mitigação.


\begin{tabular}{|>{\centering\arraybackslash}p{10cm}|>{\centering\arraybackslash}p{2cm}|>{\centering\arraybackslash}p{2cm}|}
    \hline
    \cellcolor{gray!80} Vulnerabilidades  & \cellcolor{gray!80}  Criticidade & \cellcolor{gray!80}  CVSS \\
    \hline
    \cellcolor{yellow!80} Insecure Direct Object Reference (IDOR) - Upload de arquivos & \cellcolor{yellow!80}  Média & \cellcolor{yellow!80}  6.8 \\
    \hline
\end{tabular}
## REFERÊNCIA À CLASSIFICAÇÃO DE RISCO

Forneça uma descrição clara dos critérios utilizados para classificar as vulnerabilidades identificadas durante o teste de penetração. Defina os níveis de risco (baixo, médio, alto) com base na gravidade e na probabilidade de exploração das vulnerabilidades, garantindo uma avaliação consistente e compreensível para os stakeholders.

\begin{tabular}{|>{\centering\arraybackslash}p{2cm}|>{\centering\arraybackslash}p{10cm}|>{\centering\arraybackslash}p{2cm}|}
    \hline
    \cellcolor{gray!80} Severidade  & \cellcolor{gray!80}  Descrição & \cellcolor{gray!80}  Quantidade \\
    \hline
    \cellcolor{violet!80} Critica  & \cellcolor{white!40}   Severidade máxima, elas possibilitam controle total ou parcial do sistema operacional, execução remota de código (RCE) e acesso a outros ambientes da estrutura de rede corporativa. & \cellcolor{white!40}  0 \\
    \hline
    \cellcolor{red!80} Alta  & \cellcolor{white!40}  Severidade elevada, vazamento de dados e exSposição de informações sensíveis, permitindo reconhecimento dos processos internos. & \cellcolor{white!40}  0 \\
    \hline
    \cellcolor{yellow!80} Média  & \cellcolor{white!40}  Severidade moderada, pode desencadear ataques subsequentes, comprometendo parcialmente a estrutura. & \cellcolor{white!40}  1 \\
    \hline
    \cellcolor{green!80} Baixa  & \cellcolor{white!40}  Severidade baixa, não ameaça a segurança, fornece informações técnicas úteis para o conhecimento, não requer correção urgente. & \cellcolor{white!40}  0 \\
    \hline
    \cellcolor{cyan!80} informativa  & \cellcolor{white!40}   Severidade informativa, informações técnicas ou contextuais, não representam riscos significativos. & \cellcolor{white!40}  0 \\
    \hline
\end{tabular}


# Relatório Técnico 


As vulnerabilidades serão apresentadas em ordem de criticidade:s

## Insecure Direct Object Reference (IDOR) - Upload de arquivos 

|                 |                                                                                               |
| --------------- | --------------------------------------------------------------------------------------------- |
| URL             | http://10.100.13.34/?page=login                                                               |
| Ativos afetados | 10.100.13.34                                                                                  |
| Severidade      | **\textcolor{yellow}{Média}**                                                                 |
| CVSS            | [6.8](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:N) |

### Descrição

A vulnerabilidade *IDOR (Insecure Direct Object Reference)* permite que usuários acessem diretamente objetos dentro de um sistema sem a devida autorização. Isso ocorre devido à falta de validação ou controle de acesso adequado, permitindo que usuários mal-intencionados possam explorar e acessar informações confidenciais ou realizar ações não autorizadas.



### Prova de conceito

Durant

- Requisição - *UUID* do projeto
```C
#include <stdio.h>

int main() {
    // Declaração de variáveis
    int senha_correta = 1234;
    int senha_usuario;

    // Solicitar senha ao usuário
    printf("Digite a senha: ");
    scanf("%d", &senha_usuario);

    // Verificar se a senha está correta
    if (senha_usuario == senha_correta) {
        printf("Acesso concedido!\n");
    } else {
        printf("Senha incorreta. Tente novamente.\n");
    }

    return 0;
}
```

![Requisição - *UUID* do projeto](me-01.png){ width=80% }

### Impacto técnico

- Acesso Não Autorizado: Permite que usuários mal-intencionados acessem diretamente objetos dentro do sistema, como arquivos de outros clientes, sem a devida autorização.

- Comprometimento da Integridade dos Dados: A possibilidade de realizar uploads entre clientes permite a substituição ou adulteração de arquivos legítimos, comprometendo a integridade dos dados armazenados na plataforma.

- Violação da Privacidade: Usuários não autorizados podem acessar informações confidenciais de outros clientes, violando a privacidade e a confidencialidade dos dados.

### Impacto corporativo

- Perda de Confiança dos Clientes: A exposição de dados confidenciais e a falha na proteção da privacidade dos clientes podem levar à perda de confiança dos clientes na plataforma.

- Danos à Reputação da Empresa: A divulgação pública de violações de segurança e incidentes de privacidade pode resultar em danos significativos à reputação da empresa, afetando sua credibilidade no mercado.

- Impacto Financeiro: Os custos associados à remediação de violações de segurança, à implementação de medidas corretivas e à compensação de clientes afetados podem ser significativos, resultando em impactos financeiros adversos para a empresa.

### Recomendações de correção

- Validação de Autorização por UUID: Implementar uma validação rigorosa para garantir que cada upload de arquivo esteja associado ao UUID correto do cliente autenticado. Isso pode ser feito verificando se o UUID fornecido pertence ao cliente autenticado no momento da requisição.

- Controles de Acesso Granulares: Implementar controles de acesso granulares para garantir que cada cliente só possa acessar e manipular os recursos que lhes são atribuídos. Isso inclui a aplicação de permissões de acesso adequadas e a verificação da identidade do usuário em cada interação com o sistema.

### Referências

- [Insecure Direct Object Reference Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)
- [Testing for Insecure Direct Object References](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References)
- [Insecure Direct Object Reference IDOR](https://owasp.org/www-chapter-ghana/assets/slides/IDOR.pdf)
- [Insecure direct object references (IDOR)](https://portswigger.net/web-security/access-control/idor)
