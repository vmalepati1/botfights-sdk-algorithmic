Countdown
=========

Can you write a bot that beats [Rachel Riley at Countdown](https://www.youtube.com/watch?v=ZjCbWg4ZUAY)? Your input is a list of integers, and a target, and your bot should return instructions to yield a result as close as possible to the target. For example, if your input is `[40, [7 2 3]]`, you could return `1 2 * 0 *`, for a result of 40, two away from the target.

Note your response must be encoded in [Reverse Polish Notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation), with operands referenced by index.

Your score for this round is two squared, 4; your score for a fight is the sum of scores for all rounds.

### How To Play

1\. First, clone the [botfights-sdk](https://github.com/botfights/botfights-sdk) repository, and change to the countdown directory

    $ git clone https://github.com/botfights/botfights-sdk.git
    $ cd botfights-sdk/countdown/python

2\. Next, edit the [get_play()](https://github.com/botfights/botfights-sdk/blob/main/countdown/python/sample-bot.py#L33) function in the [sample bot](https://github.com/botfights/botfights-sdk/blob/main/countdown/sample-bot.py) (get\_play takes a tuple of (target, operand\_list) like `[40, [7 2 3 ]]` and should return your code encoded as a RPN string)

3\. Test your bot locally

    $ python botfights.py local countdown sample_bot.get_play

4\. Once your bot is ready to fight online, [register](https://botfights.ai/register) to get your credentials, if you haven't done so already

5\. Fight your bot remotely to make sure everything works (replace XXXXX and YYYYYYYYYY with your credentials)

    $ python botfights.py --username XXXX --password YYYYY remote countdown sample-bot.play

6\. Enter your bot in the [BOTFIGHTS VI](https://botfights.ai/tournament/botfights_vi) tournament (note the game options are much harder, you might want to test locally first)

    $ python botfights.py --username XXXX --password YYYY --tournament_id botfights_vi countdown sample-bot.play

7\. Rinse, repeat!

