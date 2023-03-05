const FAIL_VALUE = ptr(0);
var origin_ptr = Module.findExportByName(null, 'zif_socket_connect');
var origin_func = new NativeFunction(origin_ptr, 'void', ['pointer', 'pointer']);
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
      hook_point: 'zif_socket_connect'
    };

    var zendParseParameters = getZendParseParameters(3, fmt, socket, addr, addrlen, port);
    var fmt = Memory.allocUtf8String('rs|l');
    var socket = Memory.alloc(Process.pointerSize);
    var addr = Memory.alloc(Process.pointerSize);
    var addrlen = Memory.alloc(Process.pointerSize);
    var port = Memory.alloc(Process.pointerSize);

    zendParseParameters(3, fmt, socket, addr, addrlen, port);
    message.args.push(Memory.readCString(Memory.readPointer(addr)));
    message.args.push(Memory.readUInt(port));
    message.normalized_args.push(Memory.readCString(Memory.readPointer(addr)) + ":" + Memory.readUInt(port));

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
  }, 'void', ['pointer', 'pointer']
));
