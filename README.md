# GeneticProgramming_k-means_Clustering
## Abstract:
Using **Genetic programming** to optimize the distance function for **Clustering** with k-means. The algorithm present in this repository was able to improve the results by up to 458% (v_score) in relation to the commonly used Euclidean distance.
The algorithm is capable of adapting to any dataset with little customization.

## Execution:
### Initial requirements:
* Pytho 3.8.2
* Venv (sudo apt install python3.8-venv)
* pip (sudo apt install python3-pip)

### Initial setup:
1. Create enviroment:    `python3 -m venv ./code/venv`
2. Activate enviroment:  `cd code && source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

### Execute:
1. Activate enviroment:  `cd code && source venv/bin/activate`
2. Execute: `python3 main.py`
3. Exit: `deactivate`
>> the parameters are at the beginning of the main file

### Exit:
When executing the algorithm, the function of the best individual will be printed using variables x, y and z, in addition to the individual v-scored on test of the chosen dataset. A *training_v-score.json* file will also be generated, where all training results per generation will be recorded with the following order: best value, the average and the worst value.


## Datasets:
* [Breast Cancer Coimbra](http://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Coimbra)
* [Glass Identification](https://archive.ics.uci.edu/ml/datasets/glass+identification)



