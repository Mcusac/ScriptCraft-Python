from layers.layer_1_pypi.level_1_impl.level_2.release_manager.tool import ReleaseManager


def print_release_manager_help() -> None:
    print("🎯 ScriptCraft Release Manager Tool")
    print("Usage: python -m layers.layer_1_pypi.level_1_impl.level_2.release_manager <mode> [args]")
    print("\nAvailable modes:")

    tool = ReleaseManager()
    for mode in tool.list_available_modes():
        plugin_info = tool.get_plugin_info(mode)
        if plugin_info:
            print(f"  {mode}: {plugin_info.get('description', 'No description')}")
        else:
            print(f"  {mode}")

    print("\nExample: python -m layers.layer_1_pypi.level_1_impl.level_2.release_manager python_package minor")
    print("Example: python -m layers.layer_1_pypi.level_1_impl.level_2.release_manager workspace --push")
    print("\nFor detailed help on a specific mode:")
    print("  python -m layers.layer_1_pypi.level_1_impl.level_2.release_manager <mode> --help")

