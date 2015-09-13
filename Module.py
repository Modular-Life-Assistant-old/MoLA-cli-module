from core import Daemon, ModuleManager, NotificationManager, settings
from helpers.modules.TelnetServerModule import TelnetServerModule

import time


class Module(TelnetServerModule):
    server_port = 14212

    def command_notify(self, send_handler, args, kwargs, client_key):
        NotificationManager.notify(self.module_name, ' '.join(args))
        send_handler('notification added.')

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
        self.register_command('notify', self.command_notify, 'add notification message')
        self.register_command('shutdown', self.command_shutdown, 'shutdown %s process' % settings.NAME)
        self.register_command('uptime', self.command_uptime, 'uptime of %s process' % settings.NAME)

    def new_client(self, socket, ip, port, client_key):
        personnality = ModuleManager.get('personnality')
        if personnality:
            self.send(personnality.get_greeting().capitalize() + ' ' + personnality.get_user_name() + '.', client_key)

    def __notify(self, msg):
        for client_key in self.clients:
            self.send('Notification: %s' % msg, client_key)