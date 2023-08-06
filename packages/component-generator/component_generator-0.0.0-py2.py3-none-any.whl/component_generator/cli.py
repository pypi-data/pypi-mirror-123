"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcomponent_generator` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``component_generator.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``component_generator.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse

from generate import generate_component, ComponentType

parser = argparse.ArgumentParser(description="Component Generator.")
parser.add_argument("--component", help="Component name.")
parser.add_argument("--service", help="Service name.")
parser.add_argument("--consumer", help="Consumer name.")


def main(args=None):
    args = parser.parse_args(args=args)

    if not hasattr(args, "component"):
        parser.error("Please pass component name")
    generate_component(ComponentType.COMPONENT, args.component, args.component)
    if args.service:
        generate_component(ComponentType.SERVICE, args.service, args.component)
    if args.consumer:
        generate_component(ComponentType.CONSUMER, args.consumer, args.component)
