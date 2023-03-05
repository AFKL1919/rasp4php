const FAIL_VALUE = ptr(0);
var origin_ptr = Module.findExportByName(null, 'php_stream_locate_url_wrapper');
var origin_func = new NativeFunction(origin_ptr, 'pointer', ['pointer', 'pointer', 'int']);
Interceptor.replace(origin_ptr, new NativeCallback(
  (...args) => {
    var message = {
      pid: Process.id,
      function: getFunctionName(),
      args: [],
      normalized_args: [],
      filename: getFilename(),
      lineno: getLineNo(),
      context: 'file',
      type: 'file_operation',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),
      hook_point: 'php_stream_locate_url_wrapper'
    };

    var openedFilename = Memory.readCString(args[0]);
    message.args.push(openedFilename);
    message.normalized_args.push(getRealPath(args[0]));

    if (message.function === 'main') {
      message.function = 'include_or_require';
    }

    if (message.filename !== '[no active file]') {
      send(message);
      var judge_msg = null;
      recv(message => {
        judge_msg = message;
      }).wait();

      if (judge_msg['is_blocked']) {
        block_request(judge_msg['code'], judge_msg['body'], judge_msg['headers']);
        return FAIL_VALUE;
      }
    }

    return origin_func(...args);
  }, 'pointer', ['pointer', 'pointer', 'int']
));