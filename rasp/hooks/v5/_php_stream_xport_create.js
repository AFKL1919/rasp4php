{
  onEnter: function (args) {
    var message = {pid: Process.id,
      function: getFunctionName(),
      args : [],
      normalized_args: [],
      filename: getFilename(),
      lineno: getLineNo(),
      context: 'url',
      type: 'network_access',
      request_uri: getServerEnv('REQUEST_URI'),
      remote_addr: getServerEnv('REMOTE_ADDR'),
      query_string: getServerEnv('QUERY_STRING'),
      document_root: getServerEnv('DOCUMENT_ROOT'),hook_point: ''
    };

    var remoteSocket = Memory.readCString(args[0])
    message.args.push(remoteSocket);
    if (remoteSocket.indexOf("://") === -1) {
      // no transport is specified
      message.normalized_args.push("tcp://" + remoteSocket);
    } else {
      message.normalized_args.push(remoteSocket);
    }

    send(message);recv(judge_reques_by_message);
  }
}