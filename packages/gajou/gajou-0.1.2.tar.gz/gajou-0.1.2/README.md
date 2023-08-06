牙城 

CLI

* BaseCLI - contains method to send command in terminal with logging. Allure can be passed for adding attaches to
  reports.
* CLIResponse - dataclass for CLI response deserialization.
* ReturnCodes - enum with basic CLI return codes.

HTTP

* BaseHTTP - contains all basic HTTP methods with logging. Verifies response status and raises one of errors if status
  is not 2xx. Allure can be passed for adding attaches to reports.
* HTTP errors - set of exceptions for typical HTTP error statuses.

DB
* PostgresHelper - contains all basic commands with logging. Select-command supports simple caching. Can be useful with any query language like Pypika.
* DatabaseError - simple DB exception.
* Singleton - simple implementation of singleton used in DB helper to prevent unnecessary propagation of connections. 