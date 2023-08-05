# EraLegis

[![Build Status](https://travis-ci.org/tiagocordeiro/eralegis.svg?branch=master)](https://travis-ci.org/tiagocordeiro/eralegis)
[![Updates](https://pyup.io/repos/github/tiagocordeiro/eralegis/shield.svg)](https://pyup.io/repos/github/tiagocordeiro/eralegis/)
[![Python 3](https://pyup.io/repos/github/tiagocordeiro/eralegis/python-3-shield.svg)](https://pyup.io/repos/github/tiagocordeiro/eralegis/)
[![codecov](https://codecov.io/gh/tiagocordeiro/eralegis/branch/master/graph/badge.svg)](https://codecov.io/gh/tiagocordeiro/eralegis)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/tiagocordeiro/eralegis/blob/master/LICENSE)

### Configurando o ambiente
```shell
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ 
```

### Instalando via git
```shell
git clone https://github.com/tiagocordeiro/eralegis.git
```

### Instalando via pip
```shell
pip install eralegis
```

### Importando o módulo
```shell
$ python
>>> from eralegis import thelemicdate
>>> thelemicdate.now()
'☉ in ... ☽ in ... Dies ... Anno ... æræ novæ'

>>> thelemicdate.in_day(1905, 4, 8, 12, 30)
'☉ in 18º ♈ ☽ in 28º ♉ Dies Saturnii Anno I:0 æræ novæ'

```
