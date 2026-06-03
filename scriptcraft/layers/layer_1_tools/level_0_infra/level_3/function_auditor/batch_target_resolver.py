"""Resolve batch audit targets from CLI-style argument namespaces."""

import argparse


def resolve_batch_target(args: argparse.Namespace, batch_auditor) -> list[str]:
    if args.all:
        return batch_auditor.get_all_files()
    if args.pattern:
        return batch_auditor.get_files_by_pattern(args.pattern, args.base_folder)
    if args.folder:
        return batch_auditor.get_files_in_folder(args.folder)
    if args.extension != "gd" or args.base_folder != "scripts":
        return batch_auditor.get_files_by_extension(args.extension, args.base_folder)
    if args.managers:
        return batch_auditor.get_files_by_category("managers")
    if args.ui:
        return batch_auditor.get_files_by_category("ui")
    if args.utils:
        return batch_auditor.get_files_by_category("utils")
    if args.factories:
        return batch_auditor.get_files_by_category("factories")
    if args.coordinators:
        return batch_auditor.get_files_by_category("coordinators")
    return []
