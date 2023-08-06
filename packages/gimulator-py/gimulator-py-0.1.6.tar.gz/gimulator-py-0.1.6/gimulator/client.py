from os import environ
import logging
from socket import getaddrinfo, gaierror
from time import sleep

from gimulator.proto_pb2_grpc import *
from gimulator.proto_pb2 import *
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

logger = logging.getLogger('Gimulator Client')


def check_dns(domain, port):
    def wrapper(func):
        def inner(self, *args, **kwargs):
            while True:
                try:
                    logger.warning("Waiting for Gimulator server to run on domain %s and port %d..." % (domain, port))
                    getaddrinfo(domain, port)
                    break
                except gaierror:
                    sleep(1)
            return func(self, *args, **kwargs)
        return inner
    return wrapper


def wait_for_dns(domain, port):
    while True:
        try:
            getaddrinfo(domain, port)
            break
        except gaierror:
            logger.warning("Failed to resolve DNS for Gimulator.\n%s and port %d...\nRetrying ..." % (domain, port))
            sleep(1)


class GimulatorClient:
    domain = None
    port = None
    client_token = None
    channel = None
    api = None
    metadata = None

    def __init__(self, wait_until_connected=True, **kwargs):
        # host = environ['GIMULATOR_HOST']
        host = kwargs['host'] if 'host' in kwargs else environ['GIMULATOR_HOST']
        # self.client_token = client_token = environ['GIMULATOR_TOKEN']
        self.client_token = client_token = kwargs['token'] if 'token' in kwargs else environ['GIMULATOR_TOKEN'] 
        logger.debug("Client token is " + client_token)
        self.metadata = (('token', client_token),)

        self.domain, port = host.split(':')
        self.port = int(port)
        if wait_until_connected:
            wait_for_dns(self.domain, self.port)  # FIXME this is irritating! Someone please fix this...

        self.channel = grpc.insecure_channel(host, options=(('grpc.enable_http_proxy', 0),))
        self.api = MessageAPIStub(self.channel)
        logger.info("Client connected!")

    def Get(self, key: Key):
        wait_for_dns(self.domain, self.port)  # FIXME this is irritating! Someone please fix this...
        return self.api.Get(key, metadata=self.metadata)

    def GetAll(self, key: Key):
        wait_for_dns(self.domain, self.port)  # FIXME this is irritating! Someone please fix this...
        return self.api.GetAll(key, metadata=self.metadata)

    def Put(self, message: Message):
        wait_for_dns(self.domain, self.port)  # FIXME this is irritating! Someone please fix this...
        return self.api.Put(message, metadata=self.metadata)

    def Delete(self, message: Message):
        wait_for_dns(self.domain, self.port)  # FIXME this is irritating! Someone please fix this...
        return self.api.Delete(message, metadata=self.metadata)

    def DeleteAll(self, message: Message):
        wait_for_dns(self.domain, self.port)  # FIXME this is irritating! Someone please fix this...
        return self.api.DeleteAll(message, metadata=self.metadata)

    def Watch(self, key: Key):
        wait_for_dns(self.domain, self.port)  # FIXME this is irritating! Someone please fix this...
        return self.api.Watch(key, metadata=self.metadata)


class DirectorClient(GimulatorClient):
    director_api = None

    def __init__(self, wait_until_connected=True, **kwargs):
        super().__init__(wait_until_connected, **kwargs)
        self.director_api = DirectorAPIStub(self.channel)

    def WaitUntilReady(self):
        while True:
            sleep(2)

            logger.warning("Getting users...")

            try:
                users = list(self.GetActors())
                if len(users) == 1:
                    return
            except grpc._channel._MultiThreadedRendezvous:  # FIXME this is irritating! Someone please fix this...
                logger.warning("Cannot resolve Gimulator host! Retrying...")
                sleep(1)

    def GetActors(self):
        empty = google_dot_protobuf_dot_empty__pb2.Empty()
        while True:
            try:
                return self.director_api.GetActors(empty, metadata=self.metadata)
            except grpc._channel._MultiThreadedRendezvous:  # FIXME this is irritating! Someone please fix this...
                logger.warning("Cannot resolve Gimulator host! Retrying...")
                sleep(1)

    def PutResult(self, result: Result):
        while True:
            try:
                return self.director_api.PutResult(result, metadata=self.metadata)
            except grpc._channel._MultiThreadedRendezvous:  # FIXME this is irritating! Someone please fix this...
                logger.warning("Cannot resolve Gimulator host! Retrying...")
                sleep(1)


class OperatorClient(GimulatorClient):
    operator_api = None

    def __init__(self, wait_until_connected=True, **kwargs):
        super().__init__(wait_until_connected, **kwargs)
        self.operator_api = OperatorAPIStub(self.channel)

    def SetUserStatus(self, report: Report):
        wait_for_dns(self.domain, self.port)  # FIXME this is irritating! Someone please fix this...
        return self.operator_api.SetUserStatus(report, metadata=self.metadata)


class ActorClient(GimulatorClient):
    actor_api = None

    def __init__(self, wait_until_connected=True, **kwargs):
        super().__init__(wait_until_connected, **kwargs)
        self.actor_api = UserAPIStub(self.channel)

    def ImReady(self):
        empty = google_dot_protobuf_dot_empty__pb2.Empty()
        wait_for_dns(self.domain, self.port)  # FIXME this is irritating! Someone please fix this...
        return self.actor_api.ImReady(empty, metadata=self.metadata)
