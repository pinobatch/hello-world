Bellwethers
===========

By 2009, I was tiring of making free software functional workalikes
of falling block games.  I set some rules for myself, planning
to voluntarily withdraw some of my works from the Internet if a
copyright owner either won a lawsuit or convinced Free Software
Foundation to pull the block game from [GNU Emacs Amusements].
One of those happened in June 2012.

I was treating the block game in GNU Emacs Amusements as a
[bellwether], or an indicator of future trends.  I'm developing
a list of other bellwethers for free software gaming.

[GNU Emacs Amusements]: https://www.gnu.org/software/emacs/manual/html_node/emacs/Amusements.html
[bellwether]: https://en.wiktionary.org/wiki/bellwether

Five-letter word game
---------------------

The player guesses a five-letter English word, and after each guess,
the game reports which letters are in the correct position, which
letters are present and need to be moved, and which aren't present
at all.  The player must guess the word within six tries.

In March 2024, The New York Times Company asserted copyright and
trademark against Reactle and other reimplementations of this game
whose names resemble "Wordle", the game it had acquired from
Josh Wardle.  If these disappear, we're in trouble:

- [Word] by Charles Reid, which preceded Wordle.  Includes feedback
  for correct letters, though the feedback for present letters is
  less intuitive due to lack of color on late 1970s terminals.
  Nonwords aren't rejected yet.
- [Lingo game show], first aired in 1987, predating Wordle by three
  decades.  Introduces the standard design for the guess grid with a
  color code for present and correct letters, as well as rejection of
  nonwords.  Though a [Lingo episode in 2006] uses different colors,
  a [Lingo episode in 2011] makes them yellow and green, the same
  colors that would appear years later in Wordle.  Only five tries
  are allowed because the first correct letter is given.
- [Lingo for Game Boy] by PCSL, with [review by GameBoyle], which
  includes guess grid and present/correct feedback (as circle and
  square due to grayscale display), with on-screen keyboard below it.
- [Hello] by Lynn, with [source code][lynn/hello]
- [Raw Word]: guess grid is circles and correct letters are cyan

[Word]: https://www.atariarchives.org/basicgames/showpage.php?page=181
[Lingo game show]: https://en.wikipedia.org/wiki/Lingo_%28American_game_show%29
[Lingo episode in 2006]: https://www.youtube.com/watch?v=sC0kie6dPjo&t=129s
[Lingo episode in 2011]: https://www.youtube.com/watch?v=38gklfz0SQo
[Lingo for Game Boy]: https://gamefaqs.gamespot.com/gameboy/622486-lingo
[review by GameBoyle]: https://youtu.be/bBeUcE8Mc0E?t=82
[Hello]: https://hellowordl.net/
[lynn/hello]: https://github.com/lynn/hello
[Raw Word]: https://www.rawstory.com/st/Games_-_Wordy
