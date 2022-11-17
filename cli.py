import logging
import os

import click as click

from src.npd_parsing import read_test_csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


@click.command()
@click.argument('filename', nargs=1)
def cli(filename):
    if os.environ['COMPUTERNAME'] == 'UNIWINPW01532G':
        path = r'C:\Users\Likhitha.Katta\OneDrive - Unilever\Documents\NPD INPUT FILES'
    elif os.environ['COMPUTERNAME'] == 'UNIWINJQR0WZ2':
        path = 'c:\\1'
    if os.environ['COMPUTERNAME'] == 'DESKTOP-HHS1FHQ':
        path = r'C:\Users\likhitha katta\Documents\UNILEVER PROJECTS'
    else:
        path = r'\\S2.ms.unilever.com\dfs\ES-GROUPS\cor\frd\UFO-General\INTERFACE\S1P'

    logging.info(f'using path: {path}')
    logging.info(f'parsing file: {filename}')

    read_test_csv(path=path, filename=filename)


if __name__ == "__main__":
    filename='UFO_NPD_BOT_ROUTING.20220510062351.340619.00CBM6tN.S1P.csv'
    
    cli(filename)