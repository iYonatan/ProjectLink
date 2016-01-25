import socket
import struct


def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()


def Ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]


def get_ipv4_addr(bytes_addr):
    return '.'.join(map(str, bytes_addr))


def IPv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return ttl, proto, get_ipv4_addr(src), get_ipv4_addr(target), data[20:]


def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    conn.bind(("10.92.5.59", 0))

    # Include IP headers
    conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # receive all packages
    conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    print "Continue...."

    while True:
        raw_data, addr = conn.recvfrom(65535)

        dest_mac, src_mac, proto, data = Ethernet_frame(raw_data)
        print('\nEthernet Frame:')
        print('Destination: {}, Source: {}, Protocol: {}'.format(dest_mac, src_mac, proto))


main()
