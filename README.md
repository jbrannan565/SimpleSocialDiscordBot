# SimpBot
A bot for managing a Simple Social Club over discord. 
A comprehensive layout of what a Simple Social Club is, and what the goals of such a club should be is to come.

## Getting started
Create a [.env](https://github.com/jbrannan565/SimpleSocialDiscordBot/wiki/Environment-Variables) file with at least the attributes DISCORD_TOKEN and COMMAND_PREFIX based on .example_env.

```
# Make the directory where club content should be stored
mkdir resources 
# create an envoinment file
cp .example_env .env
# edit .env to have the required data
vim .env
```

## Installation
Configure a local MongoDB service
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install discord and dotenv

```bash
pip install discord python-dotenv
```

## Usage

```
python3 main.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Changes to be Implemented
1. Parlimentary system for group goal construction.
2. System for members to report their progress on goals, called "Goals".
3. Resources commands should be updated to use the Group object rather than manual string parsing.

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
