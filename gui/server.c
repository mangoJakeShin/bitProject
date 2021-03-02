#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
 
#define PORT 8888
 
char            data[7] = "Hello!";
int             serversock, clientsock;
void            quit(char* msg, int retval);
 
int main(int argc, char** argv)
{
    struct sockaddr_in      server, client;
    int                     accp_sock;
    int                     addrlen = sizeof(client);
    int                     bytes;
    int                     dataSize = sizeof(data);
    int                     from_client;
 
    printf("Data Size is : %d\n", dataSize);
 
    /* open socket */
    if ((serversock = socket(PF_INET, SOCK_STREAM, 0)) == -1) {
        quit("socket() failed", 1);
    }
 
    /* setup server's IP and port */
    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    server.sin_addr.s_addr = INADDR_ANY;
 
    /* bind the socket */
    if (bind(serversock, (const void*)&server, sizeof(server)) == -1) {
        quit("bind() failed", 1);
    }
 
    printf("start listen....\n");
    // wait for connection
    if(listen(serversock, 10) == -1){
        quit("listen() failed.", 1);
    }
    printf("client wait....\n");
 
    accp_sock = accept(serversock, (struct sockaddr *)&client, &addrlen);
    if(accp_sock < 0){
        quit("accept() failed", 1);
    }
 
    bytes = send(accp_sock, &data, dataSize, 0);
 
    if(bytes != dataSize){
        fprintf(stderr, "Connection closed. bytes->[%d], dataSize->[%d]\n",bytes, dataSize);
        close(accp_sock);
 
        if ((accp_sock = accept(serversock, NULL, NULL)) == -1) {
            quit("accept() failed", 1);
        }
    }
 
    // Data Receive
    // bytes re-init
    printf("Get Data from client\n");
    bytes = 0;
    for(i=0; i< sizeof(from_client); i+= bytes){
        if ((bytes = recv(sock, &from_client + i, sizeof(from_client) - i, 0)) == -1) {
            is_check = 0;
            quit("recv failed", 1);
        }
    }
    printf("Contents : %d\n, from_client");
 
    quit(NULL, 0);
}
 
void quit(char* msg, int retval)
{
    if (retval == 0) {
        fprintf(stdout, (msg == NULL ? "" : msg));
        fprintf(stdout, "\n");
    } else {
        fprintf(stderr, (msg == NULL ? "" : msg));
        fprintf(stderr, "\n");
    }
 
    if (clientsock) close(clientsock);
    if (serversock) close(serversock);
 
    exit(retval);
}