{
  onEnter: function (args) {
    var CURLOPT_URL = 10002;

    if (args[1].toInt32() === CURLOPT_URL) {
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

      var url = Memory.readCString(args[2]);
      message.args.push(url);
      if (url.indexOf("://") === -1) {
        message.normalized_args.push("//" + url);
      }

      send(message);recv(judge_reques_by_message);
    }
  }
}
