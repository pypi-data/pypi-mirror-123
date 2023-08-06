###############################################################################
# (c) Copyright 2020 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
__version__ = "0.1.0"

import os
import sys
import logging
import json
import re
from collections import namedtuple
from urllib.request import urlopen

from .Project import Project, DBASE, Package, PARAM, DataProject
from .Slot import Slot, slot_factory
from .Utils import save, configToString


def service_config(config_file=None):
    """
    Returns dictionary with configs required to use external
    services like couchdb, rabbitmq or gitlab. All the
    information needed (urls, ports, tokens, username,
    passwords, etc.) should be stored in yaml file provided as an argument
    or the agreed file from the private directory will be taken.
    If yaml is not correct or does not exists, exception is raised.
    """
    import yaml

    if config_file is None:
        # if configuration file is not provided
        # try to take secrets.yaml from private directory
        if os.environ.get("PRIVATE_DIR"):
            config_file = os.path.join(os.environ["PRIVATE_DIR"], "secrets.yaml")
        else:
            config_file = os.path.expanduser(
                os.path.join("~", "private", "secrets.yaml")
            )

    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
    except (yaml.YAMLError, FileNotFoundError) as exc:
        logging.warning(f"Could not get the configuration for this service: {exc}")
        raise

    return config


def loadConfig(module=None):
    """
    Load all slots from a config module.
    """
    from importlib import import_module
    import git

    orig_path = list(sys.path)
    if module is None:
        module_name, attribute = "lhcbnightlyconf", "slots"
    elif ":" in module:
        module_name, attribute = module.split(":", 1)
    else:
        module_name, attribute = module, "slots"
    sys.path.insert(0, os.curdir)
    sys.path.insert(0, "configs")
    m = import_module(module_name)
    try:  # to get the commit id of the config directory
        config_id = (
            git.Repo(m.__path__[0], search_parent_directories=True)
            .rev_parse("HEAD")
            .hexsha
        )
    except git.GitError:
        config_id = None
    slot_list = getattr(m, attribute)
    logging.debug("using explicit configuration")
    slot_dict = {}
    for slot in slot_list:
        assert (
            slot.name not in slot_dict
        ), "Slot {} defined in 2 places: {} and {}".format(
            slot.name, slot_dict[slot.name]._source, slot._source
        )
        if config_id:
            slot.metadata["config_id"] = config_id
        slot_dict[slot.name] = slot
    sys.path = orig_path
    return slot_dict


def findSlot(name, flavour="nightly", server=None, dbname=None):
    """
    Helper to load a Slot configuration from file or dashboard.

    If server is not specified, the configuration is retrieved from the
    dashboard (the name parameter should match '<name>.<build_id>'). 
    Otherwise the server should be specified as 'file:///path/to/directory'
    and the name parameter should be name of the json file with the configuration.
    If the resource cannot be retrieved, the exception will be raised
    by urllib.request.urlopen()
    """
    url = "/".join(
        [server or service_config()["couchdb"]["url"].format(flavour=flavour), name]
    )
    logging.debug("retrieving %s", url)
    return Slot.fromDict(json.load(urlopen(url))["config"])


KeyTuple = namedtuple("KeyTuple", ["flavour", "name", "id", "project"])
KeyTuple.__str__ = lambda self: "/".join(str(i) for i in self if i is not None)


def _parse_key(key):
    """
    Parse a key like "[flavour/]slotname[/build_id][/project]" to its parts.

    Returns a named tuple with the elements.

    NOTE: if `flavour/` is present, there must be also at least one of `/build_id`
          or `/project`, as the string "a/b" is always interpreted as "slot/project"
    """
    # defaults for optional entries
    flavour, build_id, project = "nightly", "0", None
    name = None  # used to flag invalid keys

    tokens = key.split("/")
    if len(tokens) == 1:  # only slot name
        name = tokens[0]
    elif len(tokens) == 2:  # slot/build_id or slot/project
        name = tokens[0]
        if tokens[1].isdigit():
            build_id = tokens[1]
        else:
            project = tokens[1]
    elif len(tokens) == 3:  # f/s/b, f/s/p or s/b/p
        if tokens[2].isdigit():  # f/s/b
            flavour, name, build_id = tokens
        elif tokens[1].isdigit():  # s/b/p
            name, build_id, project = tokens
        else:  # f/s/p
            flavour, name, project = tokens
    elif len(tokens) == 4:
        if tokens[2].isdigit():
            flavour, name, build_id, project = tokens

    if not name:
        raise ValueError("%r is not a valid key" % key)

    return KeyTuple(flavour, name, int(build_id), project)


def get(key):
    """
    Return the instance identified by a key like "[flavour/]slotname[/build_id][/project]".

    When the build_id part is present, the slot configuration is taken from CouchDB.
    """
    flavour, slot, build_id, project = _parse_key(key)
    if build_id:
        slot = "{}.{}".format(slot, build_id)
    try:
        slot = findSlot(slot, flavour)
    except Exception as exc:
        raise IOError(f"could not find the slot due to: {exc}")
    slot.metadata["flavour"] = flavour
    # clone slot instance
    slot = Slot.fromDict(slot.toDict())
    if project is None:
        return slot
    else:
        return slot.projects[project]


def check_slot(slot):
    """
    Check that a slot configuration is valid.
    """
    good = True
    log = logging.getLogger(slot.name)

    def check_type(field_name, types, value=None):
        if value is None:
            value = getattr(slot, field_name)
        if not isinstance(value, types):
            log.error(
                'invalid %s type: found %s, expected any of [%s]', field_name,
                type(value).__name__, ', '.join(t.__name__ for t in types))
            return False
        return True

    def check_list_of_strings(field_name, name, regex):
        good = check_type(field_name, (list, tuple))
        for x in getattr(slot, field_name):
            if check_type(name, (str, ), x):
                if not re.match(regex, x):
                    log.error('invalid %s value: %r', name, x)
                    good = False
            else:
                good = False
        return good

    for field_name in ('warning_exceptions', 'error_exceptions'):
        good &= check_type(field_name, (list, tuple))
        for x in getattr(slot, field_name):
            try:
                re.compile(x)
            except Exception as err:
                good = False
                log.error('%s: invalid value %r: %s', field_name, x, err)

    good &= check_list_of_strings(
        'platforms', 'platform',
        r'^[a-z0-9_+]+-[a-z0-9_]+-[a-z0-9_]+-[a-z0-9_+]+$')
    good &= check_list_of_strings('env', 'env setting',
                                  r'^[a-zA-Z_][a-z0-9A-Z_]*=')

    return good


def check_config():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "module",
        nargs="?",
        help="name of the Python module to import to get the slots from"
        ' (by default "lhcbnightlyconf"),'
        ' an optional ":name" suffix can be used to specify the attribute '
        "of the module that contains the list of slots to use (by default "
        '"slots")',
    )
    parser.add_argument(
        "--debug",
        action="store_const",
        dest="log_level",
        const=logging.DEBUG,
        help="print debug messages",
    )
    parser.add_argument(
        "--dump-json",
        metavar="FILENAME",
        help="dump all loaded slots configuration as a JSON list of objects",
    )
    parser.set_defaults(module="lhcbnightlyconf", log_level=logging.INFO)
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    slots = loadConfig(args.module)

    print(
        "{0} slots configured ({1} enabled)".format(
            len(slots), len([s for s in list(slots.values()) if s.enabled])
        )
    )

    from tabulate import tabulate

    print(
        tabulate(
            [
                [
                    name,
                    "X" if slots[name].enabled else " ",
                    ", ".join(slots[name].deployment),
                    slots[name]._source,
                ]
                for name in sorted(slots)
            ],
            headers=("slot", "enabled", "deployment", "source"),
            tablefmt="grid",
        )
    )

    logging.debug('running semantics checks')
    if not all(check_slot(slot) for slot in slots.values()):
        return 1

    logging.debug("converting slots to JSON")
    json_str = json.dumps([slots[name].toDict() for name in sorted(slots)], indent=2)
    if args.dump_json:
        logging.info("writing slot details to %s", args.dump_json)
        with open(args.dump_json, "w") as f:
            f.write(json_str)

    return 0
