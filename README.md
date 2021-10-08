# TARDIS ScriptKit

tardis-usertools 2.0

This is intended to be a python package to extend the existing tardis-usertools package written by Kevin Campbell &lt;kev@tardis.ed.ac.uk&gt;

## Usage
Intended usage for now, to be finalised when written

For sysmans (root only)

```tardis adduser <username>```

```tardis showuser <username>```

## Extending
The main "routing" file can be found in ```tardis/interactive.py```. This contains the master ArgumentParser for the ```tardis``` command.
Docs for argparse can be found here: https://docs.python.org/2.7/library/argparse.html

To add your own command, you should create a module, or package, in the ```tardis.commands``` package.
This module should have at minimum two functions - one for setup, one for the command.

Setup should take a single argument, and will be passed the argument parser to allow for argument instantiation.
It should look somewhat like below:
```python
def setup(parser):
    parser.add_argument("username", help="Username for the new user")
```

The command function takes one argument, which is the resultant [Namespace](https://docs.python.org/2.7/library/argparse.html#the-namespace-object) object containing the relevant parsed arguments.

Carrying on from the above example, you would use it as such:
```python
def command(args):
    print(args.username)
```

Finally, add the command to ```interactive.py```.

```python
# Command: adduser
# Author: Harry Reeder <skull@tardis.ed.ac.uk>
adduser_p = subparsers.add_parser('adduser', description="Create a new user on TARDIS", help="Create a new user on TARDIS")
adduser_setup(adduser_p)
adduser_p.set_defaults(func=adduser_func)
```

A couple of style notes for interactive.py
 - Import both the setup and command in one line, aliased as ```<command>_setup``` and ```<command>_func```, where &lt;command&gt; is your command.
 - Group your command imports inside interactive.py - adduser, updateuser, and deluser should be together, as should add/update/del group for example. 
 - When creating the subparser, you MUST expose a help text, and preferably a description.
 - All subparser arguments should be defined in your setup function, keep them out of interactive.py for readability.

## Developing, Testing, and Installing
To develop, check out a copy, and then
```
$ virtualenv env            # Create a working environment
$ pip install -r requirements.txt # install requirements file
$ source env/bin/activate   # Activate it, allowing you to install and test without being root
$ pip install -e .          # Install in editable mode
```

You'll also need to make sure that you have an LDAP config file that you can read to pass to tardis.ldaptools.LDAP().

To deploy, check out a copy and then
```
$ su root
# python setup.py install
```
