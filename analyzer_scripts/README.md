# Analyer Scirpts

This folder contains scripts that analyze the results produced by the tests in the kubernetes System. Specifically for each files:

- **result_analyzer**: Reads the results that were produced by the tests and modifies them in a way to be used by the other analyzer scripts
- **create_comparison_array**: Takes the analyzed results and prints out an array with the differnces in percentage for cost, between the different schedulers
- **create_plots**: Based on the analyzed results, produce plots comparing the different schedulers on response time per app, the whole application and cost
- **create_scatter**: Based on the original results, create a scatter plot that contains each scheduler and shows the application response time and cost for each test instance

