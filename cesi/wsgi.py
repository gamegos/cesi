import os
from run import configure

app, _ = configure(os.environ["CESI_CONFIG_PATH"])
