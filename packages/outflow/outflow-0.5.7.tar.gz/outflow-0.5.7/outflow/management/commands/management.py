# -*- coding: utf-8 -*-
from outflow.core.commands import RootCommand, Command
from outflow.library.tasks import IPythonTask
from outflow.core.pipeline import config


@RootCommand.subcommand(invokable=False, db_untracked=True, backend="default")
def Management():
    pass


@Management.subcommand()
def DisplayConfig():
    print(config)


@Management.subcommand(db_untracked=False)
class Shell(Command):
    """
    Run an interactive shell with access to the pipeline context.
    """

    def setup_tasks(self):
        return IPythonTask()
