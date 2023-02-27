## 1. O Problema do Negócio

A **Themy Company** é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas. Através desse aplicativo é possível realizar o pedidos de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por um entregador também cadastrado no aplicativo da Themy Company.

A empresa gera muitas informações com o aplicativo como dados de entrega, de condição climática e de avaliações do pedido. Contudo, atualmente o CEO não tem visibilidade completa dos KPIs de crescimento da empresa para a tomada de decisões com base nas informações armazenadas em seu banco de dados.

Assim, você foi contratado como Cientista de Dados para criar soluções de dados, porém antes de treinar algoritmos é necessário organizar todos os KPIs estratégicos em uma ferramenta para que a equipe, juntamente com o CEO, possa consultar as métricas e tomar melhores decisões.

Para acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento:

**Do lado da Empresa:**
1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por cidade e tipo de tráfego.
4. A quantidade de pedidos por entregador por semana.
5. A localização central de cada cidade por tipo de tráfego.

**Do lado do entregador:**
1. A menor e maior idade dos entregadores.
2. A pior e a melhor condição de veículos.
3. A avaliação médida por entregador.
4. A avaliação média e o desvio padrão por tipo de tráfego.
5. A avaliação média e o desvio padrão por condições climáticas.
6. Os 10 entregadores mais rápidos por cidade.
7. Os 10 entregadores mais lentos por cidade.

**Do lado dos restaurantes:**
1. A quantidade de entregadores únicos.
2. A distância média dos resturantes e dos locais de entrega.
3. O tempo médio e o desvio padrão de entrega por cidade.
4. O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
5. O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
6. O tempo médio de entrega durantes os Festivais.

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

## 2. Premissas assumidas para a análise
1. A análise foi feita entre a data **11/02/2022** e **06/04/2022**.
2. O modelo de negócio assumido foi o **Marketplace**.
3. As **3 principais visões de negócio** criadas foram: **Visão Empresa**, **Visão Entregadores** e **Visão Restaurantes**.

## 3. Top 3 Insights de Dados
1. As cidades **Semi-Urban** não possuem condições baixas de trânsito.
2. As maiores variações do tempo de entrega acontecem quando o clima é **ensolarado**.
3. A maioria dos pedidos nas **metrópoles** acontecem quando a **densidade do tráfego** é **baixa**.

## 4. O Produto Final do Projeto
Dashboard em Cloud com todas as métricas pedidas pelo CEO, sendo possível filtrar por tráfego e data para melhor interpretação dos dados.
Acesse por esse link: https://lucasmeller13-themy-company-home-ct1nbt.streamlit.app/

