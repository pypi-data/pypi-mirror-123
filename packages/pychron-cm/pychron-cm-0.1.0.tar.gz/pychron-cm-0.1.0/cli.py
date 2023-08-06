# ===============================================================================
# Copyright 2021 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

import click
import platform

from render import render_template

IS_MAC = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--template",
    default=None,
    help="Device Template to use. Typically the device models name",
)
@click.argument("name")
def device(template, name):
    click.echo("Create a new device configuration")


@cli.command()
@click.option(
    "--app",
    default=None,
    help="Application style to install. pycrunch, pyexperiment,...",
)
def install():
    click.echo("Install the pychron application")


@cli.command()
@click.option("--conda", default=False, help="Use the conda package manager")
def launcher(conda):
    click.echo("launcher")
    template = "failed to make tmplate"
    if IS_MAC:
        if conda:
            template = "launcher_mac_conda"
        else:
            template = "launcher_mac"

    txt = render_template(template)
    click.echo(txt)


@cli.command()
def init():
    click.echo("make initialization file")
    template = "initialization.xml"
    txt = render_template(template)
    click.echo(txt)


if __name__ == "__main__":
    cli()
# ============= EOF =============================================
