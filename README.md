# Document Management API

A Django REST Framework (DRF) based Document Management API with **role-based permissions** for Admins, Editors, and Viewers.  
Supports **file uploads**, **filters**, **search**, **ordering**, and **pagination**.

---

## Features

- **Role-based access control**
  - **Admin**: Full CRUD access
  - **Editor**: Create and update documents (cannot delete)
  - **Viewer**: Read-only access (list & retrieve)
- **File handling**
  - Upload documents via `multipart/form-data`
  - Automatically replaces old file on update
- **Filters, Search, Ordering**
  - Filter by `title` or `user`
  - Search in document title
  - Ordering by `id`, `title`, `created_at`, `updated_at`
- **Pagination**
  - Supports page and page size query parameters
- **Swagger/OpenAPI Documentation**
  - DRF Spectacular integration for API schema generation

---

## Installation

1. Clone the repository and navigate into it:

```bash
git clone https://github.com/fatemesoleimani/sanaap-backend-challenge-api.git
```
2. Configure Environment Variables

Create and complete your .env file inside the project root.
This file should include all required environment variables (database credentials, secret keys, etc.).

3. Run the Application with Docker

To build and start all services using Docker, run:

```bash
docker-compose up --build
```

Docker will install dependencies, build the containers, and start the application automatically.