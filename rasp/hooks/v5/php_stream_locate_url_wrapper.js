{
  onEnter: function (args) {
    var message = {pid: Process.id,
      function: getFunctionName(),
      args : [],
      normalized_args: [],
      filename: getFilename(),
      lineno: getLineNo(),
      context: 'file',
      type: 'file_operation',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),hook_point: ''
    };

    var openedFilename = Memory.readCString(args[0]);
    message.args.push(openedFilename);
    message.normalized_args.push(getRealPath(args[0]));

    if (message.function === 'main') {
      message.function = 'include_or_require';
    }

    if (message.filename !== '[no active file]') {
      send(message);recv(judge_reques_by_message);
    }
  }
}