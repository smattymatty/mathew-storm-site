---
title: "02 - C Programming"
created: 2025-05-26
tags:
  - c-programming
  - introduction
  - programming-basics
  - chapter-2
  - stdio
  - variables
  - operators
  - decision-making
---

The C language facilitates a structured and disciplined approach to computer-program design. This chapter introduces C programming and presents several examples illustrating many fundamental C features. We analyze each example one statement at a time. In Chapters 3 and 4, we introduce structured programming-a methodology that will help you produce clear, easy-to-maintain programs. We then use the structured approach throughout the remainder of the text. This chapter concludes with the first of our “Secure C Programming” sections.

{~ label_seperator ~}
## A Simple C Program: Printing a Line of Text
{~~}

We begin with a simple C program that prints a line of text.

```c
// fig02_01.c
// A first program in C.
#include <stdio.h>

// function main begins program execution
int main(void) {
    printf("Welcome to C!\n"); 
    return 0; 
} // end function main
```

**Output:**
```
Welcome to C!
```

{~ accordion title="Comments" ~}
Lines 1 and 2 begin with `//`, indicating that these two lines are comments. You insert comments to document programs and improve program readability. Comments do not cause the computer to perform actions when you execute programs-they’re simply ignored.
{~~}

{~ accordion title="include Preprocessor Directive" ~}
Line 3 is a C preprocessor directive. The preprocessor handles lines beginning with `#` before compilation. Line 3 tells the preprocessor to include the contents of the standard input/output header (`<stdio.h>`). This is a file containing information the compiler uses to ensure that you correctly use standard input/output library functions such as `printf` (line 7).
{~~}

{~ accordion title="The Linker and Executables" ~}
Standard library functions like `printf` and `scanf` are not part of the C programming language. For example, the compiler cannot find a spelling error in `printf` or `scanf`. When compiling a `printf` statement, the compiler merely provides space in the object program for a “call” to the library function. But the compiler does not know where the library functions are-the linker does.

When the linker runs, it locates the library functions and inserts the proper calls to these functions in the object program. Now the object program is complete and ready to execute. The linked program is called an executable. If the function name is misspelled, the linker will spot the error-it will not be able to match the name in the program with the name of any known function in the libraries.
{~~}

{~ label_seperator ~}
## Another Simple C Program: Adding Two Integers
{~~}

Our next program uses the `scanf` standard library function to obtain two integers typed by a user at the keyboard, then computes their sum and displays the result using `printf`. The program and sample output are shown in Fig. 2.4. In the input/output dialog box of Fig. 2.4, we emphasize the numbers entered by the user in bold.

```c
// fig02_04.c
// Addition program.
#include <stdio.h>

// function main begins program execution 
int main(void) {
    int integer1 = 0; // will hold first number user enters 
    int integer2 = 0; // will hold second number user enters

    printf("Enter first integer: "); // prompt
    scanf("%d", &integer1); // read an integer

    printf("Enter second integer: "); // prompt
    scanf("%d", &integer2); // read an integer

    int sum = 0; // variable in which sum will be stored
    sum = integer1 + integer2; // assign total to sum

    printf("Sum is %d\n", sum); // print sum
    return 0;
} // end function main
```

**Sample Output:**
```
Enter first integer: 45
Enter second integer: 72
Sum is 117
```

{~ accordion title="Variable and Variable Definitions" ~}
Lines 7 and 8 are definitions. The names `integer1` and `integer2` are variables - locations in memory where the program can store values for later use. These definitions specify that `integer1` and `integer2` have type `int`. This means they’ll hold whole-number integer values, such as 7, –11, 0 and 31914.

Lines 7 and 8 initialise each variable to 0 by following the variable’s name with an `=` and a value. Although it’s not necessary to explicitly initialise every variable, doing so will help avoid many common problems.
{~~}

{~ accordion title="Define Variables Before They Are Used" ~}
All variables must be defined with a name and a type before they can be used in a program. You can place each variable definition anywhere in `main` before that variable’s first use in the code. In general, you should define variables close to their first use.
{~~}

{~ accordion title="Identifiers and Case Sensitivity" ~}
A variable name can be any valid identifier. Each identifier may consist of letters, digits and underscores (`_`), but may not begin with a digit. C is case sensitive, so `a1` and `A1` are different identifiers. A variable name should start with a lowercase letter. Later in the text, we’ll assign special significance to identifiers that begin with a capital letter and identifiers that use all capital letters.

Choosing meaningful variable names helps make a program self-documenting, so fewer comments are needed. Avoid starting identifiers with an underscore (`_`) to prevent conflicts with compiler-generated identifiers and standard library identifiers.
{~~}

{~ accordion title="Prompting Messages" ~}
Line 10 displays `"Enter first integer: "`. This message is called a prompt because it tells the user to take a specific action.
{~~}

{~ accordion title="The scanf Function and Formatted Inputs" ~}
Line 11 uses `scanf` to obtain a value from the user. The function reads from the standard input, which is usually the keyboard.

The “f” in `scanf` stands for “formatted.” This `scanf` has two arguments-`"%d"` and `&integer1`. The `"%d"` is the format control string. It indicates the type of data the user should enter. The `%d` conversion specification specifies that the data should be an integer-the `d` stands for “decimal integer”. A `%` character begins each conversion specification.

`scanf`’s second argument begins with an ampersand (`&`) followed by the variable name. The `&` is the address operator and, when combined with the variable name, tells `scanf` the location (or address) in memory of the variable `integer1`. `scanf` then stores the value the user enters at that memory location.
{~~}

{~ accordion title="Defining the sum variable" ~}
Line 16 defines the `int` variable `sum` and initializes it to `0` before we use `sum` in line 17.
{~~}

{~ accordion title="Assignment Statement" ~}
The assignment statement in line 17 calculates the total of variables `integer1` and `integer2`, then assigns the result to variable `sum` using the assignment operator (`=`). The statement is read as, “`sum` gets the value of the expression `integer1 + integer2`.” Most calculations are performed in assignments.
{~~}

{~ accordion title="Binary Operators" ~}
The `=` operator and the `+` operator are binary operators-each has two operands. The `+` operator’s operands are `integer1` and `integer2`. The `=` operator’s operands are `sum` and the value of the expression `integer1 + integer2`. Place spaces on either side of a binary operator to make the operator stand out and make the program more readable.
{~~}

{~ card title="Calculations in printf Statement" ~}
Actually, we do not need the variable `sum`, because we can perform the calculation in the `printf` statement. So, lines 16-19 can be replaced with:
{~~}

```c
printf("Sum is %d\n", integer1 + integer2);
```

{~ label_seperator ~}
## Memory Concepts
{~~}

**Understanding Memory Allocation and Values**
Every variable has a name, a type, a value, and a location in the computer's memory.

Consider Line 11 from the addition program:
```c
scanf("%d", &integer1); // read an integer
```
When a value is placed in a memory location (like `integer1`), it replaces the location's previous value, which is lost. So, this process is said to be **destructive**.

Similarly, for:
```c
scanf("%d", &integer2); // read an integer
```
The value entered by the user destructively overwrites whatever was previously in `integer2`.

Once we have values for `integer1` and `integer2`, the statement:
```c
sum = integer1 + integer2; // assign total to sum
```
adds these values and places the total into variable `sum`, replacing its previous value (which was `0` from its initialization).

The `integer1` and `integer2` values are unchanged by the calculation (`integer1 + integer2`). The calculation uses their values but does not destroy them. Thus, reading a value from a memory location is **nondestructive**.

{~ label_seperator ~}
## Arithmetic in C
{~~}

Most C programs perform calculations using the following binary **arithmetic operators**:

- `+` (addition)
- `-` (subtraction)
- `*` (multiplication)
- `/` (division)
- `%` (remainder)

Note the use of various special symbols not used in algebra. The **asterisk** (`*`) indicates multiplication, and the percent sign (`%`) denotes the remainder operator (introduced below).

{~ accordion title="Integer Division and the Remainder Operator" ~}
**Integer division** yields an integer result, so `7/4` evaluates to `1`, and `17/5` evaluates to `3`. Any fractional part in integer division is discarded (i.e., truncated-not rounded).

The integer-only **remainder operator, `%`**, yields the remainder after integer division. For example, `7 % 4` yields `3`, and `17 % 5` yields `2`. The remainder operator can only be used with integer operands.
{~~}

{~ card title="Rules of Operator Precedence" ~}
C applies the operations in arithmetic expressions in a precise sequence determined by the following **rules of operator precedence,** which are generally the same as those in algebra:

1.  **Parentheses `()`**: Expressions grouped in parentheses evaluate first. If parentheses are nested, the innermost pair evaluates first. This is the "Highest level of precedence."
2.  **Multiplication `*`, Division `/`, Remainder `%`**: These are applied next. If an expression contains several such operations, evaluation proceeds from left to right. They share the "Same level of precedence."
3.  **Addition `+`, Subtraction `-`**: These are evaluated next. If an expression contains several such operations, evaluation proceeds from left to right. These two operators have the same level of precedence, which is lower than multiplication/division/remainder.
4.  **Assignment `=`**: The assignment operator is evaluated last.
{~~}

{~ label_seperator ~}
## Decision Making: Equality and Relational Operators
{~~}

Executable statements can also make decisions. For example, a program might determine whether a person's grade on an exam is greater than or equal to 60, so it can decide whether to print a message.

A **condition** is an expression that can be true or false. This section introduces the **`if` statement**, which allows a program to make a decision based on a condition's value. If the condition is true, the statement (or block of statements in curly braces `{}`) in the `if`'s body executes; otherwise, it does not.

```c
// fig02_05.c 
// Using if statements, relational operators, and equality operators.
#include <stdio.h>

int main(void) {
    printf("Enter two integers, and I will tell you\n");
    printf("the relationship they satisfy: ");
    int number1 = 0;
    int number2 = 0;

    scanf("%d %d", &number1, &number2); // read two integers

    if (number1 == number2) {
        printf("%d is equal to %d\n", number1, number2);
    } // end if

    if (number1 != number2) {
        printf("%d is not equal to %d\n", number1, number2);
    } // end if

    if (number1 > number2) {
        printf("%d is greater than %d\n", number1, number2);
    } // end if
    
    if (number1 < number2) {
        printf("%d is less than %d\n", number1, number2);
    } // end if
    
    if (number1 >= number2) {
        printf("%d is greater than or equal to %d\n", number1, number2);
    } // end if

    if (number1 <= number2) {
        printf("%d is less than or equal to %d\n", number1, number2);
    } // end if
    return 0;
} // end function main
```

{~ label_seperator ~}
## Secure C Programming
{~~}

{~ accordion title="Avoid Single-Argument printfs" ~}
`printf`'s first argument is a format string, which `printf` inspects for conversion specifications (like `%d` or `%s`). It then replaces each conversion specification with a subsequent argument's value. `printf` tries to do this regardless of whether there is a subsequent argument to use for each conversion specifier it finds.

If a string variable `myString` might contain `%` characters, calling `printf(myString);` is a security risk. If `myString` contains format specifiers, `printf` will try to find corresponding arguments on the stack, potentially reading or writing unintended memory locations. This can lead to crashes or exploitation.

**Safe Way:** Always provide a format string as the first argument, and then the variable as a subsequent argument if you intend to print its content as a string:
`printf("%s", myString);`

This ensures `myString` is treated purely as data to be printed, not as a format string to be interpreted.
{~~}