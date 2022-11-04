//Autors : Ilan Souffir and Ben Cohen
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <errno.h>

#define PORT 5060

int fd;
struct stat file_stat;

int main(int argc, char **argv) {
    char buf[256];
    socklen_t len;
    socklen_t length;
    int file_num = 1;

    for (int j = 0; j < 2; j++) {
        if (j == 0) {
            strcpy(buf, "cubic");
        } else {
           strcpy(buf, "reno");
        }

        for (int i = 0; i < 5; i++) {

            int sock = socket(AF_INET, SOCK_STREAM, 0);
            if (sock == -1) {
                perror("failed to open socket");
                return -1;
            }

            if(i == 0)
            printf("Socket is opened...\n");

            len = sizeof(buf);
	    length = sizeof(buf);
	    
	    if (j == 1) length = strlen(buf);

            if (setsockopt(sock, IPPROTO_TCP, TCP_CONGESTION, buf, length) != 0) {
                perror("setsockopt");
                return -1;
            }

            if (getsockopt(sock, IPPROTO_TCP, TCP_CONGESTION, buf, &len) != 0) {
                perror("getsockopt");
                return -1;
            }

            struct sockaddr_in server_addr;
            memset(&server_addr, 0, sizeof(server_addr));
            server_addr.sin_family = AF_INET;
            server_addr.sin_port = htons(PORT);

            int flag = connect(sock, (struct sockaddr *) &server_addr, sizeof(server_addr));

//          Sending file 5 times
            FILE *file_ptr = fopen("1mb.txt", "rb");
            if (file_ptr == NULL) {
                fprintf(stderr, "Error opening file");
                return 1;
            }
            fd = open("1mb.txt", O_RDONLY);
            if (fd == -1) {
                fprintf(stderr, "Error opening file: %s", strerror(errno));

                exit(EXIT_FAILURE);
            }

            // get permit from server to sent the file
            char getReply[10];
            bzero(getReply, sizeof(getReply));
            read(sock, getReply, sizeof(getReply));
            if (strcmp(getReply, "Accept") == 0) {
                printf("Server accepted...\nWaiting for file to be sent...\n");
            } 

            char buffer[100];
            int b;
            int bytes = 0;

            while (!feof(file_ptr)){
                b = fread(buffer, 1, sizeof(buffer), file_ptr);
                int bytes_sent = send(sock, buffer, b, 0);
                bytes += bytes_sent;
            }

            printf("Sending file number %d (%d bytes) \n\n", file_num++, bytes);
            sleep(1);

            close(sock);
        }
    }
    return 0;
}
