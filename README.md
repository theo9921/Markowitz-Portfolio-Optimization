# Markowitz Portfolio Optimization

## Description
This is a small project that serves as an intor to the basics of the Markowitz Portfolio Optimization Method by visualizing the 'Efficient Frontier'.

## How to use
The file structure for this is very simple. The whole program is contained in the file **pyOpt.py**. In there you will find a couple of helper function definitions as well as the main programm. There is a designated variable that allows you to select the tickers of the stock investments you want to include in your portfolio and you can also change the time period of interest. 
Finally the directory **/stock_dfs** is used to locally store all the price data that is going to be used while running the code. This is done in order to reduce processing times in case you need to access the data or change some tickers. This folder will start to populate with .csv files once you run the prgram for the first time. 

## How to run
1. Copy the link for this Gihub repository and then navigate to the directory in which you want to store a copy of this project
2. On a UNIX terminal (or Git terminal) navigate to the directory of interest and run the following command:
    ```
    git clone <link of the repository>
    ```
3. Once the process is done you can either open the pyOpt.py file to edit the parameters or you can run the program by executing the command:
    ```
    python3 ./pyOpt.py
    ```

## Packages needed
The following packages are required for the project to run:
* pandas
* numpy
* matplotlib
