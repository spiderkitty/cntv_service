import datetime

import click
import papermill as pm


@click.command()
@click.option("--start_date", help="begin date.")
@click.option("--end_date", help="end date.")
@click.option("--year", help="year.", type=click.INT)
@click.option("--month", help="month.", type=click.INT)
@click.option("--program", help="program", type=click.INT)
def get_urls(start_date, end_date, year, month, program):
    if not start_date:
        start_date = datetime.date(year, month, day=1).strftime("%Y%m%d")
    if not end_date:
        if month + 1 > 12:
            year = year + 1
            month = 12
        else:
            month = month + 1
        end_date = datetime.date(year, month, day=1) - datetime.timedelta(days=1)
        end_date = end_date.strftime("%Y%m%d")

    program_map = {
        1: 'TOPC1451557646802924',  # 健康之路
        2: 'TOPC1451546588784893',  # 生活圈
    }

    pm.execute_notebook(
        './cntv_program_month_data.ipynb',
        './output.ipynb',
        parameters={
            'year': year,
            'month': month,
            'start_date': start_date,
            'end_date': end_date,
            'program': program_map[program],
        }
    )
    nb = pm.read_notebook('output.ipynb')
    click.echo('\n'.join(nb.data['dn_list']))


if __name__ == '__main__':
    get_urls()
