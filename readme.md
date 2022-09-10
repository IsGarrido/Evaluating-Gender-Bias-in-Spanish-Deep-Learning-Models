## Evaluate Categories

### Setup
Create a conda env, install dependencies.

### Setup

Create a conda env, install dependencies.

### Run FillTemplate.py

1. Create a file with the templates that you want to test in TSV format. Ex `templates_123.tsv`.
2. Place your template file inside `assets/data`. Ex `assets/data/templates_123.tsv` or `assets/data/Experiment name/templates_123.tsv`.
3. (Optional) Create a TSV file with a the list of models that your experiment will run. Any `Fill mask` model on [HuggingFace](https://huggingface.co/models) should work.
4. Run FillTemplate.py `python src/FillTemplate.py 'Experiment name' 'templates_123.tsv' 'models.tsv' 10`.
5. This will generate an output inside `assets/result/Experiment name/FillTemplate`. The interesting file is `FillTemplate.json`.

### Generating the category file

1. Grab the result of the latest experiment in `assets/result/Experiment name/FillTemplate/FillTemplate.json`
2. Head to the Category Tool
3. (Optional) If you already had categorized adjetives, you can drop them in the `Filled box` so you only have to categorize the new words. If not just start clear.
4. Drag and drop `Adjectives.json` into the box with the same name.
5. Use the "New category" input to add as many categories as needed.
6. You will be categorizing the word that is pointed by an arrow. To move its category just click a column. 
7. When you are done, just click the `Save to file` button. It will be saved in your browser's default downloads folder as `dllas-categorizedwords.json`. You can check and edit this json file to tweak category name or contents.

Changes will be saved as you work in localStorage. If you want to continue later, you can Drop again the `Adjectives.json` file and click the `Load last session` button to recover your changes.

### Run EvaluateCategories.py

1. Move the categorization result from the previous phase ( `dllas-categorizedwords.json` ) it to the folder `assets/data` with some nice name. Ex `Yulia.json`. 
2. Run `python src/EvaluateCategories.py 'Experiment name' 'Yulia.json'`. It will generate some result files on `assets/result/Experiment name/EvaluateCategories`
   
### Replicate base experiment

1. git clone the project
2. Run FillTemplate.py without params
3. Run EvaluateCategories without params

```bash
cd dllas-evaluator
python src/FillTemplate.py
python src/EvaluateCategories.py
```

### General notes on the folder structure
You should follow the folder convertion, you can check the folder structure of the default experiment:
- The base folder is on the root of the projects, named `assets`. Inside we have two folders `data` and `result`.
- `data` folder, for our `input data`. Inside you should add your data in the folder matching the `script` name, ex place `some_templates.tsv` inside `FillTemplates` folder.
- `result` folder is for our `experiment results`. Every experiment should have a `unique label` that you will be passing as a cli param. Inside `result` we will have one folder for each experiment, not much to worry here as they will be created when you run the scripts.

## Run the tests

```bash
chmod -x ./tests/TestEvaluateCategories.py
nosetests --with-watch --rednose --nologcapture src.tests
```