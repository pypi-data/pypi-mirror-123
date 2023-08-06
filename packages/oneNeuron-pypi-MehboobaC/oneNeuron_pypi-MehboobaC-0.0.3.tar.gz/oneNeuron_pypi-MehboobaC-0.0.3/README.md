# oneNeuron_pypi
Packaging simple perceptron python project

## How to use this
```python
from oneNeuron.perceptron import Perceptron

# get X and y then use below commands
model = Perceptron(eta=eta, epocha=epochs)
model.fit(X,y)
```

# References
[Official python projects packaging](https://packaging.python.org/tutorials/packaging-projects/)

[Githhub docs for github actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries)