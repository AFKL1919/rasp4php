const FAIL_VALUE = ptr(0);
var origin_ptr = Module.findExportByName(null, 'zif_move_uploaded_file');
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
      context: 'file',
      type: 'file_upload',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),
      hook_point: 'zif_move_uploaded_file'
    };

    var zendParseParameters = getZendParseParameters(2, fmt, src, srclen, dest, destlen);
    var fmt = Memory.allocUtf8String('sp');
    var src = Memory.alloc(Process.pointerSize);
    var srclen = Memory.alloc(Process.pointerSize);
    var dest = Memory.alloc(Process.pointerSize);
    var destlen = Memory.alloc(Process.pointerSize);

    zendParseParameters(2, fmt, src, srclen, dest, destlen);
    message.args.push(Memory.readCString(Memory.readPointer(src)));
    message.args.push(Memory.readCString(Memory.readPointer(dest)));

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