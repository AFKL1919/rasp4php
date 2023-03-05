{
  onEnter: function (args) {
    var message = {pid: Process.id,
      function: getFunctionName(),
      args : [],
      normalized_args: [],
      filename: getFilename(),
      lineno: getLineNo(),
      context: 'file',
      type: 'file_upload',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),hook_point: ''
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

    send(message);recv(judge_reques_by_message);
  }
}