const FAIL_VALUE = ptr(0);
var origin_ptr = Module.findExportByName(null, 'zif_proc_open');
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
      hook_point: 'zif_proc_open'
    };

    var zendParseParameters = getZendParseParameters(3, fmt, cmd, cmdLen, descriptorspec, pipes, cwd, cwdLen, environment, otherOptions);
    var fmt = Memory.allocUtf8String('saz/|s!a!a!');
    var cmd = Memory.alloc(Process.pointerSize);
    var cmdLen = Memory.alloc(Process.pointerSize);
    var descriptorspec = Memory.alloc(Process.pointerSize);
    var pipes = Memory.alloc(Process.pointerSize);
    var cwd = Memory.alloc(Process.pointerSize);
    var cwdLen = Memory.alloc(Process.pointerSize);
    var environment = Memory.alloc(Process.pointerSize);
    var otherOptions = Memory.alloc(Process.pointerSize);

    zendParseParameters(3, fmt, cmd, cmdLen, descriptorspec, pipes, cwd, cwdLen, environment, otherOptions);
    message.args.push(Memory.readCString(Memory.readPointer(cmd)))

    send(message);
    var judge_msg = null;
    recv(message => {
      judge_msg = message;
    }).wait();

    if (judge_msg['is_blocked']) {
      block_request(judge_msg['code'], judge_msg['body'], judge_msg['headers']);
      return ptr(0);
    }

    return origin_func(...args);
  }, 'void', ['pointer', 'pointer']
));
