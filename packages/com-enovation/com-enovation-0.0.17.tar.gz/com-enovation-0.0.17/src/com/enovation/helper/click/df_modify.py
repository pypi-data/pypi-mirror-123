import json
from inspect import stack

import click
from click import BadParameter
from pandas import DataFrame
import logging

_logger: logging.Logger = logging.getLogger(__name__)


@click.command('rename-columns')
@click.pass_context
@click.argument('alias-in', type=str)
@click.argument('dictionary', type=str)
@click.option('-o', '--alias-out', help="Resulting dataframe.", type=str)
def rename_columns(ctx_context, alias_in, dictionary, alias_out):
    """
    Rename dataframe columns.

    :param ctx_context: Click context.
    :param alias_in: dataframe to lad from the context, so its columns can be renamed.
    :param dictionary: dictionary to rename columns, in the form '{"col1":"new col1", ... , "colx":"new colx"}'.
    :param alias_out: alias to the cleansed dataframe, in case source dataframe should not be altered.
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias_in not in ctx_context.obj:
        raise BadParameter(
            message=f"Cannot rename columns from '{alias_in}', as this alias could not be found in context.",
            param_hint=f"Ensure you effectively have a dataframe labelled '{alias_in}' loaded in context.",
            ctx=ctx_context
        )
    if alias_out in ctx_context.obj:
        _logger.warning(
            f"Warning: another object with alias '{alias_out}' already exists, of type {type(alias_out)}. This data "
            f"will be overridden."
        )

    df_the_input: DataFrame = ctx_context.obj[alias_in]

    if not isinstance(df_the_input, DataFrame):
        raise BadParameter(
            message=f"Cannot rename columns from '{alias_in}', as this alias is of type '{type(df_the_input)}' while "
                    f"'DataFrame' is expected.",
            param_hint=f"Ensure you effectively assigned a DataFrame to the alias '{alias_in}'.",
            ctx=ctx_context
        )

    try:
        dict_the_dictionary: dict = json.loads(dictionary)
    except json.decoder.JSONDecodeError as error:
        raise BadParameter(
            message=f"Cannot transform '{dictionary}' as a dictionary to rename columns.",
            param_hint=f"Ensure you effectively provided a string with 'key':'value' assignment that can be used to "
                       f"rename columns.",
            ctx=ctx_context
        ) from error

    # We check the dictionary is a simple set of key:value assignments
    lst_the_errors: list = [
        "'"+k+"'" for k, v in dict_the_dictionary.items()
        if (
            (not isinstance(k, str))
            | (not isinstance(v, str))
        )
    ]
    if len(lst_the_errors):
        raise BadParameter(
            message=f"Cannot use '{dictionary}' as a dictionary to rename columns.",
            param_hint=f"Ensure you effectively provided a string with simple 'key as string':'value as string' "
                       f"assignment that can be used to rename columns.",
            ctx=ctx_context
        )

    # We check the dictionary only provides keys that effectively exist as columns
    lst_the_errors: list = list({k for k in dict_the_dictionary}-set(df_the_input.columns))
    if len(lst_the_errors) > 0:
        raise BadParameter(
            message=f"Columns '{', '.join(lst_the_errors)}' are to be renamed, but they do not exist in the dataframe.",
            param_hint=f"Ensure you effectively provide columns to rename that exist in the dataframe.",
            ctx=ctx_context
        )

    df_the_return: DataFrame = df_the_input.rename(columns=dict_the_dictionary)

    # We refresh the context data store
    if alias_out:
        ctx_context.obj[alias_out] = df_the_return
    else:
        ctx_context.obj[alias_in] = df_the_return

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")


@click.command('cleanse-null-values')
@click.pass_context
@click.argument('alias-in', type=str)
@click.argument('column', type=str)
@click.option('-v', '--value', help="Value to replace null.", type=str)
@click.option('-o', '--alias-out', help="Resulting dataframe.", type=str)
def cleanse_null_values(ctx_context, alias_in, column, value, alias_out):
    """
    Cleanses null values in listed columns, either replace with value when provided, or drop lines.

    :param alias_in: alias to a dataframe to cleanse.
    :param alias_out: alias to the cleansed dataframe, in case source dataframe should not be altered.
    :param column: columns labels to cleanse null values.
    :param value: value to replace null.
    :param ctx_context: Click context.
    """
    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

    if alias_in not in ctx_context.obj:
        raise BadParameter(
            message=f"Cannot cleanse '{alias_in}', as this alias could not be found in context.",
            param_hint=f"Ensure you effectively loaded some data, and labelled these with the alias '{alias_in}'.",
            ctx=ctx_context
        )

    if not isinstance(ctx_context.obj[alias_in], DataFrame):
        raise BadParameter(
            message=f"Cannot cleanse '{alias_in}', as this alias is of type '{type(ctx_context.obj[alias_in])}' while "
                    f"'DataFrame' is expected.",
            param_hint=f"Ensure you effectively used operands to generate data as a DataFrame.",
            ctx=ctx_context
        )

    df_the_measures = ctx_context.obj[alias_in]

    if column not in df_the_measures.columns:
        raise Exception(f"The command cleanse_null_values cannot access column '{column}'. First, ensure this column "
                        f"effectively exists (aka. present among the columns of a loaded file, or present among "
                        f"generated data by a command), then call this function to cleanse null values.")

    if value:
        df_the_measures = df_the_measures[column].fillna(value)
    else:
        df_the_measures = df_the_measures[df_the_measures[column].notna()]
        _logger.info(f"Rows containing null value deleted, shape '{df_the_measures.shape}'.")

    # We refresh the context data store
    if alias_out:
        ctx_context.obj[alias_out] = df_the_measures
    else:
        ctx_context.obj[alias_in] = df_the_measures

    _logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
