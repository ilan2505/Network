//Ilan Meyer Souffir and Ben Cohen
#include<netinet/in.h>
#include<stdio.h>
#include<string.h>
#include<netinet/ip_icmp.h>
#include<netinet/ip.h>
#include<net/ethernet.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include <linux/if_packet.h>
#include <unistd.h>


void sniffer(char *buf) {

    struct iphdr *iph = (struct iphdr *) (buf + sizeof(struct ethhdr));
    struct sockaddr_in sniff_sock; //internet socket

    if (iph->protocol == IPPROTO_ICMP) {  //put icmp protocol in ip protocol attribute
        printf("\nICMP PACKET SNIFFED\n");
        unsigned int iphdrlen = iph->ihl * 4;  

        sniff_sock.sin_addr.s_addr = iph->saddr;
        printf("IP_SRC : %s\n", inet_ntoa(sniff_sock.sin_addr)); //prints the ip source of the icmp packet

        sniff_sock.sin_addr.s_addr = iph->daddr;
        printf("IP_DST : %s\n", inet_ntoa(sniff_sock.sin_addr)); //prints the ip destination of the icmp packet

        struct icmphdr *icmph = (struct icmphdr *) (buf + iphdrlen + sizeof(struct ethhdr));

        uint8_t type = icmph->type;
        printf("TYPE : %d", type); //prints the type of the icmp packet
        if (type == 8) {
            printf(" Echo request\n");
        }
        if (type == 0) {
            printf(" Echo reply\n");
        }
        printf("CODE : %d\n", icmph->code); //prints the code of the icmp packet
    }
}

int main() {
    int pack_len = IP_MAXPACKET;
    struct sockaddr saddr;

    // Creates the raw socket 
    int sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));

    if (sock == -1) {
        perror("sock Error");
        return 1;
    }

    while (1) {
        char buff[IP_MAXPACKET] = {0}; //collect the packet one at a time

        size_t sizeof_addres = sizeof(saddr);
        int packet_size = recvfrom(sock, buff, pack_len, 0, &saddr, (socklen_t *) &sizeof_addres); //receive the packet from raw socket

        if (packet_size >= 0){
            sniffer(buff);
        }
    }
    close(sock);
    return 0;
}


