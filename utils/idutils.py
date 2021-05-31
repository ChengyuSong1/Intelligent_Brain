import textwrap
import good as G
from uuid import uuid4, UUID
from utils.types import typed

_GENERATORS = []
EXCEPTION_MAP = {}


class _PlatformErrorBase(type):

    def __init__(cls, name, bases, classdict):
        EXCEPTION_MAP[name] = cls
        type.__init__(cls, name, bases, classdict)


class PlatformError(Exception, metaclass=_PlatformErrorBase):

    def __init__(self, **args):
        if hasattr(self, 'defaults'):
            for k, v in self.defaults.items():
                args.setdefault(k, v)

        if hasattr(self, 'schema'):
            args = self.schema(args)
        self.message = textwrap.dedent(self.message % args).strip()
        self.params = args
        super().__init__(args)

    def __str__(self):
        return self.message

    def full_type(self):
        parts = []
        head = self.__class__
        for i in range(10):
            if head == Exception:
                break
            parts.append(head.__name__)
            head = head.__bases__[0]

        return list(reversed(parts))


class MalformedID(PlatformError):
    message = 'Id `%(bad_id)s` failed validation'
    schema = G.Schema({'bad_id': G.Maybe(str)})


class _IdGenerator(object):

    @typed
    def __init__(self, prefix: str):
        self.prefix = prefix
        for gen in _GENERATORS:
            pass

        _GENERATORS.append(self)

    def __call__(self):
        return self.prefix + uuid4().hex

    def __str__(self):
        return 'IdGenerator(%s)' % self.prefix

    @typed
    def validate(self, data: str):
        try:
            if not isinstance(data, str):
                raise ValueError()
            if not data.startswith(self.prefix):
                raise ValueError()
            UUID(data[len(self.prefix):])
            return True
        except ValueError:
            raise MalformedID(bad_id=data)


AGENT_ID = _IdGenerator('A')
ALARMS_ID = _IdGenerator('AL')
API_TOKEN = _IdGenerator('API')
BACKUP_ID = _IdGenerator('B')
CREDENTIAL_ID = _IdGenerator('C')
CLIENT_UNIQUE_ID = _IdGenerator('CID')
CONFIGURE_id = _IdGenerator('CON')
DATABASE_ID = _IdGenerator('D')
FILE_ID = _IdGenerator('F')
HOST_ID = _IdGenerator('H')
INTENTION_ID = _IdGenerator('I')
INTENTION_STATE_ID = _IdGenerator('IS')
LOGIN_ID = _IdGenerator('l')
JOB_ID = _IdGenerator('J')
JOB_EXC_ID = _IdGenerator('JX')
MESSAGE_ID = _IdGenerator('ME')
RPDSQL_INSTALL_ID = _IdGenerator('MI')
PERMISSION_ID = _IdGenerator('P')
PUBDATA_ID = _IdGenerator('PU')
TOKEN = _IdGenerator('T')
TASKS_ID = _IdGenerator('TA')
TEMPLATE_ID = _IdGenerator('TE')
USER_ID = _IdGenerator('U')
VIRHOST_ID = _IdGenerator('V')

