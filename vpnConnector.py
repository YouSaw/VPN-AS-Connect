import vpnParser
import subprocess
#Used to connect/kill VPN


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
        subprocess.run(["sudo", "openpyn", "-s",vpn], check=True, shell=True)
    except subprocess.CalledProcessError as openvpn_err:
        print("[-] Connection error",openvpn_err.output)
        return False
    return True

def kill_vpn():
    pass

