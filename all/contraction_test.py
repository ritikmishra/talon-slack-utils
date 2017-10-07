"""Test the contraction module."""
from all.talker.contractions import Decontract

# Test 1
phrase = "n't"
fixer = Decontract(phrase)
print(fixer.decontract())

# Test 2
phrase = "Bob would've ate pie"
fixer = Decontract(phrase)
print(fixer.decontract())

# Test 3
phrase = "I don't want to have a car"
fixer = Decontract(phrase)
print(fixer.decontract())
# returns tokens


# Test 4
phrase = "Bob's bad news hadn't yet spread through the populace"
fixer = Decontract(phrase)
print(fixer.decontract())
