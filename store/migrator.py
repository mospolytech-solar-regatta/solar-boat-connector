import alembic.config
import alembic.command
import alembic
import subprocess


class AlembicMigrator:
    def migrate_to_latest(self):
        process = subprocess.Popen(['alembic', 'upgrade', 'head'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        print(stderr.decode('utf-8'))
