# Copyright 2015: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os

import decorator

from rally.common.plugin import discover


PLUGINS_LOADED = False


def load():
    global PLUGINS_LOADED

    if not PLUGINS_LOADED:
        from rally.common import opts

        opts.register()

        discover.import_modules_from_package("rally.deployment.engines")
        discover.import_modules_from_package("rally.deployment.serverprovider")
        discover.import_modules_from_package("rally.plugins.common")
        try:
            import rally_openstack  # noqa
        except ImportError:
            discover.LOG.warning(
                "OpenStack plugins moved to the separate package "
                "(see https://pypi.org/project/rally-openstack). In-tree "
                "OpenStack plugins will be removed from the Rally main package"
                " soon.")
            discover.import_modules_from_package("rally.plugins.openstack")
            discover.import_modules_from_package("rally.plugins.workload")

        discover.import_modules_by_entry_point()

        discover.load_plugins("/opt/rally/plugins/")
        discover.load_plugins(os.path.expanduser("~/.rally/plugins/"))

    PLUGINS_LOADED = True


@decorator.decorator
def ensure_plugins_are_loaded(f, *args, **kwargs):
    load()
    return f(*args, **kwargs)
