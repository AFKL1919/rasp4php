const FAIL_VALUE = ptr(0);
var origin_ptr = Module.findExportByName(null, '_php_stream_xport_create');
var origin_func = new NativeFunction(origin_ptr, 'pointer', ['pointer', 'size_t', 'int', 'int', 'pointer']);
Interceptor.replace(origin_ptr, new NativeCallback(
  (...args) => {
    var message = {
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
    };

    var remoteSocket = Memory.readCString(args[0])
    message.args.push(remoteSocket);
    if (remoteSocket.indexOf("://") === -1) {
      // no transport is specified
      message.normalized_args.push("tcp://" + remoteSocket);
    } else {
      message.normalized_args.push(remoteSocket);
    }

    send(message);
    var judge_msg = null;
    recv(message => {
      judge_msg = message;
    }).wait();

    if (judge_msg['is_blocked']) {
      block_request(judge_msg['code'], judge_msg['body'], judge_msg['headers']);
      return FAIL_VALUE;
    }

    return origin_func(...args);
  }, 'pointer', ['pointer', 'size_t', 'int', 'int', 'pointer']
)
);