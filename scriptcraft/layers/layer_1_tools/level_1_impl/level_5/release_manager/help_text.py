from scriptcraft.layers.layer_1_tools.level_1_impl.level_4 import ReleaseManager


_CLI_MODULE = (
    "scriptcraft.layers.layer_1_tools.level_1_impl.level_6.release_manager.cli"
)


def print_release_manager_help() -> None:
    print("🎯 ScriptCraft Release Manager Tool")
    print(f"Usage: python -m {_CLI_MODULE} <mode> [args]")
    print("\nAvailable modes:")

    tool = ReleaseManager()
    for mode in tool.list_available_modes():
        plugin_info = tool.get_plugin_info(mode)
        if plugin_info:
            print(f"  {mode}: {plugin_info.get('description', 'No description')}")
        else:
            print(f"  {mode}")

    print(f"\nExample: python -m {_CLI_MODULE} python_package minor")
    print(f"Example: python -m {_CLI_MODULE} workspace --push")
    print("\nFor detailed help on a specific mode:")
    print(f"  python -m {_CLI_MODULE} <mode> --help")

