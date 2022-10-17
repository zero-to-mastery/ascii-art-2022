# ZTM Hacktoberfest 2022 Project - ASCII Art API

## About this project
This project (./API folder) contains Python code for a API which allows the users to get the ASCII art by uploading an image file (only `.jpeg`, `.jpg` and `.png` types are allowed). The API is build using **[`FastAPI`](https://fastapi.tiangolo.com)** library.

---

## Installation
Install the necessary dependencies by using the below command:

```bash
pip install -r requirements.txt
```

For mac or Linux users, use this command

```bash
pip3 install -r requirements.txt
```

*Note: If you need to install new libraries for more development for this API project, just add that libraries' names to the `requirements.txt` file.*

---

## How to run this code?
In your command line, run

```bash
uvicorn main:app --reload
```

If you are using any remote machine, then you can run this command

```bash
uvicorn main:app --reload --host 0.0.0.0
```

---

## Docs for this API
This API is built using `FastAPI` which creates beautiful documents automatically. From there, you can also requests to this APIs, no need to download [Postman](https://www.postman.com/downloads) if you dont want to install to your machine. To see the docs, you can use this url --> `http://127.0.0.1:8000/docs`. Or you can change the domain according to the requirements like `www.example.com/docs`.

### Thank you.
