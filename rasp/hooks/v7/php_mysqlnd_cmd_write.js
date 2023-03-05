const FAIL_VALUE = 1;
var origin_ptr = Module.findExportByName(null, 'php_mysqlnd_cmd_write');
var origin_func = new NativeFunction(origin_ptr, 'size_t', ['pointer', 'pointer']);
Interceptor.replace(origin_ptr, new NativeCallback(
  (...args) => {
    var message = {
      pid: Process.id,
      function: getFunctionName(),
      args: [],
      normalized_args: [],
      filename: getFilename(),
      lineno: getLineNo(),
      context: 'sql',
      type: 'database_operation',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),
      hook_point: 'php_mysqlnd_cmd_write'
    };

    var sql = Memory.readCString(Memory.readPointer(args[0].add(32)));
    if (sql !== null) {
      message.args.push(sql);
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
  }, 'size_t', ['pointer', 'pointer']
));