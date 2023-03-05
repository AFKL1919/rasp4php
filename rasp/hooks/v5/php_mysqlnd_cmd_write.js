{
  onEnter: function (args) {
    var message = {pid: Process.id,
      function: getFunctionName(),
      args : [],
      normalized_args: [],
      filename: getFilename(),
      lineno: getLineNo(),
      context: 'sql',
      type: 'database_operation',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),hook_point: ''
    };

    var sql = Memory.readCString(Memory.readPointer(args[0].add(32)));
    if (sql !== null) {
      message.args.push(sql);
      send(message);recv(judge_reques_by_message);
    }
  }
}