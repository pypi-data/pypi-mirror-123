import uvicorn
import typer

from mappable.server import setup_app
from mappable.map import Mappable, DEFAULT_MAPPABLE_DIR

cli = typer.Typer()


@cli.command()
def run(dir: str = DEFAULT_MAPPABLE_DIR, host: str = "127.0.0.1", port: int = 8000):

    """
    Run the Mappable interface.
    """
    mappable_instance = Mappable(dir)

    app = setup_app(mappable_instance)
    uvicorn.run(app, host=host, port=port)


# This forces typer to create a command with a single sub command,
# rather than infering that we want our single command to be the root
# application (e.g `mappable` vs `mappable run`). We want it to be
# `mappable run` so that adding other commands is backward compatible.
@cli.callback()
def callback():
    pass


if __name__ == "__main__":
    cli()
