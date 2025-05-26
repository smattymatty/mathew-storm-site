---
title: "03 - Structured Program Development"
created: 2025-05-26
tags:
  - c-programming
  - structured-programming
  - algorithms
  - pseudocode
  - control-structures
  - if-statement
  - while-loop
  - iteration
  - top-down-design
---

Before writing a program to solve a problem, you must have a thorough understanding of the problem and a carefully planned solution approach. Chapters 3 and 4 discuss developing structured computer programs. In Section 4.11, we summarize the structured programming techniques developed here and in Chapter 4.

{~ label_seperator ~}
## Algorithms
{~~}

The solution to any computing problem involves executing a series of actions in a specific order. An **algorithm** is a **procedure** for solving a problem in terms of:

1.  the actions to be executed, and
2.  the order in which to execute them

{~ label_seperator ~}
## Pseudocode
{~~}

**Pseudocode** is an informal artificial language similar to everyday English that helps you develop algorithms before converting them to structured C programs. It's convenient and user friendly, allowing you to think out a program before writing it.

{~ label_seperator ~}
## Control Structures
{~~}

Normally statements in a program execute one after the other in the order in which you write them. This is called **sequential execution**. As you'll soon see, various C statements enable you to specify that the next statement to execute may be other than the next one in sequence. This is called **transfer of control**.

{~ label_seperator ~}
## The `if` Selection Statement
{~~}

Selection statements choose among alternative courses of action. For example, suppose the passing grade on an exam is 60. The following pseudocode statement determines whether the condition “student’s grade is greater than or equal to 60” is true or false:

```
If student’s grade is greater than or equal to 60 
    Print “Passed”
```

If true, then “Passed” is printed, and the next pseudocode statement in order is “performed.” Remember that pseudocode isn’t a real programming language. If false, the printing is ignored, and the next pseudocode statement in order is performed. The preceding pseudocode is written in C as

```c
if (grade >= 60) {
    puts("Passed");
}
```

Of course, you’ll also need to declare the `int` variable `grade`, but the C `if` statement code corresponds closely to the pseudocode. This is one of the properties of pseudocode that makes it such a useful program-development tool.

{~ label_seperator ~}
## The `while` Iteration Statement
{~~}

An **iteration statement** (also called a **repetition statement** or **loop**) repeats an action while some condition remains true. The pseudocode statement

```
While there are more items on my shopping list 
    Purchase next item and cross it off my list
```

describes the iteration that occurs during a shopping trip. The condition “there are more items on my shopping list” may be true or false. If it’s true, the shopper performs the action “Purchase next item and cross it off my list” repeatedly while the condition remains true. Eventually, the condition will become false (when the last item on the shopping list has been purchased and crossed off the list). At this point, the iteration terminates, and the first pseudocode statement after the iteration statement “executes.”

### Calculating the first power of 3 greater than 100

As a `while` statement example, consider a program segment that finds the first power of 3 larger than 100. The integer variable `product` is initialized to 3. When the following code segment finishes executing, `product` will contain the desired answer:

```c
int product = 3;

while(product <= 100) {
    product = 3 * product;
}
```

The loop repeatedly multiplies `product` by 3, so it takes on the values 9, 27 and 81 successively. When `product` becomes 243, the condition `product <= 100` becomes false, terminating the iteration—`product`’s final value is 243. Execution continues with the next statement after the `while`. An action in the `while` statement’s body must eventually cause the condition to become false; otherwise, the loop will never terminate—a logic error called an infinite loop. The statement(s) contained in a `while` iteration statement constitute its body, which may be a single statement or a compound statement.

{~ label_seperator ~}
## Formulating Algorithms Case Study 1: Counter-Controlled Iteration
{~~}

Consider the following problem statement:

> A class of ten students took a quiz. The grades (integers in the range 0 to 100) for this quiz are available to you. Determine the class average on the quiz.

The class average is the sum of the grades divided by the number of students. The algorithm to solve this problem must input the grades, then calculate and display the class average.

### Pseudocode for the Class-Average Problem

Let’s use pseudocode to list the actions to execute and specify the order in which they should execute. We use counter-controlled iteration to input the grades one at a time. This technique uses a variable called a counter to specify the number of times a set of statements should execute. In this example, we know that ten students took a quiz, so we need to input 10 grades. Iteration terminates when the counter exceeds 10.

```
Set total to zero
Set grade counter to one

While grade counter is less than or equal to ten
    Input the next grade
    Add the grade into the total
    Add one to the grade counter

Set the class average to the total divided by ten
Print the class average
```

The C code implementation:
```c
#include <stdio.h>

int main(void) {
    int total = 0; // Initialize total to zero
    int counter = 1; // Initialize grade counter to one
    
    while (counter <= 10) { // Loop 10 times
        printf("%s", "Enter Grade: "); // Prompt user
        int grade = 0; // Define grade variable
        scanf("%d", &grade); // Read grade from user
        total = total + grade; // Add grade to total
        counter = counter + 1; // Increment counter
    }
    
    int average = total / 10; // Calculate average
    printf("Class average is %d\n", average); // Print average
    return 0;
}
```

{~ accordion title="Key Concepts: Totals, Counters, and Initialization" ~}
A `total` is a variable (line 8 in the C code, referring to `int total = 0;`) used to accumulate the sum of a series of values. A `counter` is a variable (line 9, `int counter = 1;`) used to count—in this case, to count the number of grades entered. Variables for totals should be initialized to zero; otherwise, the sum would include the previous value stored in the total’s memory location. You should initialize all counters and totals. Counters typically are initialized to zero or one, depending on their use—we’ll present examples of each. An uninitialized variable contains a “garbage” value—the value last stored in the memory location reserved for that variable. If a counter or total isn’t initialized, the results of your program will probably be incorrect. These are examples of logic errors.
{~~}

{~ label_seperator ~}
## Formulating Algorithms with Top-Down, Stepwise Refinement Case Study 2: Sentinel-Controlled Iteration
{~~}

Consider the following problem:

> Develop a class-averaging program that will process an arbitrary number of grades each time the program is run.

In the first class-average example, we knew there were 10 grades in advance. In this example, no indication is given of how many grades the user might input. The program must process an arbitrary number of grades. How can the program determine when to stop inputting grades? How will it know when to calculate and print the class average?

{~ accordion title="Understanding Sentinel Values" ~}
One way is to use a **sentinel value** to indicate “end of data entry.” A sentinel value also is called a signal value, a dummy value, or a flag value. The user types grades until all legitimate grades have been entered. The user then types the sentinel value to indicate “the last grade has been entered.” Sentinel-controlled iteration is often called indefinite iteration because the number of iterations isn’t known before the loop begins executing.

You should choose a sentinel value that cannot be confused with an acceptable input value. Grades on a quiz are non-negative integers, so –1 is an acceptable sentinel value for this problem. Thus, a run of the class-average program might process a stream of inputs such as 95, 96, 75, 74, 89 and –1. The program would then compute and print the class average for the grades 95, 96, 75, 74, and 89. The sentinel value –1 should not enter into the averaging calculation.
{~~}

```c
// fig03_04.c
// Class-average program with sentinel-controlled iteration.
#include <stdio.h>

// function main begins program execution
int main(void) {
   // initialization phase
   int total = 0; // initialize total
   int counter = 0; // initialize loop counter

   // processing phase
   // get first grade from user
   printf("%s", "Enter grade, -1 to end: "); // prompt for input
   int grade = 0; // grade value
   scanf("%d", &grade); // read grade from user                 

   // loop while sentinel value not yet read from user
   while (grade != -1) {
      total = total + grade; // add grade to total
      counter = counter + 1; // increment counter

      // get next grade from user
      printf("%s", "Enter grade, -1 to end: "); // prompt for input
      scanf("%d", &grade); // read next grade                  
   } // end while

   // termination phase
   // if user entered at least one grade
   if (counter != 0) {

      // calculate average of all grades entered
      double average = (double) total / counter; // avoid truncation

      // display average with two digits of precision
      printf("Class average is %.2f\n", average);
   } // end if   
   else { // if no grades were entered, output message
      puts("No grades were entered");
   } // end else
} // end function main

```

{~ accordion title="Applying Top-Down, Stepwise Refinement" ~}
We approach the class-average program with a technique called **top-down, stepwise refinement**, which is essential to developing well-structured programs. We begin with a pseudocode representation of the top:

> Determine the class average for the quiz.

The top is a single statement that conveys the program’s overall function. As such, the top is, in effect, a complete representation of a program. Unfortunately, the top rarely conveys a sufficient amount of detail for writing the C program. So we now begin the refinement process. We divide the top into smaller tasks listed in the order in which they need to be performed. This results in the following first refinement:

> Initialize variables
> Input, sum, and count the quiz grades
> Calculate and print the class average

Here, only the sequence structure has been used—the steps listed should execute in order, one after the other. Each refinement, as well as the top itself, is a complete specification of the algorithm. Only the level of detail varies.
{~~}

{~ accordion title="Type Conversion: Explicit and Implicit" ~}
Averages often are values such as 7.2 or –93.5 that contain fractional parts. These floating-point numbers can be represented by the data type `double`. Dividing two `int`s results in integer division—any fractional part of the calculation is truncated (that is, lost). You can produce a floating-point calculation with integer values by first creating temporary floating-point numbers. C provides the unary cast operator to accomplish this task. For example:
`
double average = (double) total / counter;
`
This uses the cast operator `(double)` to create a temporary floating-point copy of its operand, `total`. The value stored in `total` is still an integer. Using a cast operator in this manner is called **explicit conversion**. The calculation now consists of a floating-point value—the temporary `double` version of `total`—divided by the `int` value stored in `counter`.

C requires the operand data types in arithmetic expressions only to be identical. In mixed-type expressions, the compiler performs an operation called **implicit conversion** on selected operands to ensure that they're of the same type. For example, in an expression containing the data types `int` and `double`, copies of `int` operands are made and implicitly converted to type `double`. After we explicitly convert `total` to a `double`, the compiler implicitly makes a `double` copy of `counter`, then performs floating-point division and assigns the floating-point result to `average`.

Cast operators are formed by placing parentheses around a type name. A cast is a unary operator that takes only one operand. C also supports unary versions of the plus (`+`) and minus (`-`) operators, so you can write expressions such as `-7` or `+5`. Cast operators group right-to-left and have the same precedence as other unary operators such as unary `+` and unary `-`.
{~~}

{~ accordion title="Formatting Floating-Point Output" ~}
The `printf` conversion specification `%.2f` can be used to format a `double` value. The `f` specifies that a floating-point value will be printed. The `.2` is the precision—the value will have two (2) digits to the right of the decimal point. If the `%f` conversion specification is used without specifying the precision, the default precision is 6 digits to the right of the decimal point, as if the conversion specification `%.6f` had been used. When floating-point values are printed with precision, the printed value is rounded to the indicated number of decimal positions. The value in memory is unaltered. The following statements display the values 3.45 and 3.4, respectively:
`
printf("%.2f\n", 3.446); // displays 3.45
printf("%.1f\n", 3.446); // displays 3.4
`
{~~}

{~ label_seperator ~}
## Secure C Programming
{~~}

{~ accordion title="Understanding Arithmetic Overflow" ~}
The code presented an addition program that calculated the sum of two `int` values with the statement:
`c
sum = integer1 + integer2;
`
Even this simple statement has a potential problem. Adding the integers could result in a value too large to store in the `int` variable `sum`. This is known as **arithmetic overflow** and can cause undefined behavior, possibly leaving a system open to attack.

The constants `INT_MAX` and `INT_MIN` represent the platform-specific maximum and minimum values that can be stored in an `int` variable. These constants are defined in the header `<limits.h>`. There are similar constants for the other integral types that we’ll introduce in the next chapter. You can see your platform’s values for these constants by opening the header `<limits.h>` in a text editor.
{~~}