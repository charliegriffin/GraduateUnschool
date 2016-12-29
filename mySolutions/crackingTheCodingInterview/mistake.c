/* 12.1  Find the mistake(s) in the following code */

#include <stdio.h>

int main(void)
{
    unsigned int i;
    // for (i = 100; i >= 0; --i)
    //    printf("%d\n",i);
    // expected result print 100, 99, ..., 0
    // error is that unsigned ints are by definition >= 0
    // so loop will never exit
    // also, %u for unsigned ints

    // corrected
    for (i = 100; i != 0; --i)
        printf("%u\n",i);
    printf("%d\n",i);

    // alternative correction: int i;

    return 0;
}
