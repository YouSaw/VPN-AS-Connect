import vpnParser
import vpnConnector


def build_ip_list(prefix, ip):
    pass

def traceroute(ip):
    pass

def parse_asn_path(traceroute_output):
    """

    :param traceroute_output: raw traceroute output
    :return: list of asn
    """
    pass

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


