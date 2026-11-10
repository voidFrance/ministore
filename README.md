# MiniStore

Sistema web com objetivo didático desenvolvido com Flask + MariaDB.


## Pré-requisitos

- Python 3.x
- MariaDB instalado e rodando
- Git configurado

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/voidFrance/ministore.git
cd ministore
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

```bash
python3 setup.py
```

### 5. Execute a aplicação

```bash
python3 app.py
```

Acesse em http://127.0.0.1:5000

## Estrutura do projeto

```
ministore/
├── app.py              # ponto de entrada da aplicação
├── database.py         # conexão com o banco de dados
├── setup.py            # script de criação do banco
├── requirements.txt    # dependências do projeto
├── static/
│   ├── css/style.css   # estilos globais
│   └── js/main.js      # javascript global
├── dashboard/          # módulo de dashboard (fornecido)
├── clientes/           # módulo de clientes (fornecido)
├── categorias/         # módulo de categorias (rotas + templates)
├── produtos/           # módulo de produtos (rotas + templates)
└── vendas/             # módulo de vendas (rotas + templates)
```

## Módulos

| Módulo | Status |
|--------|--------|
| Dashboard | ✅ Pronto (totais + faturamento + ultimas vendas) |
| Clientes | ✅ Pronto |
| Categorias | ✅ Pronto |
| Produtos | ✅ Pronto |
| Vendas | ✅ Pronto (carrinho com itens, total calculado no servidor) |
