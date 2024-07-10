var init_st = (new Date()).valueOf();
var fs = require("fs");
var now = require('performance-now');
var rimraf = require("rimraf");
var init_ed = (new Date()).valueOf();

exports.node_filesystem = (req, res) => {
    var fun_st=(new Date()).valueOf();
  	var instanceId = fs.readFileSync('/proc/self/cgroup', 'utf-8');
    var cpuinfo = fs.readFileSync('/proc/cpuinfo', 'utf8');
    var meminfo = fs.readFileSync('/proc/meminfo', 'utf8');
    var uptime = fs.readFileSync('/proc/uptime', 'utf-8');
    
    var n, size;

    var rnd = Math.floor(Math.random() * 900000) + 100000;

    if(req.query && req.query.n) {
        n = req.query.n;
    } else {
        n = 10000;
    }

    if(req.query && req.query.size) {
        size = req.query.size;
    } else {
        size = 10240;
    }

    var text = '';
    
    for(let i = 0; i<size; i++) {
        text += 'A';
    }

    if(!fs.existsSync('/tmp/test')){
        fs.mkdirSync('/tmp/test');
    }

    if(!fs.existsSync('/tmp/test/'+rnd)){
        fs.mkdirSync('/tmp/test/'+rnd);
    }
    
    let startWrite = now();
    for(let i = 0; i<n; i++) {
        fs.writeFileSync('/tmp/test/'+rnd+'/'+i+'.txt', text, 'utf-8');
    }
    let endWrite = now();
    
    let startRead = now();
    for(let i = 0; i<n; i++) {
        var test = fs.readFileSync('/tmp/test/'+rnd+'/'+i+'.txt', 'utf-8');
    }
    let endRead = now();
    
    let files = fs.readdirSync('/tmp/test/'+rnd);

    if(fs.existsSync('/tmp/test/'+rnd)){
        rimraf.sync('/tmp/test/'+rnd);
    }
    var fun_ed = (new Date()).valueOf();
  	res.set("Content-Type", "application/json");
	res.status(200);
    res.send(JSON.stringify({
        success: files.length == n,
        payload: {
            "test": "filesystem test",
            "n": files.length,
            "size": Number(size),
            "timewrite": (endWrite-startWrite).toFixed(3),
            "timeread": (endRead-startRead).toFixed(3),
            "time": ((endWrite-startWrite)+(endRead-startRead)).toFixed(3)
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
