---
title: "Problem Analysis & Program Design"
created: 2025-05-22
tags:
  - ipc144
  - pseudo-code
  - flowcharts
  - program-design
  - problem-analysis
---

{~ hero layout="text_right_image_left" image_src="https://images.unsplash.com/photo-1729710877242-6305c22c18b8?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" image_alt="Abstract code on a screen representing operating systems and programming" min_height="20vh" text_color="black" text_bg_color="white-75" content_align_vertical="center" ~}
## Session Objectives

* To write pseudo code.
* To convert Flowcharts into Pseudo code.
* To perform walkthroughs on pseudo code.
* To represent data files in flowcharts and pseudo code.
* To represent arrays in flowcharts and pseudo code.
{~~}

---

## Pseudo code

Pseudo code (pseudo = fake, code = computer language) is a fake computer language (3GL). Throughout these discussions, we have been using the Program Development Cycle (PDC) to move from a high-level, general analysis of a problem to a more specific solution.

{~ accordion title="From IPO Charts to Pseudo code" ~}
The IPO Chart gave us a brief description of the inputs, the outputs, and a list of processes for transforming the inputs into the outputs. The Flowchart gave us, diagrammatically, the sequence or order in which processes and decisions are made to solve the problem.

Some people are more comfortable with pseudo code and may choose to design their algorithm directly in pseudo code. In this course, you are expected to be able to read and write both flowcharts and pseudo code.
{~~}

{~ accordion title="Nature of Pseudo code" ~}
Pseudo code is a hybrid between structured computer languages (C, Pascal, BASIC, etc.) and English. The control structures we defined in Flowcharting are represented here.

Because pseudo code is not a real computer language and it has loose rules for implementation, it can be used to develop an algorithm for any structured computer language. From the pseudo code (after testing the algorithm), the program can be coded by translating the statements in pseudo code to statements in the programming language (C in our case).
{~~}

{~ card title="Characteristics of Pseudo code" ~}
There is no real standard for pseudo code; however, it must have the following characteristics:

* Statements are written in simple English.
* Each instruction is written on a separate line.
* Keywords are used to consistently name the parts of control structures.
* Indentation is used to make parts of a control structure conspicuous.
* Each set of instructions is written from top to bottom, with only one entry point and one exit point.
{~~}

Again, the three basic structures are represented:

* Simple sequence
* Decision
* Iteration

---

## Simple Sequence

### Assigning Variables

This is where variables are manipulated within your algorithm.
The New Webster's Computer Terms dictionary definition: **A variable is a symbolic name representing a value that changes during the program's execution.**
Back to Secondary School algebra, remember these?
`5 = 5x + 4y`
`0 = 5(x + y) - 3x + 5`
Solve for `x` and `y`. `x` and `y` are the variables.

{~ accordion title="Naming Variables" ~}
When creating a name for a variable, make it meaningful. Don't make it too long (you will end up with writer's cramp now and carpal tunnel syndrome later).

`ttlOrder` may be not as meaningful as `total_order_for_customer` but it is easier to write and probably conveys enough information about how the variable is being used. The other extreme, `t`, is obviously meaningless. Use your judgement. Ask yourself: "If I had to re-read this in another year, would the variable name be meaningful?"

Try to get used to writing variables names as lower case strings of characters without spaces. You can use underscores or “camel bumps” to help make more complex variables names easier to read:

* A simple one-word variable: `section`
* A complex variable name using underscores: `total_order_for_customer`
* A complex variable name using camel bumps: `totalOrderForCustomer`
{~~}

### Types of Variable Assignments

There are two types of variable assignments:

1. When you are initializing a variable.
2. As a result of some processing.

**It will be considered BAD FORM not to initialize a variable before using it.**

Verbs used for initialization: `INITIALIZE`, `SET`.

```pseudo
INITIALIZE counter to zero
SET recordSize to 500
```

### Assignments from Processing

Expect to use the symbol `=` (will be referred to as an assignment operator).

```pseudo
totalPrice = basePrice + salesTax
```

You can use this form for initializing variables as well:

```pseudo
counterA = 0
counterB = 0
recordSize = 500
```

The value on the right side of the `=` is calculated (if necessary) and then placed into the variable that is on the left side of the `=`. You can have only one variable on the left of the `=`.

{~ card title="Flowchart vs. Pseudo code: Assignments" ~}
**Flowchart Snippet:**
![Flowchart vs. Pseudo code: Assignments](https://i.imgur.com/Da7Yap6.png)
{~~}

**Pseudo code:**

```pseudo
counterA = 0
SET recordSize to 500
```

### Input of Data

Verbs used: `READ`, `GET`.

* `READ` usually refers to data being read from a file.
* `GET` usually refers to data being entered by the user at a keyboard.

Examples:

```pseudo
READ address FROM customerFile
GET newAddress
```

{~ card title="Flowchart vs. Pseudo code: Input" ~}
**Flowchart Snippet:**
![Flowchart vs. Pseudo code: Input](https://i.imgur.com/v0T3s10.png)
{~~}

**Pseudo code:**

```pseudo
READ address FROM customerFile
GET newAddress
```

### Output of Data

Verbs used: `PRINT`, `WRITE`, `OUTPUT`, `DISPLAY`.

* `PRINT` usually refers to data being sent to a printer.
* `WRITE` usually refers to data being sent to a file.
* `OUTPUT` and `DISPLAY` usually refer to data being sent to a monitor.

In pseudo code, the output is not necessarily formatted (made to look pretty), so it is common to simply list each piece of information separated by commas. E.g., `DISPLAY count, average`.

```pseudo
PRINT "Program Completed"
WRITE newAddress TO customerFile
OUTPUT name, address, postalCode
DISPLAY "End of Data Reached"
```

{~ accordion title="Output Examples & Literal Strings" ~}
Note that any phrase that is to be output EXACTLY as written is enclosed in quotes. This helps to differentiate between a literal string and a variable name.
E.g., `DISPLAY The average is average over a range of count values`
Should be written as:
`DISPLAY “The average is”, average, “over a range of ”, count, “values”`
{~~}

{~ card title="Flowchart vs. Pseudo code: Output" ~}
**Flowchart Snippet:**
![Flowchart vs. Pseudo code: Output](https://i.imgur.com/u8u1GwV.png)
{~~}

**Pseudo code:**

```pseudo
WRITE address TO customerFile
DISPLAY newAddress
```

### Computation

Some verbs used: `ADD`, `COMPUTE`, `CALCULATE`, `MULTIPLY`, `DIVIDE`, `SUBTRACT`.

Examples:

```pseudo
ADD 1 TO counter
COMPUTE tax = price x 0.15
degreesC = (degreesF- 32) x (5/9)
```

{~ card title="Flowchart vs. Pseudo code: Computation" ~}
**Flowchart Snippet:**
![Flowchart vs. Pseudo code: Computation](https://i.imgur.com/9sQWjsC.png)
{~~}

**Pseudo code:**

```pseudo
ADD 1 TO counter
degreesC = (degreesF- 32) × (5/9)
```

### Module Call

Verbs Used: `CALL`.

```pseudo
CALL myModule
CALL yourModule(myvar)
CALL theirModule(yourVar, myVar, someVar)
```

The exception is when you are invoking a function that is returning a value to a variable in the parent flowchart:

```pseudo
var = yourFunction(a, b)
```

{~ card title="Flowchart vs. Pseudo code: Module Call" ~}
**Flowchart Snippet:**
![Flowchart vs. Pseudo code: Module Call](https://i.imgur.com/BAvCpXc.png)
{~~}

**Pseudo code:**

```pseudo
CALL dspMenu(x)
x = func(a, b, c)
```

---

## Selection (Decision)

### Simple Decision

The basic form looks like:

```pseudo
IF condition THEN
    statement(s)
ELSE
    statement(s)
ENDIF
```

* If the condition is **TRUE**, then the statements immediately following the `THEN` keyword are executed, until the `ELSE` clause. At which point the program resumes after the `ENDIF` keyword.
* If the condition is **FALSE**, then the statements immediately following the `ELSE` keyword are executed.
Note the indentation that is being used:
* Makes it easier to see the components of the selection.
* Provides for readability.

{~ card title="Flowchart vs. Pseudo code: Simple Decision" ~}
**Flowchart Snippet:**
![Flowchart vs. Pseudo code: Simple Decision](https://i.imgur.com/GBmGyiD.png)
{~~}

**Pseudo code:**

```pseudo
IF a > b THEN
    c = e + f
ELSE
    c = t x q
ENDIF
```

{~ accordion title="Visualizing Simple Decision Flow" ~}
**Flowchart Structure:**
![Flowchart vs. Pseudo code: Simple Decision](https://i.imgur.com/cKPsZQV.png)
{~~}

**Pseudo code Structure:**

```pseudo
IF condition THEN
    StatementA
    StatementB
    StatementC
ELSE
    StatementD
    StatementE
ENDIF
```

### Importance of Indentation

An example of no indentation:

```pseudo
IF a = b THEN
DISPLAY "A equals B"
c = (23 - d) / 2
lifeUniverseEverything = 42
ELSE
DISPLAY "A does not equal B"
vogons = 1
earth = 0
ENDIF
```

With indentation:

```pseudo
IF a = b THEN
    DISPLAY "A equals B"
    c = (23 - d) / 2
    lifeUniverseEverything = 42
ELSE
    DISPLAY "A does not equal B"
    vogons = 1
    earth = 0
ENDIF
```

{~ accordion title="Simple Decision without ELSE" ~}
What if you don't need an `ELSE` clause?

**Flowchart Snippet:**
![Flowchart vs. Pseudo code: Simple Decision](https://i.imgur.com/YfJ8IGA.png)
{~~}

**Pseudo code:**

```pseudo
IF avg < 50 THEN
    DISPLAY "Low average”
ENDIF
```

### Multiway Decision

The basic form looks like:

```pseudo
SWITCH (variable)
    CASE (option)
        statement(s)
    CASE (option)
        statement(s)
    . . .
    CASE (option)
        statement(s)
    DEFAULT
        statement(s)
ENDSWITCH
```

* `variable` is what is being tested.
* `option` is the possible value that `variable` takes on, and represents the new path of logic.

{~ card title="Flowchart vs. Pseudo code: Multiway Decision" ~}
**Flowchart Snippet:**
![flowchart](https://i.imgur.com/zZkX2nY.png)
{~~}

**Pseudo code:**

```pseudo
SWITCH (usrSel)
    CASE (‘A’)
        res = a + b
    CASE (‘S’)
        res = a - b
    CASE (‘M’)
        res = a × b
    CASE (‘D’)
        res = a ÷ b
    DEFAULT
        DISPLAY "Invalid option”
ENDSWITCH
```

---

## Iteration (Loop)

### Pre-Test Loop

The basic form looks like:

```pseudo
DOWHILE condition
    statement(s)
ENDWHILE
```

{~ card title="Flowchart vs. Pseudo code: Pre-Test Loop" ~}
**Flowchart Snippet:**
![Flowchart vs. Pseudo code: Pre-Test Loop](https://i.imgur.com/ACiOwqS.png)
{~~}

**Pseudo code:**

```pseudo
DOWHILE i < 10
    b = b × c
    i = i + 1
ENDWHILE
```

### Post-Test Loop

The basic form looks like:

```pseudo
DO
    statement(s)
WHILE condition
```

{~ card title="Flowchart vs. Pseudo code: Post-Test Loop" ~}
**Flowchart Snippet:**
![Flowchart vs. Pseudo code: Post-Test Loop](https://i.imgur.com/6x6cmCD.png)
{~~}

**Pseudo code:**

```pseudo
DO
    b = b × c
    i = i + 1
WHILE i < 10
```

---

## Pseudo code Walkthroughs

{~ practice title="Walkthrough 1" difficulty="Beginner" focus="Post-Test Loop & Variables" ~}
What is the output of the following pseudo code?
{~~}

```pseudo
num = 1
var = 0
DO
    var = num + var
    DISPLAY var
    num = num + 2
WHILE num < 7
```

{~ practice title="Walkthrough 2" difficulty="Intermediate" focus="Nested Loops & Factorials" ~}
What is the output of the following pseudo code?
{~~}

```pseudo
i = 5
DOWHILE i > 0
    j = i
    f = 1
    DOWHILE j > 1
        f = f * j
        j = j – 1
    ENDWHILE
    DISPLAY f
    i = i – 1
ENDWHILE
DISPLAY “Done”
```
