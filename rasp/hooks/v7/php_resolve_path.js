const FAIL_VALUE = -1;
var origin_ptr = Module.findExportByName(null, 'php_resolve_path');
var origin_func = new NativeFunction(origin_ptr, 'pointer', ['pointer', 'size_t', 'pointer']);
Interceptor.replace(origin_ptr, new NativeCallback(
  (...args) => {
    var message = {
      pid: Process.id,
      function: "include_or_require",
      args : [],
      normalized_args: [],
      filename: getFilename(),
      lineno: getLineNo(),
      context: 'file',
      type: 'file_operation',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),
      hook_point: 'php_resolve_path'
    };

    var requiredFilename = Memory.readCString(args[0]);
    message.args.push(requiredFilename);

    var retval = origin_func(...args);
    message.normalized_args.push(
      Memory.readCString(retval.add(24))
    );

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

    return retval;
  }, 'pointer', ['pointer', 'size_t', 'pointer']
));