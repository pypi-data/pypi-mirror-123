import pathlib
import re
import sys
import typing

import attr
import trio
import wheel_filename

from motr import api
from motr._api.actions import cmd as cmd_
from motr._api.requirements import action
from motr._api.requirements import target
from motr.core import result as result_


CONSTRAINTS_FILE = pathlib.Path(".motr/constraints.txt")
REQUIREMENTS = pathlib.Path(".motr/requirements")
REQUIREMENTS_FILE = api.Input(pathlib.Path(".motr/requirements_old.txt"))

CONSTRAINTS_ENV = {"PIP_CONSTRAINT": api.Input(CONSTRAINTS_FILE)}


@attr.dataclass(frozen=True)
class SinglePythonPackage:
    root: pathlib.Path
    src: bool

    @property
    def requirements_file(self):
        return api.Input((REQUIREMENTS / self.root).with_suffix(".txt"))


@attr.dataclass(frozen=True)
class MultiPythonPackage:
    root: pathlib.Path
    packages: typing.Tuple[SinglePythonPackage, ...]


def common_ancestor(path1, path2):
    parent = None
    for parent1, parent2 in zip(reversed(path1.parents), reversed(path2.parents)):
        if parent1 != parent2:
            break
        parent = parent1
    return parent


def combine_packages(singles: typing.Sequence[SinglePythonPackage]) -> MultiPythonPackage:
    prefix = None
    for single in singles:
        if prefix is None:
            prefix = single.root
        else:
            prefix = common_ancestor(prefix, single.root)
        assert prefix is not None
    packages = []
    for single in singles:
        assert prefix is not None
        packages.append(attr.evolve(single, root=single.root.relative_to(prefix)))
    return MultiPythonPackage(prefix, tuple(packages))


MPP = combine_packages(
    [SinglePythonPackage(pathlib.Path(".").resolve(), True)]
)


def make_parent(input_file):
    path = api.Input(input_file.path.parent)
    yield from api.mkdir(path)
    return path


def virtualenv(root: pathlib.Path, python=None):
    bin_dir = root / "bin"
    root_parent = yield from make_parent(api.Input(root))
    args = [sys.executable, "-m", "virtualenv", "--clear"]
    if python is not None:
        args.extend(["--python", python])
    args.append(root)
    yield from api.cmd(args, root_parent, api.Input(bin_dir).as_output())
    return FreshVirtualenv(bin_dir)


@attr.dataclass(frozen=True)
class FreshVirtualenv:
    bin: pathlib.Path

    def upgrade_pip(self, post_upgrade_args, env=None):
        env = env or {}
        pip = self.bin / "pip"
        yield from api.cmd(
            [api.Input(pip).as_output(), "install", "--upgrade", "pip"],
            api.Input(self.bin),
            env=env,
        )
        return UpgradedVirtualenv(self.bin, post_upgrade_args)


@attr.dataclass(frozen=True)
class InstallArgs:
    args: tuple
    env: typing.Mapping = {}


@attr.dataclass(frozen=True)
class UpgradedVirtualenv:
    bin: pathlib.Path
    install_args: InstallArgs

    def command(self, command):
        pip = api.Input(self.bin / "pip")
        cmd = api.Input(self.bin / command)
        yield from api.cmd(
            [pip, "install", *self.install_args.args],
            cmd.as_output(),
            env=self.install_args.env,
        )
        return cmd


@attr.dataclass(frozen=True)
class Venv:
    root: pathlib.Path
    name: str

    @property
    def root_path(self):
        return self.root / self.name

    @property
    def bin_dir(self):
        return self.root_path / "bin"

    @property
    def pip(self):
        return api.Input(self.bin_dir / "pip")

    def create(self):
        yield from api.cmd(
            [sys.executable, "-m", "venv", "--clear", str(self.root_path)],
            api.Input(self.bin_dir).as_output(),
        )

    def update(self):
        yield from api.cmd(
            [self.pip.as_output(), "install", "-U", "pip"],
            api.Input(self.bin_dir),
        )

    def install(self, *pip_args, env=None, command):
        env = env or {}
        command_path = api.Input(self.bin_dir / command)
        yield from api.cmd((self.pip, "install") + pip_args, command_path.as_output(), env=env)
        return command_path


dot_dir = pathlib.Path(".motr")
requirements_dir = pathlib.Path("requirements")
reports_dir = pathlib.Path("reports")


def setup_venv(name, command, *pip_args, env=None):
    venv = Venv(dot_dir, name)

    yield from venv.create()
    yield from venv.update()
    return (yield from venv.install(*pip_args, env=env or {}, command=command))


def setup_virtualenv(name, command, install_args, python=None):
    root = dot_dir / "env" / name / (python or "default")
    fresh_virtualenv = yield from virtualenv(root, python)
    upgraded_virtualenv = yield from fresh_virtualenv.upgrade_pip(install_args)
    return (yield from upgraded_virtualenv.command(command))


@attr.dataclass(frozen=True)
class PyprojectBuild:
    executable: pathlib.Path
    packages: MultiPythonPackage

    async def __call__(self):
        dist_dir = pathlib.Path(".motr/dist")
        await trio.Path(dist_dir).mkdir()
        constraints = []
        for package in self.packages.packages:
            result, data = await cmd_.Cmd(
                (
                    str(self.executable),
                    "--outdir",
                    str(dist_dir),
                    str(self.packages.root / package.root)
                )
            )()
            if result is not result_.Result.PASSED:
                return result_.Result.ABORTED, {}
            build_log = data["out"]
            wheel_re = re.compile(
                r"^Successfully built .* (\S+\.whl)$", flags=re.MULTILINE,
            )
            build_match = re.search(wheel_re, build_log)
            if build_match is None:
                return result_.Result.ABORTED, {}
            build_path = dist_dir / build_match.group(1)
            package_name = wheel_filename.parse_wheel_filename(build_path).project
            constraints.append(f"{package_name} @ {build_path.as_uri()}\n")
            await trio.Path(package.requirements_file.path).write_text(package_name)
        await trio.Path(CONSTRAINTS_FILE).write_text("".join(constraints))


def pyroject_build(package_roots):
    executable = yield from setup_virtualenv("build", "pyproject-build", InstallArgs(("pyproject-build",)))
    action_ = PyprojectBuild(executable.path, package_roots)
    yield from action.action(action_, executable.path)
    yield from target.target(CONSTRAINTS_FILE, action_)
    for package in package_roots.packages:
        yield from target.target(package.requirements_file.path, action_)


@attr.dataclass(frozen=True)
class FlitToRequirements:
    flit: api.Input
    outfile: api.Input

    async def __call__(self):
        result, data = await cmd_.Cmd(
            (
                str(self.flit.path), "build", "--format", "wheel",
            ),
        )()
        if result is not result_.Result.PASSED:
            return result_.Result.ABORTED, {}
        build_log = data["err"]
        wheel_re = r"Built wheel:\s*(\S*)"
        build_match = re.search(wheel_re, build_log)
        if build_match is None:
            return result_.Result.ABORTED
        build_path = pathlib.Path(build_match.group(1))
        package_name = wheel_filename.parse_wheel_filename(build_path).project
        await trio.Path(self.outfile.path).write_text(
            f"{package_name} @ {build_path.resolve().as_uri()}\n"
        )
        return result_.Result.PASSED, {}


def flit(outfile):
    flit_cmd = yield from setup_virtualenv("flit", "flit", InstallArgs(("flit",)))
    flit_to_requirements = FlitToRequirements(flit_cmd, outfile)
    yield from action.action(flit_to_requirements, flit_cmd.path)
    yield from target.target(outfile.path, flit_to_requirements)
    return outfile


def venv_wrapper(name, command, requirements_file, *pip_args):
    return (
        yield from setup_venv(
            name,
            command,
            "-r",
            str((requirements_dir / requirements_file).with_suffix(".txt")),
            *pip_args,
        )
    )


def pytest_suffix(junit_file):
    return (
        "tests",
        "-p",
        "no:cacheprovider",
        "--junitxml",
        junit_file.as_output(),
    )


def run_pytest(
    env_name, requirement_name, runner, report_name, test_extra_inputs=()
):
    command_name = runner[0]
    requirements_file = yield from flit(REQUIREMENTS_FILE)
    command = yield from venv_wrapper(
        env_name, command_name, requirement_name, "-r", requirements_file
    )
    runner = (command,) + runner[1:]
    report_dir = api.Input(reports_dir / report_name)
    yield from api.mkdir(report_dir)
    junit_file = api.Input(report_dir.path / "junit.xml")
    pytest_action = yield from (
        api.cmd(
            runner + pytest_suffix(junit_file),
            report_dir.path,
            *test_extra_inputs,
            allowed_codes=[1],
        )
    )
    junit2html = yield from venv_wrapper(
        "junit-report", "junit2html", "junit-report"
    )
    html_file = api.Input(report_dir.path / "index.html")
    yield from (
        api.cmd(
            [
                junit2html,
                junit_file,
                html_file.as_output(env_name),
            ],
        )
    )
    return pytest_action


def changes():
    flake8_report_dir = api.Input(reports_dir / "flake8")
    flake8_report_file = api.Input(flake8_report_dir.path / "index.html")
    flake8 = yield from venv_wrapper("check", "flake8", "check")
    yield from api.mkdir(flake8_report_dir)
    yield from api.cmd(
        [
            flake8,
            "--format=html",
            "--htmldir",
            flake8_report_dir,
            "--isort-show-traceback",
            "src",
            "tests",
        ],
        flake8_report_file.as_output("check"),
        allowed_codes=[1],
    )

    requirements_file = yield from flit(REQUIREMENTS_FILE)

    mypy_report_dir = api.Input(reports_dir / "mypy")
    mypy_report_file = api.Input(mypy_report_dir.path / "junit.xml")
    mypy_coverage_dir = api.Input(reports_dir / "mypy-coverage")
    mypy_coverage_file = api.Input(mypy_coverage_dir.path / "index.html")
    mypy = yield from venv_wrapper("mypy", "mypy", "mypy", "-r", requirements_file)
    yield from api.mkdir(mypy_report_dir)
    yield from api.mkdir(mypy_coverage_dir)
    yield from api.cmd(
        [
            mypy,
            "--html-report",
            mypy_coverage_dir,
            "--junit-xml",
            mypy_report_file.as_output(),
            "src",
        ],
        mypy_report_dir,
        mypy_coverage_file.as_output("mypy"),
        allowed_codes=[1],
    )
    junit2html = yield from venv_wrapper(
        "junit-report", "junit2html", "junit-report"
    )
    mypy_report_html = api.Input(mypy_report_dir.path / "index.html")
    yield from api.cmd(
        [junit2html, mypy_report_file, mypy_report_html.as_output("mypy")],
    )

    yield from run_pytest(
        "nocov", "pytest", ("python", "-m", "pytest"), "pytest"
    )

    coverage = yield from venv_wrapper("coverage", "coverage", "coverage")
    coverage_deleted = api.Input(api.deleted(pathlib.Path(".coverage")))
    yield from api.cmd([coverage, "erase"], coverage_deleted.as_output())
    initial_coverage = api.Input("initial-coverage")
    updated_coverage_file = api.Input(pathlib.Path(".coverage"))
    yield from run_pytest(
        "cover",
        "cover",
        ("coverage", "run", "-m", "pytest"),
        "pytest-cover",
        (coverage_deleted, initial_coverage.as_output()),
    )
    yield from api.cmd(
        [coverage, "combine"],
        initial_coverage,
        updated_coverage_file.as_output(),
    )
    yield from api.cmd(
        [
            coverage,
            "html",
            "--show-contexts",
            "-d",
            api.Input(reports_dir / "coverage").as_output("cover"),
        ],
        updated_coverage_file,
    )
    yield from api.cmd(
        [
            coverage,
            "report",
            "--skip-covered",
            "-m",
            "--fail-under=100",
        ],
        updated_coverage_file,
        api.Input("coverage-report").as_output("cover"),
        allowed_codes=[2],
    )

    profile_dir = api.Input(reports_dir / "profile")

    yield from api.mkdir(profile_dir)
    yield from run_pytest(
        "profile",
        "profile",
        (
            "pyinstrument",
            "--renderer",
            "html",
            "--outfile",
            api.Input(profile_dir.path / "index.html").as_output("profile"),
            "-m",
            "pytest",
        ),
        "pytest-profile",
        (profile_dir,),
    )


MOTR_CONFIG = api.build(changes())
