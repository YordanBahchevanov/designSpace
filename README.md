# DesignSpace

 DesignSpace is a Django-powered web application tailored for creative professionals, including architects, interior designers, 3D artists, and other designers. The platform provides tools for showcasing your work, sharing insights, and connecting with collaborators to enhance your creative journey.

---

## 1. Overview

**DesignSpace** is your go-to platform for:

- **Uploading Projects**: Showcase completed work to boost your visibility and attract potential collaborators or clients.
- **Writing Articles**: Share insights, expertise, and ideas to engage with the creative community. *(Restricted to users with writer permissions.)*

This streamlined system supports designers looking to grow their networks, display their skills, and exchange knowledge with like-minded professionals.

---

## 2. Platform Features

### Core Functionality

- **Unified User Role**: A single user profile to manage your projects and articles with ease.
- **Home Page**: Your central hub to view and access all projects and articles, offering a dynamic overview of the community.

### Profile Page

A dedicated space to:
- Organize and showcase your uploaded projects.
- Share and manage your published articles.
- Save inspiring projects or articles from other users into personalized folders.

### Project Showcase

- Upload and display your work to build a professional portfolio that highlights your skills.

### Article Publishing

- Write and publish articles to share knowledge and foster engagement in the design community. *(Restricted to users with writer permissions.)*

---

## Technology Stack

- **Backend**:  
  Django & Django REST Framework for a secure and scalable foundation.

- **Frontend**:  
  HTML, CSS, JavaScript for an intuitive and responsive user experience across devices.

- **Database**:  
  PostgreSQL for efficient data management.

- **Authentication**:  
  Django's built-in authentication system ensures user security.

---

## Future Enhancements

- **Messaging System**:  
  Enable direct communication between users for seamless collaboration.

- **Review & Rating System**:  
  Allow users to rate and review projects or articles, fostering credibility and recognition.

- **Advanced Portfolio Features**:  
  Add customizable templates for portfolio displays to better reflect your creative identity.

---

## Getting Started

### Step 1: Clone the Repository
Clone the project repository and navigate into the directory:

```bash
git clone https://github.com/YordanBahchevanov/designSpace.git
cd designSpace
```
### Step 2: Clone the Repository
Create a .env file in the project root directory using the .env.template file for refference:

### Step 3: Install PostgreSQL or Set Up Docker
If PostgreSQL is not installed locally, you can use Docker to set up PostgreSQL. Run the following command:

```bash
docker run --name designspace-db -e POSTGRES_USER=your_database_user \
  -e POSTGRES_PASSWORD=your_database_password -e POSTGRES_DB=your_database_name \
  -p 5432:5432 -d postgres
```
Alternatively, install PostgreSQL using your system's package manager or installer.

### Step 4: Install Dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```
### Step 5: Apply Database Migrations
Run the database migrations to set up the initial schema:

```bash
python manage.py migrate
```
### Step 6: Run the Development Server
Start the development server to test the application:

```bash
python manage.py runserver
```







