"""Shared CLI wrapper utilities for small tool entrypoints (impl-level)."""
import argparse
import sys

from collections.abc import Callable, Sequence
from typing import Optional, TypeVar

TParser = TypeVar("TParser", bound=argparse.ArgumentParser)


def build_arg_parser(
  *,
  description: str,
  epilog: Optional[str] = None,
  formatter_class: type[argparse.HelpFormatter] = argparse.RawDescriptionHelpFormatter,
) -> argparse.ArgumentParser:
  return argparse.ArgumentParser(
    description=description,
    formatter_class=formatter_class,
    epilog=epilog,
  )


def run_cli_and_exit(
  main_func: Callable[[Optional[Sequence[str]]], int],
  argv: Optional[Sequence[str]] = None,
) -> None:
  args = sys.argv[1:] if argv is None else argv
  raise SystemExit(main_func(args))

