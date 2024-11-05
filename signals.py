import scripts.data_pull as dp
from datetime import date
from dateutil.relativedelta import relativedelta
from pathlib import Path

project_root = Path(__file__).resolve().parent 
data_folder = project_root / "data" / "raw"

start_date = (date.today() - relativedelta(days=59)).strftime("%Y-%m-%d")
end_date = date.today().strftime("%Y-%m-%d")
dp.load_data(data_folder,start_date,end_date,"1h")

import models.MA
import models.MACD
import models.momemtum
import models.OBV
import models.signal_gen
import scripts.backtest
import scripts.trades
import scripts.position_sizing