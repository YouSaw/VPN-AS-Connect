import vpnParser
import vpnConnector
import time
import subprocess



#TODO vielleicht ip mapping based on my database
def traceroute(ip):
    proc = subprocess.Popen(["sudo", "traceroute", "-T", "-n", "-A", ip], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = proc.communicate()
    stdout = stdout.decode()
    return stdout

def parse_asn_path(traceroute_output, ip):
    """
    :param traceroute_output: raw traceroute output
    :return: list of asn
    """
    asn_path = []
    for entry in traceroute_output.splitlines()[1:]:
        asn_list = entry[entry.find("[") + 1:entry.find("]")].split("/")
        asn_path.append(asn_list[0])
    print("[+] Path taken to",ip,":", asn_path)
    return asn_path



if __name__ == '__main__':
    to_trace = "google.de"
    vpnConnector.tunnel_to_as(9009)
    trace_output = traceroute(to_trace)
    asn_path = parse_asn_path(trace_output ,to_trace)
    vpnConnector.kill_vpn()
