## Evaluate Categories


#### Default experiment
```bash
cd /home/isgarrido/dllas-evaluator ; /usr/bin/env /home/isgarrido/anaconda3/envs/dllas-evaluator/bin/python /home/isgarrido/dllas-evaluator/src/FillTemplate.py

cd /home/isgarrido/dllas-evaluator ; /usr/bin/env /home/isgarrido/anaconda3/envs/dllas-evaluator/bin/python /home/isgarrido/dllas-evaluator/src/EvaluateCategories.py
```

#### Custom experiment
You should follow the folder convertion, you can check the folder structure of the default experiment:
- The base folder is on the root of the projects, named ``assets``. Inside we have two folders ``data`` and ``result``.
- ``data`` folder, for our ``input data``. Inside you should add your data in the folder matching the ``script`` name, ex place ``some_templates.tsv`` inside ``FillTemplates`` folder.
- ``result`` folder is for our ``experiment results``. Every experiment should have a ``unique label`` that you will be passing as a cli param. Inside ``result`` we will have one folder for each experiment, not much to worry here as they will be created when you run the scripts.

```bash
cd /home/isgarrido/dllas-evaluator ; /usr/bin/env /home/isgarrido/anaconda3/envs/dllas-evaluator/bin/python /home/isgarrido/dllas-evaluator/src/FillTemplate.py 'Experiment name' 'templates_123.tsv'

cd /home/isgarrido/dllas-evaluator ; /usr/bin/env /home/isgarrido/anaconda3/envs/dllas-evaluator/bin/python /home/isgarrido/dllas-evaluator/src/EvaluateCategories.py 'Experiment name' 'Yulia.json'
```

#### Run tests

```bash
chmod -x ./tests/TestEvaluateCategories.py
nosetests --with-watch --rednose --nologcapture src.tests
```