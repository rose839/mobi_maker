import os
import io

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
                headers_info[-1]['next_headers'].append({  # only suport 2 level toc
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
    toc_file_name = os.path.join(source_dir, "toc.md")
    title, headers = _parse_headers(toc_file_name)

if __name__ == '__main__':
    print(_parse_headers('../example/toc.md'))