from __future__ import unicode_literals

from builtins import object

from rasp.utils.message import install_message_queue
from rasp.utils.log import logger
from rasp.utils.waitgroup import RASP_WAITGROUP

from rasp.core.fpm import fpm
from rasp.core.runtime import Runtime
from rasp.core.hooks import HooksManager
from rasp.core.thread import HookMasterThread, HookWorkerThread, NotificationThread

class Application(object):
    is_installed = False

    def __init__(self, mode="monitoring"):
        self.mode = mode

    def start(self):
        self.environment = Runtime().environment

        self.bootstrap()
        self.start_threads()

        self.is_installed = True

    def bootstrap(self):
        # logger.info("{} is starting.".format(self.name))

        logger.info("Checking whether the PHP-FPM is running . . .")
        if not fpm.init():
            msg = "PHP-FPM is not running"
            logger.error(msg)
            raise Exception(msg)
        
        logger.info("OK, PHP-FPM {} is running on {}".format(fpm.full_version, self.environment['platform']))

        self.environment['rasp_mode'] = self.mode

        # Get phpinfo
        self.environment['fpm_master'] = fpm.master
        self.environment['fpm_workers'] = fpm.workers
        self.environment['fpm_version'] = fpm.version
        self.environment['fpm_enabled_modules'] = fpm.enabled_modules
        self.environment['fpm_disabled_functions'] = fpm.disabled_functions

        logger.info("PHP-FPM enabled modules: {}".format(set(self.environment['fpm_enabled_modules'])))
        logger.info("PHP-FPM disabled functions: {}".format(self.environment['fpm_disabled_functions']))

    # def exit_callback(self, signum, frame):
    #     self.detach_event.set()
    #     message_queue.put({'type': 'exit'})
    #     logger.info("{} is exiting".format(self.name))
    #     exit(0)

    # def set_signal_handler(self):
    #     signal.signal(signal.SIGINT, self.exit_callback)
    #     signal.signal(signal.SIGTERM, self.exit_callback)

    def start_threads(self):
        NotificationThread().start()

        RASP_WAITGROUP.add(1)

        hooks = HooksManager().get_hook_scripts(self.environment)
        HookMasterThread(self.environment['fpm_master'], hooks).start()

        for worker_pid in self.environment['fpm_workers']:
            HookWorkerThread(worker_pid, hooks).start()

        RASP_WAITGROUP.done()
        RASP_WAITGROUP.wait()

        install_message_queue.put({""})



RASP_APP = Application()
# RASP_APP.set_signal_handler()