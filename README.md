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

Clone the repository and navigate into it:

```bash
git clone https://github.com/fatemesoleimani/sanaap-backend-challenge-api.git
```
