Following is the information on how the dataset csv files present in archive folder were archived.

### Olympic
```python
import pods

data = pods.datasets.olympic_marathon_men()
x = data['X']
y = data['Y']
```

### Motorcycle Helmet
```python
import pods

data = pods.datasets.mcycle()
x = data['X']
y = data['Y']
```

### Della Gatta Gene
```python
import pods

data = pods.datasets.della_gatta_TRP63_gene_expression(data_set='della_gatta',gene_number=937)

x = data['X']
y = data['Y']
```