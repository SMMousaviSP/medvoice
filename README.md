# MedVoice

This is simple API, designed to store and retrieve `.wav` audio files. For demonstration purposes only, the `.wav` files are stored in base64 format. This is not practical since the memory can be exhausted quickly.

## Managing the Environment and Dependencies
First install `virtualenv` with pip.
```bash
pip install virtualenv
```

Then create an empty virtual environment.
```bash
virtualenv .venv
```
Note that `.venv` is the name of the virtual environment directory, this
directory is omitted in the `.gitignore` file.

After creating the virtual environment, activate it.

UNIX based Operating Systems (GNU/Linux, macOS, etc.)
```bash
source .venv/bin/activate
```

Windows
```batch
.\venv\Scripts\activate
```

Now you can install the required python packages in the clean environment you
just created.
```bash
pip install -r requirements.txt
```

## Running the Service
After installing the dependencies, you need to crate `config_local.py`. Use the `config_local.py.sample` file as a template. The `config_local.py` will be ignore by `.gitignore` file for security reasons. Then you can go to the `app` directory and run the service by executing the following command.
```bash
python main.py
```

## Running the Tests
You can run the tests by running the `app/test.py` file.
```bash
python test.py
```

## API Documentation
The API documentation is available at `/apidocs` route. If you haven't changed the default port and host, you can access the documentation at `http://localhost:5000/apidocs`.

## Assumptions
It is assumed that the user only wants to store `.wav` files. The API will not accept other file types. There are only two API endpoints, one for posting and the other for getting all of the existing records.

## Notes on possible improvements
- The `.wav` files are stored in base64 format. This is not practical since the memory can be exhausted quickly. The files should be stored in a file system or a database.

- The unit tests are not comprehensive. The tests should be improved by adding more test cases for internal parts of the application like the model.

- Since we are using a basic authentication method, it is better to limit the API with a limiter to prevent brute force attacks.

- Returned error messages can be improved by using `abort` and add error handlers, the readability of the code will be improved.

- Pagination should be added to get all the records endpoint. In case there are a lot of records, the response will be too large.

- More API endpoints are needed to make the API more useful. For example, an endpoint to get a single record by its ID.
