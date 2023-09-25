import os
import shutil
import subprocess
import tempfile

import pytest

from ansys.tools.repo_sync.repo_sync import synchronize

from .conftest import (
    ASSETS_DIRECTORY,
    ROOT_PATH,
    SKIP_LOCALLY,
    TOKEN,
    check_files_in_pr,
    cleanup_remote_repo,
    get_pr_from_cli,
)


def test_synchronize():
    """Test synchronization tool (without manifest)."""

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest.txt")

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
            include_manifest=manifest,
            skip_ci=True,
            random_branch_name=True,
        )

        # Assertions or validations
        assert f"https://github.com/ansys/ansys-tools-repo-sync/pull/" in result

        # Check that the proper modified files have been added
        list_of_files = ["src/ansys/api/test/v0/hello_world.py", "src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(owner, repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(owner, repository, result)


def test_synchronize_with_only_proto_manifest():
    """Test synchronization tool (with manifest)."""

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest_only_proto.txt")

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
            include_manifest=manifest,
            skip_ci=True,
            random_branch_name=True,
        )

        # Assertions or validations
        assert f"https://github.com/ansys/ansys-tools-repo-sync/pull/" in result

        # Check that the proper modified files have been added
        list_of_files = ["src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(owner, repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(owner, repository, result)


def test_synchronize_with_cleanup():
    """Test synchronization tool (with --clean-to-dir flag)."""

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest.txt")

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
            include_manifest=manifest,
            clean_to_dir=True,
            skip_ci=True,
            random_branch_name=True,
        )

        # Assertions or validations
        assert f"https://github.com/ansys/ansys-tools-repo-sync/pull/" in result

        # Check that the proper modified files have been added
        list_of_files = [
            "src/ansys/api/test/v0/hello_world.py",
            "src/ansys/api/test/v0/test.proto",
            "src/ansys/tools/repo_sync/__init__.py",
            "src/ansys/tools/repo_sync/__main__.py",
            "src/ansys/tools/repo_sync/repo_sync.py",
        ]
        assert check_files_in_pr(owner, repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(owner, repository, result)


@pytest.mark.skipif(SKIP_LOCALLY, reason="Only runs on workflow")
def test_synchronize_from_cli():
    """Test synchronization tool (without manifest) from CLI."""

    # Define a temp directory and copy assets in it
    temp_dir = tempfile.TemporaryDirectory(prefix="repo_clone_cli_")
    shutil.copytree(
        ASSETS_DIRECTORY,
        temp_dir.name,
        dirs_exist_ok=True,
    )

    # Requires installing project
    subprocess.run(
        [
            "pip",
            "install",
            ".",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT_PATH,
    )

    # Call CLI tool
    completed_process = subprocess.run(
        [
            "repo-sync",
            "--token",
            TOKEN,
            "--owner",
            "ansys",
            "--repository",
            "ansys-tools-repo-sync",
            "--from-dir",
            "ansys",
            "--to-dir",
            "src/ansys",
            "--include-manifest",
            "manifest.txt",
            "--skip-ci",
            "--random-branch-name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=temp_dir.name,
    )

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Get the PR associated to the CLI
    pr_url = get_pr_from_cli("ansys", "ansys-tools-repo-sync", completed_process.stdout)

    # Check that the proper modified files have been added
    list_of_files = ["src/ansys/api/test/v0/hello_world.py", "src/ansys/api/test/v0/test.proto"]
    assert check_files_in_pr("ansys", "ansys-tools-repo-sync", pr_url, list_of_files)

    # Clean up remote repo
    cleanup_remote_repo("ansys", "ansys-tools-repo-sync", pr_url)


@pytest.mark.skipif(SKIP_LOCALLY, reason="Only runs on workflow")
def test_synchronize_with_only_proto_manifest_from_cli():
    """Test synchronization tool (with manifest) from CLI."""

    # Define a temp directory and copy assets in it
    temp_dir = tempfile.TemporaryDirectory(prefix="repo_clone_cli_")
    shutil.copytree(
        ASSETS_DIRECTORY,
        temp_dir.name,
        dirs_exist_ok=True,
    )

    # Requires installing project
    subprocess.run(
        [
            "pip",
            "install",
            ".",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT_PATH,
    )

    # Call CLI tool
    completed_process = subprocess.run(
        [
            "repo-sync",
            "--token",
            TOKEN,
            "--owner",
            "ansys",
            "--repository",
            "ansys-tools-repo-sync",
            "--from-dir",
            "ansys",
            "--to-dir",
            "src/ansys",
            "--include-manifest",
            "manifest_only_proto.txt",
            "--skip-ci",
            "--random-branch-name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=temp_dir.name,
    )

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Get the PR associated to the CLI
    pr_url = get_pr_from_cli("ansys", "ansys-tools-repo-sync", completed_process.stdout)

    # Check that the proper modified files have been added
    list_of_files = ["src/ansys/api/test/v0/test.proto"]
    assert check_files_in_pr("ansys", "ansys-tools-repo-sync", pr_url, list_of_files)

    # Clean up remote repo
    cleanup_remote_repo("ansys", "ansys-tools-repo-sync", pr_url)


@pytest.mark.skipif(SKIP_LOCALLY, reason="Only runs on workflow")
def test_synchronize_with_cleanup_cli():
    """Test synchronization tool (with --clean-to-dir flag) from CLI."""

    # Define a temp directory and copy assets in it
    temp_dir = tempfile.TemporaryDirectory(prefix="repo_clone_cli_")
    shutil.copytree(
        ASSETS_DIRECTORY,
        temp_dir.name,
        dirs_exist_ok=True,
    )

    # Requires installing project
    subprocess.run(
        [
            "pip",
            "install",
            ".",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT_PATH,
    )

    # Call CLI tool
    completed_process = subprocess.run(
        [
            "repo-sync",
            "--token",
            TOKEN,
            "--owner",
            "ansys",
            "--repository",
            "ansys-tools-repo-sync",
            "--from-dir",
            "ansys",
            "--to-dir",
            "src/ansys",
            "--include-manifest",
            "manifest.txt",
            "--skip-ci",
            "--random-branch-name",
            "--clean-to-dir",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=temp_dir.name,
    )

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Get the PR associated to the CLI
    pr_url = get_pr_from_cli("ansys", "ansys-tools-repo-sync", completed_process.stdout)

    # Check that the proper modified files have been added
    list_of_files = [
        "src/ansys/api/test/v0/hello_world.py",
        "src/ansys/api/test/v0/test.proto",
        "src/ansys/tools/repo_sync/__init__.py",
        "src/ansys/tools/repo_sync/__main__.py",
        "src/ansys/tools/repo_sync/repo_sync.py",
    ]
    assert check_files_in_pr("ansys", "ansys-tools-repo-sync", pr_url, list_of_files)

    # Clean up remote repo
    cleanup_remote_repo("ansys", "ansys-tools-repo-sync", pr_url)
