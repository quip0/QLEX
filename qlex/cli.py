"""CLI entry point for QLEX. Uses argparse — no external dependencies."""

from __future__ import annotations

import argparse
import json
import sys


def _cmd_list(args: argparse.Namespace) -> None:
    """Print all code names and IDs."""
    import qlex

    for code in qlex.list_codes():
        print(f"  {code.id:<25} {code.name}")


def _cmd_get(args: argparse.Namespace) -> None:
    """Print full summary of a code."""
    import qlex

    code = qlex.get(args.id)
    print(code.summary())


def _cmd_search(args: argparse.Namespace) -> None:
    """Print matching codes."""
    import qlex

    results = qlex.search(args.query)
    if not results:
        print(f"No codes matched '{args.query}'")
        return
    for code in results:
        print(f"  {code.id:<25} {code.name}")


def _cmd_compare(args: argparse.Namespace) -> None:
    """Print comparison table."""
    import qlex

    comp = qlex.compare(*args.ids)
    print(comp.table())


def _cmd_export(args: argparse.Namespace) -> None:
    """Print export config as JSON."""
    import qlex

    code = qlex.get(args.id)
    config = code.to_export_config()
    print(json.dumps(config, indent=2))


def _cmd_filter(args: argparse.Namespace) -> None:
    """Print filtered codes."""
    import qlex

    kwargs: dict = {}
    if args.family:
        kwargs["family"] = args.family
    if args.hardware:
        kwargs["hardware"] = args.hardware
    if args.min_threshold is not None:
        kwargs["min_threshold"] = args.min_threshold
    if args.fault_tolerant:
        kwargs["fault_tolerant"] = True
    if args.tag:
        kwargs["tags"] = args.tag

    results = qlex.filter(**kwargs)
    if not results:
        print("No codes matched the given filters")
        return
    for code in results:
        print(f"  {code.id:<25} {code.name}")


def _cmd_version(args: argparse.Namespace) -> None:
    """Print version and brand line."""
    import qlex

    print(f"QLEX {qlex.__version__}")
    print("by Qorex")


def _cmd_tui(args: argparse.Namespace) -> None:
    """Launch the TUI."""
    from qlex.ui.app import run

    run()


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="qlex",
        description="QLEX — The Quantum Lexicon. QEC code registry by Qorex.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # list
    subparsers.add_parser("list", help="Print all code names and IDs")

    # get
    p_get = subparsers.add_parser("get", help="Print full summary of a code")
    p_get.add_argument("id", help="Code ID")

    # search
    p_search = subparsers.add_parser("search", help="Print matching codes")
    p_search.add_argument("query", help="Search query")

    # compare
    p_compare = subparsers.add_parser("compare", help="Print comparison table")
    p_compare.add_argument("ids", nargs="+", help="2 or 3 code IDs to compare")

    # export
    p_export = subparsers.add_parser("export", help="Print export config as JSON")
    p_export.add_argument("id", help="Code ID")

    # filter
    p_filter = subparsers.add_parser("filter", help="Print filtered codes")
    p_filter.add_argument("--family", help="Filter by code family")
    p_filter.add_argument("--hardware", help="Filter by hardware platform")
    p_filter.add_argument("--min-threshold", type=float, dest="min_threshold", help="Minimum circuit-level threshold")
    p_filter.add_argument("--fault-tolerant", action="store_true", dest="fault_tolerant", help="Only fault-tolerant codes")
    p_filter.add_argument("--tag", action="append", help="Filter by tag (repeatable, AND logic)")

    # version
    subparsers.add_parser("version", help="Print version and brand line")

    args = parser.parse_args()

    if args.command is None:
        # No subcommand: launch TUI
        _cmd_tui(args)
    elif args.command == "list":
        _cmd_list(args)
    elif args.command == "get":
        _cmd_get(args)
    elif args.command == "search":
        _cmd_search(args)
    elif args.command == "compare":
        _cmd_compare(args)
    elif args.command == "export":
        _cmd_export(args)
    elif args.command == "filter":
        _cmd_filter(args)
    elif args.command == "version":
        _cmd_version(args)


if __name__ == "__main__":
    main()
