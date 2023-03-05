const FAIL_VALUE = ptr(0);
var origin_ptr = Module.findExportByName(null, 'compile_string');
var origin_func = new NativeFunction(origin_ptr, 'pointer', ['pointer', 'pointer', 'pointer']);
Interceptor.replace(origin_ptr, new NativeCallback(
  (...args) => {
    var message = {
      pid: Process.id,
      function: 'eval',
      args: [],
      normalized_args: [],
      filename: getFilename(),
      lineno: -1,
      context: 'code',
      type: 'code_execution',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),
      hook_point: 'compile_string'
    };
    var evalStringOffset = 24;
    var evalString = Memory.readCString(Memory.readPointer(args[0]).add(evalStringOffset));
    var evalFile = Memory.readCString(args[1]);

    message.args.push(evalString);
    message.filename = evalFile.split('(')[0];
    message.lineno = parseInt(evalFile.split('(')[1].split(')')[0], 10);

    if (evalFile.includes("assert code")) {
      message.function = "assert";
    } else if (evalFile.includes("runtime-created function")) {
      message.function = "create_function";
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
  }, 'pointer', ['pointer', 'pointer', 'pointer']
)
);