# Vogala
A programming language completely in Dutch, inspired by the [Rockstar programming language](https://codewithrockstar.com/online)!

I named this Vogala, after the famous first three Dutch written words "Hebban olla Vogala", where Vogala would mean birds.
I saw the Rockstar programming language when looking over the adventofcode subreddit, and thought it would be fun to write my own!
It was a bit of a challenge, but I had tried to make my own interpreter before (back then, with the help of [this blog by Ruslan Pivak](https://ruslanspivak.com/lsbasi-part1/). I have gained more programming experience though, so it went smoother this time. 

### Summary

The file "primes.va" gives an example of what a program might look like. You can check inside "keywords.json" what the keywords for different operations actually are. Sometimes there are multiple for the same operation, and usually the default operator you would expect is also in there (e.g. = for assignment, or + for addition).

What the program does is that it translates the given script into tokens. It reads the given script, removes any enters and splits it at any whitespace locations. It starts translating it into tokens, based on what it expects. The expected statements can be seen in "grammar.txt". I do not know precisely how to formally write a grammar for a language, but I think that that is the idea of it. 

#### Program
The basics are: the program consists of compound statements and loops. A loop is simply a loop expression of the form
```
  id GOES (?:FROM int expr) TO int expr END
```
followed by a compound statement, and ended with a `LOCAL END` keyword, or 
```WHILE condition DO END```
where usually the `END` token you would use would be ":". Again, followed by a compound statement, and ended with a `BREAK` keyword or a `LOCAL END` keyword.

#### Compound Statement
A compound statement is really just 0 or more statements. A compound statement is ended with a `LOCAL END` keyword, like `...`, `!` or `?`.

#### Statement
A statement can be a few things. For example
```id (OBJ ASSIGN|STR ASSIGN) expr```
which would assign a value `expr` to `id`. Note that variable id's may have spaces in them all you want! My language doesn't care about capitalization either, so the variable `Dennis Hilhorst` would be the same as `DeNnIs    HiLHorSt`. However, it is a different variable than `Den nis Hil horst`.
A statement can also be a pritn expression, simply
```PRINT expr```
which speaks for itself. You can also have an epxression that is just an object. This can be an integer, a string, an `id` or whatever. The program will basically just ignore this statement. I did this so that you could make your program look more like text! Something I added after all of this was in place was conditionals. You can have an expression of the form
```
IF (expr) END
    compound statement
    BREAK
ELSE END
```

One of the last things I did was adding functions. You can assign functions as
```id FUNC ASSIGN (?: arg_id (,|OP))*```
followed by a compound statement, and eventually a `RETURN expr` statement. You can also call functions using
```id CALL (expr ,)*```
so the function id, followed by a `CALL` keyword, followed by comma-separated expressions to use as arguments.

Before I mentioned an `OP` token, this is one of `ADD, SUB, MUL, DIV, OR, AND`, but also `GT, LT, LE, GE`, etc. You can find all these in "keywords.json". 

#### Expressions
and `expr` is and expression of the form
```
  NOT? (id|value) (OP NOT? (id|value))*
```
where `NOT` acts as both the logical not AND the unary minus operation. Similar to Python, the built in types can all also be used as booleans, where and `INT` is False if and only if it is 0 etc. An expression can also be of the form
```
id CALL (argument,)*
```
which is a function that would return something. 

#### Value types
I implemented only a few value types. `INT`, `REAL`, `BOOL`, `STRING` and `FUNCTION`, if you would even call that a value type. First things first, an unknown expression is usually interpreted as integer, where each word represents 1 digit with its length (similar to the Rockstar Programming Language), so for example `A MAN` would be 13.

The tokenizer can sometimes immediately determine what type of variable something is. For example, a `STR ASSIGN` is always followed by a string, until and `END` or `LOCAL END` keyword is found. A string can also be signified to be a string if it is padded with single or double quotes. Note however, that any `END` keyword within the string will be interpreted as part of the string. 

A `REAL` is an expression with 1 comma, so for example `MAN, I WANT A DRINK` would be intepreted as 3.1415. Then there are default variable names. These can be found in the "vars.json" file. Examples are the numbers `EEN`, `TWEE`, up to `TIEN`, which just translates to ONE, TWO, ..., TEN. These are interpreted as the corresponding digits. There are also words like `NIETS`, `WAARDELOOS`, and some others, which would translate to NOTHING and WORTHLESS, and correspond to the `INT` 0, or `EENZAAM`, `ALLEEN` which correspond to the `INT` 1.

Booleans (true/false) must be represented this way. Their keywords are `WAAR`, `GELIJK` (or TRUE, RIGHT) for true and `ONWAAR`, `ONGELIJK` for false.

#### Prev keywords
Prev keywords are also something I learnt from the Rockstar language. Basically, by using one of these keywords, you reference the previous variable that was accessed. So for example the snippet 
```
Je moeder was niet alleen. Zij is met je vader. roep je moeder.
```
which would translate to 
```
Your mother was not alone. She is with your father. Call your mother.
```
(where call is not the function call keyword, those are similar to the word USE). and which would compile to
```
[JE MOEDER] OBJ ASSIGN NOT [1]
[PREV] IADD [JE VADER]
PRINT [JE MOEDER]
```
would assign the value NOT 1 (so -1) to the `JE MOEDER` variable, then it would add `JE VADER`, which is not an assigned variable, so interpreted as 25, to the previous variable accessed (so `JE MOEDER` would then be 24). And then it would `PRINT` the expression `JE MOEDER`, which evaluates to 24 then. 

#### IDE
I also made an IDE with syntax highlighting. It also has a compile button, which turns the code you wrote into the tokens, and formats them the way I did above. You can then also run the program, and observe its output! Making the syntax highlighting was also a fun challenge.

#### A longer example
I will explain the "primes.va" script I wrote as an example below. This script nicely displays the capabilities and available methods in the language.

The program is:
```
Boris Johnson is de premier van Engeland.

Engelsen gebruiken thee en koekjes:
    zolang thee zo goed is als koekjes:
        thee is zonder koekjes...
    geef me thee!

John Bercow gebruikt de hamer:
    Willem Alexander loopt van NL naar de hamer:
        als niets zo goed is als Engelsen op de hamer, Willem Alexander:
            geef me geen gelijk!
        Maxima is Willem Alexander maal zichzelf.
        als Maxima beter is dan de hamer:
            ga terug!!
    geef me gelijk...


Donald Trump loopt van NL naar Boris Johnson:
    als John Bercow op Donald Trump:
        roep Donald Trump!!
```
Note that the formatting of the text does not matter, but it is nicer to see what happens with it. The program translates to: Boris Johnson is the prime minister of England. English use tea and cookies: While tea is as good as cookies: tea is without cookies... Give me tea!
John Bercrow uses the hammer: Willem Alexander goes from NL to the hammer: If nothing is as good as the English on the hammer, Willem Alexander: Don't agree with me `(in Dutch this is the same as Don't give me right)`. Maxima is Willem Alexander times himself `(A nice use of the PREV keyword to calculate a square)`. If Maxima is better than the hammer: Go back!! `(Double LOCAL END statement to end the IF and the FOR loop`. Don't agree with me `(Again, Don't give me right)`.
Donald Trump goes from NL to Boris Johnson: If John Bercrow on Donald Trump: Call Donald Trump!!
Since I implemented the "normal" operators, I can also translate this into something that is a lot more readable:

```
limit = 2738;

Modulo gebruikt input, base:
    terwijl input >= base:
        input -= base!
    geef me input!

IsPrime gebruikt number:
    Potential Divisor gaat van 2 naar number:
        als 0 >= Modulo op number, Potential Divisor:
            geef me onwaar!
        Square = Potential Divisor * Potential Divisor.
        als Square >= number:
            ga terug!!
    geef me gelijk!


Integer loopt van 2 naar limit:
    als IsPrime op Integer:
        roep Integer!!
```
Where it is a lot more clear what it does. It calculates all primes up to 2738! The tokenizer turn this into:
```
[BORIS JOHNSON] OBJ ASSIGN [DE PREMIER VAN ENGELAND]
[ENGELSEN] FUNC ASSIGN [THEE] [KOEKJES]
    WHILE [THEE] GEQ [KOEKJES]
        [THEE] ISUB [KOEKJES]
    RETURN [THEE]
[JOHN BERCOW] FUNC ASSIGN [DE HAMER]
    [WILLEM ALEXANDER] GOES FROM [NL] TO [DE HAMER]
        IF [0] GEQ FUNC CALL [DE HAMER] , [WILLEM ALEXANDER]
            RETURN NOT [True]
        [MAXIMA] OBJ ASSIGN [WILLEM ALEXANDER] MUL [PREV]
        IF [MAXIMA] GT [DE HAMER]
            BREAK
    RETURN [True]
[DONALD TRUMP] GOES FROM [NL] TO [BORIS JOHNSON]
    IF FUNC CALL [DONALD TRUMP]
        PRINT [DONALD TRUMP]
```
After which is it a bit more clear what it does. And after running, it produces
```
INT(2)
INT(3)
INT(5)
INT(7)
INT(11)
INT(13)
INT(17)
INT(19)
INT(23)
INT(29)
INT(31)
INT(37)
INT(41)
INT(43)
INT(47)
INT(53)
INT(59)
INT(61)
INT(67)
...
```
Precisely as we had hoped!
