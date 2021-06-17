from . import markdown2jupyter, create_executor
import click
import logging
import subprocess

@click.command()
@click.argument('markdown_file')
@click.option('--output', '-o', default=None, help='jupyter file name')
@click.option('--execution-path', default=None, help='sets the notebook execution path')
@click.option('--execution-timeout', default=600, help='The time to wait (in seconds) for output from executions.\nIf a cell execution takes longer, an exception (TimeoutError\n on python 3+, RuntimeError on python 2) is raised.')
@click.option('--html', is_flag=True, help='convert to html format')
@click.option('--slides', is_flag=True, help='convert to slides format')
def cli(markdown_file, output, execution_path, execution_timeout, html, slides):
    FORMAT = "%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d: %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    if output is None:
        output = '.'.join(markdown_file.split('.')[:-1]) + '.ipynb'
    if execution_path is not None:
        logging.info('Using exucutor on path "{}", with timeout {}'.format(execution_path, execution_timeout))
        executor = create_executor(execution_path, execution_timeout)
    else:
        executor = None
    logging.info('Writing jupyter notebook to {}'.format(output))
    markdown2jupyter(markdown_file, output, preprocessor=executor)
    if html:
        subprocess.call("jupyter nbconvert --to html {}".format(output).split())
    if html:
        subprocess.call("jupyter nbconvert --to slides {}".format(output).split())


if __name__ == '__main__':
    cli()
