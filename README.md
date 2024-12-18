# designSpace
DesignSpace is a Django-powered web application tailored for creative professionals, including architects, interior designers, 3D artists, and other designers. The platform provides tools for showcasing your work, sharing insights, and connecting with collaborators to enhance your creative journey.

# Overview
DesignSpace is your go-to platform for:

  Uploading Projects: Showcase completed work to boost your visibility and attract potential collaborators or clients.

  Writing Articles: Share insights, expertise, and ideas to engage with the creative community.
  This streamlined system supports designers looking to grow their networks, display their skills, and exchange knowledge with like-minded professionals.

# Platform Features

  Core Functionality:
    Unified User Role: A single user profile to manage your projects and articles with ease.
    Home Page: Your central hub to view and access all projects and articles, offering a dynamic overview of the community.
  
  Profile Page: 
    A dedicated space to:
    Organize and showcase your uploaded projects.
    Share and manage your published articles.
    Save inspiring projects or articles from other users into personalized folders.
  
  Project Showcase: 
    Upload and display your work to build a professional portfolio that highlights your skills.
    
  Article Publishing: 
    Write and publish articles to share knowledge and foster engagement in the design community.

# Technology Stack:

  Backend: 
    Django & Django REST Framework for a secure and scalable foundation.
  Frontend: 
    HTML, CSS, JavaScript for an intuitive and responsive user experience across devices.
  Database: 
    PostgreSQL for efficient data management.

# Authentication: 
  Django's built-in authentication system ensures user security.

# Future Enhancements

  Messaging System: 
    Enable direct communication between users for seamless collaboration.
  Review & Rating System: 
    Allow users to rate and review projects or articles, fostering credibility and recognition.
  Advanced Portfolio Features: 
    Add customizable templates for portfolio displays to better reflect your creative identity.

# Getting Started
Clone the repository:

bash
Copy code
git clone https://github.com/YordanBahchevanov/designSpace.git
cd designSpace

Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
python manage.py migrate
python manage.py runserver
