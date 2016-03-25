import importlib
import sys

import gevent
try:
    import geventwebsocket  # noqa
    _websocket_available = True
except ImportError:
    _websocket_available = False
try:
    import uwsgi
except ImportError:
    uwsgi = None


class Thread(gevent.Greenlet):  # pragma: no cover
    """
    This wrapper class provides gevent Greenlet interface that is compatible
    with the standard library's Thread class.
    """
    def __init__(self, target, args=[], kwargs={}):
        super(Thread, self).__init__(target, *args, **kwargs)

    def _run(self):
        return self.run()


class WebSocketWSGI(object):  # pragma: no cover
    """
    This wrapper class provides a gevent WebSocket interface that is
    compatible with eventlet's implementation.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        self.environ = environ
        if uwsgi and 'uwsgi.version' in environ:
            # we are running under uwsgi
            uwsgi.websocket_handshake(environ['HTTP_SEC_WEBSOCKET_KEY'],
                                      environ.get('HTTP_ORIGIN', ''))
            self._sock = None
        elif 'wsgi.websocket' in environ:
            self._sock = environ['wsgi.websocket']
            #self.version = self._sock.version
            #self.path = self._sock.path
            #self.origin = self._sock.origin
            #self.protocol = self._sock.protocol
        else:
            raise RuntimeError('You need to use the gevent-websocket server. '
                               'See the Deployment section of the '
                               'documentation for more information.')
        return self.app(self)

    def close(self):
        if self._sock:
            return self._sock.close()

    def send(self, message):
        print("send", message)
        if self._sock is None:
            return uwsgi.websocket_send(message)
        return self._sock.send(message)

    def wait(self):
        print("reading")
        if self._sock is None:
            return uwsgi.websocket_recv()
        return self._sock.receive()


async = {
    'threading': sys.modules[__name__],
    'thread_class': 'Thread',
    'queue': importlib.import_module('gevent.queue'),
    'queue_class': 'JoinableQueue',
    'websocket': sys.modules[__name__] if _websocket_available else None,
    'websocket_class': 'WebSocketWSGI' if _websocket_available else None
}
