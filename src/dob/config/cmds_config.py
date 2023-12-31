# This file exists within 'dob':
#
#   https://github.com/tallybark/dob
#
# Copyright © 2019-2020 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it  and/or  modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any later version  (GPLv3+).
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or  FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU  General  Public  License  for  more  details.
#
# If you lost the GNU General Public License that ships with this software
# repository (read the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

from gettext import gettext as _

from click_hotoffthehamster.exceptions import MissingParameter
from config_decorator.key_chained_val import KeyChainedValue
from easy_as_pypi_termio.errors import exit_warning
from easy_as_pypi_termio.paging import click_echo

# Load all the upstream config packages to ensure `dob config dump`, etc.,
# show all config values.
from dob_bright import config as dob_bright_config  # noqa: F401
from dob_bright.config.config_table import echo_config_decorator_table
from dob_bright.crud.interrogate import run_editor_safe
from dob_viewer import config as dob_viewer_config  # noqa: F401
from nark import config as nark_config  # noqa: F401 '<>' imported but unused

__all__ = (
    "alert_if_config_unwell",
    "echo_config_table",
    "echo_config_value",
    "edit_config_file",
    "write_config_value",
    # PRIVATE:
    #  'echo_config_value_setting',
    #  'echo_config_value_section',
    #  'exit_error_no_setting',
    #  'fetch_config_object',
    #  'fetch_config_objects',
    #  'error_exit_not_one',
    #  'config_parts_pop_value',
    #  'must_parts',
    #  'must_be_config_setting',
)


# *** [DUMP] TABLE


# dob-config-show command.
def echo_config_table(
    controller,
    section,
    keyname,
    output_format,
    table_type,
):
    """"""
    parts = list(filter(None, (section, keyname)))
    conf_objs = fetch_config_objects(controller, parts)
    include_hidden = section and keyname
    echo_config_decorator_table(
        cfg_decors=conf_objs,
        include_hidden=include_hidden,
        # Passed on to render_results:
        controller=controller,
        output_format=output_format,
        table_type=table_type,
    )


# *** [EDIT] CONFIG


# dob-config-edit command.
def edit_config_file(controller):
    run_editor_safe(filename=controller.configurable.config_path)


# *** [GET] ECHO


# dob-config-get command.
def echo_config_value(ctx, controller, parts):
    must_parts(ctx, parts, _("“KEYNAME”"))
    section_or_setting = fetch_config_object(controller, parts)
    if isinstance(section_or_setting, KeyChainedValue):
        echo_config_value_setting(section_or_setting)
    else:
        echo_config_value_section(section_or_setting)


def echo_config_value_setting(setting):
    click_echo(setting.value)


def echo_config_value_section(section):
    counts = []
    if section._sections:
        counts.append("{} {}".format(len(section._sections), _("sections")))
    if section._key_vals or not section._sections:
        counts.append("{} {}".format(len(section._key_vals), _("settings")))
    exit_warning(
        _("Configuration section “{}” contains {}.").format(
            section._name,
            _("and").join(counts),
        )
    )


# *** [SET] CONFIG


# dob-config-set command.
def write_config_value(ctx, controller, parts):
    parts, value = config_parts_pop_value(ctx, parts)
    section_or_setting = fetch_config_object(controller, parts)
    setting = must_be_config_setting(section_or_setting)
    try:
        setting.value = value
    except ValueError as err:
        exit_warning(str(err))
    controller.write_config(skip_unset=True)


# *** [GET/SET] FETCH


def fetch_config_object(controller, parts):
    conf_objs = fetch_config_objects(controller, parts)
    if len(conf_objs) == 1:
        return conf_objs[0]
    error_exit_not_one(parts, conf_objs)


def fetch_config_objects(controller, parts):
    try:
        conf_objs = controller.configurable.find_all(parts)
    except AttributeError:
        exit_error_no_setting(parts)
    except KeyError:
        # Raised by configurable on unknown part(s).
        exit_error_no_setting(parts)
    return conf_objs


def error_exit_not_one(parts, conf_objs):
    dotted = ".".join(parts)
    if len(conf_objs) > 1:
        exit_warning(_("ERROR: Too many config objects named: “{}”").format(dotted))
    else:
        # FIXME/2019-11-17 02:18: Should errors be paged if --pager?
        # - See also/Consolidate: echo_exit, exit_warning, exit_warning_crude.
        exit_warning(_("ERROR: Not a config object: “{}”.").format(dotted))


# *** [SECTION] [KEYNAME] [VALUE] VALIDATING


def config_parts_pop_value(ctx, parts):
    parts = list(parts)
    must_parts(ctx, parts, _("“KEYNAME” “VALUE”"), param_type="arguments")
    value = parts.pop()
    must_parts(ctx, parts, _("“VALUE”"))
    return parts, value


def must_parts(ctx, parts, param_hint, param_type="argument"):
    parts = list(parts)
    if not parts:
        raise MissingParameter(
            ctx=ctx,
            param_hint=param_hint,
            param_type=param_type,
        )
    return parts


def must_be_config_setting(section_or_setting):
    if not isinstance(section_or_setting, KeyChainedValue):
        exit_warning(
            _(
                "ERROR: Not a configuration setting: “{}”.".format(
                    section_or_setting._name
                )
            )
        )
    return section_or_setting


def exit_error_no_setting(parts):
    exit_warning(_("ERROR: Not a configuration setting: “{}”.".format(".".join(parts))))


# *** @decorator


def alert_if_config_unwell(func):
    """ """

    def wrapper(ctx, controller, *args, **kwargs):
        controller.alert_user_if_config_file_unwell()
        func(ctx, controller, *args, **kwargs)

    return wrapper
