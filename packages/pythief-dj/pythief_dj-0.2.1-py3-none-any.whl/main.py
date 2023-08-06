import os
import sys

import click
from dotenv import load_dotenv
from context.py_thief_args import PyThiefArgs
from context.py_thief_context import PyThiefContext
from auth.auth_service import AuthService
from download.downloader import Downloader
from services.logger import Logger
from services.mp3ifier import Mp3ifier
from services.storage import Storage
from services.url_resolver_service import UrlResolverService

# load env
load_dotenv(os.path.join(os.getcwd(), './.secret/.env'))


@click.argument('videos', nargs=-1)
@click.option('-k', '--keep-raw', default=False, type=click.BOOL, help="Keep the raw MP4 files downloaded from YouTube that this tool converts to MP3 for use (false by default).")
@click.option('-f', '--format', default='mp3', help='The format into which you wish to convert the audio data from the video (mp3 by default).')
@click.option('-o', '--out-dir', default='pythief-dj-output', type=click.Path(file_okay=False, resolve_path=True), help="The directory into which you want to save the files downloaded")
@click.option('-t', '--txt', type=click.Path(exists=True, resolve_path=True), help="Path to a text file containing the videos to download. One per line.")
@click.command()
def cli(**kwargs):
    """Download audio for the videos specified in VIDEOS, in --txt, or both."""
    if len(sys.argv) < 2:
        _echo_command_help(cli)
        exit()

    args = PyThiefArgs.from_kwargs(kwargs)
    if not args.is_valid:
        click.echo('Invalid args. Want some help?')
        _echo_command_help(cli)
        exit(1)

    # services
    # auth_service = AuthService()
    # auth_service.start()

    logger = Logger()
    downloader = Downloader(logger)
    storage = Storage.from_out_root(args.out_dir)
    context = PyThiefContext(args, storage)

    # resolve video URLs from args passed
    resolver = UrlResolverService()
    video_urls = resolver.resolve(context)

    # get mp4s
    downloaded = downloader.download(video_urls, context)

    # convert to the desired format
    Mp3ifier().mp3ify(downloaded, args)

    # clean up raws if directed
    if not args.keep_raw:
        context.storage.delete_raw()

    logger.log(f'All done! Downloaded {len(video_urls)} file{"" if len(video_urls) == 1 else "s"}.')


def _echo_command_help(command: click.Command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


if __name__ == '__main__':
    cli()
