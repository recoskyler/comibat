"""
This module provides functionality to parse XML, handle file paths,
compress files into CBZ format, and manage temporary files and directories.
It is used by the main module to perform the actual processing.
It adds a title page to CBZ files if it doesn't already exist.
"""

from xml.dom.minidom import parseString
from os.path import join
from os import getcwd, walk
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
from tempfile import gettempdir
from shutil import rmtree
import click

__version__ = '0.1.3'

def get_last_folder_name(extracted_path):
    """
    Gets the last folder name of a directory path.

    @param extracted_path: The directory path.
    @return: The last folder name.
    """

    # Split the path into a list of folder names
    folder_names = str(extracted_path).split(sep='/')

    return folder_names[-1]


def get_folder_name(extracted_path):
    """
    Gets the folder name of a directory path.

    @param extracted_path: The directory path.
    @return: The folder name.
    """

    # Split the path into a list of folder names
    folder_names = str(extracted_path).split(sep='/')

    folder_names.pop(-1)

    folder_name = '/'.join(folder_names)

    if str(extracted_path)[0] == '/':
        folder_name = '/' + folder_name

    return folder_name


def compress_to_cbz(extracted_path, output_path, overwrite):
    """
    Compresses a directory to a CBZ file.

    @param extracted_path: The path to the extracted directory.
    @param output_path: The output directory.
    @param overwrite: Whether to overwrite existing files.
    """

    print(f'Compressing {extracted_path} to CBZ...')

    name = get_last_folder_name(extracted_path)

    if not overwrite:
        name += ' (FIXED)'

    zip_name = join(output_path, name + '.cbz')

    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zip_ref:
        for folder_name, _sub_folders, filenames in walk(extracted_path):
            for filename in filenames:
                file_path = join(folder_name, filename)
                zip_ref.write(file_path, arcname=filename)

                print(f'Added {file_path} to {zip_name}')

    zip_ref.close()

    print(f'Done compressing {extracted_path} to CBZ')


def get_file_name(file):
    """
    Gets the file name of a file path. Uses the last dot as the separator.

    @param file: The file path.
    @return: The file name.
    """

    folder_names = str(file).split(sep='/')

    file_name_parts = folder_names[-1].split(sep='.')
    file_name_parts.pop(-1)

    file_name = '.'.join(file_name_parts)

    return file_name



def check_for_meta(extracted_path):
    """
    Checks if the ComicInfo.xml file exists in the specified directory.

    @param extracted_path: The path to the extracted directory.
    @return: True if the ComicInfo.xml file exists, False otherwise.
    """

    print(f'Checking for ComicInfo.xml in {extracted_path}...')

    for path in Path(extracted_path).rglob('ComicInfo.xml'):
        if path.is_file():
            print(f'Found ComicInfo.xml in {extracted_path}')
            return True

    print(f'No ComicInfo.xml found in {extracted_path}')

    return False


def check_for_title_page(extracted_path):
    """
    Checks if the ComicInfo.xml file contains a title page.

    @param extracted_path: The path to the extracted directory.
    @return: True if the ComicInfo.xml file contains a title page, False otherwise.
    """

    comic_info_path = join(extracted_path, 'ComicInfo.xml')

    print(f'Checking for title page in {comic_info_path}...')

    with open(comic_info_path, 'r', encoding='utf-8') as file:
        xml = file.read()

    dom = parseString(xml)

    for node in dom.getElementsByTagName('Page'):
        if node.getAttribute('Type') == 'FrontCover':
            print(f'Found title page in {comic_info_path}')
            return True

    print(f'No title page found in {comic_info_path}')

    return False


def set_title_page(extracted_path, image_files):
    """
    Sets the title page in the ComicInfo.xml file.

    @param extracted_path: The path to the extracted directory.
    @param image_files: A list of image file paths.
    """

    comic_info_path = join(extracted_path, 'ComicInfo.xml')

    print(f'Setting title page in {comic_info_path}...')

    with open(comic_info_path, 'r', encoding='utf-8') as file:
        xml = file.read()

    dom = parseString(xml)

    # Check if DOM contains a Pages node

    if dom.getElementsByTagName('Pages'):
        page_elements = dom.getElementsByTagName('Page')

        # Sort page elements by Image attribute, ascending

        page_elements.sort(key=lambda x: int(x.getAttribute('Image')))

        # Set the first image element as the title page

        page_elements[0].setAttribute('Type', 'FrontCover')

        print(f'Title page set in {comic_info_path}')
    else:
        print(f'No Pages node found in {comic_info_path}')

        # Add a Pages node inside the ComicInfo node

        comic_info = dom.getElementsByTagName('ComicInfo')[0]

        pages = dom.createElement('Pages')

        is_first = True

        # Add a Page node for each image file
        for image_file in image_files:
            image_name = get_file_name(image_file).lstrip('0')

            page = dom.createElement('Page')
            page.setAttribute('Image', image_name)

            if is_first:
                page.setAttribute('Type', 'FrontCover')
                is_first = False

                print(f'Title page set in {comic_info_path}')

            pages.appendChild(page)

            print(f'Page {image_name} added to {comic_info_path}')

        comic_info.appendChild(pages)

    # Write the modified XML to a file

    with open(comic_info_path, 'w', encoding='utf-8') as file:
        file.write(dom.toxml())

    print(f'Saved updated {comic_info_path}')


def get_image_files(extracted_path):
    """
    Gets a list of image files in the specified directory.
    It supports JPG, PNG, GIF, BMP, JPEG, and TIFF formats.

    @param extracted_path: The path to the extracted directory.
    @return: A list of image file paths.
    """

    print(f'Getting image files in {extracted_path}...')

    files = []
    extensions = ['*.jpg', '*.png', '*.gif', '*.bmp', '*.jpeg', '*.tiff']

    for extension in extensions:
        for path in Path(extracted_path).rglob(extension):
            if path.is_file():
                files.append(path)

    # Sort files by name, ascending
    files.sort(key=lambda x: x.name)

    print(f'Found {len(files)} image files in {extracted_path}')

    return files


def delete_extracted_path(extracted_path):
    """
    Deletes the extracted directory.

    @param extracted_path: The path to the extracted directory.
    """

    print(f'Deleting {extracted_path}...')

    rmtree(extracted_path)

    print(f'Done deleting {extracted_path}')


def extract_cbz(file):
    """
    Extracts a CBZ file to a temporary directory.

    @param file: The path to the CBZ file.
    @return: The path to the extracted directory.
    """

    print(f'Extracting {file}...')

    name = get_file_name(file)
    temp_dir = Path(gettempdir())
    extracted_path = join(temp_dir, name)

    zip_file = ZipFile(file)
    zip_file.extractall(path=extracted_path)

    return Path(extracted_path)


def get_cbz_files(directory, recursive, pattern='*.cbz'):
    """
    Gets a list of CBZ files in the specified directory.

    @param directory: The directory to search in.
    @param recursive: Whether to search recursively.
    @param pattern: The pattern to match. Default is '*.cbz'.
    @return: A list of CBZ file paths.
    """

    print('Getting CBZ files...')

    files = []

    if pattern == '':
        pattern = '*.cbz'

    if recursive:
        for path in Path(directory).rglob(pattern):
            files.append(path)
    else:
        for path in Path(directory).glob(pattern):
            files.append(path)

    return files


def process_file(file, overwrite, output_path):
    """
    Processes a single CBZ file.

    @param file: The path to the CBZ file.
    @param overwrite: Whether to overwrite existing files.
    @param output_path: The output directory.
    """

    print(f'\nProcessing {file}...')

    extracted_path = extract_cbz(file)

    if not check_for_meta(extracted_path):
        print(f'No ComicInfo.xml found in {extracted_path}. Skipping...')
        return

    image_files = get_image_files(extracted_path)

    if output_path == '':
        output_path = get_folder_name(extracted_path)

    if not check_for_title_page(extracted_path):
        print(f'No title page found in {extracted_path}. Setting one...')
        set_title_page(extracted_path, image_files)

    compress_to_cbz(extracted_path, output_path, overwrite)
    delete_extracted_path(extracted_path)

    print(f'Done processing {file}')


@click.command(help='A tool to add a title page to CBZ comic book archives. If no files are specified, ComiBat will look for CBZ files in the current directory if no files are specified.')
@click.option('--overwrite', is_flag=True, default=False, help='Overwrite existing files', show_default=True)
@click.option('--version', is_flag=True, default=False, help='Show version', show_default=True)
@click.option('-o', '--output-path', type=click.Path(exists=True), default=getcwd(), help='Output directory', show_default=True)
@click.option('-r', '--recursive', is_flag=True, default=False, help='Recursively search for CBZ files', show_default=True)
@click.argument('files', type=click.Path(exists=True, dir_okay=False), nargs=-1)
def cli(files, overwrite, version, output_path, recursive):
    """
    The main function of the program.

    @param files: A list of file paths to process.
    @param overwrite: Whether to overwrite existing files.
    @param version: Whether to show the version.
    @param output_path: The output directory.
    @param recursive: Whether to search for CBZ files recursively.
    """

    print(f'ComiBat v{__version__}')
    print('by recoskyler - 2024')
    print('--------------------')

    if version:
        return

    directory = getcwd()

    if len(files) == 0:
        files = get_cbz_files(directory, recursive)
    elif recursive and len(files) > 0 and '*' not in files[0]:
        print('Cannot use --recursive with specific files')
        return
    elif len(files) == 1 and '*' in files[0]:
        files = get_cbz_files(directory, recursive, files[0])

    print(f'\nFound {len(files)} files:\n')

    for file in files:
        process_file(file, overwrite, output_path)

    print('Done!')
