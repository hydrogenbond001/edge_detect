#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "MQTTClient.h"

#define ADDRESS     "tcp://frp-end.com:20008" // 修改为你的broker地址
#define CLIENTID    "ExamplePublisher"
#define TOPIC       "test/topic"
#define PAYLOAD     "Hello MQTT from C"
#define QOS         1
#define TIMEOUT     10000L
int i;
int main() {
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    int rc;

    MQTTClient_create(&client, ADDRESS, CLIENTID, MQTTCLIENT_PERSISTENCE_NONE, NULL);

    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;

    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS) {
        printf("Failed to connect, return code %d\n", rc);
        exit(EXIT_FAILURE);
    }
	while(i<=10){
		
    MQTTClient_publish(client, TOPIC, strlen(PAYLOAD), PAYLOAD, QOS, 0, NULL);
    printf("Message%d published!\n",i++);
    
    }

    MQTTClient_disconnect(client, 10000);
    MQTTClient_destroy(&client);
    return rc;
}
