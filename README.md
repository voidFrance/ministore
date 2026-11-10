# MiniStore

Sistema web com objetivo didático desenvolvido com Flask + MariaDB.


## Pré-requisitos

- Python 3.x
- MariaDB instalado e rodando
- Git configurado

## Instalação

### 1. Clone o repositório do professor

```bash
git clone https://github.com/gutosolar72/ministore.git
cd ministore
```

### 2. Desvincule do repositório original e conecte ao seu

```bash
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/ministore.git
git push -u origin main
```

### 3. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure o banco de dados

```bash
python3 setup.py
```

### 6. Execute a aplicação

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
