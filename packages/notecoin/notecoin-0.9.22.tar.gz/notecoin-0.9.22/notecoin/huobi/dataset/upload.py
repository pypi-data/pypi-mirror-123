from notedrive.lanzou import LanZouCloud
from notetool.log import logger
from notetool.tool.secret import read_secret

downer = LanZouCloud()
downer.ignore_limits()
downer.login_by_cookie()

logger.info('begin')
#print(downer.sync_directory(path_root='/root/workspace/tmp/coin', folder_id='3358325'))
downer.upload_file('/root/workspace/tmp/coin/dbs/huobi-SHIBUSDT.db', folder_id='3907901')
