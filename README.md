## Data Streaming APIs

Project is a publisher/subscriber model to process streaming data and provide an up-to-date view of incoming data.

### Built With
Below are all major frameworks library used

* [FastAPI](https://fastapi.tiangolo.com/)
* [pandas](https://pandas.pydata.org/)

### Project File Structure
-------------------
├── app                      <- FastApi project folder
│  ├── csv_reader.py         <- python file to perform csv operations
├── main.py               <- python file initializing FastApi app object
├── processor.py          <- python file to process data

├── csv_data                 <- Folder to store csv
├── sku_info_csv.csv      <- static sku info csv
├── transaction_csv.csv   <- csv to store incoming transactions data

├── .gitignore               <- git ignore file
├── Dockerfile               <- docker file to create project image
├── README.md                <- git readme file 
├── requirements.txt         <- python requirement file

