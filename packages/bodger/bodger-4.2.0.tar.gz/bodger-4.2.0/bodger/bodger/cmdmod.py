import fnmatch
import sys
from typing import List

__virtualname__ = "cmd"


def put(hub, tcmd: str or List[str]):
    """
    Add a command to the queue
    """
    if isinstance(tcmd, str):
        hub.bodger.RUNS.put(tcmd)
    else:
        for cmd in tcmd:
            hub.bodger.RUNS.put(cmd)


def match(hub):
    """
    Find the command to execute in the config, match the grains data and run

    build.conf format:
    .. code-block:: yaml

    bodger:
      cmd:
        "grain:glob*":
          - tcmd
          - tcmd 2
        "*":
          - tcmd
          - tcmd 2
    """
    # Look for all the targets/globs under the cmd
    for tgt in hub.OPT.bodger[hub.OPT.bodger.cmd]:
        if tgt == "*":
            hub.log.debug("'*' matches all grains")
            tcmd = hub.OPT.bodger[hub.OPT.bodger.cmd][tgt]
            hub.bodger.cmd.put(tcmd)
        else:
            grain, glob = tgt.split(":", maxsplit=1)
            val = hub.grains.GRAINS.get(grain, "")
            # If the glob matches, add the following commands to the queue
            if fnmatch.fnmatch(val, glob):
                hub.log.debug(f"Grain '{grain}={val}' matches glob '{glob}'")
                tcmd = hub.OPT.bodger[hub.OPT.bodger.cmd][tgt]
                hub.bodger.cmd.put(tcmd)
            else:
                hub.log.debug(f"Grain '{grain}={val}' does not match glob '{glob}'")


async def run_all(hub):
    """
    Run all the commands in the queue
    """
    for run in hub.bodger.RUNS.queue:
        hub.log.debug(f"bodger cmd: {run}")
        ret = await hub.exec.cmd.run(run, shell=True, stdout=sys.stdout.buffer)
        if ret.retcode != 0:
            # Stop on the first command that fails
            raise ChildProcessError(
                f"Command '{run}' executed by bodger exited with a bad return code '{ret.retcode}': {ret.stderr}"
            )
    print("Success!")
