# 🦴 BoneGuard Vision API - Microsserviço de IA

Este repositório contém o microsserviço de Inteligência Artificial do projeto **BoneGuard**, desenvolvido para a Global Solution da FIAP. A API é responsável por receber imagens de radiografias (raio-x) e aplicar um modelo de Deep Learning para classificar a saúde óssea do paciente.

## 🎯 Objetivo e Contexto de Negócio
O BoneGuard atua como uma ferramenta de triagem precoce para médicos e sistemas de saúde. O modelo foi otimizado (através de *Fine-Tuning* e *Class Weights*) para priorizar a sensibilidade na classe inicial da doença. O nosso modelo atinge **97% de taxa de acerto (recall) na detecção de Osteopenia**, garantindo que pacientes em estágio inicial de perda de massa óssea sejam identificados rapidamente para intervenção clínica, minimizando os falsos negativos.

## 🏗️ Arquitetura
Este projeto atua como um **Microsserviço de IA Isolado**, encapsulado via Docker. Ele não possui interface gráfica própria (frontend) e não comunica diretamente com a base de dados. Foi desenhado segundo as melhores práticas de Arquitetura de Microsserviços para ser consumido via requisições HTTP (`POST`) pelo Backend principal da aplicação (Gateway/API em Java).

### Tecnologias Utilizadas:
* **Python 3.12**
* **TensorFlow / Keras** (Modelo EfficientNetB0 customizado)
* **FastAPI** (Construção da API RESTful de alta performance)
* **Uvicorn** (Servidor ASGI)
* **Docker** (Containerização e padronização de ambiente)

## 📊 Desempenho e Validação do Modelo (V2)

Durante o processo de *Quality Assurance* (QA), optámos por sacrificar uma pequena margem de acurácia global para maximizar a assertividade médica. Os gráficos abaixo demonstram o comportamento do modelo.

### Evolução do Treino (Overfitting Controlado para Sensibilidade)
| Acurácia | Perda (Loss) |
| :---: | :---: |
| <img src="graphics/grafico_acuracia.png" width="400"> | <img src="graphics/grafico_perda.png" width="400"> |
*Nota: O distanciamento nas épocas finais reflete a penalização forçada nas classes minoritárias para garantir a elevada taxa de recall em Osteopenia.*

### Matriz de Confusão
Na matriz abaixo, é possível verificar a eficácia do modelo em diagnosticar corretamente a Osteopenia (97% de Recall), concentrando os acertos no quadrante central.

<div align="center">
  <img src="graphics/grafico_matriz_confusao.png" width="500">
</div>

## ⚙️ Como Executar o Projeto Localmente

### Opção 1: Usando Docker (Recomendado)
A aplicação está totalmente contentorizada para garantir que corre em qualquer ambiente sem problemas de dependências.

1. Na raiz do projeto, construa a imagem referenciando o ficheiro dentro da pasta `docker/`:
   ```bash
   docker build -f docker/Dockerfile -t boneguard-api .
   ```

2. Corra o contentor mapeando a porta 8000:
   ```bash
   docker run -p 8000:8000 boneguard-api
   ```

### Opção 2: Usando Ambiente Virtual Python (VENV)

1. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # (No Windows)
   # ou
   source venv/bin/activate      # (No Linux/Mac)
   ```

2. Instale as dependências listadas na pasta docker:
   ```bash
   pip install -r docker/requirements.txt
   ````

3. Mude para a diretoria da API e inicie o servidor:
   ```bash
   cd api
   uvicorn api:app --reload
   ```


## 📡 Documentação dos Endpoints

Quando o servidor estiver a correr, a documentação interativa (Swagger UI) pode ser acedida através de:

👉 http://localhost:8000/docs

POST /analisar-radiografia
Recebe o upload de uma imagem .jpg ou .png via multipart/form-data e retorna a predição clínica.

Exemplo de Requisição via cURL:

   ```bash
   curl -X 'POST' \
   'http://localhost:8000/analisar-radiografia' \
   -H 'accept: application/json' \
   -H 'Content-Type: multipart/form-data' \
   -F 'file=@caminho/para/o/raiox_paciente.png'
   ```

Exemplo de Resposta de Sucesso (JSON):

   ```JSON
   {
      "classificacao": "Osteopenia",
      "confianca": 0.9785,
      "probabilidades_brutas": {
         "Normal": 0.0112,
         "Osteopenia": 0.9785,
         "Osteoporosis": 0.0103
      }
   }
   ```