# IT Company Task Manager

A **Django-based project** designed to simplify task management processes in IT companies.

## Features

* **Task Management:** Create, edit, delete, and prioritize tasks directly from the website interface.
* **Status Monitoring:** Keep track of task statuses (e.g., **_Pending_**, **_Completed_**).
* **User Authentication:** Login and registration functionality for Workers.
* **Admin Panel:** Powerful admin panel for advanced managing.

## System Requirements

* **Python:** 3.11 or newer.
* **Operating System:** Compatible with Linux, macOS, and Windows.

## Getting started

Follow these steps to set up and run the project locally:

1. Clone the repository:
    ```shell
    git clone https://github.com/vladyslav-tmf/it-company-task-manager.git
    cd it-company-task-manager
    ```
2. Create and activate a virtual environment:
    - For Linux/Mac:
      ```shell
      python3 -m venv venv
      source venv/bin/activate
      ```
    - For Windows:
      ```shell
      python -m venv venv
      venv\Scripts\activate
      ```
3. Install dependencies:
    ```shell
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the root directory of the project (look at the `.env.sample`).
Replace `<email>` with your email address and `<password>` with the corresponding password.
5. Apply migrations to set up the database:
    ```shell
    python manage.py migrate
    ```
6. Load example data (optional):
    ```shell
    python manage.py loaddata dataset.json
    ```
7. Start the development server:
    ```shell
    python manage.py runserver
    ```
8. Open your browser and visit: [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Demo

Here’s a preview of the website interface:

![Website Interface](demo.png)

## Testing

To run the automated tests:
```shell
python manage.py test
```
