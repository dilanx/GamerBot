const fs = require('fs');
const tmi = require('tmi.js');

const user = "GamerBotTwitch";
const key = fs.readFileSync('.keys', 'utf8');

const channelList = ["blockhead7360"];

var commands = {};

for (var i = 0; i < channelList.length; i++) {
	
	var chan = channelList[i];
	fs.readFile("../channels/" + chan + ".txt", 'utf8', (err, data) => {
		if (err){
			
			return;
			
		}
		
		var lines = data.split("\n");
		
		commands[chan] = {};
		
		for (var l = 0; l < lines.length; l++) {
			
			var lineData = lines[l].split(" : ");
			
			if (lineData[0].length < 2 || lineData[1].length < 2) {
				
				continue;
				
			}
			
			commands[chan][lineData[0]] = lineData[1];
			
			
		}
		
		
	});
}

const options = {
	
	identity: {
		username: user,
		password: key
	},
	channels: channelList
	
};

const client = new tmi.client(options);

client.on('message', messageHandler);
client.on('connected', connectionHandler);

client.connect();

function messageHandler(target, context, msg, self){
	
	if (self) return;
	
	var channel = target.substring(1);

	if (!(channel in commands)) return;
	
	var possibleCommands = commands[channel];
	
	const cmd = msg.trim().toLowerCase();
	
	if (cmd in possibleCommands) {
		
		client.say(channel, possibleCommands[cmd]);
		
	}
	
}

function connectionHandler(address, port) {
	
	console.log(`i've connected to ${address}:${port}!`);
	
}



