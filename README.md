# ⚠️ Deprecated
This repository is no longer maintained. Please use [Mikegraph]([]) instead.
# timearea
 Python Package for calculating a time area curve for a Mike Urban Database.

<b>To install:</b>

```
python -m pip install https://github.com/enielsen93/timearea/tarball/master
```

## Example:
```
import mikegraph
import timearea
graph = mikegraph.Graph(r"model.mdb")
graph.map_network()

rainseries = timearea.TimeArea(r"CDS T 5.txt")

rainseries.timeareaCurve("Node_1", graph)
