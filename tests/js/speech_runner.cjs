// stdin: JSON [{transcript, options:[{id,label}]}] -> stdout: JSON [id|null, ...]; komutlar için {command:true}
const S = require('../../vr/src/speech.js');
const cases = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const out = cases.map((c) => c.command ? S.matchCommand(c.transcript) : ((S.matchOption(c.transcript, c.options) || {}).id || null));
process.stdout.write(JSON.stringify(out));
