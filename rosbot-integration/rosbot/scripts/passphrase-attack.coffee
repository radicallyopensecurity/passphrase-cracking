# Description:
#
# Dependencies:
#
# Configuration:
#
# Commands:
#   crackphrase
#
# Author:
#   Luc

module.exports = (robot) ->

  run_cmd = (cmd, args, cb ) ->
    spawn = require("child_process").spawn
    child = spawn(cmd, args)
    child.stdout.on "data", (buffer) -> cb buffer.toString()
    child.stderr.on "data", (buffer) -> cb buffer.toString()

  robot.respond /crackphrase\s(.*)/i, id:'chatops.crackphrase', (msg) ->
    cmd = '/usr/bin/pyton';
    args = ['-f', 'bash/crackphrase', '--'];
    args.push msg.match[1];
    run_cmd cmd, args, (text) -> msg.send text;

