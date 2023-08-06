"""
MIT License

Copyright (c) 2021 FWANI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import click

from .coverage2img import coverage_to_img


@click.command()
@click.option("--input-file", "-i", type=str, required=False, default='coverage.json', show_default=True,
              help="The input path of coverage.json file that is made by coverage of python")
@click.option("--output-file", "-o", type=str, required=False, default='coverage.png', show_default=True,
              help="The output path")
def main(input_file, output_file):
    """coverage2img command line interface

    Usage:
        coverage2img -i coverage.json -o coverage.png
    """
    coverage_to_img(input_path=input_file, output_path=output_file)


if __name__ == "__main__":
    main()
