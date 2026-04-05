import socket, threading, argparse, json
from tqdm import tqdm

lock = threading.Lock()

portas_abertas = []
PORTAS_COMUNS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 5432, 6379, 8080, 8443, 27017]


def salvar_json(host):
    dados = {"host": host, "portas": portas_abertas}
    with open("resultado.json", "w") as f:
        json.dump(dados, f, indent=4)
    print("Resultado salvo em resultado.json")

def scan_port(host, porta, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    resultado = s.connect_ex((host, porta))

    if resultado == 0:
        try:
            banner = s.recv(1024).decode(errors="ignore").strip()
        except:
            banner = ""
    s.close()        
    if resultado == 0:
        return True, banner
    return False, "" 

def checar_porta(host, porta, timeout, semaforo):
    with semaforo:
        resultado, banner = scan_port(host, porta, timeout)
        if resultado == True:
            with lock:
                try:
                    servico = socket.getservbyport(porta)
                except:
                    servico = "Desconhecido"

                print(f"Porta {porta} ({servico}): Aberta | Banner: {banner}" if banner else f"Porta {porta} ({servico}): Aberta")
                portas_abertas.append({"porta": porta, "servico": servico, "banner": banner})

def scan_range(host, porta_inicio, porta_fim, timeout, semaforo):
    threads = []
    for porta in range(porta_inicio, porta_fim + 1):
        t = threading.Thread(target=checar_porta, args=(host, porta, timeout, semaforo))
        t.start()
        threads.append(t)

    for t in tqdm(threads):
        t.join()
    print("Scan finalizado")
    print(f"Portas abertas: {sorted([p['porta'] for p in portas_abertas])}")
    salvar_json(host)

def scan_quick(host, timeout, semaforo):
    threads = []
    for porta in PORTAS_COMUNS:
        t = threading.Thread(target=checar_porta, args=(host, porta, timeout, semaforo))
        t.start()
        threads.append(t)

    for t in tqdm(threads):
        t.join()
    print("Scan finalizado")
    print(f"Portas abertas: {sorted([p['porta'] for p in portas_abertas])}")
    salvar_json(host)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout em segundos")
    parser.add_argument("host", help="Host a escanear")
    parser.add_argument("porta_inicio", nargs="?", help="...")
    parser.add_argument("porta_fim", nargs="?", help="...")
    parser.add_argument("--threads", type=int, default=100, help="Número máximo de threads simultâneas")
    parser.add_argument("--quick", action="store_true", help="Escaneia apenas portas comuns")
    args = parser.parse_args()
    semaforo = threading.Semaphore(args.threads)
    if args.quick:
        scan_quick(args.host, args.timeout, semaforo)
    else:
        scan_range(args.host, args.porta_inicio, args.porta_fim, args.timeout, semaforo)