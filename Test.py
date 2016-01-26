import socket
import struct

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t   '
DATA_TAB_2 = '\t\t   '
DATA_TAB_3 = '\t\t\t   '
DATA_TAB_4 = '\t\t\t\t   '


def get_mac_addr(mac_raw):
    byte_str = map('{:02x}'.format, mac_raw)
    mac_addr = ':'.join(byte_str).upper()
    return mac_addr


def Ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    print dest_mac
    print src_mac
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]


def get_ipv4_addr(bytes_addr):
    return socket.inet_ntoa(bytes_addr)


def IPv4_packet(data):
    version_header_length, ttl, proto, src, target = struct.unpack('! B 7x B B 2x 4s 4s', data[:20])

    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4

    return version, ttl, proto, get_ipv4_addr(src), get_ipv4_addr(target), data[20:]


def ICMP_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:]


def TCP_segment(data):
    (src_port, dest_port, sequence, ack, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) * 4

    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = (offset_reserved_flags & 1)

    return src_port, dest_port, sequence, ack, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]


def UDP_segment(data):
    (src_port, dest_port, checksum) = struct.unpack('! H H 2x H', data[:8])
    return src_port, dest_port, checksum, data[8:]


def main():
    # TODO: Get computer's ip through the config file

    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    conn.bind(("10.0.0.10", 0))

    # Include IP headers
    conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # receive all packages
    conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    print "Continue...."

    while True:
        raw_data, addr = conn.recvfrom(65535)

        version, ttl, proto, src, dest, data = IPv4_packet(raw_data)
        print('\nIP Packet:')
        print('Version: {}, Destination: {}, Source: {}, Next Protocol: {}'.format(version, dest, src, proto))

        if proto == 1:
            (icmp_type, code, checksum, data) = ICMP_packet(data)
            print TAB_1 + "ICMP Packet:"
            print (TAB_2 + 'icmp_type: {}, code: {}, checksum: {}'.format(icmp_type, code, checksum, data))

        elif proto == 6:
            (src_port, dest_port, sequence, ack,
             flag_urg,
             flag_ack,
             flag_psh,
             flag_rst,
             flag_syn,
             flag_fin,
             data) = TCP_segment(data)

            print TAB_1 + "TCP segment:"
            print (TAB_2 + 'src_port: {}, dest_port: {}'.format(src_port, dest_port, ))
            print (
                TAB_3 + 'flag_urg: {}, flag_ack: {}, flag_psh: {},flag_rst: {}, flag_syn: {}, flag_fin: {}'.format(
                    flag_urg,
                    flag_ack,
                    flag_psh,
                    flag_rst,
                    flag_syn,
                    flag_fin))

        elif proto == 17:
            (src_port, dest_port, length, data) = UDP_segment(data)
            print TAB_1 + "UDP segment:"
            print (TAB_2 + 'Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, length))

        else:
            print(TAB_1 + 'Other IPv4 Data...')


main()
