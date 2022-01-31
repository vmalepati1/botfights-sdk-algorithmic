Wordle
======

### How To Play

1\. First, clone the [botfights-sdk](https://github.com/botfights/botfights-sdk) repository

    $ git clone https://github.com/botfights/botfights-sdk.git
    $ cd botfights-sdk/wordle/python

2\. Next, edit the [play()](https://github.com/botfights/botfights-sdk/blob/main/wordle/python/sample-bot.py#L33) function in the [sample bot](https://github.com/botfights/botfights-sdk/blob/main/wordle/python/sample-bot.py) (play takes a string like `"-----:00000,arose:31112,amend:31211"` and should return your next guess like `"abbey"`)

3\. Test your bot locally

    $ python wordle.py bot wordlist.txt sample-bot.play 10

4\. Once your bot is ready to fight online, [register](https://botfights.ai/register) to get your credentials

5\. Fight your bot in the test tournament to make sure everything works (replace XXXXX and YYYYYYYYYY with your credentials)

    $ python wordle.py botfights sample-bot.play XXXXX YYYYYYYYYY test

6\. Enter your bot in the [BOTFIGHTS I](https://botfights.ai/tournament/botfights_i) tournament (the full 1000 words)

    $ python wordle.py botfights sample-bot.play XXXXX YYYYYYYYYY botfights_i

7\. Rinse, repeat!

