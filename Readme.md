# Project: Event Data Scraper

## Overview

This project introduces an efficient tool for extracting and organizing event data from specific URLs. Designed to streamline the process of collecting event details for work purposes, it eliminates the repetitive task of manually opening links and copying & pasting data. Through automated scraping and data structuring, it provides a quick and accurate means to gather essential information about various events, including tournament names, dates, locations, and age groups.

## Features

- **Automated Web Scraping**: Quickly scrapes data from provided event URLs without manual intervention.
- **Data Organization**: Structures the collected data into an easily understandable format, making it convenient for users to analyze and utilize the information.
- **Multiple Event Handling**: Capable of handling and grouping data from multiple events, facilitating bulk data processing.
- **Customizable Age Groups**: Includes a predefined set of age groups but allows for easy customization to cater to specific needs.

## Requirements

- Python 3.x
- Beautiful Soup 4
- Requests

## Installation

To use this tool, you need to have Python installed on your system. If you haven't installed Python yet, download and install it from [python.org](https://www.python.org/downloads/). Additionally, you need to install the required packages using pip. Run the following command in your terminal or command prompt:


## Usage

1. Clone or download this repository to your local machine.
2. Open your terminal or command prompt and navigate to the directory containing the script.
3. Run the script using Python:


4. Follow the on-screen prompts to input the number of events and their corresponding URLs.
5. The script will scrape the data and display the organized information in the console.

## Sample Output

```plaintext
EVENT #1
Headline/Tournament Name: XYZ Championship
Event Dates: June 1-5, 2024
Facility/Field Name: National Sports Complex
Location: Springfield, IL
Age Group: 10U Open, 12U (60/90), 14U Open,
Link for event: https://www.example.com/event1
Specific Benefits/Callouts: 

EVENT #2
Headline/Tournament Name: ABC Regional Qualifier
Event Dates: July 10-15, 2024
Facility/Field Name: City Ballpark
Location: Anytown, USA
Age Group: 9U Open, 11U (54/80), 13U Open,
Link for event: https://www.example.com/event2
Specific Benefits/Callouts: 
