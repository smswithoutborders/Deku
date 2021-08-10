#!/usr/bin/python3

''' testing criterias----
- when modem is present a broker should start up
    - should be able to receive messages from a producer
'''

import sys, os

import pika

sys.path.append(os.path.abspath(os.getcwd()))
from mmcli_python.modem import Modem

class Node:
    def __init__(self, m_index, queue_name='', exchange_type='direct'):
        ''' 
        queue_name : should be name of isp - no cus this would delete the entirty when 
        closed
        '''

        # TODO: put in config
        self.exchange='sms'
        self.m_index=m_index
        self.queue_name=queue_name
        self.exchange_type=exchange_type

        # TODO: put in config
        connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel=connection.channel()

        ''' listening exchange '''
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)

        ''' listening queue '''
        # result=channel.queue_declare(queue=queue_name, exclusive=True)
        self.channel.queue_declare(queue=self.queue_name)

        ''' bind queue to exchange '''
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name)

        ''' consumer properties '''
        ''' no auto_ack '''

        # TODO: delete this, ack should be manual
        self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=self.__callback, auto_ack=True)

        '''
        self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=self.__callback)
        '''

        ''' set fair dispatch '''
        # TODO: put in config
        self.channel.basic_qos(prefetch_count=1)

    def __callback(self, ch, method, properties, body):
        print(f'\t* message: {body}')

    def start_consuming(self):
        print(f'\t[{self.m_index}]* waiting for message...')
        self.channel.start_consuming()

if __name__ == "__main__":
    ''' - when modem open worker
        - when no worker close worker
    '''
    def available_modem():
        return Modem.list()

    # indexes=available_modem()
    indexes=['1']
    print('* starting brokers for modems with indexes:', indexes)

    for m_index in indexes:
        # isp_name=Tools.ISP.modem('cameroon', '')
        isp_name="MTN1"
        print('\t* starting broker for:', m_index, isp_name)
        node=Node(m_index, isp_name)
        node.start_consuming()