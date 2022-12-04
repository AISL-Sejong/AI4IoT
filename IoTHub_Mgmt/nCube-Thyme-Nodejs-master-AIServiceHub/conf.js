/**
 * Created by Il Yeup, Ahn in KETI on 2017-02-23.
 */

/**
 * Copyright (c) 2018, OCEAN
 * All rights reserved.
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
 * 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote products derived from this software without specific prior written permission.
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

var ip = require("ip");

var conf = {};
var cse = {};
var ae = {};
var cnt_arr = [];
var sub_arr = [];
var acp = {};

conf.useprotocol = 'mqtt'; // select one for 'http' or 'mqtt' or 'coap' or 'ws'

conf.sim = 'disable'; // enable / disable

// build cse
cse.host        = '{IP}';
cse.port        = '{PORT}';
cse.name        = 'Mobius';
cse.id          = '/Mobius2';
cse.mqttport    = '{PORT}';
cse.wsport      = '{PORT}';


// build ae
ae.name         = 'AIServiceHub';
ae.id           = ae.name;
ae.parent       = '/' + cse.name;
ae.appid        = 'AIServiceHub';
ae.port         = '{PORT}';
ae.bodytype     = 'json'; // select 'json' or 'xml' or 'cbor'
ae.tasport      = '{PORT}'; //CSE tas hosting port


// build cnt
var count = 0;

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name;
cnt_arr[count].lbl = 'target';
cnt_arr[count++].name = 'target';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name;
cnt_arr[count].lbl = 'visualLocalization';
cnt_arr[count++].name = 'visualLocalization';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name;
cnt_arr[count].lbl = 'humanDetection';
cnt_arr[count++].name = 'humanDetection';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name;
cnt_arr[count].lbl = 'humanPoseEstimation';
cnt_arr[count++].name = 'humanPoseEstimation';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name;
cnt_arr[count].lbl = 'beverageCf';
cnt_arr[count++].name = 'beverageCf';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[1].name;
cnt_arr[count].lbl = 'report';
cnt_arr[count++].name = 'report';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[2].name;
cnt_arr[count].lbl = 'report';
cnt_arr[count++].name = 'report';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[3].name;
cnt_arr[count].lbl = 'report';
cnt_arr[count++].name = 'report';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[4].name;
cnt_arr[count].lbl = 'report';
cnt_arr[count++].name = 'report';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name;
cnt_arr[count].lbl = 'status';
cnt_arr[count++].name = 'status';

cnt_arr[count] = {};
cnt_arr[count].parent = '/' + cse.name + '/' + ae.name;
cnt_arr[count].lbl = 'availableAIModel';
cnt_arr[count++].name = 'availableAIModel';



// build sub
var count = 0;

sub_arr[count] = {};
sub_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[0].name;
sub_arr[count].name = 'target';
sub_arr[count++].nu = 'mqtt://' + cse.host + '/' + ae.name + '_target' + '?ct=' + ae.bodytype; // mqtt
//sub_arr[count++].nu = 'http://' + ip.address() + ':' + ae.port + '/noti?ct=json'; // http


sub_arr[count] = {};
sub_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[1].name + '/' + cnt_arr[5].name;
sub_arr[count].name = 'report';
sub_arr[count++].nu = 'mqtt://' + cse.host + '/' + ae.name + '_visualLocalizationReport' + '?ct=' + ae.bodytype; // mqtt
//sub_arr[count++].nu = 'http://' + ip.address() + ':' + ae.port + '/noti?ct=json'; // http


sub_arr[count] = {};
sub_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[2].name + '/' + cnt_arr[6].name;
sub_arr[count].name = 'report';
sub_arr[count++].nu = 'mqtt://' + cse.host + '/' + ae.name + '_humanDetectionReport' + '?ct=' + ae.bodytype; // mqtt
//sub_arr[count++].nu = 'http://' + ip.address() + ':' + ae.port + '/noti?ct=json'; // http


sub_arr[count] = {};
sub_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[3].name + '/' + cnt_arr[7].name;
sub_arr[count].name = 'report';
sub_arr[count++].nu = 'mqtt://' + cse.host + '/' + ae.name + '_humanPoseEstimationReport' + '?ct=' + ae.bodytype; // mqtt
//sub_arr[count++].nu = 'http://' + ip.address() + ':' + ae.port + '/noti?ct=json'; // http


sub_arr[count] = {};
sub_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[4].name + '/' + cnt_arr[8].name;
sub_arr[count].name = 'report';
sub_arr[count++].nu = 'mqtt://' + cse.host + '/' + ae.name + '_beverageCfReport' + '?ct=' + ae.bodytype; // mqtt
//sub_arr[count++].nu = 'http://' + ip.address() + ':' + ae.port + '/noti?ct=json'; // http

sub_arr[count] = {};
sub_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[9].name ;
sub_arr[count].name = 'status';
sub_arr[count++].nu = 'mqtt://' + cse.host + '/' + ae.name + '_status' + '?ct=' + ae.bodytype; // mqtt
//sub_arr[count++].nu = 'http://' + ip.address() + ':' + ae.port + '/noti?ct=json'; // http

// build acp: not complete
acp.parent = '/' + cse.name + '/' + ae.name;
acp.name = 'acp-' + ae.name;
acp.id = ae.id;


conf.usesecure  = 'disable';

if(conf.usesecure === 'enable') {
    cse.mqttport = '{PORT}';
}

conf.cse = cse;
conf.ae = ae;
conf.cnt = cnt_arr;
conf.sub = sub_arr;
conf.acp = acp;


module.exports = conf;


// build cnt
var count = 0;
// cnt_arr[count] = {};
// cnt_arr[count].parent = '/' + cse.name + '/' + ae.name;
// cnt_arr[count].lbl = 'radar-sensor';
// cnt_arr[count].name = 'radar-sensor';

// // build sub
// sub_arr[count] = {};
// sub_arr[count].parent = '/' + cse.name + '/' + ae.name + '/' + cnt_arr[count].name;
// sub_arr[count].name = 'radar-sensor';
// sub_arr[count++].nu = 'mqtt://' + cse.host + '/' + ae.id + '?ct=' + ae.bodytype; // mqtt
// //sub_arr[count++].nu = 'http://' + ip.address() + ':' + ae.port + '/noti?ct=json'; // http

//---------------------------------------------------------------------------------------//
