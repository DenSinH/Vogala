# Vogala
A programming language completely in Dutch, inspired by the [Rockstar programming language](https://codewithrockstar.com/online)!

I named this Vogala, after the famous first three Dutch written words "Hebban olla Vogala", where Vogala would mean birds.
I saw the Rockstar programming language when looking over the adventofcode subreddit, and thought it would be fun to write my own!
It was a bit of a challenge, but I had tried to make my own interpreter before (back then, with the help of [this blog by Ruslan Pivak](https://ruslanspivak.com/lsbasi-part1/). I have gained more programming experience though, so it went smoother this time. 

### Summary

The file primes.va gives an example of what a program might look like. You can check inside "keywords.json" what the keywords for different operations actually are. Sometimes there are multiple for the same operation, and usually the default operator you would expect is also in there (e.g. = for assignment, or + for addition).

What the program does is that it translates the given script into tokens
