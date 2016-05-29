def stringCompression(string):# basic string compression using counts of repeated chars
    compressedString = ''
    count = 0                 # this will account for repeated characters
    lastChar = ''             # initially empty
    for char in string:
        if char != lastChar:  # this is when you add the last num and next letter
            if count > 1:
                compressedString += str(count)
            compressedString += char
            count = 1
            lastChar = char
        else:                 # char = lastChar
            count += 1        # tallies up the number of times the character is repeated
    if count > 1:  compressedString += str(count)
    return compressedString

testString = 'aabcccccaaa'
print stringCompression(testString), 'should be "a2b1c5a3"'