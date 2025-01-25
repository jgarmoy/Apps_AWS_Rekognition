import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'apps_aws_rekognition' # Debe coincidir con el nombre de la carpeta 
AUTHOR = 'Juan Manuel García Moyano'
AUTHOR_EMAIL = 'juanmi_4000@hotmail.es'
URL = 'https://github.com/juanmi4000'

LICENSE = ''
DESCRIPTION = 'Sistema artificial capaz de analizar imágenes, de forma que se identifiquen y procesen los rostros de las personas, con el fin de generar un valor añadido'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'opencv-python'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)