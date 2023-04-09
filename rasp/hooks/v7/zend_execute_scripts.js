var origin_ptr = Module.findExportByName(null, 'zend_execute_scripts');
Interceptor.attach(
  Module.findExportByName(null, 'zend_execute_scripts'),
  {
    onEnter(args) {
      var message = {
        pid: Process.id,
        function: getFunctionName(),
        args: [],
        normalized_args: [],
        filename: getFilename(),
        lineno: getLineNo(),
        context: 'start_request',
        type: 'start_request',
        request_uri: getServerEnv('REQUEST_URI'),
        remote_addr: getServerEnv('REMOTE_ADDR'),
        query_string: getServerEnv('QUERY_STRING'),
        document_root: getServerEnv('DOCUMENT_ROOT'),
        hook_point: 'zend_execute_scripts'
      };

      send(message);
      var judge_msg = null;
      recv(message => {
        judge_msg = message;
      }).wait();

      if (judge_msg['is_blocked']) {
        block_request_for_blacklist_ip(
          judge_msg['code'], judge_msg['body'], judge_msg['headers']
        );
        args[2].writeInt(0);
      }
    }
  }
);