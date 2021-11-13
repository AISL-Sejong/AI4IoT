var net = require('net'); 
var socket = net.connect({port : 3105}); 

const exec = require('child_process').exec; 
//const result_ex = exec('python3 upper_broken.py');


socket.on('connect', function(){ 
    console.log('connected to server!');
    socket.write('{"ctname": "display2", "con": "hello"}'+ '<EOF>')
             +  ('{"ctname": "classifier", "con": "hello"}'+ '<EOF>'); //modify
    // const normal_ex = exec('python3 normal.py');
    console.log('normal');
});

    
socket.on('data', function(chunk){ 
    console.log('recv:' + chunk);
    if(chunk== '"both"'+"<EOF>") {
        console.log('recv:' + chunk);
        const both_ex = exec('python3 both_broken.py');
    }

    if(chunk== '"under"'+"<EOF>") {
        console.log('recv:' + chunk);
        const under_ex = exec('python3 under_broken.py');
    }

    if(chunk== '"upper"'+"<EOF>") {
        console.log('recv:' + chunk);
        const upper_ex = exec('python3 upper_broken.py');
    }
    if(chunk== '"servo_upper_act"'+"<EOF>") {
        console.log('recv:' + chunk);
        const supper_ex = exec('python3 upper_broken.py')
    }
    if(chunk== '"servo_under_act"'+"<EOF>") {
        console.log('recv:' + chunk);
        const sunder_ex = exec('python3 under_broken.py')
    }
     
});
        // 접속이 종료됬을때 메시지 출력 
socket.on('end', function(){ console.log('disconnected.'); }); 
        // 에러가 발생할때 에러메시지 화면에 출력 
socket.on('error', function(err){ console.log(err); }); 
        // connection에서 timeout이 발생하면 메시지 출력 
socket.on('timeout', function(){ console.log('connection timeout.');
    });
