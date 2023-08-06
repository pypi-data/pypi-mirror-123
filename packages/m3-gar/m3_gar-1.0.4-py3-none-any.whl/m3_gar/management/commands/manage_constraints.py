from django.core.management import (
    BaseCommand,
)
from django.db import (
    connections,
    transaction,
)

from m3_gar import (
    config,
)
from m3_gar.importer.constraints import (
    remove_constraints_from_model,
    restore_constraints_for_model,
)
from m3_gar.util import (
    get_models,
)


class Command(BaseCommand):
    help = 'Manage DB constraints and indexes'

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            'state',
            choices=['enable', 'disable'],
            help='Enable/disable all database foreign constraints and indexes',
        )

        parser.add_argument(
            '--commit',
            action='store_true',
            default=False,
            help='Commit produced SQL to the database',
        )

    def handle(
        self, *args,
        state,
        commit,
        **kwargs,
    ):
        alter_constraints_for_model = (
            restore_constraints_for_model
            if state == 'enable'
            else remove_constraints_from_model
        )

        models = get_models()
        sql_collected = []

        for model in models:
            for sql in alter_constraints_for_model(model):
                sql_collected.extend(sql)

        if commit:
            with transaction.atomic(using=config.DATABASE_ALIAS):
                conn = connections[config.DATABASE_ALIAS]
                with conn.cursor() as cursor:
                    for sql in sql_collected:
                        cursor.execute(sql)

        for sql in sql_collected:
            self.stdout.write(sql)
