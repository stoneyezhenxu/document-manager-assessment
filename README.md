# Propylon Document Manager

The **Propylon Document Management System** is a streamlined web application comprising a fundamental API backend and a client  based on Django and **React**. It facilitates users in storing files at specific URLs for subsequent retrieval. The system employs **Django Restful Framwork** as the backend  and adheres to a RESTful design for its API endpoints.



## 1. Main Functionalities

The primary functional modules of the "Propylon Document Management" System include:

#### 1.1 Login Module

- Facilitates user registration, login, and logout functionalities.
- Validates fields such as username/email and password.

#### 1.2 User Dashboard 

Upon logging in, users can access a comprehensive view of uploaded file details.

- Supports filtering files by type (Images, Documents, Videos, Procedures, Others).
- Displays detailed information such as Filename, Version, URL, Size, Type, CreateTime, and Description.
- Provides pagination functionality.

#### 1.3 File Upload Module 

- Stores files of any type and name
- Stores files at any URL

#### 1.4 File retrieve Module

- Restricts interaction to authenticated users only.
- Prevents a user from accessing files submitted by another user.

#### 1.5  Download the Resource Module 

- Supports the Download of User-Indexed Resources

### 1.6 Auth Management Module

- Restricts interaction to authenticated users only.

- Ensures a user cannot access files submitted by another user.
  

## 2. API Documents

- Base Url  :  `http://localhost:8001`  

- Api Version:  `v1`

Only the Register API and Login API do not require authentication.

For other APIs, the Auth Token should be included in the headers.

#### 2.1 Register API

User registration involves providing a unique email, username, and password. The email must be unique across users.

`POST  /api/v1/register/`

| Params   | Value            | Type   | Required | Desc                                        |
| :------- | ---------------- | :----- | :------- | :------------------------------------------ |
| username | zhenxu           | string | Yes      | Limited length of username between 4 and 15 |
| email    | zhenxu@gmail.com | string | Yes      | Follow email format.                        |
| password | zhenxu0101       | string | Yes      | Limited length of username between 4 and 15 |

```shell
curl -X POST  \
  'http:/ip:port/api/v1/register/' \
  -H 'Content-Type:application/json' \
  -d '{"username":"zhenxu","email":"zhenxu@gmail.com","password":"zhenxu0101"}'
```

**Responses**

```json
{
 "code": 200,
 "data": 'Register successful!'
}
```



#### 2.2 Login API

Obtain the Auth Token by logging in.

`POST  /api/v1/login/`

| Params   | Value            | Type   | Required | Desc                                                         |
| :------- | ---------------- | :----- | :------- | :----------------------------------------------------------- |
| username | zhenxu@gmail.com | string | Yes      | this params value equal to the email of register .  <br />Todo:  change to  the email fields. |
| password | zhenxu0101       | string | Yes      | Limited length of username between 4 and 15                  |

```shell
curl -X POST  \
  'http:/ip:port/api/v1/login/' \
  -H 'Content-Type:application/json' \
  -d '{"username":"zhenxu@gmail.com","password":"zhenxu0101"}'
```

**Responses**

```json
{
 "code": 200,
 "data": {
 			{"token":"3a7c21d3be77cee9761fc3d50c1e145ca469a0be","user_id":1}
 }
}
```

#### 2.3 Logout API

Remove the Auth Token by logging out.

`GET  /api/v1/logout/`

| Params | Value                                                        | Type | Required | Desc                   |
| :----- | ------------------------------------------------------------ | :--- | :------- | :--------------------- |
| Header | { "Authorization": "Token 3a7c21d3be77cee9761fc3d50c1e145ca469a0be"} | Dict | Yes      | Authorization by Token |

```shell
curl -X GET  \
  'http:/ip:port/api/v1/logout/' \
   -H "Authorization: Token 6119fb3fa535d92e0b23fdbe04f610bde1ab4611" 
```

**Responses**

```json
{
 "code": 200,
 "data": 'Logout successful!'
}
```

#### 2.4 Upload File API


Users can specify any valid URL like  `/xx/xxxx/xxxxx/xxxx/` ,

Then `file_url` will be generate with format like  ` /files/{user specific url}/{file_name}'`

`POST  /api/v1/files/`

Body :  `form-data`

Form-data including fields as follow:

| Fields    | Type   | Required | Desc                                                         |
| :-------- | :----- | :------- | :----------------------------------------------------------- |
| file_desc | string | Yes      | current desc for file like modify infos                      |
| file_url  | string | Yes      | generated with format like '/files/{user specific url}/{file_name}' |
| file_name | string | Yes      | file name                                                    |
| file_size | float  | Yes      | file size                                                    |
| file_uid  | string | Optional | file unique id                                               |
| file_obj  | File   | Yes      | file obj                                                     |

```shell
curl -X POST  \
  'http:/ip:port/api/v1/files/' \
  -H "Authorization: Token 6119fb3fa535d92e0b23fdbe04f610bde1ab4611" 
  -d  {form-data}
```

**Responses**

```shell
{
 "code": 200,
 "data": [{...},{...},{...},{...}]
}
```



#### 2.5 All files List API

Retrieve all files of the logged-in user and display file information in the dashboard.

`GET  /api/v1/files/`

```shell
curl -X GET  \
  'http:/ip:port/api/v1/files/' 
   -H "Authorization: Token 6119fb3fa535d92e0b23fdbe04f610bde1ab4611" 
```

**Responses**

```shell
{
 "code": 200,
 "data": [{...},{...},{...},{...}]
}
```



#### 2.6 File Versions List API

Tips:
	 	Obtain all versions of a specific file by  `hash(file_url)` ,

​		 where`file_url_hash`  is obtained using `hashlib.md5() ` of  `file_url`

`GET  /api/v1/files/{file_url_hash} `

```shell
curl -X GET  \
  'http:/ip:port/api/v1/files/{file_url_hash}' 
   -H "Authorization: Token 6119fb3fa535d92e0b23fdbe04f610bde1ab4611" 
```

**Responses**

```shell
{
 "code": 200,
 "data": [{...},{...},{...},{...}]
}
```

#### 2.7 File Details API

Tips:
	 	Get the  file details by  specific `file_url` and `revision`

​		 where `file_url_hash` is obtained by using  `hashlib.md5() `  of  `file_url`

​		 `revision` is the `file_version`



`GET  /api/v1/files/{file_url_hash}?revision=1 `

```shell
curl -X GET  \
  'http:/ip:port/api/v1/files/{file_url_hash}?revision={file_version}' 
   -H "Authorization: Token 6119fb3fa535d92e0b23fdbe04f610bde1ab4611" 
```

**Responses**

```shell
{
 "code": 200,
 "data": [{...},{...},{...},{...}]
}
```



#### 2.8 Download File API 

Retrieve file content data by `file_uuid`, `file_type`, and `file_name`.

Locate the file object data from the server storage (local static file) and return it.

`GET  /api/v1/files/content `

Params:    `?file_uuid={file_uuid}&file_type={file_type}&file_name={file_name}`

```shell
curl -X GET  \
  'http:/ip:port/api/v1/files/content?file_uuid={file_uuid}&file_type={file_type}&file_name={file_name}' 
   -H "Authorization: Token 6119fb3fa535d92e0b23fdbe04f610bde1ab4611" 
```

**Responses**

```shell
{
 "code": 200,
 "data": xxxxxxxxxxxxxxxxxxxxxxxx
}
```

​	



## 3. Getting Started

### 3.1 Clone the repository

```shell
git clone https://github.com/stoneyezhenxu/document-manager-assessment
```

#### 3.2 Start backend  server

1. [Install Pipenv](https://pipenv.pypa.io/en/latest/installation/)  Manages your Python virtual environments by Pipenv.
2. This project requires Python 3.11 so you will need to ensure that this version of Python is installed on your OS before building the virtual environment.
3. `pipenv install -r requirements/local.txt`.  
4. `pipenv run python manage.py migrate` to create the database.
5. `pipenv run python manage.py runserver 0.0.0.0:8001` to start the development server on port 8001.

#### 3.3 Run frontend application

1. Navigate to the client/doc-manager directory.

2. `yarn install` to install the dependencies.

3. `yarn start` to start the React development server.

   

## 4. Screenshots

#### 2.1 Register Page 

<img src="https://github.com/stoneyezhenxu/imgHosting/blob/main/imgs/image-20231124191748247.png?raw=true" alt="image-20231124191748247" style="zoom:50%;" />

#### 2.2 Login Page

<img src="https://github.com/stoneyezhenxu/imgHosting/blob/main/imgs/image-20231124192401321.png?raw=true" alt="image-20231124192401321" style="zoom:50%;" />

#### 2.3 Dashboard Page

![image-20231124194208364](https://github.com/stoneyezhenxu/imgHosting/blob/main/imgs/image-20231124194208364.png?raw=true)



#### 2.4 Upload Page 

![image-20231124194523468](https://github.com/stoneyezhenxu/imgHosting/blob/main/imgs/image-20231124194523468.png?raw=true)

#### 2.5 File All Versions Page

![image-20231124194714919](https://github.com/stoneyezhenxu/imgHosting/blob/main/imgs/image-20231124194714919.png?raw=true)

#### 2.6  File Details Page![image-20231124194925506](https://github.com/stoneyezhenxu/imgHosting/blob/main/imgs/image-20231124194925506.png?raw=true)



## 5. Basic Commands

### 5.1 Setting Up Your Users

- To create a **superuser account**, use this command:

  ```shell
  $ python manage.py createsuperuser
  ```

### 5.2 Type checks

Running type checks with mypy:

```shell
$ mypy propylon_document_manager
```

### 5.3 Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```shell
$ coverage run -m pytest
$ coverage html
$ open htmlcov/index.html
```

### 5.4 Running tests with pytest

```shell
$ pytest
```

