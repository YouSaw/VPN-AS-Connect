import vpnParser
import subprocess
import time

from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read


def vpn_in_asrange(asn):
    server_list = vpnParser.get_server_by_asn(asn)
    return server_list

def tunnel_to_as(asn):
    server_list = vpn_in_asrange(asn)
    if len(server_list) == 0:
        print("[-] There is no server in this as range!")
        return False
    for entry in server_list:
        is_connected = connect_to(entry)
        if is_connected:
            print("[+] Connection was made!")
            return True
    print("[-] Could not connect a server out of",len(server_list),"servers!")
    return False


def connect_to(vpn):
    try:
        proc = subprocess.Popen(["sudo", "openpyn", "-s",vpn],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        flags = fcntl(proc.stdout, F_GETFL)  # get current p.stdout flags
        fcntl(proc.stdout, F_SETFL, flags | O_NONBLOCK)

        output_string = ""
        time.sleep(5)
        while True:
            try:
                substring = read(proc.stdout.fileno(), 100).decode()
                output_string += substring
                print(substring, end="") #Debug
                time.sleep(1)
            except OSError:
                break

        print(output_string) #Debug
        if "completed" in output_string:
            return  True
        return False

    except subprocess.CalledProcessError as openvpn_err:
        print("[-] Connection error",openvpn_err.output)
        return False

def kill_vpn():
    subprocess.run(["sudo", "openpyn", "-k"], stdout=subprocess.DEVNULL)
    print("[!] Killed the running openvpn process!")
    time.sleep(1)

if __name__ == '__main__':
    #kill_vpn()
    tunnel_to_as(9009)

