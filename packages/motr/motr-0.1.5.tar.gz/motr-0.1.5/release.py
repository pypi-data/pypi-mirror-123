#!/usr/bin/env python3

import contextlib
import pathlib
import subprocess
import time
import types

HG = "hg"
TOPIC = "topics"
NEWSFRAGMENTS = pathlib.Path("newsfragments")

PATCH = "patch"
MINOR = "minor"
MAJOR = "major"

PARTS = frozenset({PATCH, MINOR, MAJOR})
# This logic depends on the major version.
# The values must be updated after 1.0.0.
PART_FROM_TYPE = types.MappingProxyType(
    {
        "feature": PATCH,  # MINOR
        "bugfix": PATCH,
        "doc": PATCH,
        "removal": MINOR,  # MAJOR
        "misc": PATCH,
    }
)


def get_part():
    parts = set()
    for path in NEWSFRAGMENTS.iterdir():
        name = path.name
        if name.startswith("."):
            continue
        parts.add(PART_FROM_TYPE[name.split(".")[1]])
    while not parts:
        parts.add(input("New newsfiles found. Please enter a version part: "))
        parts &= {PATCH, MINOR}  # PARTS
    # By a strange coincidence, the semver field names are in lexical order.
    # There was a 1 in 3 chance of that working out.
    return min(parts)


def get_version():
    version_str = run(
        "python", "-c", "import motr; print(motr.__version__, end='')"
    ).stdout
    # Rewrite check after release
    assert version_str.startswith("0.")
    return version_str


def run(*args):
    return subprocess.run(args, capture_output=True, check=True, text=True)


def not_command_line_flag(string):
    if string.startswith("-"):
        raise ValueError(f"{string!r} appears to be a command-line flag")


def strip_trailing_newline(string):
    if string.endswith("\n"):
        return string[:-1]
    return string


def output_summary(result):
    return (
        f"{result.args!r} printed output {result.stdout!r} and error"
        f" {result.stderr!r}"
    )


def no_outstanding_changes():
    status_result = run(HG, "status")
    if status_result.stdout or status_result.stderr:
        raise RuntimeError(output_summary(status_result))


def get_current_topic():
    topics_result = run(HG, TOPIC, "--current")
    stripped_out = strip_trailing_newline(topics_result.stdout)
    if not stripped_out or topics_result.stderr:
        raise RuntimeError(output_summary(topics_result))
    return stripped_out


def topic_revset(topic):
    return "--rev", f"topic({topic})"


def heads_on_topic(topic):
    return "\n".split(
        strip_trailing_newline(
            run(
                HG, "heads", *topic_revset(topic), "--template", "{rev}\n"
            ).stdout
        )
    )


@contextlib.contextmanager
def temporary_topic(current, new):
    not_command_line_flag(new)
    no_outstanding_changes()
    heads = heads_on_topic(current)
    if len(heads) != 1:
        raise RuntimeError(f"Current topic ({current}) has heads: {heads}")
    try:
        run(HG, TOPIC, new)
        yield
    except:
        run(HG, "update", "--clean", current)
        run(HG, "prune", *topic_revset(new))
        raise


def main():
    part = get_part()
    release_topic = f"release_{time.time()}".replace(".", "_")
    current_topic = get_current_topic()
    with temporary_topic(current_topic, release_topic):
        run("bumpversion", part)
        run("pip", "install", ".")
        version = get_version()
        run("towncrier", "build", "--yes")
        run(HG, "commit", "--message", f"Release version {version}")
    run(HG, TOPIC, current_topic, *topic_revset(release_topic))
    run(HG, "tag", f"v{version}")
    run("flit", "build")
    # run("flit", "publish")


if __name__ == "__main__":
    main()
