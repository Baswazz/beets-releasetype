from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from mediafile import MediaField, MP3DescStorageStyle, StorageStyle
import inquirer


class ReleaseTypePlugin(BeetsPlugin):
    def __init__(self):
        super(ReleaseTypePlugin, self).__init__()

        field = MediaField(
            MP3DescStorageStyle(u'releasetype'),
            StorageStyle(u'releasetype')
        )
        self.add_media_field('releasetype', field)
        self.register_listener('album_imported', self.album_imported)

    def commands(self):
        cmd = Subcommand(
            'releasetype', help='Assign release type')
        cmd.parser.add_option(
            '--album', '-a', help='Album name')
        cmd.func = self.release_type
        return [cmd]

    def album_imported(self, lib, album):
        release_type = self.determine_release_type(album)
        if release_type == 'album':
            release_type = self.determine_secondary_release_type(
                release_type, album) or release_type
        self.set_release_type(album, release_type)
        self._log.info('Release type set for album: %s (%s)' %
                       (album, release_type))

    def release_type(self, lib, opts, args):
        album = None
        album_name = None

        if opts.album:
            album_name = opts.album
            album_query = f'album:"{album_name}"'
            matching_albums = lib.albums(album_query)
            if matching_albums:
                album = matching_albums[0]
                release_type = self.determine_release_type(album)
                if release_type == 'album':
                    release_type = self.determine_secondary_release_type(
                        release_type, album) or release_type
                self.set_release_type(album, release_type)
                self._log.info('Release type set for album: %s (%s)' %
                               (album, release_type))
            else:
                print(f"No album found with name: {album_name}")
        else:
            for album in lib.albums():
                release_type = self.determine_release_type(album)
                if release_type == 'album':
                    release_type = self.determine_secondary_release_type(
                        release_type, album) or release_type
                self.set_release_type(album, release_type)
                self._log.info('Release type set for album: %s (%s)' %
                               (album, release_type))

    def determine_release_type(self, album):
        total_tracks = len(album.items())
        total_length = sum(item.length for item in album.items())
        longest_track_length = max(item.length for item in album.items())

        if (
            total_tracks <= 3 and
            total_length <= 1800 and
            all(item.length <= 600 for item in album.items())
        ):
            release_type = 'single'
        elif (
            (total_tracks >= 1 and total_tracks <= 3 and longest_track_length >= 600) or
            (total_tracks >= 4 and total_tracks <= 6 and total_length <= 1800)
        ):
            release_type = 'ep'
        elif (
            total_tracks >= 7 or
            (total_tracks >= 1 and total_tracks <= 6 and total_length > 1800)
        ):
            release_type = 'album'
        else:
            release_type = None

        return release_type

    def determine_secondary_release_type(self, release_type, album):
        questions = [
            inquirer.List(
                'secondary_release_type',
                message=f'Please select a secondary release type for album "{album.albumartist} - {album.album}"',
                choices=['', 'Compilation', 'Demo',
                         'DJ-mix', 'Live', 'Remix', 'Soundtrack']
            )
        ]
        answers = inquirer.prompt(questions)
        secondary_release_type = answers.get('secondary_release_type').lower()
        if secondary_release_type:
            return f'{release_type}; {secondary_release_type}'
        return None

    def set_release_type(self, album, release_type):
        for item in album.items():
            item['releasetype'] = release_type
            item.write()
