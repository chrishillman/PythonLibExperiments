import sys
from socket import *
from struct import *

host = gethostbyname(gethostname())
try:
  s=socket(AF_INET, SOCK_RAW)
  s.bind((host,0))
  s.ioctl(SIO_RCVALL, RCVALL_ON)
except:
  s=socket(AF_INET, SOCK_RAW, IPPROTO_TCP)

while True:
  packet = s.recvfrom(65565)

  packet = packet[0]
  ip_header = packet[0:20]
  iph = unpack('!BBHHHBBH4s4s' , ip_header)
  version_ihl = iph[0]
  version = version_ihl >> 4
  ihl = version_ihl & 0xF
  iph_length = ihl * 4
  ttl = iph[5]
  protocol = iph[6]
  s_addr = inet_ntoa(iph[8]);
  d_addr = inet_ntoa(iph[9]);

  print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
  tcp_header = packet[iph_length:iph_length+20]
  tcph = unpack('!HHLLBBHHH' , tcp_header)
  source_port = tcph[0]
  dest_port = tcph[1]
  sequence = tcph[2]
  acknowledgement = tcph[3]
  doff_reserved = tcph[4]
  print "TCP Header: " + tcp_header
  print "My data (Binary Flags):  " + str(bin(tcph[5])[2:]) + " or " + str(tcph[5])

  tcph_length = doff_reserved >> 4
  print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
  h_size = iph_length + tcph_length * 4
  data_size = len(packet) - h_size
  data = packet[h_size:]
  print 'Data : ' + data
  print
