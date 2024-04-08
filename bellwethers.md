Bellwethers
===========

By 2009, I was tiring of making free software functional workalikes of falling block games. I set some rules for myself, planning to voluntarily withdraw some of my works from the Internet if a copyright owner either won a lawsuit or convinced Free Software Foundation to pull the block game from [GNU Emacs Amusements](https://www.gnu.org/software/emacs/manual/html_node/emacs/Amusements.html). One of those happened in June 2012.

I was treating the block game in GNU Emacs Amusements as a [bellwether](https://en.wiktionary.org/wiki/bellwether), or an indicator of future trends. I'm developing a list of other bellwethers for free software gaming.

Five-letter word game
---------------------

The player guesses a five-letter English word, and after each guess, the game reports which letters are in the correct position, which letters are present and need to be moved, and which aren't present at all. The player must guess the word within six tries.

In March 2024, The New York Times Company asserted copyright and trademark against Reactle and other reimplementations of this game whose names resemble "Wordle", the game it had acquired from Josh Wardle. If these disappear, we're in trouble:

- [Word](https://www.atariarchives.org/basicgames/showpage.php?page=181) by Charles Reid, which preceded Wordle. Includes feedback for correct letters, though the feedback for present letters is less intuitive due to lack of color on late 1970s terminals. Nonwords aren't rejected yet.
- [Lingo game show](https://en.wikipedia.org/wiki/Lingo_(American_game_show)), first aired in 1987, predating Wordle by three decades. Introduces the standard design for the guess grid with a color code for present and correct letters, as well as rejection of nonwords. Though [an episode in 2006](https://www.youtube.com/watch?v=sC0kie6dPjo&t=129s) uses different colors, an [episode in 2011](https://www.youtube.com/watch?v=38gklfz0SQo) makes them yellow and green, the same colors that appear in Wordle. Only five tries are allowed because the first correct letter is given.
- [Lingo for Game Boy](https://gamefaqs.gamespot.com/gameboy/622486-lingo) by PCSL, with [review by GameBoyle](https://youtu.be/bBeUcE8Mc0E?t=82), which includes guess grid and present/correct feedback (as circle and square due to grayscale display), with on-screen keyboard below it.
- [Hello](https://hellowordl.net/) by Lynn, with [source code](https://github.com/lynn/hello)
- [Raw Word](https://www.rawstory.com/st/Games_-_Wordy): guess grid is circles and correct letters are cyan
