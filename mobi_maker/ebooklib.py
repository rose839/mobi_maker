import os
import io
import pathlib
import tempfile
import time

def format_file_name(path: str) -> str:
    """
    strip illegal characters
    """
    return path.replace('/', '').replace(' ', ''). \
        replace('+', '-').replace('"', '').replace('\\', ''). \
        replace(':', '-').replace('|', '-')

class Ebook:
    def __init__(self, title: str, author=None):
        self.title = title
        self.author = author
        self.cover_path = None
        self.cover_content = None
        self.chapter_list = list()
        self._tempdir = pathlib.Path(tempfile.gettempdir()) / str(time.time())
        self._tempdir.mkdir()

    @property
    def dest_file_path(self) -> pathlib.Path:
        return pathlib.Path('{}.mobi'.format(format_file_name(self.title)))

    @property
    def tmpdir(self) -> pathlib.Path:
        return self._tempdir

    @property
    def full_dest_file_path(self) -> pathlib.Path:
        return self.tempdir / self.dest_file_path

    def set_cover(self, cover_path: str = None, cover_content: bytes = None) -> 'Ebook':
        if cover_path:
            self.cover_path = cover_path
            self.cover_content = None
            return
        if cover_content:
            self.cover_content = cover_content
            self.cover_path = None
            return
        return ValueError('cover image path and content both are empty.')



def _parse_headers(toc_file_name):
    """
    parse headers from toc.md
    :param toc_file_name:
    :return:
    """
    if not os.path.isfile(toc_file_name):
        raise ValueError("'toc.md file not exists:{}'.format(toc_file_name)")

    headers_info = []
    with io.open(toc_file_name) as fobj:
        headers = fobj.readlines()
        if not headers:
            raise ValueError("invalid toc md file: file is empty")

        # first not empty line is title
        title_line = 0
        while not headers[title_line].strip() and title_line < len(headers):
            title_line += 1
        if title_line == len(headers):
            raise ValueError('invalid toc md file:  no title')
        title = headers[title_line].strip()

        # parse headers
        for h in headers[title_line+1:]:
            if h.startswith('# '):
                headers_info.append({
                    'title': h[2:].strip(),
                    'next_headers': []
                })
            elif h.startswith('## '):
                if len(headers_info) == 0:
                    raise ValueError("invalid toc md file: format not correct")

                # only suport 2 level toc
                headers_info[-1]['next_headers'].append({
                    'title': h[3:].strip(),
                })
        if not headers_info:
            raise ValueError("invalid toc md file: no headers")

        return title, headers_info


def make_ebook(source_dir, output_dir):
    """
    make ebook with the files in source_dir and put the ebook made in output_dir
    :param source_dir: html+toc.md directory
    :param output_dir:
    :return: destination filename of the mobi file
    """
    # parse toc.md file
    toc_file_name = os.path.join(source_dir, "toc.md")
    title, headers = _parse_headers(toc_file_name)



if __name__ == '__main__':
    print(_parse_headers('../example/toc.md'))