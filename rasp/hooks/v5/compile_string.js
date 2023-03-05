{
  onEnter: function (args) {
    var message = {pid: Process.id,
      function: 'eval',
      args : [],
      normalized_args: [],
      filename: getFilename(),
      lineno: -1,
      context: 'code',
      type: 'code_execution',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),hook_point: ''
    };
    var evalStringOffset = 0;
    var evalString = Memory.readCString(Memory.readPointer(args[0]).add(evalStringOffset));
    var evalFile = Memory.readCString(args[1]);

    message.args.push(evalString);
    message.filename = evalFile.split('(')[0];
    message.lineno = parseInt(evalFile.split('(')[1].split(')')[0], 10);

    if (evalFile.includes("assert code")) {
      message.function = "assert";
    } else if (evalFile.includes("runtime-created function")) {
      message.function = "create_function";
    }

    send(message);recv(judge_reques_by_message);
  }
}