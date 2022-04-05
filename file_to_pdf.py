#!/usr/bin/env python
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from pathlib import Path
import os, subprocess, tempfile,sys
import argparse


def run_shell_cmd(cmd):
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            print("Error %s" % stderr.decode())
            return None
        return stdout.decode("utf-8")

def get_files(dir,filter):
    result = []
    dir_len = 0
    if dir != '.' and dir != './':
        dir_len = len(dir)

    for maindir, subdir, files in os.walk(dir):
        for filename in files:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext in filter:
                apath = apath[dir_len:]
                result.append(apath)

    return result

def file_to_html(files,html_dir):
    cmd = "highlight -I -l --out-format=html --inline-css  --syntax  cpp --style molokai"
    html_files = []
    for file in files:
        if file[0] == '.' and file[1] == '/':
            file = file[2:]
            print(file)
        dir = os.path.dirname(file)
        if dir != '' and dir != '.':
            dir = os.path.join(html_dir, dir)
            if not os.path.exists(dir):
                os.makedirs(dir)

        dst_file = file + ".html"
        html_files.append(dst_file)
        run_cmd = cmd + " " + file + " > " + html_dir + "/" + dst_file
        print(run_cmd)
        out = run_shell_cmd(run_cmd)
    return html_files

def html_to_pdf(html_files,html_dir,pdf_dir):
    pdf_files = []
    for file in html_files:

        dst_file = os.path.splitext(file)[0] + ".pdf"

        dst_path = pdf_dir + "/" + os.path.dirname(file)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        cmd = "wkhtmltopdf " + html_dir + "/" + file + " " + pdf_dir + "/" + dst_file
        print(cmd)
        run_shell_cmd(cmd)
        pdf_files.append(dst_file)

    return pdf_files


def merge_pdf(files,pdf_dir,output_file):
    merger = PdfFileMerger()
    page_count = 0
    for file in files:
        mark_name = os.path.splitext(file)[0]
        filename = pdf_dir + "/" + file
        input = PdfFileReader(open(filename, 'rb'))
        merger.append(input)
        merger.addBookmark(mark_name, page_count)
        print(filename + " " + str(page_count) + " " + mark_name)
        page_count += input.getNumPages()
    merger.write(output_file)
    merger.close()


parser = argparse.ArgumentParser(description='Convert files to pdf')
parser.add_argument('-i', dest='i', type=str, help='input directory')
parser.add_argument('-o', dest='o', type=str, help='output file')

args = parser.parse_args()

if __name__ == '__main__':

    input_dir = str(args.i);
    output_file = str(args.o);

    file_filter = [".S",".c",".cpp",".h",".hpp"]

    html_dir = tempfile.mkdtemp()

    pdf_dir = tempfile.mkdtemp()

    files = get_files(input_dir,file_filter)

    html_files = file_to_html(files, html_dir)

    pdf_files = html_to_pdf(html_files, html_dir, pdf_dir)

    pdf_files.sort()

    merge_pdf(pdf_files,pdf_dir,output_file)

    os.unlink(html_dir)
    os.unlink(pdf_dir)
    os.unlink(output_file)

