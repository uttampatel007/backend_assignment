## Data Streaming APIs

Project is a publisher/subscriber model to process streaming data and provide an up-to-date view of incoming data.

### Built With
Below are all major frameworks library used

* [FastAPI](https://fastapi.tiangolo.com/)
* [pandas](https://pandas.pydata.org/)

### Project File Structure

```

├── app                       <- FastApi project folder
│   ├── csv_reader.py         <- python file to perform csv operations
│   ├── main.py               <- python file initializing FastApi app object
│   ├── processor.py          <- python file to process data
│
├── csv_data                  <- Folder to store csv
│   ├── sku_info_csv.csv      <- static sku info csv
│   ├── transaction_csv.csv   <- csv to store incoming transactions data
│
├── .gitignore                <- git ignore file
├── Dockerfile                <- docker file to create project image
├── README.md                 <- git readme file
├── requirements.txt          <- python requirement file

```
### Prerequisites
* Docker : In case of running and deploying project using docker
* Python : Python needs to be installed while running locally

### Installing and Set Up
#### Using Docker
* Create docker image of the project<br/>
`
$ docker build -t image_name .
`

* Run docker container detached mode and on port 8000<br/>
`
$ docker run -d -p 8000:8000 image_name
`
* Access apis on localhost:8000

#### Locally Without Docker
* Install all requirements in a virtual environment<br/>
`
$ pip install -r requirements.txt
`
* Run FastApi using uvicorn<br/>
`
$ uvicorn app.main:app --reload
`
* Access apis on localhost:8000

### API Documentation
After running project find api documentation at:
* localhost:8000/docs
* localhost:8000/redoc