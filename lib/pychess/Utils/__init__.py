import asyncio
import weakref

from pychess.Utils.lutils.ldata import MATE_VALUE, MATE_DEPTH


def prettyPrintScore(s, depth, format_mate=False):
    """The score parameter is an eval value form White point of view"""

    if s is None:
        return "?"

    if s == 0:
        return "0.00/%s" % depth

    if s > 0:
        pp = "+"
    else:
        pp = "-"
        s = -s

    if depth:
        depth = "/" + depth
    else:
        depth = ""

    if s >= MATE_VALUE - MATE_DEPTH:
        mate_in = MATE_VALUE - s
        if format_mate:
            if mate_in == 0:
                return _("Mate")
            return "%s #%d" % (_("Mate"), mate_in)
        else:
            return "%s#%.0f" % (pp, s)
    else:
        return "%s%0.2f%s" % (pp, s / 100.0, depth)


def createStoryTextAppEvent(text):
    try:
        import storytext
        storytext.applicationEvent(text)
    except AttributeError:
        pass
    except ImportError:
        pass


class wait_signal(asyncio.Future):
    """A future for waiting for a given signal to occur."""

    def __init__(self, obj, name, *, loop=None):
        super().__init__(loop=loop)
        self._obj = weakref.ref(obj, lambda s: self.cancel())
        self._hnd = obj.connect(name, self._signal_callback)

    def _signal_callback(self, *k):
        obj = self._obj()
        if obj is not None:
            obj.disconnect(self._hnd)
        self.set_result(k)

    def cancel(self):
        if self.cancelled():
            return False
        super().cancel()
        obj = self._obj()
        if obj is not None:
            obj.disconnect(self._hnd)
        return True
