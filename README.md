# Port Scanner

Scanner de portas TCP feito em Python com suporte a threading, banner grabbing e exportação em JSON.

## Funcionalidades

- Scan por range de portas
- Modo rápido com portas mais comuns (`--quick`)
- Banner grabbing automático
- Barra de progresso com `tqdm`
- Controle de threads simultâneas
- Exportação automática em JSON
- Timeout configurável

## Instalação
```bash
git clone https://github.com/Vini-Labs/port-scanner.git
cd port-scanner
pip install -r requirements.txt
```

## Uso
```bash
python scanner.py <host> <porta_inicio> <porta_fim> [opções]
```

## Opções

| Argumento | Descrição | Padrão |
|---|---|---|
| `--quick` | Escaneia apenas portas comuns | False |
| `--timeout` | Timeout por porta em segundos | 1.0 |
| `--threads` | Máximo de threads simultâneas | 100 |

## Exemplos
```bash
# Range de portas
python scanner.py google.com 1 1000

# Modo rápido
python scanner.py google.com --quick

# Com opções
python scanner.py google.com --quick --timeout 0.5 --threads 50
```

## Aviso Ético

Esta ferramenta é apenas para fins educacionais e testes em ambientes que você possui autorização. O uso não autorizado pode ser ilegal.