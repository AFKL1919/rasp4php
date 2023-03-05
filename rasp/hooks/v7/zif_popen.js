const FAIL_VALUE = ptr(0);
var origin_ptr = Module.findExportByName(null, 'zif_popen');
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
      context: 'command',
      type: 'command_execution',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),
      hook_point: 'zif_popen'
    };

    var zendParseParameters = getZendParseParameters(2, fmt, cmd, cmdLen, mode, modeLen);
    var fmt = Memory.allocUtf8String('ps');
    var cmd = Memory.alloc(Process.pointerSize);
    var cmdLen = Memory.alloc(Process.pointerSize);
    var mode = Memory.alloc(Process.pointerSize);
    var modeLen = Memory.alloc(Process.pointerSize);

    zendParseParameters(2, fmt, cmd, cmdLen, mode, modeLen);
    message.args.push(Memory.readCString(Memory.readPointer(cmd)))
    message.args.push(Memory.readCString(Memory.readPointer(mode)))

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