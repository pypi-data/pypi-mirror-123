#!/usr/bin/env python3

"""
gitstat.py

Copyright 2019-2020  John Begenisich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import configparser
import os
import subprocess
import sys
from ast import literal_eval
from enum import Enum, auto, unique
from itertools import repeat
from multiprocessing import Pool, cpu_count, freeze_support
from operator import itemgetter
from pathlib import Path
from textwrap import dedent
from typing import Dict, List, Optional, Tuple, Union

import click
import colr.codes
from click_default_group import DefaultGroup
from colr import ColorCode, Colr
from tqdm import tqdm

from . import VERSION


@unique
class GitStatus(Enum):
    """An Enum to hold various statuses about git repositories."""
    UNSTAGED = auto()
    UNCOMMITTED = auto()
    UNTRACKED = auto()
    UNPUSHED = auto()
    PULL_REQUIRED = auto()
    UP_TO_DATE = auto()
    DIVERGED = auto()
    # these are more like errors
    URL_MISMATCH = auto()
    ERROR_FETCHING = auto()
    ERROR_PULLING = auto()
    NO_UPSTREAM_BRANCH = auto()
    ERROR_ORIGIN_URL = auto()

    def __str__(self) -> str:
        return self.name


OUTPUT_MESSAGES = {
    GitStatus.UNSTAGED: 'unstaged changes',
    GitStatus.UNCOMMITTED: 'uncommitted changes',
    GitStatus.UNTRACKED: 'untracked files',
    GitStatus.UNPUSHED: 'unpushed commits',
    GitStatus.PULL_REQUIRED: 'pull required',
    GitStatus.UP_TO_DATE: 'up-to-date',
    GitStatus.URL_MISMATCH: 'URL mismatch',
    GitStatus.DIVERGED: 'DIVERGED',
    GitStatus.ERROR_FETCHING: 'error fetching',
    GitStatus.ERROR_PULLING: 'error pulling',
    GitStatus.NO_UPSTREAM_BRANCH: 'no matching upsteam branch',
    GitStatus.ERROR_ORIGIN_URL: 'error in origin URL',
}

# Default colors; more or less following git-prompt's colorization
DEFAULT_COLORS = {
    # stash: green
    # conflicts: red
    GitStatus.UNSTAGED: ColorCode('green').code,
    GitStatus.UNCOMMITTED: ColorCode('yellow').code,
    GitStatus.UNTRACKED: ColorCode('red').code,
    GitStatus.UNPUSHED: ColorCode('cyan').code,
    GitStatus.PULL_REQUIRED: ColorCode('magenta').code,
    GitStatus.UP_TO_DATE: ColorCode('green').code,
}
COLORS = DEFAULT_COLORS.copy()

DEFAULT_COLOR_STYLES = {
    GitStatus.DIVERGED: 'bold',
    GitStatus.PULL_REQUIRED: 'italic',
}
COLOR_STYLES = DEFAULT_COLOR_STYLES.copy()

# Gitstat uses two config files:
#   1. Gitstat options
#   2. Repos being tracked by gitstat
REPOS_CONFIG = configparser.ConfigParser()
OPTIONS_CONFIG = configparser.ConfigParser()

# -------------------------------------------------


def print_error(message: str, repo_path: str, stdout: Optional[bytes] = None, stderr: Optional[bytes] = None) -> None:
    """
    Print an error message (e.g., from subprocess output).

    Args:
        message (str): The message to print
        repo_path (str): The path to the git repo about which this error is regarding
        stdout (bytes): stdout output
        stdout (bytes): stderr output

    Returns: Nothing
    """
    print('\033[0;31m{}{}\033[0m'.format(message, ': {}'.format(repo_path) if repo_path else ''))
    if stdout or stderr:
        if stdout:
            print(stdout.decode().strip())
        if stderr:
            print('\033[0;31m{}\033[0m'.format(stderr.decode().strip()))


def repos_config_filename() -> Path:
    """
    Get the path to our repos config file.

    Returns: the Path to the repos config file
    """
    return Path(click.get_app_dir('gitstat')) / 'repos.conf'


def read_repos_config() -> None:
    """Read repos config file into global "REPOS_CONFIG" var."""
    global REPOS_CONFIG
    filename = repos_config_filename()
    if filename.is_file():
        REPOS_CONFIG.read(filename)


def write_repos_config() -> None:
    """Write repos config file to global "REPOS_CONFIG" var."""
    global REPOS_CONFIG
    filename = repos_config_filename()
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(repos_config_filename(), 'w') as file_writer:
        REPOS_CONFIG.write(file_writer)


def options_config_filename() -> Path:
    """
    Get the path to our options config file.

    Returns: the Path to the options config file
    """
    return Path(click.get_app_dir('gitstat')) / 'gitstat.conf'


def read_options_config() -> None:
    """
    Read config file into global "OPTIONS_CONFIG" var.

    Updates COLORS and COLOR_STYLES if any colors/styles are specified in the config.
    """
    global OPTIONS_CONFIG, COLORS, COLOR_STYLES
    filename = options_config_filename()
    if not filename.is_file():
        with open(filename, 'w') as writer:
            writer.write("""# gitstat.conf

# Run "gitstat config" to show the "Status" list and the default colors.
# For each Status, a COLOR and STYLE can be specified.
# STYLES can be: bold, dim, italic, underline, flash, reverse
# COLORS can be:
#   - a 6-hex string  #123456
#   - an RGB tuple    (255, 0, 0)
#   - a name          red

[colors]
# UNTRACKED_COLOR = (255, 0, 0)
# UNTRACKED_STYLE = bold
# PULL_REQUIRED_COLOR = #00FF11
# UNCOMMITTED_COLOR = cyan
""")
    OPTIONS_CONFIG.read(filename)
    # update colors
    if 'colors' in OPTIONS_CONFIG:
        for option in OPTIONS_CONFIG['colors']:
            option = option.upper()  # ConfigParser converts option strings to lowercase
            value = OPTIONS_CONFIG['colors'][option]
            if option.endswith('_STYLE'):
                is_style = True
                option = option[:-6]
            elif option.endswith('_COLOR'):
                is_style = False
                option = option[:-6]
            else:
                # invalid
                print('"{}" is not a valid option'.format(option))
                continue
            # find the matching GitStatus
            try:
                git_status = getattr(GitStatus, option)
            except AttributeError:
                print('"{}" is not a valid status'.format(option))
                continue
            if is_style:
                if value not in colr.codes['style']:
                    print('"{}" is an invalid style code'.format(value))
                    continue
                COLOR_STYLES[git_status] = value
                continue
            # it's a color, not a style; could be (r, g, b), #123456, or a color name
            try:
                if '(' in value:  # (r, g, b) tuple
                    value = literal_eval(value)
                color_code = ColorCode(value).code
            except ValueError:
                print('"{}" is not a valid color'.format(OPTIONS_CONFIG['colors'][option]))
                continue
            COLORS[git_status] = color_code


def colorize_status(status: GitStatus, use_defaults: bool = False, use_color: bool = True) -> Colr:
    if not use_color:
        return OUTPUT_MESSAGES[status]
    if use_defaults:
        fore = DEFAULT_COLORS[status] if status in DEFAULT_COLORS else 'red'
        style = DEFAULT_COLOR_STYLES[status] if status in DEFAULT_COLOR_STYLES else 'normal'
    else:
        fore = COLORS[status] if status in COLORS else 'red'
        style = COLOR_STYLES[status] if status in COLOR_STYLES else 'normal'
    return Colr(OUTPUT_MESSAGES[status], fore=fore, style=style)


def fetch_from_origin(path: str) -> Union[str, int]:
    """
    Fetch from origin.

    Args:
        path (str): The path to the git repo

    Returns:
        On success: the path (str) (because with multithreading we want to display our progress)
        On failure: -1
    """
    result = subprocess.run(['git', 'fetch', '--quiet'], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print_error(path, 'error fetching; "git fetch" output follows:', result.stdout, result.stderr)
        return -1
    return path


def pull_from_origin(path: str) -> Union[str, int]:
    """
    Pull from origin.

    Args:
        path (str): The path to the git repo

    Returns:
        On success: the path (str) (because with multithreading we want to display our progress)
        On failure: -1
    """
    result = subprocess.run(['git', 'pull', '--quiet'], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print_error(path, 'error fetching; "git pull" output follows:', result.stdout, result.stderr)
        return -1
    return path


def get_local(path: str) -> Union[str, int]:
    """
    Find upstream revision.

    Args:
        path (str): The path to the git repo

    Returns:
        On success: str from "git rev-parse @"
        On failure: -1
    """
    result = subprocess.run(['git', 'rev-parse', '@'], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print_error('error doing "rev-parse @"; aborting', path, result.stdout, result.stderr)
        return -1
    return result.stdout.decode().strip()


def get_remote(path: str) -> Union[Tuple[str, Optional[GitStatus]], int]:
    """
    Find upstream revision.

    Args:
        path (str): The path to the git repo

    Returns:
        On success: A tuple of (remote: str, changes: GitStatus)
            changes can indicate if there is no matching upstream branch (or empty string)
        On failure: -1
    """
    upstream = '@{u}'
    result = subprocess.run(['git', 'rev-parse', upstream], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return result.stdout.decode().strip(), None
    else:
        err = result.stderr.decode().strip()
        if 'no upstream configured' in err:
            # fatal: no upstream configured for branch 'dummy'
            changes = GitStatus.NO_UPSTREAM_BRANCH
        else:
            print_error('error doing "rev-parse {}"; aborting'.format(upstream), path, result.stdout, result.stderr)
            return -1
    return result.stdout.decode().strip(), changes


def update_index(path: str) -> Union[None, int]:
    """
    Updates the index.

    Args:
        path (str): The path to the git repo

    Returns:
        On success: None
        On failure: -1
    """
    result = subprocess.run(['git', 'update-index', '-q', '--ignore-submodules', '--refresh'], cwd=path)
    if result.returncode != 0:
        print_error('error updating index; aborting', path, result.stdout, result.stderr)
        return -1
    return None


def get_base(path: str) -> Union[str, int]:
    """
    Find as good common ancestors as possible for a merge.

    Args:
        path (str): The path to the git repo

    Returns:
        On success: str representing the base
        On failure: -1
    """
    upstream = '@{u}'
    result = subprocess.run(['git', 'merge-base', '@', upstream],
                            cwd=path,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if result.returncode != 0:
        print_error('error doing "merge-base @"; aborting', path, result.stdout, result.stderr)
        return -1
    return result.stdout.decode().strip()


def check_unstaged_changes(path: str) -> bool:
    """
    Determine whether there are unstaged changes in the working tree.

    Args:
        path (str): The path to the git repo

    Returns:
        bool: True if there are unstaged changes; else False
    """
    result = subprocess.run(['git', 'diff-files', '--quiet', '--ignore-submodules'], cwd=path)
    return result.returncode != 0


def check_uncommitted_changes(path: str) -> bool:
    """
    Determine whether there are uncommitted changes in the index.

    Args:
        path (str): The path to the git repo

    Returns:
        bool: True if there are uncommitted changes in the index; else False
    """
    result = subprocess.run(['git', 'diff-index', '--cached', '--quiet', 'HEAD', '--ignore-submodules'], cwd=path)
    return result.returncode != 0


def check_untracked_files(path: str) -> bool:
    """
    Determine whether there are untracked files.

    Args:
        path (str): The path to the git repo

    Returns:
        bool: True if there are untracked files; else False
    """
    result = subprocess.run(['git', 'ls-files', '-o', '--exclude-standard'],
                            cwd=path,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    return True if result.stdout else False


def check_unpushed_commits(path: str) -> bool:
    """
    Determine whether there are unpushed commits.

    Note this just calls "git diff", so this will also return True
    if a pull from origin is required.

    Args:
        path (str): The path to the git repo

    Returns:
        bool: True if there are unpushed commits; else False
    """
    # note, no escaping curly braces here
    result = subprocess.run(['git', 'diff', '--quiet', '@{u}..'],
                            cwd=path,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    return result.returncode != 0


def get_repo_url(path: str) -> Union[str, int]:
    """
    Return the origin URL.

    Args:
        path (str): The path to the git repo

    Returns:
        On success: str representing the origin URL
        On failure: -1
    """
    # get repo URL; return None on error
    result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], stdout=subprocess.PIPE, cwd=path)
    if result.returncode != 0:
        # print_error('error getting git URL', path)
        return -1
    return result.stdout.decode().strip()


def checkrepo(path: str, even_if_uptodate: bool = False) -> Union[Dict, int, None]:
    """
    Run various checks on a repo to determine its general state.

    If even_if_uptodate == False and there are no changes, return None;
    else return a dict of {'path': path, 'changes': List[GitStatus]}

    Args:
        path (str): The path to the git repo
        even_if_uptodate (bool): configure whether to return something even if repo is up-to-date

    Returns:
        On success: a Dict of {'path': path, 'changes': List of GitStat or None})
            If even_if_uptodate == False and there are no changes, 'changes' will be None; else 'up-to-date' will
            be included in the list.
        On failure: -1
    """
    changes: List[GitStatus] = []
    # check that the origin URL matches our config file
    origin_url = get_repo_url(path)
    if type(origin_url) == int:  # error
        return {'path': path, 'changes': [GitStatus.ERROR_ORIGIN_URL]}
    else:
        # check origin URL matches URL in gitstat REPOS_CONFIG
        # skip this check if the repo is not being tracked by gitstat
        if REPOS_CONFIG.has_section(path) and origin_url != REPOS_CONFIG[path]['url']:
            print_error(path, 'origin URL mismatch')
            print('  gitstat: {}'.format(REPOS_CONFIG[path]['url']))
            print('  origin:  {}'.format(origin_url))
            changes.append(GitStatus.URL_MISMATCH)
    # get local, remote, and base revisions
    local = get_local(path)
    if type(local) == int:  # error already printed
        return -1
    remote_result = get_remote(path)
    if type(remote_result) == int:  # error already printed
        return -1
    remote, result = remote_result
    if result:
        # no origin branch
        changes.append(result)
    else:
        # get the base so we can compare it to local to determine if a pull is required
        base = get_base(path)
        if type(base) == int:  # error already printed
            return -1
        # compare local/remote/base revisions
        if local == remote:
            pass  # up-to-date
        elif local == base:
            changes.append(GitStatus.PULL_REQUIRED)
        elif remote == base:
            pass  # need to push - later we'll do a git diff which will catch this and other situations)
        else:
            # diverged - shouldn't ever see this?
            changes.append(GitStatus.DIVERGED)
    result = update_index(path)
    if type(result) == int:  # error already printed
        return -1
    if check_unstaged_changes(path):
        changes.append(GitStatus.UNSTAGED)
    if check_uncommitted_changes(path):
        changes.append(GitStatus.UNCOMMITTED)
    if check_untracked_files(path):
        changes.append(GitStatus.UNTRACKED)
    # When a pull is required, git-diff will indicate there's a difference, and we should pull first anyway.
    # so skip this check when we need to pull.
    if GitStatus.PULL_REQUIRED not in changes:
        if check_unpushed_commits(path):
            changes.append(GitStatus.UNPUSHED)
    if not changes and even_if_uptodate:
        changes.append(GitStatus.UP_TO_DATE)
    # if something changed, return the changes; else nothing
    if changes:
        return {'path': path, 'changes': changes}  # return the path to ease using the result with subprocessing
    return None


def checkrepo_bool(path: str, even_if_uptodate: bool = False) -> Union[bool, int]:
    """
    Returns a bool if there are changes to the repo.

    This is just a wrapper for checkrepo(); it would be faster
    if we do the checks "manually" because we could bail as soon as
    one check indicated there are changes.  But this is simpler.

    Args:
        path (str): The path to the git repo
        even_if_uptodate (bool): configure whether to return something even if repo is up-to-date

    Returns:
        On success: True if changes; else False
        On failure: -1
    """
    result = checkrepo(path)
    if type(result) == int:
        return result  # error
    return False if result is None else True


def get_paths(paths: List[str], include_ignored: bool, missing_ok: bool = False) -> List[str]:
    """
    Return a list of strings representing zero or more paths to git repos.

    Paths are checked if they exist and if they are git repos.
    If paths is not empty, use them; otherwise, use paths being tracked in config.

    Args:
        path (List[str]): The paths to the git repos
        include_ignored (bool): whether to include repos ignored in the config
        missing_ok (bool): if True, don't skip & show and error missing repos

    Returns:
        A list of str of paths to git repos
    """
    if not paths:
        paths = [x for x in REPOS_CONFIG.sections()]
    new_path_list: List[str] = []
    for path in paths:
        if REPOS_CONFIG.has_section(path) and REPOS_CONFIG.getboolean(path, 'ignore', fallback=False) and not include_ignored:
            continue
        if not missing_ok:
            if not os.path.isdir(path):
                print_error('not found', path)
                continue
            elif not os.path.isdir(os.path.join(path, '.git')):
                print_error('not a git directory', path)
                continue
        new_path_list.append(path)
    return new_path_list


def check_paths(paths: List[str], include_uptodate: bool, progress_bar: bool) -> List[Dict]:
    """Return a list of dicts representing the result of checking multiple git repos."""
    output: List[Dict] = []
    with Pool(processes=cpu_count()) as pool:
        with tqdm(total=len(paths), disable=not progress_bar, leave=False) as pbar:
            for result in pool.starmap(checkrepo, zip(paths, repeat(include_uptodate)), chunksize=1):
                pbar.update()
                if result is None:
                    continue
                if type(result) == int:
                    continue  # already printed error
                assert isinstance(result, Dict)
                output.append(result)
    return output


def check_paths_with_exit_code(paths: List[str], include_uptodate: bool, progress_bar: bool) -> int:
    """Return an int representing the return code with which we should exit: 0 for no changes; 1 for changes."""
    exit_code: int = 0
    with Pool(processes=cpu_count()) as pool:
        with tqdm(total=len(paths), disable=not progress_bar, leave=False) as pbar:
            for result in pool.starmap(checkrepo_bool, zip(paths, repeat(include_uptodate)), chunksize=1):
                if type(result) == int:
                    continue  # already printed error
                if result:
                    exit_code = 1
                    pool.terminate()
                    pbar.close()
                    break
    return exit_code


@click.group(cls=DefaultGroup, default='check', default_if_no_args=True)
@click.version_option(version=VERSION)
def cli() -> None:
    """
    Succinctly display information about git repositories.

    Gitstat looks for unstaged changes, uncommitted changes, untracked/unignored
    files, unpushed commits, and whether a pull from upstream is required.

    Gitstat can maintain a list of repos about which it will report.
    Use "gitstat track" to add repo(s) to its list.

    If no paths to git repos are specified on the command line, gitstat will show
    information about the repos it is tracking.

    Run "gitstat COMMAND --help" for help about a specific command.
    """
    freeze_support()
    read_options_config()
    read_repos_config()


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
@click.option('-a', '--all', 'all_', type=bool, default=False, is_flag=True,
              help='Include repos that are up-to-date.')
@click.option('--include-ignored', type=bool, default=False, is_flag=True,
              help='Include repos set by gitstat to be ignored.')
@click.option('-q', '--quiet', type=bool, default=False, is_flag=True,
              help='Be quiet; return 1 if any repo has changes, else return 0.')
@click.option('-p', '--progress', type=bool, default=False, is_flag=True,
              help='Show progress bar.')
@click.option('--color/--no-color', 'use_color', default=True, help='Colorize output.')
@click.pass_context
def check(ctx: click.Context, path: Tuple[str], all_: bool, include_ignored: bool, quiet: bool, progress: bool,
          use_color: bool) -> None:
    """Check repo(s)."""
    ctx.ensure_object(dict)
    if not path and len(REPOS_CONFIG.sections()) == 0:
        print(
            dedent("""
            No repos specified and no repos are being tracked.
            Either specify path(s) to git repos on the command line, or
            track repo(s) with "gitstat track /path/to/repo".
            """))
        # show top level help and exit
        ctx.fail(ctx.find_root().get_help())
    if quiet:
        int_result = check_paths_with_exit_code(get_paths(list(path), include_ignored=include_ignored),
                                                include_uptodate=all_, progress_bar=progress)
        sys.exit(int_result)
    # everything went as expected!
    result: List[Dict] = check_paths(get_paths(list(path), include_ignored=include_ignored),
                                     include_uptodate=all_, progress_bar=progress)
    if result:
        # print the array of {'path': path, 'changes': [changes]}
        width = max(len(x['path']) for x in result)
        for item in sorted(result, key=itemgetter('path')):
            changes = Colr(', ', fore=None).join(colorize_status(i, use_color=use_color) for i in item['changes']).strip()
            print('{path:{width}} {changes}'.format(path=item['path'], width=width, changes=changes))


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
                required=True)
def track(path: tuple) -> None:
    """Track repo(s)."""
    global REPOS_CONFIG
    changed = False
    for track_path in path:
        if track_path.endswith('/.git'):
            track_path = track_path[:-5]
        if track_path in REPOS_CONFIG.sections():
            print_error('already being tracked', track_path)
            continue
        if not os.path.isdir(os.path.join(track_path, '.git')):
            print_error('not a git directory', track_path)
            continue
        url = get_repo_url(track_path)
        if type(url) == int:  # error already printed
            continue
        # add it to config file
        REPOS_CONFIG.add_section(track_path)
        REPOS_CONFIG[track_path]['url'] = url
        changed = True
    if changed:
        write_repos_config()


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(exists=False, file_okay=False, dir_okay=True, resolve_path=True),
                required=True)
def untrack(path: tuple) -> None:
    """Untrack repo(s)."""
    global REPOS_CONFIG
    changed = False
    for untrack_path in path:
        if untrack_path not in REPOS_CONFIG.sections():
            print_error('already not being tracked', untrack_path)
            continue
        REPOS_CONFIG.remove_section(untrack_path)
        changed = True
    if changed:
        write_repos_config()


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(exists=False, file_okay=False, dir_okay=True, resolve_path=True),
                required=True)
def ignore(path: tuple) -> None:
    """Ignore repo(s)."""
    global REPOS_CONFIG
    changed = False
    for ignore_path in path:
        if ignore_path not in REPOS_CONFIG.sections():
            print_error('not being tracked', ignore_path)
            continue
        if REPOS_CONFIG.getboolean(ignore_path, 'ignore', fallback=False):
            print_error('already ignored', ignore_path)
            return
        REPOS_CONFIG[ignore_path]['ignore'] = 'true'
        changed = True
    if changed:
        write_repos_config()


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
                required=True)
def unignore(path: tuple) -> None:
    """Un-ignore repo(s)."""
    global REPOS_CONFIG
    changed = False
    for ignore_path in path:
        if ignore_path not in REPOS_CONFIG.sections():
            print_error('not being tracked', ignore_path)
            continue
        if not REPOS_CONFIG.getboolean(ignore_path, 'ignore', fallback=False):
            print_error('already un-ignored', ignore_path)
            return
        REPOS_CONFIG[ignore_path]['ignore'] = 'false'
        changed = True
    if changed:
        write_repos_config()


@cli.command()
@click.option('--include-existing', type=bool, default=False, is_flag=True,
              help='Include repos that already exist.')
@click.option('--include-ignored', type=bool, default=False, is_flag=True,
              help='Include repos set by gitstat to be ignored.')
def showclone(include_existing: bool, include_ignored: bool) -> None:
    """Show "git clone" commands needed to clone missing repos."""
    global REPOS_CONFIG
    paths = get_paths([], include_ignored=include_ignored, missing_ok=True)
    for path in paths:
        if include_existing or not (Path(path) / '.git').is_dir():
            print('git clone {} {}'.format(REPOS_CONFIG[path]['url'], path))
    sys.exit()


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
@click.option('--include-ignored', type=bool, default=False, is_flag=True,
              help='Include repos set by gitstat to be ignored.')
@click.option('-p', '--progress', type=bool, default=False, is_flag=True,
              help='Show progress bar.')
def fetch(path: tuple, include_ignored: bool, progress: bool) -> None:
    """Fetch from origin."""
    paths_to_fetch = get_paths(list(path), include_ignored=include_ignored)
    if len(paths_to_fetch) == 0:
        return  # might want to chain commands...
    with Pool(processes=cpu_count()) as pool:
        with tqdm(total=len(paths_to_fetch), disable=not progress, leave=False) as pbar:
            for result in pool.imap_unordered(fetch_from_origin, paths_to_fetch, chunksize=1):
                if type(result) == int:  # error
                    pass
                pbar.update()


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
@click.option('--include-ignored', type=bool, default=False, is_flag=True,
              help='Include repos set by gitstat to be ignored.')
@click.option('-p', '--progress', type=bool, default=False, is_flag=True,
              help='Show progress bar.')
def pull(path: tuple, include_ignored: bool, progress: bool) -> None:
    """Pull from origin (if no local changes).  Hint: run "gitstat fetch" first."""
    paths_to_check: List[str] = get_paths(list(path), include_ignored=include_ignored)
    if len(paths_to_check) == 0:
        return  # might want to chain commands...
    output = check_paths(paths_to_check, include_uptodate=False, progress_bar=progress)
    paths_to_pull: List[str] = []
    for item in output:
        # only pull from repos with origin changes and no local changes
        if len(item['changes']) == 1 and item['changes'][0] == GitStatus.PULL_REQUIRED:
            paths_to_pull.append(item['path'])
    if len(paths_to_pull) == 0:
        sys.exit()
    with Pool(processes=cpu_count()) as pool:
        with tqdm(total=len(paths_to_pull), disable=not progress, leave=False) as pbar:
            for result in pool.imap_unordered(pull_from_origin, paths_to_pull, chunksize=1):
                if type(result) == int:  # error
                    continue
                pbar.write(result)
                pbar.update()


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(file_okay=False, dir_okay=True, resolve_path=True), required=True)
@click.option('-q', '--quiet-if-tracked', type=bool, default=False, is_flag=True,
              help='Don\'t output anything if the repo is being tracked.')
def is_tracked(path: tuple, quiet_if_tracked: bool) -> None:
    """Show whether repo(s) are tracked by gitstat."""
    global REPOS_CONFIG
    for path_to_check in path:
        if path_to_check.endswith('/.git'):
            path_to_check = path_to_check[:-5]
        if path_to_check not in REPOS_CONFIG.sections():
            print_error('not being tracked', path_to_check)
            continue
        if not quiet_if_tracked:
            print_error('is being tracked', path_to_check)


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(file_okay=False, dir_okay=True, resolve_path=True), required=True)
def update_origin(path: tuple) -> None:
    """Update repo(s) origins in gitstat config."""
    global REPOS_CONFIG
    paths_to_check: List[str] = get_paths(list(path), include_ignored=True)
    if len(paths_to_check) == 0:
        return
    for result in check_paths(paths_to_check, include_uptodate=False, progress_bar=False):
        if 'changes' not in result or GitStatus.URL_MISMATCH not in result['changes']:
            print_error('No URL mismatch', result['path'])
            continue
        new_origin: str = get_repo_url(result['path'])
        print(f"{result['path']}: Updating origin -> {new_origin}")
        REPOS_CONFIG[result['path']]['url'] = new_origin
    write_repos_config()


@cli.command()
def config() -> None:
    """Show configuration information."""
    print('Gitstat config: {}'.format(options_config_filename()))
    print('  Repos config: {}'.format(repos_config_filename()))
    print()
    status_width = max(len(str(x)) for x in GitStatus)
    msg_width = max(len(OUTPUT_MESSAGES[x]) for x in OUTPUT_MESSAGES)
    print('{status}  {default}  {customized}'.format(
        status=Colr('Status', style='underline').ljust(status_width),
        default=Colr('Default color', style='underline').ljust(msg_width),
        customized=Colr('Customized color', style='underline')))
    for git_status in OUTPUT_MESSAGES:
        print('{status}  {default_color}  {customized_color}'.format(
            status=str(git_status).ljust(status_width),
            default_color=colorize_status(git_status, use_defaults=True).ljust(msg_width),
            customized_color=colorize_status(git_status, use_defaults=False)))
