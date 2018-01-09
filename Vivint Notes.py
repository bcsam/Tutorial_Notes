'''send.py'''
import pika

#replace localhost with IP address to use different machine
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

#create the queue
channel.queue_declare(queue="queue's name", durable=True)

#default exchange
channel.basic_publish(exchange='',
                      routing_keys='hello', #pass the queue's name if default exchange
                      body='Hello World!', #the message to be sent
                      properties=pika.BasicProperties(
                          delivery_mode = 2, #makes the messages persistent
                      ))
#print to say that you sent
connection.close()


'''receive.py'''
#replace localhost with IP address to use different machine
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

#good practice to declare the queue in both send and receive
channel.queue_declare(queue="queue's name", durable=True)

#tells RabbitMQ to not give more than one message to a worker at a time
#don't dispatch new message until worker has processed and acknowledged previous
channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback_func_name,
                      queue="queue's name",
                      no_ack=True) #turns acknowledgements off

channel.start_consuming() #

def callback_func_name(channel, method, properties, body):
    pass

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

def callback(ch, method, properties, body):
    #do your work here

    ch.basic_ack(delivery_tag = method.delivery_tag) #do not forget this!!
channel.basic_consume(callback, queue="queue's name")