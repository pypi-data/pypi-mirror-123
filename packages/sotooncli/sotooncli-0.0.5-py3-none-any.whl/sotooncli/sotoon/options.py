try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata

import click

from sotooncli.settings import APP_NAME


def get_version_option():
    def version_callback(ctx, param, value):
        if not value:
            return
        package_name = APP_NAME
        try:
            version = metadata.version(package_name)
        except metadata.PackageNotFoundError:
            raise click.ClickException(f"Could not found {package_name!r} package.")
        if version is None:
            raise click.ClickException(
                f"Could not determine the version for {package_name!r} automatically."
            )

        click.echo(version)
        ctx.exit()

    version_option = click.Option(
        param_decls=["--version", "-v"],
        is_flag=True,
        show_default=False,
        expose_value=False,
        help="Show the version and exit.",
        is_eager=True,
        callback=version_callback,
    )
    return version_option
