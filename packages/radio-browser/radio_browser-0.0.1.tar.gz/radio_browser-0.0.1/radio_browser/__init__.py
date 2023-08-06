#!/bin/env python
import socket

import requests


class RadioBrowser:
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'PyRadioBrowser/0.0.1'}

    @staticmethod
    def get_radiobrowser_base_urls():
        """
        Get all base urls of all currently available radiobrowser servers

        Returns:
        list: a list of strings

        """
        hosts = []
        # get all hosts from DNS
        ips = socket.getaddrinfo('all.api.radio-browser.info',
                                 80, 0, 0, socket.IPPROTO_TCP)
        for ip_tupple in ips:
            ip = ip_tupple[4][0]

            # do a reverse lookup on every one of the ips to have a nice name for it
            host_addr = socket.gethostbyaddr(ip)
            # add the name to a list if not already in there
            if host_addr[0] not in hosts:
                hosts.append(host_addr[0])

        # sort list of names
        hosts.sort()
        # add "https://" in front to make it an url
        return list(map(lambda x: "https://" + x, hosts))

    @classmethod
    def get_radio(cls, path, param=None):
        servers = cls.get_radiobrowser_base_urls()
        for server_base in servers:
            uri = server_base + path
            try:
                return requests.get(uri, params=param,
                                    headers=cls.headers).json()
            except Exception as e:
                pass
        return {}

    @classmethod
    def get_country_stations(cls, countrycode):
        return cls.get_radio("/json/stations/bycountrycodeexact/" +
                             countrycode)

    @classmethod
    def search_radio(cls, name):
        params = {
            "hidebroken": True,
            "limit": 50,
            "reverse": True,
            "order": "stationcount",
            "name": name
        }
        return cls.get_radio(f"/json/stations/search", params)

    @classmethod
    def search_tags(cls, name):
        params = {
            "hidebroken": True,
            "limit": 50,
            "reverse": True,
            "order": "stationcount"
        }
        return cls.get_radio(f"/json/tags/{name}", params)
