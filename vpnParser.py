import sys
import requests
import subprocess
from colorama import Fore, Style
from openpyn import root
import time

__basefilepath__ = "/usr/local/lib/python3.5/dist-packages/openpyn/"

def update_config_files():
    root.verify_root_access("Root access needed to write files in " +
                            "'" + __basefilepath__ + "files/" + "'")
    try:
        subprocess.check_call(
            ["sudo", "wget", "https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip", "-P", __basefilepath__])
    except subprocess.CalledProcessError:
        print(
            Fore.RED + "Exception occured while wgetting zip, is the internet working? \
            is nordcdn.com blocked by your ISP or Country?, If so use Privoxy \
            [https://github.com/jotyGill/openpyn-nordvpn/issues/109]" + Style.RESET_ALL)
        sys.exit()
    try:
        subprocess.check_call(
            ["sudo", "unzip", "-u", "-o", __basefilepath__ + "ovpn", "-d", __basefilepath__ + "files/"],
            stderr=subprocess.DEVNULL)
        subprocess.check_call(
            ["sudo", "rm", __basefilepath__ + "ovpn.zip"])
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(
                ["sudo", "rm", "-rf", __basefilepath__ + "files/ovpn_udp"])
            subprocess.check_call(
                ["sudo", "rm", "-rf", __basefilepath__ + "files/ovpn_tcp"])
            subprocess.check_call(
                ["sudo", "unzip", __basefilepath__ + "ovpn", "-d", __basefilepath__ + "files/"])
            subprocess.check_call(
                ["sudo", "rm", __basefilepath__ + "ovpn.zip"])
        except subprocess.CalledProcessError:
            print(Fore.RED + "Exception occured while unzipping ovpn.zip, is unzip installed?" +
                  Style.RESET_ALL)
            sys.exit()

# Using requests, GETs and returns json from a url.
def get_json(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

    try:
        json_response = requests.get(url, headers=headers).json()
    except requests.exceptions.HTTPError:
        print("Cannot GET the json from nordvpn.com, Manually Specify a Server\
        using '-s' for example '-s au10'")
        sys.exit()
    except requests.exceptions.RequestException:
        print("There was an ambiguous exception, Check Your Network Connection.",
              "forgot to flush iptables? (openpyn -x)")
        sys.exit()
    return json_response


# Gets json data, from api.nordvpn.com. filter servers by protocoll.
def get_server_data_from_api(tcp):

    url = "https://api.nordvpn.com/server"
    json_response = get_json(url)
    remaining_servers = []

    for res in json_response:
        # when connecting using TCP only append if it supports OpenVPN-TCP
        if tcp is True and res["features"]["openvpn_tcp"] is True:
            remaining_servers.append([res['ip_address'],res["domain"][:res["domain"].find(".")], res["load"]])
        # when connecting using TCP only append if it supports OpenVPN-TCP
        elif tcp is False and res["features"]["openvpn_udp"] is True:
            remaining_servers.append([res['ip_address'],res["domain"][:res["domain"].find(".")], res["load"]])

    return remaining_servers

#Check if config is localy avaiable
def get_vpn_server_ip(server, port):
    # grab the ip address of vpnserver from the config file
    if port == "tcp":
        folder = "ovpn_tcp/"
    else:
        folder = "ovpn_udp/"

    vpn_config_file = __basefilepath__ + "files/" + folder + server + \
        ".nordvpn.com." + port + ".ovpn"
    with open(vpn_config_file, 'r') as openvpn_file:
        for line in openvpn_file:
            if "remote " in line:
                vpn_server_ip = line[7:]
                vpn_server_ip = vpn_server_ip[:vpn_server_ip.find(" ")]
        openvpn_file.close()
        return vpn_server_ip

def ip_asn_writeup(ip_list):
    #NEED RESEARCH
    #REQUEST FORMAT?
    for entry in ip_list:
        pass

#Create SQLite Database With SERVER/ASN mapping
def server_asn_writeup(tcp):
    update_config_files()
    protokoll = "tcp"
    if tcp == False:
        protokoll = "udp"

    server_data = get_server_data_from_api(tcp=tcp)
    for entry in server_data:
        try:
            if entry[0] != get_vpn_server_ip(entry[1], protokoll):
                continue
            #PARSING
        except FileNotFoundError:
            continue


#Testing
if __name__ == '__main__':
    server_data = get_server_data_from_api(tcp=False)
    for entry in server_data:
        if entry[0] != get_vpn_server_ip(entry[1],"udp"):
            "Problem!!!"

