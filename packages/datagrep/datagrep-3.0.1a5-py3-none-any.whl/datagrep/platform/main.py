import platform
from pathlib import Path
from typing import Iterable, Optional

import click
import plumbum
import typer
from click import Context
from cookiecutter.main import cookiecutter
from plumbum import FG, local


class OrderedCommands(click.Group):
    def list_commands(self, ctx: Context) -> Iterable[str]:
        return self.commands.keys()


app = typer.Typer(cls=OrderedCommands)


@app.callback()
def callback():
    """
    The datagrep platform CLI.
    """


@app.command()
def init(
    domain_name: Optional[str] = typer.Option("datagrep.com", help="The domain name."),
    project_name: Optional[str] = typer.Option("datagrep", help="The project name."),
    project_slug: Optional[str] = typer.Option(
        "com.datagrep", help="The project folder name."
    ),
):
    """
    Initialize...
    """
    typer.echo("Initializing...")

    cookiecutter(
        "datagrep/",
        no_input=True,
        overwrite_if_exists=True,
        extra_context={
            "domain_name": domain_name,
            "project_name": project_name,
            "project_slug": project_slug,
        },
    )


@app.command()
def build():
    """
    Build...
    """
    typer.echo("Building...")

    try:
        jq = local["jq"]
        jq["--version"] & FG

    except plumbum.commands.processes.CommandNotFound:
        typer.launch(f"https://stedolan.github.io/jq")
        raise typer.Exit(code=1)

    try:
        multipass = local["multipass"]
        multipass["version"] & FG

    except plumbum.commands.processes.CommandNotFound:
        typer.launch(f"https://multipass.run")
        raise typer.Exit(code=1)

    try:
        hostctl = local["hostctl"]
        hostctl["--version"] & FG

    except plumbum.commands.processes.CommandNotFound:
        typer.launch(f"https://guumaster.github.io/hostctl")
        raise typer.Exit(code=1)


@app.command()
def deploy(
    target: Optional[str] = typer.Argument(
        "local", help="Where to deploy the platform?"
    ),
    num_worker_nodes: Optional[int] = typer.Argument(
        2, help="The number of worker nodes to create."
    ),
):
    """
    Deploy the platform to TARGET with NUM_WORKER_NODES worker nodes.
    """
    typer.echo(
        f"Deploying the platform to {target} with {num_worker_nodes} worker nodes..."
    )

    if target == "local":
        multipass = local["multipass"]

        (
            multipass[
                "launch",
                "--cloud-init",
                "cloud-config.yaml",
                "--cpus",
                "4",
                "--disk",
                "40G",
                "--mem",
                "4G",
                "--name",
                "datagrep-head",
            ]
            & FG
        )
        multipass["exec", "datagrep-head", "sudo", "ufw", "allow", "25000/tcp"] & FG

        for worker_node_i in range(num_worker_nodes):
            (
                multipass[
                    "launch",
                    "--cloud-init",
                    "cloud-config.yaml",
                    "--cpus",
                    "4",
                    "--disk",
                    "40G",
                    "--mem",
                    "4G",
                    "--name",
                    f"datagrep-worker-{worker_node_i}",
                ]
                & FG
            )
            add_node = (
                multipass["exec", "datagrep-head", "microk8s", "add-node"]
                | local["grep"]["^microk8s join"]
            )
            (
                multipass[
                    "exec", f"datagrep-worker-{worker_node_i}", add_node().split()
                ]
                & FG
            )

        (
            multipass[
                "exec",
                "datagrep-head",
                "git",
                "clone",
                "https://github.com/ray-project/ray.git",
            ]
            & FG
        )
        multipass["exec", "datagrep-head", "microk8s", "enable", "helm3"] & FG
        (
            multipass[
                "exec",
                "datagrep-head",
                "helm",
                "--",
                "-n",
                "ray",
                "install",
                "ray-cluster",
                "--create-namespace",
                "./ray/deploy/charts/ray",
            ]
            & FG
        )
        multipass["list"]

    else:
        raise Exception("Not implemented!")


@app.command()
def release(domain: Optional[str] = typer.Argument("localhost", envvar="DOMAIN_NAME")):
    """
    Release the platform to DOMAIN.
    """
    typer.echo(f"Releasing the platform to {domain}...")

    if domain == "localhost" or ".local" in domain:
        multipass = local["multipass"]
        jq = local["jq"]
        ip = (
            multipass["info", "datagrep-head", "--format", "json"]
            | jq['.info["datagrep-head"]["ipv4"][0]']
        )

        Path("./.etchosts").write_text(
            "\n".join(
                [
                    " ".join([(ip().strip()).replace('"', ""), domain]),
                    " ".join([(ip().strip()).replace('"', ""), f"minio.{domain}"]),
                    " ".join(
                        [(ip().strip()).replace('"', ""), f"console.minio.{domain}"]
                    ),
                ]
            )
        )

        if platform.system() == "Windows":
            sudo = local["runas"]["user:administrator"]  # TODO: Test on Windows

        else:
            sudo = local["sudo"]

        sudo["hostctl", "replace", "datagrep", "--from", f"{Path.cwd()}/.etchosts"] & FG

        typer.echo(f"The platform is ready at https://{domain}.")

    else:
        raise Exception("Not implemented!")
