var init_st = (new Date()).valueOf();
const now = require('performance-now');
const fs = require('fs');
var init_ed = (new Date()).valueOf();

exports.node_matrix = (req, res) => {
  var fun_st=(new Date()).valueOf();
  var instanceId = fs.readFileSync('/proc/self/cgroup', 'utf-8');
  var cpuinfo = fs.readFileSync('/proc/cpuinfo', 'utf8');
  var meminfo = fs.readFileSync('/proc/meminfo', 'utf8');
  var uptime = fs.readFileSync('/proc/uptime', 'utf-8');

  var n;

    if(req.query && req.query.n) {
        n = req.query.n;
    } else {
        n = 100;
    }

  let start = now();
  let result = matrix(n);
  let end = now();

  var fun_ed = (new Date()).valueOf();
  res.set("Content-Type", "application/json");
	res.status(200);
  res.send(JSON.stringify({
      success: true,
      payload: {
          "test": "matrix test",
          "n": Number(n),
          "time": Number((end-start).toFixed(3))
      },
      metrics: {
          machineid: '',
          instanceid: instanceId,
          cpu: cpuinfo,
          mem: meminfo,
          uptime: uptime
      },
      log:{"info":',InitStart:'+init_st+',' + 'InitEnd:'+init_ed+',' + 'functionStart:'+fun_st+','+ 'functionEnd:'+fun_ed+','}
  }));

};

const randomTable = (size) => Array.from(
  {length: size}, 
  () => Array.from({length: size}, () => Math.floor(Math.random() * 100))
)


function matrix(n) {
  let matrixA = randomTable(n);
  let matrixB = randomTable(n);
  let matrixMult = [];
 
  for (var i = 0; i < matrixA.length; i++) {
    matrixMult[i] = [];
    for (var j = 0; j < matrixB.length; j++) {
      var sum = 0;
      for (var k = 0; k < matrixA.length; k++) {
        sum += matrixA[i][k] * matrixB[k][j];
      }
      matrixMult[i][j] = sum;
    }
  }

  return matrixMult;
}

