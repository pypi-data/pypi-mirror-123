# python-griddingmachine

## Note
1. Compile and and upload it to TestPyPI before unloaded it to PyPI:
```shell
$ python setup.py sdist
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

2. Download the testing package:
```shell
$ pip install -i https://test.pypi.org/simple/ python-griddingmachine
```

3. Test the package
```python
from griddingmachine import *
udpate_GM()
query_collection("VCMAX_2X_1Y_V1")
request_LUT("VCMAX_2X_1Y_V1", 33, 115)
request_LUT("VCMAX_2X_1Y_V1", 33, 115, interpolation=True)
```

4. Upload the package to PyPI (not TestPyPI)
```shell
```
