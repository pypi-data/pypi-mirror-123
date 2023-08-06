from mangas_origines.exceptions.exceptions import ScanNotFound, MangasOriginesNotAvailable
from mangas_origines.script.progress_bar import ProgressBar
from mangas_origines.mangas_origines import MangasOrigines
from mangas_origines.script import arguments_builder
from mangas_origines.script.spinner import Spinner
from mangas_origines.script import cursor
from mangas_origines import utils
import urllib.parse
import setproctitle
import aiofiles
import asyncio
import aiohttp
import json
import os


class Update:
    def __init__(self):
        self.images_url_len = 0
        self.images_downloaded = 0
        self.to_download = []
        self.scan = None

    async def generate_json(self, spinner: Spinner, path: str):
        spinner.set_text('Generate JSON...')
        await spinner.start()

        json_content = {
            'scan_id': self.scan.scan_id, 'name_id': self.scan.name_id, 'url': self.scan.url,
            'genres': self.scan.genres, 'types': self.scan.types, 'title': self.scan.title,
            'year_of_release': self.scan.year_of_release, 'image_url': self.scan.image_url,
            'author_name': self.scan.author_name, 'author_url': self.scan.author_url,
            'artist_name': self.scan.artist_name, 'artist_url': self.scan.artist_url,
            'notes': self.scan.notes, 'ratting_count': self.scan.ratting_count,
            'has_seasons': self.scan.has_seasons
        }

        async with aiofiles.open(path + 'infos.json', 'wb') as f:
            await f.write(json.dumps(json_content, indent=4, ensure_ascii=False).encode('utf-8'))

        async with aiohttp.ClientSession(headers=self.scan.headers) as client_session:
            async with client_session.get(urllib.parse.quote(self.scan.image_url, safe='://')) as r:
                async with aiofiles.open(path + 'icon.png', 'wb') as f:
                    async for data in r.content.iter_chunked(1024):
                        await f.write(data)
        await spinner.stop()

    async def download(self, element: list, progress_bar: ProgressBar):
        file_name = os.path.basename(element[0])

        utils.create_folder(element[2])
        if os.path.isfile(element[1] + file_name) is False:
            async with aiohttp.ClientSession(headers=self.scan.headers) as client_session:
                try:
                    async with client_session.get(urllib.parse.quote(element[0], safe='://'), timeout=800) as r:
                        async with aiofiles.open(element[2] + file_name, 'wb') as f:
                            try:
                                async for data in r.content.iter_chunked(1024):
                                    await f.write(data)
                            except aiohttp.ClientPayloadError:
                                return utils.print_error(f'Incorrect link: {element[0]}')
                except asyncio.TimeoutError:
                    return utils.print_error(f'Timeout: {element[0]}')
            utils.create_folder(element[1])
            os.rename(element[2] + file_name, element[1] + file_name)
        self.images_downloaded += 1

        progress_bar.progress(self.images_downloaded)

        self.to_download.remove(element)

    async def get_scan_pictures(self, spinner: Spinner, scan: str, path: str, temp_path: str, force_check: bool) -> bool:
        cursor.hide()

        try:
            if 'mangas-origines.fr' in scan:
                self.scan = await MangasOrigines().get_scan_by_url(scan)
            else:
                self.scan = await MangasOrigines().get_scan_by_name_id(scan)
        except ScanNotFound:
            await spinner.stop()
            cursor.show()
            return utils.print_error(f"I can't found scan: {scan}!")
        except MangasOriginesNotAvailable as e:
            await spinner.stop()
            cursor.show()
            return utils.print_error(f'Mangas Origines is not available, error: {e.error_code}!')

        has_downloaded = False

        for x in self.scan.chapters_url:
            chapter = self.scan.get_chapter_name(x)

            if self.scan.has_seasons:
                season = self.scan.get_chapter_season(x)
                gen_path = path + season + os.sep + chapter + os.sep
                gen_temp_path = temp_path + season + os.sep + chapter + os.sep
            else:
                chapter = self.scan.get_chapter_name(x)
                gen_path = path + chapter + os.sep
                gen_temp_path = temp_path + chapter + os.sep

            if os.path.exists(gen_path) is False or force_check:
                has_downloaded = True
                get_chapter = await self.scan.get_chapter_by_url(x)
                for x1 in get_chapter.images_url:
                    self.to_download.append([x1, gen_path, gen_temp_path])
                self.images_url_len += len(get_chapter.images_url)

        return has_downloaded

    async def update(self, command_return: dict):
        cursor.hide()

        arguments = command_return['args']
        arg_index = arguments.index('-S')
        force_check = '--check' in arguments
        generate_json = '--generate-json' in arguments

        if len(arguments) >= arg_index + 2:
            if len(arguments) >= arg_index + 4:
                spinner = Spinner(text='Loading')
                await spinner.start()

                path_to_clean = arguments[arguments.index('-P') + 1]
                path = path_to_clean if path_to_clean[-1] == os.sep else path_to_clean + os.sep
                temp_path = path + 'temp' + os.sep

                if os.access(os.path.dirname(path), os.W_OK) is False:
                    await spinner.stop()
                    cursor.show()
                    return utils.print_error("I can't use this folder (bad permission, or incorrect path).")
                utils.create_folder(path)

                await self.get_scan_pictures(spinner, arguments[arg_index + 1], path, temp_path, force_check)
                await spinner.stop()

                if generate_json:
                    await self.generate_json(spinner, path)

                if not self.to_download:
                    utils.delete_folder(temp_path)
                    cursor.show()
                    return print('Nothing to download.')

                progress_bar = ProgressBar(self.images_url_len, 'Download all images')

                while self.to_download:
                    await utils.limit_tasks(15, *[self.download(element, progress_bar) for element in self.to_download])

                utils.delete_folder(temp_path)
                utils.clear_line()

                print('\r\033[1mDownload complete!\033[0m')
                cursor.show()
            else:
                utils.print_error('You must enter download path (with -P option).')
                return cursor.show()
        else:
            utils.print_error('You must enter scan url/name.')
            return cursor.show()

    async def update_all_scans(self, command_return: dict):
        cursor.hide()

        arguments = command_return['args']
        arg_index = arguments.index('-U')
        force_check = '--check' in arguments

        if len(arguments) >= arg_index + 2:
            spinner = Spinner(text='Loading')
            await spinner.start()

            path = arguments[arg_index + 1] if arguments[arg_index + 1][-1] == os.sep else arguments[arg_index + 1] + os.sep

            if os.access(os.path.dirname(path), os.W_OK) is False:
                await spinner.stop()
                cursor.show()
                return utils.print_error("I can't use this folder (bad permission, or incorrect path).")

            total = len(os.listdir(path))
            downloaded = 0
            json_not_found = 0
            json_not_found_list = []

            for folder in os.listdir(path):
                path_gen = path + folder + os.sep
                path_temp_gen = path_gen + 'temp' + os.sep
                if os.path.exists(path_gen + 'infos.json'):
                    async with aiofiles.open(path_gen + 'infos.json', 'rb') as f:
                        text = await f.read()
                    text_parsed = json.loads(text)
                    if 'name_id' in text_parsed:
                        add_scan_pictures = await self.get_scan_pictures(spinner, text_parsed['name_id'], path_gen, path_temp_gen, force_check)
                        downloaded += 1 if add_scan_pictures else 0
                else:
                    json_not_found_list.append(path_gen)
                    json_not_found += 1

            await spinner.stop()

            if not self.to_download:
                return print('Nothing to download.')

            progress_bar = ProgressBar(self.images_url_len, 'Download all images')

            while self.to_download:
                await utils.limit_tasks(15, *[self.download(element, progress_bar) for element in self.to_download])

            for folder in os.listdir(path):
                utils.delete_folder(path + folder + os.sep + 'temp' + os.sep)

            utils.clear_line()

            print(
                f'\r\033[1mDownload complete ({downloaded}/{total} downloaded, {json_not_found} json not founded)!\033[0m'
            )
            cursor.show()
        else:
            utils.print_error('You must enter path to check.')
            return cursor.show()


async def get_infos(command_return: dict):
    cursor.hide()

    arguments = command_return['args']
    arg_index = arguments.index('-I')

    if arg_index + 2 == len(arguments):
        spinner = Spinner(text='Loading')
        await spinner.start()

        try:
            scan = await MangasOrigines().get_scan_by_name_id(arguments[arg_index + 1])
        except ScanNotFound:
            await spinner.stop()
            cursor.show()
            return utils.print_error(f"I can't found scan: {arguments[arg_index + 1]}!")
        except MangasOriginesNotAvailable as e:
            await spinner.stop()
            cursor.show()
            return utils.print_error(f'Mangas Origines is not available, error: {e.error_code}!')

        scan_infos_text = f"\n{scan.title}'s infos:\n"
        scan_infos_text += f"   ID: {scan.scan_id}\n"
        scan_infos_text += f"   Author: {'No information' if scan.year_of_release is None else scan.author_name} - {'No information' if scan.year_of_release is None else scan.author_url}\n"
        scan_infos_text += f"   Artiste: {'No information' if scan.year_of_release is None else scan.artist_name} - {'No information' if scan.year_of_release is None else scan.artist_url}\n"
        genres_list = ', '.join([x for x in scan.genres])
        scan_infos_text += f"   Genres: {genres_list}\n"
        scan_types = ', '.join([x for x in scan.types])
        scan_infos_text += f"   Types: {scan_types}\n"
        scan_infos_text += f"   Year of release: {'No information' if scan.year_of_release is None else scan.year_of_release}\n"
        scan_infos_text += f"   Chapters number: {len(scan.chapters_url)}\n"
        scan_infos_text += f"   Has season: {'Yes' if scan.has_seasons else 'No'}\n"
        scan_infos_text += f"   Notes: {scan.notes}\n"
        scan_infos_text += f"   Ratting count: {scan.ratting_count}\n"
        await spinner.stop()
        print(scan_infos_text)
        cursor.show()
    else:
        utils.print_error('You must enter scan url/name.')
        return cursor.show()


def get_version(command_return: dict):
    from mangas_origines import __version__, __license__

    version_text = f'\033[1mMangasOrigines {__version__}\033[0m\n'
    version_text += f'Created by \033[1mAsthowen\033[0m - \033[1mcontact@asthowen.fr\033[0m\n'
    version_text += f'License: \033[1m{__license__}\033[0m'

    print(version_text)


def start():
    setproctitle.setproctitle('MangasOrigines')
    parser = arguments_builder.ArgumentsBuilder('A script to make some things on mangas-origines.fr.')

    parser.add_argument(
        '-S', action=Update().update, description='Download scan.', command_usage='-S scan-id -P path [--check, --generate-json]'
    )
    parser.add_argument('-U', action=Update().update_all_scans, description='Update all scans in folder.', command_usage='-U path')
    parser.add_argument('-I', action=get_infos, description='Get scan infos.', command_usage='-I scan_id')
    parser.add_argument('-V', action=get_version, description='Get version infos.', command_usage='-V')

    try:
        parser.build()
    except aiohttp.ClientConnectionError:
        cursor.show()
        utils.clear_line()
        utils.print_error("I don't have access to Internet.")
    except KeyboardInterrupt:
        cursor.show()
        utils.clear_line()
        utils.print_error('Script stopped by user.')


if __name__ == '__main__':
    start()
