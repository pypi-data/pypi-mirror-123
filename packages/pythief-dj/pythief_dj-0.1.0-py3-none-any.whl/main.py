from genericpath import exists
import os
import click
from dotenv import load_dotenv
from args.parsed_args import ParsedArgs
from auth.auth_service import AuthService
from download.downloader import Downloader
from services.logger import Logger
from services.mp3ifier import Mp3ifier
from services.url_resolver_service import UrlResolverService

# load env
load_dotenv(os.path.join(os.getcwd(), './.secret/.env'))


@click.option('-k', '--keep-raw', default=False, type=click.BOOL, help="Keep the raw MP4 files downloaded from YouTube that this tool converts to MP3 for use (false by default).")
@click.option('-f', '--format', default='mp3', help='The format into which you wish to convert the audio data from the video (mp3 by default).')
@click.option('-o', '--out-dir', default='output', help="The directory into which you want to save the files downloaded")
@click.option('-t', '--txt', type=click.Path(exists=True), help="Path to a text file containing the videos to download. One per line.")
@click.option('-v', '--video', help="The IDs or URLs of the video(s) you want to download. One of --videos, --txt, or --csv is required.", multiple=True)
@click.command()
def cli(**kwargs):
    # services
    # auth_service = AuthService()
    # auth_service.start()

    args = ParsedArgs.from_kwargs(kwargs)

    if not args.is_valid:
        print('Invalid args.')
        exit(1)

    logger = Logger()
    downloader = Downloader(logger)

    # resolve video URLs from args passed
    resolver = UrlResolverService()
    video_urls = resolver.resolve(args)

    # get mp4s
    downloaded = downloader.download(video_urls, args.out_dir)

    # convert to the desired format
    Mp3ifier().mp3ify(downloaded, args)

    logger.log(f'All done! Downloaded {len(video_urls)} files{"" if len(video_urls) == 1 else "s"}.')


if __name__ == '__main__':
    cli()
