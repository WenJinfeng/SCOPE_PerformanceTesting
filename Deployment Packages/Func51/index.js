var init_st = (new Date()).valueOf();
const now = require('performance-now');
const fs = require('fs');
var init_ed = (new Date()).valueOf();


exports.node_factors = (req, res) => {
  var fun_st=(new Date()).valueOf();
  var instanceId = fs.readFileSync('/proc/self/cgroup', 'utf-8');
  var cpuinfo = fs.readFileSync('/proc/cpuinfo', 'utf8');
  var meminfo = fs.readFileSync('/proc/meminfo', 'utf8');
  var uptime = fs.readFileSync('/proc/uptime', 'utf-8');

	
  var n;

    if(req.query && req.query.n) {
        n = req.query.n;
    } else {
        n = 2688834647444046;
    }

  let start = now();
  let result = factors(n);
  let end = now();

  var fun_ed = (new Date()).valueOf();
  res.set("Content-Type", "application/json");
	res.status(200);
  res.send(JSON.stringify({
      success: true,
      payload: {
          "test": "cpu test",
          "n": Number(n),
          "result": result,
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
  
  // console.log(',InitStart:{},'.format(init_st) + 'InitEnd:{},'.format(init_ed) + 'functionStart:{},'.format(fun_st) + 'functionEnd:{},'.format(fun_ed))


};

function factors(num) {
  let n_factors = [];
 
  for (let i = 1; i <= Math.floor(Math.sqrt(num)); i += 1)
    if (num % i === 0) {
      n_factors.push(i);
      if (num / i !== i) {
        n_factors.push(num / i);
      }
    }

  n_factors.sort(function(a, b){return a - b;});

  return n_factors;
}
