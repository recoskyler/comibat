import click

__version__ = '0.1.0'

def compress_to_cbz(extracted_path, output_path, overwrite):
    from zipfile import ZipFile, ZIP_DEFLATED
    import os

    print(f'Compressing {extracted_path} to CBZ...')

    name = get_file_name(extracted_path) if overwrite else get_file_name(extracted_path) + ' (FIXED)'
    zip_name = os.path.join(output_path, name + '.cbz')

    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zip_ref:
        for folder_name, subfolders, filenames in os.walk(extracted_path):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_ref.write(file_path, arcname=filename)

                print(f'Added {file_path} to {zip_name}')

    zip_ref.close()

    print(f'Done compressing {extracted_path} to CBZ')


def get_file_name(file):
    return file.stem


def check_for_meta(extracted_path):
    from pathlib import Path

    print(f'Checking for ComicInfo.xml in {extracted_path}...')

    for path in Path(extracted_path).rglob('ComicInfo.xml'):
        if path.is_file():
            print(f'Found ComicInfo.xml in {extracted_path}')
            return True

    print(f'No ComicInfo.xml found in {extracted_path}')

    return False


def check_for_title_page(extracted_path):
    from xml.dom.minidom import parseString
    from os.path import join

    comic_info_path = join(extracted_path, 'ComicInfo.xml')

    print(f'Checking for title page in {comic_info_path}...')

    with open(comic_info_path, 'r') as file:
        xml = file.read()

    dom = parseString(xml)

    for node in dom.getElementsByTagName('Page'):
        if node.getAttribute('Type') == 'FrontCover':
            print(f'Found title page in {comic_info_path}')
            return True

    print(f'No title page found in {comic_info_path}')

    return False


def set_title_page(extracted_path, image_files):
    from xml.dom.minidom import parseString
    from os.path import join

    comic_info_path = join(extracted_path, 'ComicInfo.xml')

    print(f'Setting title page in {comic_info_path}...')

    with open(comic_info_path, 'r') as file:
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

    with open(comic_info_path, 'w') as file:
        file.write(dom.toxml())

    print(f'Saved updated {comic_info_path}')


def get_image_files(extracted_path):
    from pathlib import Path

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
    import shutil

    print(f'Deleting {extracted_path}...')

    shutil.rmtree(extracted_path)

    print(f'Done deleting {extracted_path}')


def extract_cbz(file):
    from tempfile import gettempdir
    from zipfile import ZipFile
    from pathlib import Path
    import os

    print(f'Extracting {file}...')

    name = get_file_name(file)
    temp_dir = Path(gettempdir())
    extracted_path = os.path.join(temp_dir, name)

    zip = ZipFile(file)
    zip.extractall(path=extracted_path)

    return extracted_path


def get_cbz_files(directory):
    from pathlib import Path

    print('Getting CBZ files...')

    files = []

    for path in Path(directory).rglob('*.cbz'):
        files.append(path)

    return files


def process_file(file, overwrite):
    print(f'\nProcessing {file}...')

    extracted_path = extract_cbz(file)

    if not check_for_meta(extracted_path):
        print(f'No ComicInfo.xml found in {extracted_path}. Skipping...')
        return

    image_files = get_image_files(extracted_path)

    if not check_for_title_page(extracted_path):
        print(f'No title page found in {extracted_path}. Setting one...')
        set_title_page(extracted_path, image_files)

    compress_to_cbz(extracted_path, file, overwrite)
    delete_extracted_path(extracted_path)

    print(f'Done processing {file}')


@click.command()
@click.option('--overwrite', is_flag=True, default=False, help='Overwrite existing files', show_default=True)
@click.option('--to-epub', is_flag=True, default=False, help='Convert to EPUB', show_default=True)
@click.option('--version', is_flag=True, default=False, help='Show version', show_default=True)
@click.option('--delete-cbz', is_flag=True, default=False, help='Delete CBZ files after conversion', show_default=True)
@click.argument('files', type=click.Path(exists=True), nargs=-1)
def main(files, overwrite, to_epub, version, delete_cbz):
    from os import getcwd, remove

    print(f'ComiBat v{__version__}')
    print('by recoskyler - 2024')
    print('--------------------')

    if version:
        return

    directory = getcwd()

    if len(files) == 0:
        files = get_cbz_files(directory)

    print(f'\nFound {len(files)} files:\n')

    for file in files:
        process_file(file, overwrite)

        if delete_cbz and to_epub:
            remove(file)
        elif delete_cbz:
            print('Cannot delete CBZ files if not converting to EPUB')

    print('Done!')
