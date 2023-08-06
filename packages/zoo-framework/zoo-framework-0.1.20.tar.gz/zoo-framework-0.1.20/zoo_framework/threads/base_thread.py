import time

from zoo_framework.utils import LogUtils


class BaseThread(object):
    
    def __init__(self, props: dict):
        self._props = props
        self.state = {}
        self._destroy_func = None
    
    def is_loop(self):
        if self._props.get('is_loop'):
            return self._props.get('is_loop')
        return False
    
    @property
    def name(self):
        if self._props.get('name'):
            return self._props.get('name')
        return self.__class__.__name__
    
    def _destroy(self, result):
        pass
    
    def _execute(self):
        pass
    
    def run(self):
        try:
            LogUtils.info("{} Worker is Start".format(self.name), self.__class__.__name__)
            result = self._execute()
            self._destroy(result)
            LogUtils.info("{} Worker is Stop".format(self.name), self.__class__.__name__)
        except Exception as e:
            self._on_error()
            LogUtils.error(str(e), self.__class__.__name__)
        finally:
            self._on_done()
        
        if self._props.get('delay_time'):
            time.sleep(self._props["delay_time"])
    
    def _on_error(self):
        pass
    
    def _on_done(self):
        pass
