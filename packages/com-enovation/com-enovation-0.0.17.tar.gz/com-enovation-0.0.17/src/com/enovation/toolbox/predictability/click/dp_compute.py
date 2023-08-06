import logging
from inspect import stack

import click
from click import BadParameter
from pandas import DataFrame

from com.enovation.toolbox.predictability.bean import PredictabilityBean
from com.enovation.toolbox.predictability.dp_date_predictability.dp_computer import DatePredictabilityComputer


_logger: logging.Logger = logging.getLogger(__name__)


@click.command('dp_compute')
@click.pass_context
@click.argument('alias-in', type=str)
@click.option('-o', '--alias-out', help="Resulting dataframe.", type=str)
@click.option(
    '--resample/--no-resample', type=bool, default=False,
    help='To resample daily the measures, to have better graphing.',
)
def dp_compute_date_predictability(ctx_context, alias_in, alias_out, resample):
    """
    Rename dataframe columns.

    :param ctx_context: Click context.
    :param alias_in: dataframe to lad from the context, so its columns can be renamed.
    :param alias_out: alias to the cleansed dataframe, in case source dataframe should not be altered.
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias_in not in ctx_context.obj:
        raise BadParameter(
            message=f"No object labelled '{alias_in}' could be found in context, which is not expected.",
            param_hint=f"Ensure you effectively have an object labelled '{alias_in}' in context.",
            ctx=ctx_context
        )
    elif not isinstance(ctx_context.obj[alias_in], DataFrame):
        raise BadParameter(
            message=f"Object labelled '{alias_in}' is of type '{type(ctx_context.obj[alias_in])}', which is not "
                    f"expected.",
            param_hint=f"Ensure to provide an 'DataFrame' instance.",
            ctx=ctx_context
        )

    if alias_out in ctx_context.obj:
        _logger.warning(
            f"Warning: another object with alias '{alias_out}' already exists, of type "
            f"'{type(ctx_context.obj[alias_in])}'. This data will be overridden."
        )

    df_the_input: DataFrame = ctx_context.obj[alias_in]

    obj_the_computer: DatePredictabilityComputer = DatePredictabilityComputer()

    obj_the_bean: PredictabilityBean = obj_the_computer.compute_historical_date_predictability(
        df_measures=df_the_input,
        b_resample=resample
    )

    # We refresh the context data store
    if alias_out:
        ctx_context.obj[alias_out] = obj_the_bean
    else:
        ctx_context.obj[alias_in] = obj_the_bean

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
