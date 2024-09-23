import psutil
import platform
from datetime import datetime
import GPUtil
from tabulate import tabulate

# Função para converter bytes em formato legível
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

# Função para coletar informações do sistema
def get_system_info():
    uname = platform.uname()
    system_info = [
        ["Sistema", uname.system],
        ["Nome do Computador", uname.node],
        ["Versão", uname.release],
        ["Versão do Sistema", uname.version],
        ["Máquina", uname.machine],
        ["Processador", uname.processor]
    ]
    print(tabulate(system_info, headers=["Descrição", "Informação"], tablefmt="fancy_grid"))

# Função para obter o tempo de inicialização
def get_boot_time():
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Hora de Inicialização: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

# Função para coletar informações da CPU
def get_cpu_info():
    cpufreq = psutil.cpu_freq()
    cpu_info = [
        ["Físicos", psutil.cpu_count(logical=False)],
        ["Lógicos", psutil.cpu_count(logical=True)],
        ["Máx. Frequência", f"{cpufreq.max:.2f}Mhz"],
        ["Mín. Frequência", f"{cpufreq.min:.2f}Mhz"],
        ["Frequência Atual", f"{cpufreq.current:.2f}Mhz"]
    ]
    print(tabulate(cpu_info, headers=["Descrição", "Informação"], tablefmt="fancy_grid"))

    print("\nUso da CPU por núcleo:")
    cpu_cores = [[f"Núcleo {i}", f"{percentage}%"] for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1))]
    print(tabulate(cpu_cores, headers=["Núcleo", "Uso"], tablefmt="fancy_grid"))
    
    print(f"\nUso Total da CPU: {psutil.cpu_percent()}%")

# Função para coletar informações da memória
def get_memory_info():
    svmem = psutil.virtual_memory()
    memory_info = [
        ["Total", get_size(svmem.total)],
        ["Disponível", get_size(svmem.available)],
        ["Usado", get_size(svmem.used)],
        ["Percentual", f"{svmem.percent}%"]
    ]
    print(tabulate(memory_info, headers=["Descrição", "Memória"], tablefmt="fancy_grid"))

    swap = psutil.swap_memory()
    swap_info = [
        ["Total", get_size(swap.total)],
        ["Disponível", get_size(swap.free)],
        ["Usado", get_size(swap.used)],
        ["Percentual", f"{swap.percent}%"]
    ]
    print("\nInformações da Memória Swap:")
    print(tabulate(swap_info, headers=["Descrição", "Memória"], tablefmt="fancy_grid"))

# Função para coletar informações dos discos
def get_disk_info():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"\n=== Partição: {partition.device} ===")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            partition_info = [
                ["Ponto de Montagem", partition.mountpoint],
                ["Sistema de Arquivos", partition.fstype],
                ["Total", get_size(partition_usage.total)],
                ["Usado", get_size(partition_usage.used)],
                ["Livre", get_size(partition_usage.free)],
                ["Percentual", f"{partition_usage.percent}%"]
            ]
            print(tabulate(partition_info, headers=["Descrição", "Informação"], tablefmt="fancy_grid"))
        except PermissionError:
            continue
    
    disk_io = psutil.disk_io_counters()
    disk_io_info = [
        ["Total de Leitura", get_size(disk_io.read_bytes)],
        ["Total de Escrita", get_size(disk_io.write_bytes)]
    ]
    print("\nEstatísticas de IO do Disco:")
    print(tabulate(disk_io_info, headers=["Descrição", "Informação"], tablefmt="fancy_grid"))

# Função para coletar informações da rede
def get_network_info():
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        print(f"\n=== Interface: {interface_name} ===")
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                net_info = [
                    ["IP", address.address],
                    ["Máscara de Sub-rede", address.netmask],
                    ["Broadcast IP", address.broadcast]
                ]
                print(tabulate(net_info, headers=["Descrição", "Informação"], tablefmt="fancy_grid"))
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                net_info = [
                    ["MAC", address.address],
                    ["Broadcast MAC", address.broadcast]
                ]
                print(tabulate(net_info, headers=["Descrição", "Informação"], tablefmt="fancy_grid"))

    net_io = psutil.net_io_counters()
    net_io_info = [
        ["Total de Bytes Enviados", get_size(net_io.bytes_sent)],
        ["Total de Bytes Recebidos", get_size(net_io.bytes_recv)]
    ]
    print("\nEstatísticas de IO de Rede:")
    print(tabulate(net_io_info, headers=["Descrição", "Informação"], tablefmt="fancy_grid"))

# Função para coletar informações da GPU
def get_gpu_info():
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        list_gpus.append([
            gpu.id, gpu.name, f"{gpu.load*100}%", f"{gpu.memoryFree}MB", 
            f"{gpu.memoryUsed}MB", f"{gpu.memoryTotal}MB", 
            f"{gpu.temperature} °C", gpu.uuid
        ])

    print("\nInformações da GPU:")
    print(tabulate(list_gpus, headers=("ID", "Nome", "Carga", "Memória Livre", "Memória Usada", "Memória Total", "Temperatura", "UUID"), tablefmt="fancy_grid"))

# Função principal para exibir todas as informações
def main():
    print("="*40, "Informações do Sistema", "="*40)
    get_system_info()
    print("="*40, "Hora de Inicialização", "="*40)
    get_boot_time()
    print("="*40, "Informações da CPU", "="*40)
    get_cpu_info()
    print("="*40, "Informações da Memória", "="*40)
    get_memory_info()
    print("="*40, "Informações do Disco", "="*40)
    get_disk_info()
    print("="*40, "Informações de Rede", "="*40)
    get_network_info()
    print("="*40, "Informações da GPU", "="*40)
    get_gpu_info()

if __name__ == "__main__":
    main()
input("Aperte ENTER para fechar.")