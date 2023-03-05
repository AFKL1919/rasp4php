{
  onEnter: function (args) {
    var message = {pid: Process.id,
      function: getFunctionName(),
      args : [],
      normalized_args: [],
      filename: getFilename(),
      lineno: getLineNo(),
      context: 'command',
      type: 'command_execution',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),hook_point: ''
    };

    var zendParseParameters = getZendParseParameters(1, fmt, cmd, cmdLen);
    var fmt = Memory.allocUtf8String('s');
    var cmd = Memory.alloc(Process.pointerSize);
    var cmdLen = Memory.alloc(Process.pointerSize);

    zendParseParameters(1, fmt, cmd, cmdLen);
    message.args.push(Memory.readCString(Memory.readPointer(cmd)));

    send(message);recv(judge_reques_by_message);
  }
}
