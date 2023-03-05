/*  PHP API */
function getFilename() {
  var getFilenameAddr = Module.findExportByName(null, 'zend_get_executed_filename');
  var _getFilename = new NativeFunction(getFilenameAddr, 'pointer', []);
  var filename = Memory.readCString(ptr(_getFilename()));

  if (filename.indexOf('(') !== -1) {
    return filename.substring(0, filename.indexOf('('));
  }

  return filename;
}
function getLineNo() {
  var getLinenoAddr = Module.findExportByName(null, 'zend_get_executed_lineno');
  var _getLineno = new NativeFunction(getLinenoAddr, 'uint32', []);

  return _getLineno();
}
function getServerEnv(env) {
  // $_SERVER
  var sapi_getenv_addr = Module.findExportByName(null, 'sapi_getenv');
  var sapi_getenv = new NativeFunction(sapi_getenv_addr, 'pointer', ['pointer', 'int']);
  var envName = Memory.allocUtf8String(env);
  var envValue = sapi_getenv(envName, env.length);

  return Memory.readCString(envValue);
}
function getFunctionName() {
  var getFunctionAddr = Module.findExportByName(null, 'get_active_function_name');
  var _getFunction = new NativeFunction(getFunctionAddr, 'pointer', []);
  var getClassNameAddr = Module.findExportByName(null, 'get_active_class_name');
  var _getClassName = new NativeFunction(getClassNameAddr, 'pointer', ['pointer']);
  var spacePointer = Memory.alloc(Process.pointerSize);

  var functionName = Memory.readCString(ptr(_getFunction()));
  var className = Memory.readCString(ptr(_getClassName(spacePointer)));

  if (className !== '') {
    return className + '::' + functionName;
  } else {
    return functionName;
  }
}
function getRealPath(pathPointer) {
  var tsrmRealPathAddr = Module.findExportByName(null, 'tsrm_realpath');
  var tsrmRealPath = new NativeFunction(tsrmRealPathAddr, 'pointer', ['pointer', 'pointer']);
  var realpathPointer = Memory.alloc(100);
  var path = Memory.readCString(pathPointer);

  if (path.startsWith('file://')) {
    var newPathPointer = Memory.allocUtf8String(path.substring(7));
    tsrmRealPath(newPathPointer, realpathPointer);
  } else {
    tsrmRealPath(pathPointer, realpathPointer);
  }

  return Memory.readCString(ptr(realpathPointer));
}
function getZendParseParameters(parameters) {
  var params = [];
  for (var i = 0; i < arguments.length; i++) {
    if (typeof arguments[i] === 'number') {
      params.push('int');
    } else {
      params.push('pointer');
    }
  }

  var zendParseParametersAddr = Module.findExportByName(null, 'zend_parse_parameters');
  var zendParseParameters = new NativeFunction(zendParseParametersAddr, 'int', params);

  return zendParseParameters;
}

var php_output_discard_all = new NativeFunction(
  Module.findExportByName(null, 'php_output_discard_all'), 'void', []
);

const SAPI_HEADER_REPLACE = 0;
const SAPI_HEADER_DELETE_ALL = 3;
var sapi_header_op = new NativeFunction(
  Module.findExportByName(null, 'sapi_header_op'), 'int', ['int', 'pointer']
);

var php_output_write = new NativeFunction(
  Module.findExportByName(null, 'php_output_write'), 'size_t', ['pointer', 'size_t']
);

var php_output_flush_all = new NativeFunction(
  Module.findExportByName(null, 'php_output_flush_all'), 'void', ['void']
);

var php_output_end_all = new NativeFunction(
  Module.findExportByName(null, 'php_output_end_all'), 'void', ['void']
);

var zend_error_noreturn = new NativeFunction(
  Module.findExportByName(null, 'zend_error_noreturn'), 'void', ['int', 'pointer']
);

function block_request(status_code, body, headers) {
  php_output_discard_all();

  sapi_header_op(SAPI_HEADER_DELETE_ALL, ptr(0));

  for (const [k, v] of Object.entries(headers)) {

    var header = `${encodeURIComponent(k)}: ${encodeURIComponent(v)}`;
    var header_ptr = Memory.allocUtf8String(header);
    var sapi_header_line_ptr = Memory.alloc(Process.pointerSize + 8 + 4);

    sapi_header_line_ptr.writePointer(header_ptr);
    sapi_header_line_ptr.add(Process.pointerSize).writeS8(header.length);
    sapi_header_line_ptr.add(Process.pointerSize + 8).writeInt(status_code);

    sapi_header_op(SAPI_HEADER_REPLACE, sapi_header_line_ptr);
  }

  php_output_write(
    Memory.allocUtf8String(body), ~-encodeURI(body).split(/%..|./).length
  );
  php_output_flush_all(ptr(0));
  php_output_end_all(ptr(0));
  
  zend_error_noreturn(
    64, Memory.allocUtf8String(
      "RASP blocked the request."
    )
  );
}