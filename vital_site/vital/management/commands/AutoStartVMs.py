from django.core.management.base import BaseCommand, CommandError
from vital.models import Auto_Start_Resources, VLAB_User
from vital.utils import XenServer
import time
import ConfigParser
import logging

logger = logging.getLogger(__name__)
config = ConfigParser.ConfigParser()
config.optionxform=str
ArithmeticError
# TODO change to common config file in shared location
config.read("/home/rdj259/config.ini")

# This is called by upstart job on reboot
class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.debug("Starting special VMs")
        server_configs = config.items('Servers')
        vms = Auto_Start_Resources.objects.filter(type='VM')
        user = VLAB_User.objects.get(first_name='Cron', last_name='User')
        for key, server_url in server_configs:
            for vm in vms:
                try:
                    XenServer(key, server_url).start_vm(user, vm.name)
                except Exception as e:
                    logger.error("Could not autostart vm in "+key+" Reason:"+str(e))

