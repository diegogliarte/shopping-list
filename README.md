# Personal Shopping List Application

This is a personal shopping list application built using **FastAPI**. It allows you to manage your shopping items in real-time, with WebSocket functionality to keep the list synchronized across multiple devices. The application is hosted on my **Raspberry Pi** for personal use.

## Features

- **Real-time Updates**: Uses WebSockets to add, edit, and remove items from the shopping list in real-time across multiple devices.
- **Database Support**: Uses SQLite for local data storage, but can be configured to use PostgreSQL or any other supported databases.
- **Environment Variables**: Sensitive information such as JWT secrets and database URLs are stored in a `.env` file for security and flexibility.
- **Lightweight Hosting**: The project is hosted on a Raspberry Pi, making it a simple and efficient solution for personal use.
- 
> **Note**: Currently, there is **no authentication** implemented. Anyone with access to the application URL can view and edit the shopping list.

## Tech Stack

- **FastAPI**: Python web framework used to build the application.
- **Uvicorn**: ASGI server for serving the FastAPI app.
- **SQLite**: Default database used for storing shopping list items.
- **Docker & Docker Compose**: Used for containerizing the application for easy deployment on the Raspberry Pi.
- **WebSockets**: Used to synchronize shopping list changes in real-time.

## Installation

To run this project on your own machine or Raspberry Pi, follow these steps:

### Prerequisites

- **Docker** and **Docker Compose** should be installed on your Raspberry Pi or any other server.
- **Python 3.9+** is required for local development.

### Clone the Repository

```
git clone https://github.com/diegogliarte/shopping-list.git
cd personal-shopping-list
```

### Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./test.db
```

> Make sure to update the `SECRET_KEY` for security purposes.

### Running with Docker Compose

1. Build and run the application using Docker Compose:
   ```
   docker-compose up --build
   ```

2. Access the application in your web browser at `http://localhost:8000`.

## Hosting on Raspberry Pi

This project was specifically designed to be hosted on a **Raspberry Pi** for personal use. The lightweight nature of **FastAPI** combined with **Docker** makes it easy to deploy on resource-constrained devices like the Raspberry Pi.

To deploy it on your Raspberry Pi:

1. Install Docker and Docker Compose on your Raspberry Pi:

2. Clone the project and follow the steps outlined above for using Docker Compose to build and run the app.

## Usage

- **Add/Edit Items**: You can add new shopping list items or edit existing ones. Changes will be synchronized in real-time across all connected devices.
- **Remove Items**: Items can be removed from the list at any time.