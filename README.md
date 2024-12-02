# IT Company Task Manager

A **Django-based project** designed to simplify task management processes in IT companies.

## Features

* **Task Management:** Create, edit, delete, and prioritize tasks directly from the website interface.
* **Status Monitoring:** Keep track of task statuses (e.g., **_Pending_**, **_Completed_**).
* **User Authentication:** Login and registration functionality for Workers.
* **Admin Panel:** Powerful admin panel for advanced managing.
* **Email Confirmation:** Send a confirmation link to the user's email for account activation.
* **Localization Support:** Switch the language of the website interface.

## System Requirements

* **Python:** 3.11 or newer.
* **Operating System:** Compatible with Linux, macOS, and Windows.

## Environment Variables

The project requires certain environment variables to function properly. These should be defined in a `.env` file located in the root directory of the project. Below is a list of the key environment variables:

- `EMAIL_HOST_USER`: The email address used for sending emails.
- `EMAIL_HOST_PASSWORD`: The password for the specified email address.

Create a `.env` file as shown in the `.env.sample` and replace `<email>` and `<password>` with your actual values.

```dotenv
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password
```

Ensure that the `.env` file is not included in your version control system (e.g., Git) as it contains sensitive information.

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
4. Apply migrations to set up the database:
    ```shell
    python manage.py migrate
    ```
5. Load example data (optional):
    ```shell
    python manage.py loaddata dataset.json
    ```
6. Compile translation files (if using localization):
    ```shell
    python manage.py compilemessages -i "venv*"
    ```
    This command compiles `.po` files into `.mo` files, ignoring directory `venv`.
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

## Additional Resources

The front-end of this project utilizes a Bootstrap template.

- **Template Name**: Soft UI Design System
- **Author**: © Creative Tim - Coded by AppSeed
- **Source**: [Link to Official Website](https://app-generator.dev/product/soft-ui-dashboard/django/)
- **License**: [View License](https://www.creative-tim.com/license)

This template provides the base styling and layout, customized to fit the needs of this project.
