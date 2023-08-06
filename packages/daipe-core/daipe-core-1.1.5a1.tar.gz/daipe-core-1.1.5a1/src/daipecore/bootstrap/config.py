import os
from pyfonybundles.loader import entry_points_reader


def _read():
    bootstrap_config_readers = [
        entry_point for entry_point in entry_points_reader.get_by_key("daipe") if entry_point.name == "bootstrap_config_reader"
    ]

    is_databricks_workspace = os.getcwd().startswith("/Workspace/Repos")

    if len(bootstrap_config_readers) == 0 or is_databricks_workspace:
        from daipecore.bootstrap import config_reader

        return config_reader.read()
    elif len(bootstrap_config_readers) == 1:
        config_loader = bootstrap_config_readers[0].load()

        return config_loader()
    else:
        raise Exception("Multiple bootstrap_config_reader entry points defined in project packages")


bootstrap_config = _read()
