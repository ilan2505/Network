//Autors : Ilan Souffir and Ben Cohen
#include<stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>

#define PORT 5060  

int main() {
    char buff[100];
    struct sockaddr_in server_addr;
    struct sockaddr_in client_addr;  
    socklen_t client_addr_len = sizeof(client_addr);

//  Openning new socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("failed to open socket");
        return -1;
    }
    printf("Socket opened...\n");

//  Listening to connections
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);

//  Binding the socket to the port with any IP at this port
    int b = bind(sock, (struct sockaddr *) &server_addr, sizeof(server_addr));
    if (b == -1) {
        printf("Binding failed with error code : %d", errno);
        return -1;
    }
    printf("Binding was successful!\n");

    // Socket listening
    int flag = listen(sock, 500);
    if (flag == -1) {
        printf("Listening failed with error code : %d", errno);
        return -1;
    }

    printf("Waiting for TCP-connections...\n\n");

    
    for (int i = 0; i < 2; i++) {
        int bytes_sent = 0;
        int file = 1;
        double time = 0;
        while (file <= 5) {
            memset(&client_addr, 0, sizeof(client_addr));
            int client_sock = accept(sock, (struct sockaddr *) &client_addr, &client_addr_len);
            if (client_sock == -1) {
                printf("Accepting failed with error code : %d", errno);
                close(sock);
                return -1;
            }

            int bytes;            
            char reply[10] = "Accept"; 
            write(client_sock, reply, sizeof(reply));

            struct timeval stop, start;
            gettimeofday(&start, NULL);

            int bytes_sent = 0;
		    while ((bytes = recv(client_sock, buff, 100, 0)) != 0)
		    {
		    	bytes_sent += bytes;
		    }

            gettimeofday(&stop, NULL);
            double dt = (double) ((stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec) / 1000000;
            time += dt;

            if (bytes_sent == 1048576) {
                printf("Received %d bytes from file %d in %f seconds\n", bytes_sent, file++, dt);
            } 
            bytes_sent = 0;
            buff[bytes] = '\0';
            sleep(1);

        }

//      Calculate the average
        double avg_time = time / 5;
        if (i == 0)
            printf("\nAverage time for Cubic algorithm is: %f \n\n", avg_time);
        else
            printf("\n\nAverage time for Reno algorithm is: %f\n\n", avg_time);
    }

    close(sock);
    return 0;
}
