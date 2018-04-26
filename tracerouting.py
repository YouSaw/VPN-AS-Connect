import vpnParser
import vpnConnector
import time
import subprocess
#Today:
#Python3 Support for BGP
#Abgegriffene Daten Analysieren
#Own Database / Lookup Sites?
#Sutruktur BA verfeinern



def build_ip_list(prefix, ip):
    pass

def traceroute(ip):
    proc = subprocess.Popen(["sudo", "traceroute", "-T", "-n", "-A", ip], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = proc.communicate()
    stdout = stdout.decode()
    return stdout

def parse_asn_path(traceroute_output):
    """
    :param traceroute_output: raw traceroute output
    :return: list of asn
    """
    asn_path = []
    for entry in traceroute_output.splitlines()[1:]:
        asn_list = entry[entry.find("[") + 1:entry.find("]")].split("/")
        asn_path.append(asn_list[0])
    print("[+] Path taken: ", asn_path)
    return asn_path


#Policen überlegen
def validate_ip_path(taken_asn_path, announced_asn_path,  missing_link_list, prefix_owners):

    """
    Validates the ip path taken vs. the the announced path.
    Needs research!!!
    :param taken_asn_path: list of asn (path taken)
    :param announced_asn_path list: of asn (path announced)
    :param missing_link_list: list of asn tuples representing a link. [[ip1,ip2],[ip2,ip3],[ip4,ip5]]
    :param prefix_owners: list of ips that should be owning the prefix
    :returns
    :returns
    """
    pass


if __name__ == '__main__':
    traceroute("google.de")