import os
import queue
import sys


def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # Add another function to call from your run.py to start the app
    hub.pop.sub.add(dyne_name="grains")
    hub.bodger.RUNS = queue.Queue()

    # Set a new value for grains timeout
    if "GRAINS_TIMEOUT" not in os.environ:
        os.environ["GRAINS_TIMEOUT"] = "10"


def cli(hub):
    hub.pop.config.load(["bodger", "grains"], cli="bodger")
    # Check for the command in the build file to fail early
    print(hub.OPT.grains)
    if hub.OPT.bodger.cmd not in hub.OPT.bodger:
        raise KeyError(
            f"Command '{hub.OPT.bodger.cmd}' not found in {sorted(hub.OPT.bodger.keys())}!"
        )

    if getattr(sys, "frozen", False):
        # https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#ld-library-path-libpath-considerations
        os.environ.pop("DYLD_LIBRARY_PATH", None)  # Darwin
        os.environ.pop("LD_LIBRARY_PATH", None)  # Linux
        os.environ.pop("LIBPATH", None)  # AIX

    hub.log.debug("Collecting grains data")
    hub.grains.init.standalone()
    hub.log.debug("Matching bodger commands from config")
    hub.bodger.cmd.match()
    hub.log.debug(f"Running {hub.bodger.RUNS.qsize()} commands")
    hub.pop.loop.start(hub.bodger.cmd.run_all())
