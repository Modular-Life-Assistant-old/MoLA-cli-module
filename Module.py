from core import Daemon, NotificationManager, settings
from helpers.modules.TelnetServerModule import TelnetServerModule

import time


class Module(TelnetServerModule):
    server_port = 14212

    def command_shutdown(self, send_handler, args, kwargs, client_key):
        send_handler('shutdown %s ...' % settings.NAME)
        Daemon.stop()

    def command_uptime(self, send_handler, args, kwargs, client_key):
        diff = time.time() - settings.START_TIME
        days = diff // 86400
        hours = diff // 3600 % 24
        minutes = diff // 60 % 60
        seconds = diff % 60

        uptime = '%d seconds' % seconds
        if minutes: uptime = '%d minutes and %s' % (minutes, uptime)
        if hours:   uptime = '%d hours, %s' % (hours, uptime)
        if days:    uptime = '%d days, %s' % (days, uptime)

        send_handler('uptime is %s' % uptime)

    def init(self):
        super().init()
        NotificationManager.register(self.module_name, self.__notify)
        self.register_command('shutdown', self.command_shutdown, 'shutdown %s process' % settings.NAME)
        self.register_command('uptime', self.command_uptime, 'uptime of %s process' % settings.NAME)

    def __notify(self, msg):
        for client_key in self.clients:
            self.send('Notification: %s' % msg, client_key)