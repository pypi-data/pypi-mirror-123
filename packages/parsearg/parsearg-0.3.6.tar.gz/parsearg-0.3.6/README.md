# Quickstart

## Overview

`parsearg` is a Python package for writing command-line interfaces ("CLI")
that augments (rather than replaces) the standard Python module for writing
CLIs, `argparse`. There is nothing wrong with `argparse`: It's fine in terms of
the *functionality* that it provides, but it can be clunky to use, especially
when a program's structure has subcommands, or nested subcommands (*i.e.*
subcommands that have subcommands).  Moreover, because of the imperative
nature of `argparse`, it makes it hard to understand how a program's interface
is structured (*viz.* the program's "view").

`parsearg` puts a layer on top of `argparse` that makes writing a CLI easy: You
declare your view (*i.e.* the CLI), with a `dict` so that the view
is a data structure (*i.e.* pure configuration). The data structure declares
the *intent* of the CLI and you no longer have to instruct `argparse`
on how to put the CLI together: `parsearg` does that for you.
In this respect, `parsearg` turns `argparse` on its head, in the sense that
it replaces imperative instructions with declarative data.

## Usage

Suppose we wish to create a program called `quickstart-todos.py` to manage the TO-DOs
of a set of different users. We want to have subprograms of `quickstart-todos.py`; for
example, we may want to create a user (`python quickstart-todos.py create user`, say),
or we may want to create a TO-DO for a particular user (`python quickstart-todos.py
create todo`, say).  We might also want to add optional parameters to each
subprogram such as the user's email and phone number, or the TO-DO's 
due date. An invocation of the program's CLI might look like
the following:
```bash
$ python quickstart-todos.py create user Bob --email=bob@email.com --phone=+1-212-555-1234
$ python quickstart-todos.py create todo Bob 'taxes' --due-date=2021-05-17
```
With `argparse`, the subprogram `create` would necessitate fiddling
with subparsers.  With `parsearg`, the CLI for the above is declared
with a `dict` and `parsearg.parser.ParseArg` supplants the normal use of
`argparse.ArgumentParser`. Moreover, the callback associated with
each subcommand is explicitly linked to its declaration.

```python
import sys
from parsearg import ParseArg

def create_user(args):
    print(f'created user: {args.name!r} (email: {args.email}, phone: {args.phone})')
    
def create_todo(args):
    print(f'created TO-DO for user {args.user!r}: {args.title} (due: {args.due_date})')
    
view = {
    'create|user': {
        'callback':   create_user,
        'name':       {'help': 'create user name', 'action': 'store'},
        '-e|--email': {'help': "create user's email address", 'action': 'store', 'default': ''},
        '-p|--phone': {'help': "create user's phone number", 'action': 'store', 'default': ''},
    },
    'create|todo': {
        'callback':   create_todo,
        'user':       {'help': 'user name', 'action': 'store'},
        'title':      {'help': 'title of TO-DO', 'action': 'store'},
        '-d|--due-date': {'help': 'due date for the TO-DO', 'action': 'store', 'default': None},
    },
}

def main(args):
    # ParseArg takes the place of argparse.ArgumentParser
    parser = ParseArg(d=view)

    # parser.parse_args returns an argparse.Namespace
    ns     = parser.parse_args(args)

    # ns.callback contains the function in the 'callback' key of 'view'
    result = ns.callback(ns)

if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    main(' '.join(args))
```

A fully-worked version of this TO-DO example is presented in the docs. The output
of the above is:
```
$ python quickstart-todos.py create user Bob --email=bob@email.com --phone=212-555-1234
created user: 'Bob' (email: bob@email.com, phone: 212-555-1234)

$ python quickstart-todos.py create todo Bob 'taxes' --due-date=2021-05-17
created TO-DO for user 'Bob': taxes (due: 2021-05-17)
```

Because `parsearg` is built on top of `argparse`, all the usual features
are available, such as the extensive help features (essentially
making the CLI self-documenting):
```
$ python quickstart-todos.py --help
usage: quickstart-todos.py [-h] {create} ...

positional arguments:
  {create}

optional arguments:
  -h, --help  show this help message and exit

$ python quickstart-todos.py create --help
usage: quickstart-todos.py create [-h] {todo,user} ...

positional arguments:
  {todo,user}

optional arguments:
  -h, --help   show this help message and exit

$ python quickstart-todos.py create user --help
usage: quickstart-todos.py create user [-h] [-e EMAIL] [-p PHONE] name

positional arguments:
  name                  create user name

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        create user's email address
  -p PHONE, --phone PHONE
                        create user's phone number
$ python quickstart-todos.py create todo --help
usage: quickstart-todos.py create todo [-h] [-d DUE_DATE] user title

positional arguments:
  user                  user name
  title                 title of to-do

optional arguments:
  -h, --help            show this help message and exit
  -d DUE_DATE, --due-date DUE_DATE
                        due date for the to-do
```