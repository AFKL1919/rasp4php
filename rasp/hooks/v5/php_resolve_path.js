{
  onEnter: function (args) {
    var message = {pid: Process.id,
      function: "include_or_require",
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

    var requiredFilename = Memory.readCString(args[0]);
    message.args.push(requiredFilename);

    this.message = message;
  },
  onLeave: function (retval) {
      if (parseInt(retval)) {
        this.message.normalized_args.push(Memory.readCString(ptr(retval).add(24)));
        if (this.message.filename !== '[no active file]') {
          send(this.message);
        }
      }
  }
}