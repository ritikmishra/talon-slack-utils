from contractions import Decontract
#Test 1
phrase = "n't"
fixer = Decontract(phrase)
print fixer.decontract()

#Test 2
phrase = "Bob would've ate pie"
fixer = Decontract(phrase)
print fixer.decontract()

#Test 3
phrase = "I don't want to have herpes"
fixer = Decontract(phrase)
print fixer.decontract()
#returns tokens


#Test 4
phrase = "Bob's herpes hadn't yet spread from person to person"
fixer = Decontract(phrase)
print fixer.decontract()
