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
newcommand_p = subparsers.add_parser('newcommand', description='Enter a short description of your new command')
newcommand_p.add_argument('positional_argument')
```
This would add a new command, to be called with ```tardis newcommand```, requiring one argument (which would be specified in the help text as ```positional_argument```)