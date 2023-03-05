const FAIL_VALUE = 0;
var origin_ptr = Module.findExportByName(null, 'curl_multi_setopt');
var origin_func = new NativeFunction(origin_ptr, 'int', ['pointer', 'int', 'pointer']);
Interceptor.replace(origin_ptr, new NativeCallback(
  (...args) => {
    var CURLOPT_URL = 10002;

    if (args[1].toInt32() === CURLOPT_URL) {
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
        hook_point: 'curl_multi_setopt'
      };

      var url = Memory.readCString(args[2]);
      message.args.push(url);
      if (url.indexOf("://") === -1) {
        message.normalized_args.push("//" + url);
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
    }
  }, 'int', ['pointer', 'int', 'pointer']
));
