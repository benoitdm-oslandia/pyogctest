# -*- coding: utf-8 -*-
import time
import docker
import requests
from enum import Enum


NAME="pyogctest"
OGCCITE_WMS130="ogccite/ets-wms13"


class Teamengine(object):

    class TestSuite(Enum):

        WMS130 = 0

    def __init__(self, suite, port=8080):
        self.suite = suite
        self.port = port

        if self.suite == Teamengine.TestSuite.WMS130:
            self.image = OGCCITE_WMS130

    def pull(self):
        client = docker.from_env()
        client.images.pull(self.image)

    def start(self):
        self.stop()

        client = docker.from_env()
        client.containers.run(self.image, detach=True, ports={8080: self.port}, name=NAME, remove=True)
        time.sleep(5)  # teamengine takes some time to start


    def stop(self):
        client = docker.from_env()

        try:
            cont = client.containers.get(NAME)
            cont.stop()
            time.sleep(5)
        except docker.errors.NotFound:
            pass

    def run(self, url):
        request = None

        if self.suite == Teamengine.TestSuite.WMS130:
            getcapa = "{}?REQUEST=GetCapabilities%26VERSION=1.3.0%26SERVICE=WMS".format(url)
            teamengine = "http://localhost:{}/teamengine/rest/suites/wms13/run".format(self.port)

            request = ('{0}?queryable=queryable&basic=basic&recommended=recommended&'
                       'capabilities-url={1}'
                       .format(teamengine, getcapa))

        if request:
            r = requests.get(request, headers={'Accept': 'application/xml'})
            return r.text

        return None