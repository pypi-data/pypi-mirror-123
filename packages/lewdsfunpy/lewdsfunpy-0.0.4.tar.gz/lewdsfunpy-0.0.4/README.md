# LewdsFunPy
For Use with the Lewds image API!


## Installation
```bash
pip3 install lewdsfunpy
```

## API Keys:
```env
# .env
LEWDS_API_KEY=[REPLACE_WITH_YOUR_OWN_KEY]
```

## Example Usage:
```py
from lewdsfunpy import LewdsAPI
def test():
    """ Tests the Lewds API Endpoints """
resultz = LewdsAPI.nsfw("ass")
print("{name}".format(name=resultz))
```

### Join the  [Discord Server](https://discord.lewds.fun)