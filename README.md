## Data Streaming APIs

Project is a publisher/subscriber model to process streaming data and provide an up-to-date view of incoming data.

### Built With
Below are all major frameworks library used

* [FastAPI](https://fastapi.tiangolo.com/)
* [pandas](https://pandas.pydata.org/)

### Project File Structure
-------------------
├── app                      <- FastApi project folder<br />
│   ├── csv_reader.py         <- python file to perform csv operations<br />
│   ├── main.py               <- python file initializing FastApi app object<br />
│   ├── processor.py          <- python file to process data<br />
│<br />
├── csv_data                 <- Folder to store csv<br />
│   ├── sku_info_csv.csv      <- static sku info csv<br />
│   ├── transaction_csv.csv   <- csv to store incoming transactions data<br />
│<br />
├── .gitignore               <- git ignore file<br />
├── Dockerfile               <- docker file to create project image<br />
├── README.md                <- git readme file<br />
├── requirements.txt         <- python requirement file<br />

