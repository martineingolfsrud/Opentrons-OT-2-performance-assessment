# Opentrons OT-2 performance assessment

This repository contains developed code and gathered raw data from my Master's thesis titled "Automated Versus Manual Proteomics Sample Preparation: A Comparative Evaluation of Liquid Handling Workflows". The aims of this thesis were to:

-	Develop and implement proteomics sample preparation protocols using an automated liquid handling system. 
-	Evaluate the performance of a liquid handling robot in comparison to human operators. 
-	Apply the sample preparation protocols to real-world biological samples.

The proteomics sample preparation protocols adapted and developed for the OT-2 were the bicinchoninic acid (BCA) protein assay and the single-pot, solid-phase-enhanced sample preparation (SP3) protocol. To compare performance between the Opentrons OT-2 pipetting robot and human operators, BCA assay absorbances and protein group and peptide counts from LC-MS analysis of MDA lysate samples were collected. Additionally, pipetting steps were timed to compare operating speed. Finally, the OT-2 was tested on real-world yeast samples, yielding quantitative proteomics data. 

## Table of contents
- [Folder descriptions](#folder-descriptions)
- [Requirements](#requirements)
- [Usage](#usage)
- [Contact](#contact)
- [Author](#author)
- [References](#references)

## Folder descriptions
- **BCA:** Contains two single-channel and one multi-channel script ready for upload to the Opentrons App.
- **Rawdata:** Contains time data for performed SP3 and BCA runs (SP3_times and BCA_times), protein group and peptide counts for MDA lysates (SP3MDA_protcount), protein quantities for yeast samples (SP3yeast_protquant) and absorbances of BCA samples (BCA_absorbances).
- **SP3:** Contains seven major and one minor version scripts ready for upload to the Opentrons App.
## Requirements
To execute the code in this library the following software and libraries are required:
- **Software:** Python (version 3.10.18) and Opentrons (version 8.3.0 or newer)
- **Python packages:** opentrons (API version 2.24)

## Usage
To use the code in this repository, clone the repository to your local machine using the following command:
```
git clone https://github.com/martineingolfsrud/Opentrons-OT-2-performance-assessment.git
```

## Contact
For any questions or further assistance, feel free to contact me at martineingolfsrud@gmail.com

## Author
Martine Ingolfsrud


