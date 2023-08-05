from django.core.management.base import BaseCommand

from ...ftp.utils import parse_all_users_files


class Command(BaseCommand):
    help = 'Load users files found in ftp user folders'

    def handle(self, *args, **options):
        try:
            parsed_users = parse_all_users_files()

        except Exception as e:
            self.stdout.write(self.style.ERROR('Error parsing ftp user files: "{}"'.format(e)))

        loaded_files = 0
        for uf in parsed_users:
            loaded_files += len(parsed_users[uf])

        self.stdout.write(self.style.SUCCESS('{} files loaded'.format(loaded_files)))
