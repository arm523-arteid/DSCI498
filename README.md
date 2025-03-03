# DSCI498
This repo contains code and materials for a project which aims to detect potential events (disorders) in healthcare data using deep learning-based anomaly detection methods. 
The data source is synthetic data from Synthea. Synthea uses probabilistic models and clinical modules to mimic real-world patient disease progressions, encounters, procedures, lab tests, and medications.
It is entirely synthetic. However, it retains realistic patterns of care.
There are a lot of pros that come from using synthetic data. Healthcare data is highly regulated due to it's private nature. 
Synthetic data pose no privacy concerns therefore elminating any HIPPA and confidentiality concerns. 
Data from these 5 states (California, Texas, Florida, New York, Pennsylvania) were generated.
These 5 states likely cover the broadest cross-section of urban, suburban, and rural populations and see diverse disease profiles. 


Objectives:
Explore deep learning methods to improve detection

Directory structure:
1. data/ 
    raw/:       Given size, they reside in GoogleDrive. This will remain empty
    processed/: Includes cleaned data ready for training

2. src/ 
    python scripts & data generation scripts

3. docs/ 
    Additional documentation 

4. results/
    Generated plots, metrics & other outputs.