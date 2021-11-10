Miscellaneous files
---

* `cracked-lists.py` -- A program that automates reading of [Cracked](http://www.cracked.com/)'s list-articles by loading them and displaying only their headers.

* `dominoes.py` -- A solution for the dominoes problem [posted in The Guardian on 15th Jun 2020](https://www.theguardian.com/science/2020/jun/15/can-you-solve-it-domino-dancing#comment-141591276).

* `gchq-morse.py` -- A program that solves the Morse part of [GCHQ's centenary puzzle](https://static.standard.co.uk/s3fs-public/thumbnails/image/2019/02/14/16/gchqplaque1402.jpg).

* `knight_around_board.py` -- A program that finds a way for a knight to visit all the fields on the board.

* `knuth-puzzle.py` -- A program that (usually :-)) solves [Knuth's puzzle](https://twitter.com/nhigham/status/752947988977311744).

* `lock.py` -- A programmatic solution for a lock problem.

* `match_brackets.py` -- A simple module to tackle a problem of checking if the brackets in an expression match.

* `mhmt.py` -- A crude solver for [Move Here Move There](https://www.newgrounds.com/portal/view/718498).

* `nonogram.py` -- [Nonogram](https://en.wikipedia.org/wiki/Nonogram) solver.

* `pardoners_puzzle.py` -- A program that solves the [Pardoner's puzzle](http://math-fail.com/2015/02/the-pardoners-puzzle.html).

* `pastebin.py` -- A simple module for pasting text to [Pastebin](https://pastebin.com/). No other fancy features (for now).

* `pdf-pages.py` -- A native Python module to get pages' sizes from PDF. I needed this to get pages' sizes from huge PDFs (containing large images) without big memory consumption.

* `prob_55_56.py` -- A parallel processing exercise: experimental verification of a probability experiment (throw dice until you get `55` or `56`; which is more likely?).

* `pyver.py` -- A simple program that prints the version of Python and some of its commonly used libraries (SciPy, NumPy, Matplotlib).

* `sandwich.py` -- A quick solution to the [club sandwich problem](https://www.theguardian.com/science/2019/dec/16/can-you-solve-it-the-club-sandwich-problem) from Guardian.

* `sanitizer.py` -- A Python module that implements `@sanitizer` decorator for creating properties with trivial getter and deleter, but full control of assigned values through a setter.

* `sorting_elves.py` -- A quick solution to the [elves sorting problem](https://www.theguardian.com/science/2016/dec/19/can-you-solve-it-are-you-more-sorted-than-a-german-elf-at-christmas).

* `two_teams.py` -- A programmatic solution for a [fun probability problem](https://twitter.com/DrFrostMaths/status/1247632591408242688).

* `unshake.sh` -- A very rudimentary bash script to unshake videos. The results go to `/tmp/unshake/` without modifying the original files. It requires [`ffmpeg`](https://ffmpeg.org/) compiled with the `--enable-libvidstab` option (which most distros' versions are). For more details, see [here](https://scottlinux.com/2016/09/17/video-stabilization-using-vidstab-and-ffmpeg-on-linux/).
