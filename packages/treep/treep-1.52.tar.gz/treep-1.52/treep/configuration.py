# Treep, copyright 2019 Max Planck Gesellschaft
# Author : Vincent Berenz

# This file is part of Treep.

#    Treep is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Treep is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Treep.  If not, see <https://www.gnu.org/licenses/>.


class Configuration:
    def __init__(self, origin_prefixes):
        self._origin_prefixes = origin_prefixes

    def get_origin(self, repo_name, yaml_origin, remote_type):
        """Generate the https and ssh origin for a given repo name and origin.

        Args:
            repo_name (str): git repository name
            yaml_origin (str): the value next to "origin" in the
                               repositories_XXX.yaml files
            remote_type (str): "ssh" or "https", they correspond respectively
                               to the url used during cloning with
                               ssh or https. e.g. with github the ssh url is
                               git@github.com:organization_name/repository_name
                               and the https url is
                               https://github.com/organization_name/repository_name

        Returns:
            [str]: if remote_type is 'ssh': ssh_origin
                   elif remote_type is https: https_origin
                   else yaml_origin
        """
        if yaml_origin is None:
            if "default" in self._origin_prefixes.keys():
                return self._origin_prefixes["default"] + repo_name

        origin_name = remote_type + "-" + yaml_origin
        if origin_name in self._origin_prefixes.keys():
            origin_prefix = self._origin_prefixes[origin_name]
            # if the yaml_origin lacks the final slash we add it here.
            if origin_prefix[-1] != "/":
                origin_prefix += "/"
            return origin_prefix + repo_name
        elif yaml_origin in self._origin_prefixes.keys():
            return self._origin_prefixes[yaml_origin] + repo_name

        return yaml_origin

    def extend(self, other):

        for k, v in other._origin_prefixes.items():
            self._origin_prefixes[k] = v
