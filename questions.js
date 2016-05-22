// ** Can you give me an example of a living animal?
// ** Can you tell me the name of a famous actor?
// ** CAN YOU TELL JOKES
// ** Is the capital of Italy Milan?
// ** Name something you would find on a beach.
// ** Name something you would find at the North Pole.
// ** CAN I HAVE A PICTURE OF YOU
// ** Can you name two of Earth's oceans?
// ** Milk comes from what animal?
// ** Are you going on vacation thisll year?
// ** Will you teach me something?
// ** May I tell you a joke?
var args = process.argv.slice(2);
var question = args[0]
var ra = require("/usr/lib/node_modules/qtypes/lib/ruleClassify.js");

new ra(function(q) {
  var qtype = q.questionType(question);
  console.log(qtype)


});
