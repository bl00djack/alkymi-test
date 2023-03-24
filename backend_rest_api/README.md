# Backend REST API Design and Implementation

# Setup

For Local:
```
# Create a python 3.9 virtual environment and activate it.
$ virtualenv -p python3.9 venv
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Make sure MongoDB is running in your local

# Run the app
$ ./run.sh
```

# File Upload API

The API accepts a tabular data file and then process the file and detect temporal data

## Endpoints

- User Signup (POST `/api/auth/signup`)
- User Login (POST `/api/auth/login`)
- Upload a tabular data file (POST `/v1/table`)
- Retrieve data file (GET `/v1/table/:file_id`)

## - User Signup (POST `/api/auth/signup`)
---
Endpoint to create a user. Sends a request with a JSON payload which contains username and password. Returns a newly created user id.

### Request
---
```sh
POST /api/auth/signup

$ curl 'http://localhost:5000/api/auth/signup' --header 'Content-Type: application/json' --data '{"username": "username", "password": "password"}'
```

#### Header
---
`Content-Type`: `application/json`

#### JSON Payload
---
`username` *string*

A unique username

`password` *string*

A secure password

#### Response
---
```json
{
    "id": "641dae82faf45d9837ca11c6"
}
```

#### Returns
---
`id` *string*

A unique id of a user that just got created

## - User Login (POST `/api/auth/login`)
---
Endpoint for user login. Sends a request with a JSON payload which contains username and password. Returns a token which you will use to access other API endpoints.

### Request
---
```sh
POST /api/auth/login

$ curl 'http://localhost:5000/api/auth/login' --header 'Content-Type: application/json' --data '{"username": "username", "password": "password"}'
```

#### Header
---
`Content-Type`: `application/json`

#### JSON Payload
---
`username` *string*

Username

`password` *string*

Password associated with username

#### Response
---
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3OTY2NjgyNCwianRpIjoiOWRlYzJjNTAtMWI5ZS00NjY3LWE1MTQtYWEzZGFmMGY4M2FkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY0MWRhZTgyZmFmNDVkOTgzN2NhMTFjNiIsIm5iZiI6MTY3OTY2NjgyNCwiZXhwIjoxNjgwMjcxNjI0fQ.b_OMdjYsWd_6VJfkwZuyNuzaTnBIloBKJf11bAmRdw0"
}
```

#### Returns
---
`token` *string*

A JWT token to pass in the Authorization header to access other API endpoints.

## - Upload a tabular data file (POST `/v1/table`)
---
Upload a tabular data file with a parameter `headerRow`. The API will save the file (to be processed later) and return a file ID and status. Currently it only accepts CSV files.

#### Request
---
```sh
POST /v1/table?headerRow=true

$ curl 'http://localhost:5000/v1/table?headerRow=true' --header 'Authorization: Bearer <token>' --form 'file=@"/absolute/path/to/file.csv"'
```

#### Header
---
`Authorization`: `Bearer <token>`

Replace `<token>` with the token returned from `/api/auth/login`

#### Parameters
---
`headerRow` *boolean*

Specifies if the data file has a header row or not (example values: `true` or `false`).

#### Response
---
```json
{
  "file_id": "129ca274-4545-4681-b2a1-66c1fd8c693f",
  "status": "processing"
}
```

#### Returns
---
`file_id` *uuid*

ID of the uploaded file.

`status` *string*

Current status of the file (example values: 'processing' or 'finished').


## - Retrieve data file (GET `/v1/table/:file_id`)
---
Retrieve a file which has a JSON representation of its tabular data, and the column, row and character indexes for any temporals that were detected. Supply the unique identifier of the file in the URL.

### Request
---
```sh
GET /v1/table/:file_id

$ curl 'http://localhost:5000/v1/table/129ca274-4545-4681-b2a1-66c1fd8c693f' --header 'Authorization: Bearer <token>'
```

#### Header
---
`Authorization`: `Bearer <token>`

Replace `<token>` with the token returned from `/api/auth/login`

### Parameters
---
None

### Response
---
```json
{
  "header": [
    "fund",
    "date",
    "amount"
  ],
  "rows": [
    [
      "cookie capital",
      "2020-01-01",
      "200"
    ],
    [
      "Bonbon Bonds",
      "On Jan 1st, 1980",
      "100"
    ]
  ],
  "temporals": [
    {
      "column": 1,
      "temporal": "2020-01-01",
      "startIdx": 0,
      "row": 0,
      "text": "2020-01-01",
      "endIdx": 10
    },
    {
      "column": 1,
      "temporal": "1980-01-01",
      "startIdx": 3,
      "row": 1,
      "text": "Jan 1st, 1980",
      "endIdx": 16
    }
  ]
}
```

### Returns
---

`header` *list*

Header of the columns in the data file

`rows` *list*

All the rows in the data file

`temporals` *list*

List of `temporal` objects

#### `Temporal` object

#### Attributes
---
`row` *int*

Row index of the detected temporal cell

`column` *int*

Column index of the detected temporal cell

`text` *string*

Parsed text of the temporal cell

`temporal` *string*

Temporal data

`startIdx` *int*

Start index of the raw text which was parsed

`endIdx` *int*

End index of the raw text which was parsed

---

# Known Issues

- If the APScheduler Job fails in the middle of processing a task, the file will be in locked state forever

# To Do

- Add Docker container
