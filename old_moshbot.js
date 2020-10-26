var Discord = require("discord.io");

var auth = require("./auth.json");
var data = require("./data.json");

console.log("hjskfgwisgfs");
var dataPath = require("path").resolve(__dirname, "data.json");

var bot = new Discord.Client({
	token: auth.token,
	autorun: true
});

bot.on('ready', function() {
	console.log("Logged in as %s - %s\n", bot.username, bot.id);
});

bot.on('message', function(user, userID, channelID, msg, event) {
	var message = msg.toLowerCase().replace(/  +/g, " ");;

	if (isCommand(message)) {

		var args = message.substring(1).split(" ");

		//ABORT COMMAND (ADMIN ONLY)
		if (args[0] === "abort") {

			if (checkAdmin(channelID, userID)){
				bot.sendMessage({to: channelID, message: ":flower_playing_cards: Wird heruntergefahren. Bis bald!"});
				console.log("Bot has been disabled by  "+ user + "#" + event.d.author.discriminator + ".")
				bot.disconnect();
			} else {
				noPermissions(channelID);
			}

		//ADD NEW SWEAR COMMAND (ADMIN ONLY)
		} else if (args[0] === "addswear") {

			if (checkAdmin(channelID, userID)) {
				bot.sendMessage({to: channelID, message: ":loudspeaker: **" + args[1] + "** wird ab sofort als ein Schimpfwort erkannt!"});
				data.swears.push(args[1]);

				fs.writeFile(dataPath, JSON.stringify(data, null, 4), function (err){
					if (err) return console.log(err);
					console.log("User " + user + "#" + event.d.author.discriminator + " added a new swear: " + args[1]);
				});

			} else {
				noPermissions(channelID);
			}

		//DELETE EXISTING SWEAR COMMAND (ADMIN ONLY)
		} else if (args[0] === "deleteswear") {

			if (checkAdmin(channelID, userID)) {
				var swearIndex = data.swears.indexOf(args[1]);

				if (swearIndex > -1) {

					bot.sendMessage({to: channelID, message: ":loudspeaker: **" + args[1] + "** wird nicht mehr als Schimpfwort erkannt!"});
					data.swears.splice(swearIndex, 1);

					fs.writeFile(dataPath, JSON.stringify(data, null, 4), function (err){
						if (err) return console.log(err);
						console.log("User " + user + "#" + event.d.author.discriminator + " deleted a swear: " + args[1]);
					});

				} else {
					bot.sendMessage({to: channelID, message: ":zap: **" + args[1] + "** wurde nicht in dem Verzeichnis gefunden."});
					console.log("User " + user + "#" + event.d.author.discriminator + " tried deleting the swear " + args[1] + ", however it has not been found.")
				}
			} else {
				noPermissions(channelID);
			}
		}

	} else {
		swearDetect(user, userID, channelID, message, msg, event);
	}

});

function swearDetect(user, userID, channelID, message, UpperMessage, event) {
	if (userID === bot.id) {return false; }
	data.swears.forEach(function(element) {
		if (message.includes(element)) {
			console.log("User " + user + "#" + event.d.author.discriminator + " said the swearword \"" + element + "\".");

			bot.deleteMessage({channelID:channelID, messageID:event.d.id});

			bot.sendMessage({to: userID, message: ":warning: In deiner Nachricht haben wir ein Schimpfwort erkannt! \`\`\`" + UpperMessage + "\`\`\`"});
		}
	});
}

function getMember(channelID, userID) {
	var server = getServer(channelID)
	return server.members[userID];
}

function getServer(channelID) {
	try {
		return bot.servers[bot.channels[channelID].guild_id];
	} catch (e) {
		return undefined;
	}
}

function checkAdmin(channelID, userID) {
	if (getServer(channelID, userID) === undefined) {return false;}

	var roles = [];
	admin = false;
	var member = getMember(channelID, userID);

	member.roles.forEach(function(role) {
		roles.push(getServer(channelID).roles[role]);
	});

	roles.forEach(function(role) {
		if (role.GENERAL_ADMINISTRATOR) {
			admin = true;
		}
	});

	return admin;
}

function isCommand(message) {
	if (message.substring(0, 1) == "!") {
		return true;
	} else {
		return false;
	}
}

function noPermissions(channelID) {
	bot.sendMessage({to: channelID, message: ":no_entry: Deine Rechte reichen für diesen Command nicht aus!"});
}