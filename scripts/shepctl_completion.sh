#!/bin/bash

# Copyright (c) 2025 Lunatic Fringers
#
# This file is part of Shepherd Core Stack
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

_shepctl_completion() {
    COMPREPLY=()
    args="${COMP_WORDS[@]:1}"
    cur="${COMP_WORDS[COMP_CWORD]}"

    tokens=$(shepctl __complete $args)
    readarray -t tokens_array <<< "$tokens"
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to get completions from shepctl" >&2
        return 1
    fi

    COMPREPLY=( $(compgen -W "${tokens_array[*]}" -- ${cur}) )
    return 0
}

complete -F _shepctl_completion shepctl
