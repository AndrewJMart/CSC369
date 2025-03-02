# Data Cleaning and Exploratory Data Analysis (EDA)


## Scripts and Notebooks

The following scripts and notebooks were used to perform the data cleaning and exploratory data analysis:

- [Data Cleaning Script](./AnalysisProjectBasePipeline.ipynb)
- [Exploratory Data Analysis Notebook](./InitialBasicExploration.ipynb)

## Exploratory Data Analysis (EDA)

### Missing Data

Fortunately, there is only 8 rows for non-essential columns that contain missing values. Conceputally this makes sense as this data was grabbed directly from Steam's API and thrown onto Kaggle. Meaning I was lucky that I did not have to put much thought into how I will handle missing rows.

However, in the additional dataset I found that hosts information regarding publishers of a large repo of steam data (necessary missing data to assess whether a game from a AAA dev or not), there were many missing rows within this dataset. To alleviate this I removed them before joining.

## Data Parsing and Quality Issues

### 1. Parsing Issues
While loading the reviews dataset there was funky logic with loading chinese characters within PyArrow that caused me to migrate into using polars to load the entire thing instead. I tried various encoding formats within PyArrow in conjunction with faulty row skipping to no avail ...

### 2. Missing Important Data

While all of the reviews host information about the review given and other interesting metrics I can use to visualize "performance" of previous AAA release (such as total player time), the dataset had no information on publishers. Because of this I found an additional dataset on kaggle that contains publisher data for over 10000 games on steam, processed it, and joined it. 


## Conclusion

The conclusion of the data exploration is that I have a proper dataset to answer my hypothesis, along with some additional information I think could be cool. Meaning it would be interesting to plot all time hours played data for Good / Bad AAA games across different decades etc.

I do not have any other additional concerns, other than I need to compile a list of developers I consider to be AAA across decades, however I can easily do this.



