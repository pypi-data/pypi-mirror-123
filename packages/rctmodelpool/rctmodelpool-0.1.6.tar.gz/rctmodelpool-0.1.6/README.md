# rct-modelpool

## Installation
You can git install `rctmodelpool` via `pip`:

```bash
pip install git+https://github.com/rct-ai/rct-modelpool
```
or
```bash
pip install rctmodelpool
```

## Usage
You can import the *rctmodelpool.modelpool* from the package like so:

### `sync_model`
```python
from rctmodelpool import modelpool

path = modelpool.sync_model("rcthub://CPM.csv")
print(path)

```

### sync tgz
```python
import os
import tarfile
from rctmodelpool import modelpool
from pathlib import Path

local_path = modelpool.sync_model("rcthub://"+config.bert_model_path)
parent_path = Path(local_path).parent
print("rcthub sync:",local_path)
modeltar = tarfile.open(local_path)
inside_folder = os.path.commonprefix(modeltar.getnames())
real_model_path = os.path.join(parent_path, inside_folder)
print('model folder:', real_model_path)
if not os.path.exists(real_model_path):
    modeltar.extractall(parent_path)
    print('tar extraction:', parent_path, local_path)

```