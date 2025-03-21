# MIT License
#
# Copyright (c) 2025 Lunatic Fringers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import override

from service import Service


class DatabaseService(Service):
    @override
    def build_image(self):
        """Build the DBMS image."""
        pass

    @override
    def bootstrap(self):
        """Bootstrap the DBMS service."""
        pass

    @override
    def start(self):
        """Start the DBMS service."""
        pass

    @override
    def halt(self):
        """Halt the DBMS service."""
        pass

    @override
    def reload(self):
        """Reload the DBMS service."""
        pass

    @override
    def show_stdout(self):
        """Show the DBMS stdout."""
        pass

    @override
    def get_shell(self):
        """Get a shell session for the DBMS."""
        pass

    def get_sql_shell(self):
        """Get a SQL shell session."""
        pass

    def create_user(self, user: str, psw: str):
        """Create a new database user."""
        pass

    def create_directory(self, user: str, directory_name: str):
        """Create a directory object in the database."""
        pass

    def remove_user(self, user: str):
        """Drop an existing database user."""
        pass


class DatabaseMng:
    def build_image(self):
        """Build a DBMS image."""
        pass

    def bootstrap(self):
        """Bootstrap a DBMS service."""
        pass

    def start(self):
        """Start a DBMS service."""
        pass

    def halt(self):
        """Halt a DBMS service."""
        pass

    def stdout(self):
        """Show a DBMS stdout."""
        pass

    def shell(self):
        """Get a DBMS shell session."""
        pass

    def sql_shell(self):
        """Get a SQL shell session."""
        pass

    def create_database_user(self, user: str, psw: str):
        """Create a new database user."""
        pass

    def create_database_directory(self, user: str, directory_name: str):
        """Create a directory object in a database."""
        pass

    def remove_database_user(self, user: str):
        """Drop an existing user."""
        pass
