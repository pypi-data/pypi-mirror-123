import logging
from inspect import stack

import click

from com.enovation.helper.click.df_load import load_csv, load_xls
from com.enovation.helper.click.df_write import to_stdout, to_xlsx
from com.enovation.helper.click.df_modify import rename_columns, cleanse_null_values
from com.enovation.toolbox.predictability.click.dp_compute import dp_compute_date_predictability
from com.enovation.toolbox.predictability.click.dp_demo import dp_demo_date_predictability
from com.enovation.toolbox.predictability.click.dp_persist \
    import dp_write_bean_date_predictability, dp_load_bean_date_predictability
from com.enovation.toolbox.predictability.click.dp_graph import dp_graph_to_dash_date_predictability


_logger: logging.Logger = logging.getLogger(__name__)


@click.group(chain=True)
@click.option(
    '--verbose/--no-verbose', type=bool, default=None,
    help='Level of logging verbosity: INFO (--verbose), WARNING (default) or ERROR (--no-verbose).',
)
@click.pass_context
def enov(ctx_context, verbose):
    """
    The click application to call com.enovation modules...
    """

    if verbose is True:
        click.echo("logging: INFO")
        logging.basicConfig(level="INFO")
    elif verbose is False:
        click.echo("logging: ERROR")
        logging.basicConfig(level="ERROR")
    else:
        click.echo("logging: WARNING")
        logging.basicConfig(level="WARNING")

    _logger.debug(f"Function enov called.")
    _logger.info(f"Welcome!")

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    # Ensure that ctx_context.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    # This is effectively the context, that is shared across commands
    ctx_context.ensure_object(dict)

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")


# com.enovation.helper.click.df_load
enov.add_command(load_csv)
enov.add_command(load_xls)

# com.enovation.helper.click.df_write
enov.add_command(to_stdout)
enov.add_command(to_xlsx)

# com.enovation.helper.click.df_modify
enov.add_command(rename_columns)
enov.add_command(cleanse_null_values)

# com.enovation.toolbox.predictability.click - Date Predictability
enov.add_command(dp_compute_date_predictability)
enov.add_command(dp_write_bean_date_predictability)
enov.add_command(dp_load_bean_date_predictability)
enov.add_command(dp_graph_to_dash_date_predictability)
enov.add_command(dp_demo_date_predictability)


if __name__ == '__main__':
    enov()
