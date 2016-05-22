let nlp = require("nlp_compromise");
var args = process.argv.slice(2);
var verb = args[0]
var tense = args[1]


//should go like
//node conjugate.js [verb] [tense] [noun type]
console.log(nlp.verb(verb).conjugate()[tense])
