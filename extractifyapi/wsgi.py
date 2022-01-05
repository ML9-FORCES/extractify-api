"""
WSGI config for extractifyapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import gdown
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extractifyapi.settings')

application = get_wsgi_application()

# ML registry
import inspect
from apps.ml.registry import MLRegistry
from apps.ml.classifier.ml import Wrapper
from apps.ml.classifier.ml import bert_classifier
from apps.ml.classifier.ml import linking_classifier

try:
    registry = MLRegistry() # create ML registry
    
    #Downloading Model - Single time step
    url='https://drive.google.com/drive/folders/1UjpkmlaFIExoE4slCLdaEAxjTBOZ28Fy'
    if not os.path.isdir('./MODELS'):
        gdown.download_folder(url,output='/MODELS', quiet=True)
    
    # Bert classifier
    bc=bert_classifier()
    lc=linking_classifier()
    rf = Wrapper(bc,lc)
    # add to ML registry
    registry.add_algorithm(endpoint_name="model",
                            algorithm_object=rf,
                            algorithm_name="Bert",
                            algorithm_status="production",
                            algorithm_version="0.0.1",
                            owner="ML9-Forces",
                            algorithm_description="Bidirectional Encoder Representations from Transformers",
                            algorithm_code=inspect.getsource(Wrapper))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
