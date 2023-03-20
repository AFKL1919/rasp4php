import json
import datetime
from sqlalchemy import Column, Integer, String, DATETIME
from dashboard.core.db import DB_BASE

class Message(DB_BASE.Model):
    """
    {
      pid: Process.id,
      function: getFunctionName(),
      args: [],
      normalized_args: [],
      filename: getFilename(),
      lineno: getLineNo(),
      context: 'url',
      type: 'network_access',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),
      hook_point: '_php_stream_xport_create'
    }
    """
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    pid = Column(Integer)
    time = Column(DATETIME, default=datetime.datetime.utcnow)
    function = Column(String(120))
    args = Column(String(120))
    normalized_args = Column(String(120))
    filename = Column(String(120))
    lineno = Column(Integer)
    context = Column(String(120))
    type = Column(String(120))
    request_uri = Column(String(120))
    remote_addr = Column(String(120))
    query_string = Column(String(120))
    document_root = Column(String(120))
    hook_point = Column(String(120))

    def __init__(self, payload: dict):
      self.pid = payload["pid"]
      self.function = payload["function"]
      self.args = json.dumps(payload["args"])
      self.normalized_args = json.dumps(payload["normalized_args"])
      self.filename = payload["filename"]
      self.lineno = payload["lineno"]
      self.context = payload["context"]
      self.type = payload["type"]
      self.request_uri = payload["request_uri"]
      self.remote_addr = payload["remote_addr"]
      self.query_string = payload["query_string"]
      self.document_root = payload["document_root"]
      self.hook_point = payload["hook_point"]
    
    def serialize(self) -> dict:
      data = dict(vars(self))
      data.pop('_sa_instance_state')
      data['args'] = json.loads(data['args'])
      data['normalized_args'] = json.loads(data['normalized_args'])
      return data