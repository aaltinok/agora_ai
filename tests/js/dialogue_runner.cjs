// Kullanım: node dialogue_runner.cjs <json> <topic> <pick> <reflectPick> <earlyAfter>
const fs = require('fs');
const D = require('../../vr/src/dialogue.js');
const [, , file, topic, pick, reflect, earlyAfter] = process.argv;
const script = D.fromJSON(JSON.parse(fs.readFileSync(file, 'utf8')));
const st = D.newState(script, topic);
let n = 0;
while (st.phase !== 'done') {
  if (Number(earlyAfter) >= 0 && n === Number(earlyAfter)) { D.finishEarly(script, st); n += 1000; continue; }
  const opts = D.options(script, st);
  const i = st.phase === 'reflection' ? Number(reflect) : Number(pick) % opts.length;
  D.choose(script, st, opts[i].id); n += 1;
}
process.stdout.write(JSON.stringify(st));
