# TARDIS ScriptKit

tardis-usertools 2.0

This is intended to be a python package to extend the existing tardis-usertools package written by Kevin Campbell <kev@tardis.ed.ac.uk>

## Usage
Intended usage for now, to be finalised when written

For sysmans (root only)

```tardis adduser <username>```

```tardis deluser <username>```

For all users

```tardis create sip```

```tardis create xmpp```

## Extending
The main "routing" file can be found in ```tardis/script.py```. This contains the master ArgumentParser for the ```tardis``` command.

Adding a new command can be done like so:
```python
newcommand_p = subparsers.add_parser('newcommand', description='Enter a short description of your new command', help='Enter another short description of your new command')
newcommand_p.add_argument('positional_argument')
```
This would add a new command, to be called with ```tardis newcommand```, requiring one argument (which would be specified in the help text as ```positional_argument```)

At minimum the argument name and help are required (Pull requests without providing help text will be rejected). Help text shows in the subcommand list as such:
```
usage: tardis [-h] {adduser,deluser} ...

optional arguments:
  -h, --help         show this help message and exit

Subcommands:
  TARDIS Project Toolkit

  {adduser,deluser}
    adduser          Create a new user on TARDIS
    deluser          Delete a user from TARDIS
```
 - The string "Create a new user on TARDIS" is the help text for the adduser_p subparser
 - The string "TARDIS Project Toolkit" is the description text for the main parser
 
Each subparser gets its own help page too, so ```tardis adduser -h``` would produce specific help for the adduser command.
Docs for argparse can be found here: https://docs.python.org/2.7/library/argparse.html