import argparse

def main():
    parser = argparse.ArgumentParser(description='TARDIS Project Toolkit')
    subparsers = parser.add_subparsers()

    adduser_p = subparsers.add_parser('adduser', description="Create a new user on TARDIS")
    adduser_p.add_argument("username")

    deluser_p = subparsers.add_parser('deluser', description="Delete a user from TARDIS")
    deluser_p.add_argument("username")

    parser.parse_args()
