# template for Lab #4, Task #2
import lab4
 
def correct_errors(binmsg): 
    # your function definition here 
 
    # this version of the function always declares
    # a DecodingError!
    raise lab4.DecodingError,"uncorrectable error!"

if __name__ == '__main__':
    lab4.test_correct_errors(correct_errors)