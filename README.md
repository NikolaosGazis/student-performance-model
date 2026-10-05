# Student Performance Model

## Description

This Python program uses machine learning tools to analyze and graph data that represent the performance results for students. It reads a dataset, categorizes student performances and displays statistics for each group, where the user can add further information about students. KMeans clustering is utilized in the program to group students according to their scores, which allows determining peers who are closest with almost equal results.

## Key Features

  - Data Preprocessing: Works with pandas and scikit-learn to read student performance data, turning the categorical variables into numeric values.

  - Clustering: Divides students into groups based on their average scores using KMeans clustering, so that the user may choose the number of intervals.

  - User Interaction: Provides an interface that is straightforward to work with, which allows a user to enter new information about a student and provides relevant data on other students who perform in close proximity.

  - Data Visualization: With Matplotlib, it generates a scatter plot containing the clusters created by the KMeans algorithm.

## Usage

  - Clone the repository.

  - Ensure that the necessary libraries are installed (pandas, scikit-learn and matplotlib).

  - The data is only analyzed and interactable when you run the program, as instructed (python student_performance.py).

  - Best used in the IDE **Spyder** from Anaconda Navigator, due to its flexibility to work with and visualize data.

## Contributing

  - Open issues, propose changes or submit pull requests to enhance the functionality of this program as well as how it will be used.

## License
This repository is licensed under the [MIT License](https://github.com/NikolaosGazis/student-performance-model?tab=MIT-1-ov-file).
