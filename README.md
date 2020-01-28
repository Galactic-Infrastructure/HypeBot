# METACRUNCHER

HypeBot cog for the Red Discord bot.

Uses Solvertools by Robyn Speer. See LICENSE for details.

For ✈✈✈ Galactic Trendsetters ✈✈✈.


### Setup

First, make sure you have the "downloader" cog loaded on Red. Then:
  
    [p]repo add hypebot https://github.com/Galactic-Infrastructure/HypeBot
    [p]cog update
    [p]cog install hypebot hypebot

After installing, you can use

    [p]helper

to view the list of commands that HypeBot provides (separate from Eliza's default help command).


### Future Tasks

Currently, a good chunk of HypeBot's functionality has been gutted in order to port it as a cog for Red--namely, the Nikoli puzzle solving tools that rely on Z3Prover, which appears to require separate installation and isn't very portable as a Red cog.

It could possibly be useful to refactor this cog into multiple cogs for better organization.

It will probably also be useful to find a way to clean up the help command in a way that doesn't flood you with all of HypeBot's commands.