# pladder-client

A client for the Web API of the Pladder Bot.

## Installation

    pip install pladder-client

You may need to replace `pip` with `pip3`.

## Usage

Create a token using `create-token` at the bot to get access. Then invoke `pladder-client` like this:

    pladder-client 'echo This is a test command'

The first time, `pladder-client` will ask for the API endpoint URL and the API token and then store it in a config file.

A `strutern` alias for `pladder-client` is also installed. They can be used interchangeably.
