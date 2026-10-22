import subprocess
from dbcm import UseDatabase


dbconfig = {
    'host': '127.0.0.1',
    'database': 'UTM5',
    'user': 'tempuser',
    'password': 'temppass'
}

actual_date_start = '2022-01-01 00:00'
actual_date_end = '2022-02-01 00:00'

dbquery = f'''
    SELECT account_id FROM UTM5.payment_transactions
    WHERE actual_date >= UNIX_TIMESTAMP('{actual_date_start}')
    AND actual_date < UNIX_TIMESTAMP('{actual_date_end}')
'''

tool = '/netup/utm5/bin/utm5_payment_tool'
config = '/netup/utm5/utm5_payment_tool.cfg'
sum = 150
method = 100
comment = 'corrective payment'

shell_command = '''{} -C {} -b {} -m {} -L '{}' -k '{}' -i'''.format(
    tool, config, sum, method, comment, comment
)


if __name__ == '__main__':
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(dbquery)
        rows = cursor.fetchall()
        for row in rows:
            command = shell_command + f''' -a {row['account_id']}'''
            print(command)
            subprocess.run(command, shell=True)
