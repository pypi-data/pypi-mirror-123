# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtcli', 'mtcli.indicator']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'python-dotenv>=0.19,<0.20']

entry_points = \
{'console_scripts': ['atr = mtcli.cli:rm',
                     'bars = mtcli.cli:bars',
                     'mm = mtcli.cli:mm',
                     'mt = mtcli.cli:cli',
                     'rm = mtcli.cli:rm',
                     'sma = mtcli.cli:mm']}

setup_kwargs = {
    'name': 'mtcli',
    'version': '0.14',
    'description': 'Converte gráfico do MetaTrader 5 para texto',
    'long_description': '# mtcli  \n  \nFerramenta de linha de comando para leitura de gráficos do MetaTrader 5 para deficientes visuais.  \n  \n[PyPI](https://pypi.python.org/pypi/mtcli)  \n[Documentação](https://vfranca.github.io/mtcli)  \n  \n------------\n\n## Pré-requisitos  \n\n* [MetaTrader5](https://www.metatrader5.com/pt) - Plataforma de trading.  \n* [Python](https://www.python.org/downloads/windows) - Interpretador de comandos disponível no prompt de comando.  \n\n\n## Instalação  \n\n1. Instale o Python. Obtenha o instalador em https://www.python.org/downloads/windows. Durante a instalação marque a opção para ficar disponível no path do Windows.\n\n2. No prompt de comando execute:\n```\n> pip install mtcli\n```\n\n3. Instale o MetaTrader 5. De preferência obtenha o instalador no site da sua corretora, caso contrário o instalador está disponível para download no site oficial do MetaTrader.  \n\n4. Baixe no link abaixo o arquivo contendo os arquivos de trabalho do mtcli:  \nhttps://drive.google.com/file/d/1olFEKJnnunBI1SDoW7QoMT9p6_yRQyhp/view?usp=sharing  \n\n5. Descompacte o arquivo mtcli.zip. Uma pasta mtcli será criada. Essa pasta deverá ser usada para executar os atalhos de comandos do mtcli. Além disso nela estará o indicador mtcli.ex5 que deverá ser anexados ao gráfico do MetaTrader 5.\n \n6. No MetaTrader 5 abra a pasta de dados (CTRL+SHIFT+D) e copie o camimnho da pasta mql5/Files para a área de transferência.\n\n7. Configure o mtcli com o caminho copiado da pasta do MetaTrader 5:\n```cmd\n> cd mtcli\n> conf CSV_PATH <cole-aqui-o-caminho-da-pasta>\n```\n\n8. Anexe o indicador mtcli.ex5 ao gráfico do MetaTrader 5.  \n\nPronto! O mtcli estará pronto para ser usado.  \n\n\n## Comandos  \n  \n```cmd\nmt bars <ativo> - Exibe as barras do gráfico do ativo especificado.\nmt mm <ativo> - Exibe a média móvel simples dos últimos 20 períodos do ativo.\nmt rm <ativo> - Exibe o range médio dos últimos 14 períodos do ativo.\n```\n\n------------\n  \n  ## Agradecimentos  \n  \nAo @MaiconBaggio desenvolvedor do PyMQL5 que faz uma comunicação com o MetaTrader5 e fornecedor do primeiro EA exportador das cotações.  \nAo Claudio Garini que transferiu a geração das cotações para um indicador.  \n\n\n------------\n  \n## Licenciamento  \n\nEste aplicativo está licenciado sob os termos da [GPL](../LICENSE).  \n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': 'Valmir Franca',
    'maintainer_email': 'vfranca3@gmail.com',
    'url': 'https://github.com/vfranca/mtcli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
