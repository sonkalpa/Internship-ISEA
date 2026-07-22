#include <arpa/inet.h>
#include <errno.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define ROLL_NO "CS-BTC24-08"
#define BUFFER_SIZE 65536

#ifndef TH_ECE
#define TH_ECE 0x40
#endif

#ifndef TH_CWR
#define TH_CWR 0x80
#endif

static int assigned_protocol_from_roll(const char *roll_no) {
    int last_digit = -1;
    size_t i;

    for (i = 0; roll_no[i] != '\0'; i++) {
        if (roll_no[i] >= '0' && roll_no[i] <= '9') {
            last_digit = roll_no[i] - '0';
        }
    }

    if (last_digit < 0) {
        return IPPROTO_ICMP;
    }

    if (last_digit <= 3) {
        return IPPROTO_ICMP;
    }
    if (last_digit <= 6) {
        return IPPROTO_UDP;
    }
    return IPPROTO_TCP;
}

static const char *protocol_name(int proto) {
    if (proto == IPPROTO_ICMP) {
        return "ICMP";
    }
    if (proto == IPPROTO_UDP) {
        return "UDP";
    }
    if (proto == IPPROTO_TCP) {
        return "TCP";
    }
    return "UNKNOWN";
}

static void tcp_flags_to_text(unsigned int flags, char *out, size_t out_len) {
    struct {
        unsigned int bit;
        const char *name;
    } flag_map[] = {
        {TH_SYN, "SYN"},
        {TH_ACK, "ACK"},
        {TH_FIN, "FIN"},
        {TH_RST, "RST"},
        {TH_PUSH, "PSH"},
        {TH_URG, "URG"},
        {TH_ECE, "ECE"},
        {TH_CWR, "CWR"},
    };

    size_t i;
    int wrote = 0;

    out[0] = '\0';

    for (i = 0; i < sizeof(flag_map) / sizeof(flag_map[0]); i++) {
        if ((flags & flag_map[i].bit) != 0U) {
            if (wrote) {
                strncat(out, "|", out_len - strlen(out) - 1U);
            }
            strncat(out, flag_map[i].name, out_len - strlen(out) - 1U);
            wrote = 1;
        }
    }

    if (!wrote) {
        strncat(out, "NONE", out_len - strlen(out) - 1U);
    }
}

int main(int argc, char *argv[]) {
    int capture_target = 20;
    int assigned_proto = assigned_protocol_from_roll(ROLL_NO);
    int sockfd;
    unsigned char buffer[BUFFER_SIZE];
    int captured = 0;

    if (argc == 2) {
        capture_target = atoi(argv[1]);
        if (capture_target <= 0) {
            fprintf(stderr, "Invalid packet count: %s\n", argv[1]);
            return 1;
        }
    }

    sockfd = socket(AF_INET, SOCK_RAW, assigned_proto);
    if (sockfd < 0) {
        perror("socket");
        fprintf(stderr, "Hint: run with sudo/root privileges.\n");
        return 1;
    }

    printf("ROLL_NO=%s\n", ROLL_NO);
    printf("ASSIGNED_PROTOCOL=%s\n\n", protocol_name(assigned_proto));

    while (captured < capture_target) {
        ssize_t data_size;
        struct sockaddr_in src_addr;
        socklen_t src_len = sizeof(src_addr);
        struct iphdr *ip_header;
        char src_ip[INET_ADDRSTRLEN];
        char dst_ip[INET_ADDRSTRLEN];

        data_size = recvfrom(
            sockfd,
            buffer,
            sizeof(buffer),
            0,
            (struct sockaddr *)&src_addr,
            &src_len
        );
        if (data_size < 0) {
            if (errno == EINTR) {
                continue;
            }
            perror("recvfrom");
            close(sockfd);
            return 1;
        }

        ip_header = (struct iphdr *)buffer;
        if (ip_header->protocol != assigned_proto) {
            continue;
        }

        inet_ntop(AF_INET, &ip_header->saddr, src_ip, sizeof(src_ip));
        inet_ntop(AF_INET, &ip_header->daddr, dst_ip, sizeof(dst_ip));

        captured++;
        printf("PACKET_NO=%d\n", captured);
        printf("SRC_IP=%s\n", src_ip);
        printf("DST_IP=%s\n", dst_ip);
        printf("PROTOCOL=%s\n", protocol_name(ip_header->protocol));
        printf("PROTOCOL_NO=%d\n", ip_header->protocol);
        printf("TTL=%u\n", ip_header->ttl);
        printf("PACKET_SIZE=%zd\n", data_size);
        printf("IP_IDENTIFICATION=%u\n", ntohs(ip_header->id));

        if (assigned_proto == IPPROTO_TCP) {
            struct tcphdr *tcp_header;
            unsigned int ip_header_len = (unsigned int)ip_header->ihl * 4U;
            char flag_text[64];

            if ((ssize_t)(ip_header_len + sizeof(struct tcphdr)) > data_size) {
                printf("TCP_SRC_PORT=NA\n");
                printf("TCP_DST_PORT=NA\n");
                printf("TCP_FLAGS=NA\n\n");
                continue;
            }

            tcp_header = (struct tcphdr *)(buffer + ip_header_len);
            tcp_flags_to_text(tcp_header->th_flags, flag_text, sizeof(flag_text));

            printf("TCP_SRC_PORT=%u\n", ntohs(tcp_header->th_sport));
            printf("TCP_DST_PORT=%u\n", ntohs(tcp_header->th_dport));
            printf("TCP_FLAGS=%s\n\n", flag_text);
        } else {
            printf("ADDITIONAL_FIELD=Not Implemented for this protocol in this build\n\n");
        }
    }

    close(sockfd);
    return 0;
}
