# designSpace
DesignSpace is a Django-powered web application designed for creative professionals, including architects, interior designers, 3D architectural artists, and other designers. The platform serves as a comprehensive hub for finding and posting job opportunities, showcasing portfolios, and connecting with collaborators to create stunning projects.

Overview
DesignSpace provides a seamless workflow for users who can:

Post Jobs: Share job openings or project requirements with detailed descriptions, budgets, and timelines.
Apply for Jobs: Browse available opportunities and submit applications to potential collaborators or clients.
Upload Projects: Showcase completed work to enhance visibility and attract opportunities.
This unified system streamlines the design and collaboration process for users who want to grow their professional networks and bring their creative visions to life.

Key Features
Unified User Role: A single user type capable of posting jobs, applying to opportunities, and uploading projects.
Job Listings: Create and manage detailed job posts with clear specifications for potential applicants.
Application Workflow: Submit applications for posted jobs and manage responses efficiently.
Portfolio Showcase: Upload projects to build a professional portfolio that demonstrates skills and expertise.
Notifications: Stay informed with real-time notifications for job applications, approvals, and updates.
Dashboard: Manage all activities, including jobs, applications, and portfolio uploads, in one centralized dashboard.

Technology Stack
Backend: Django & Django REST Framework for a robust and secure backend.
Frontend: HTML, CSS, JavaScript, with responsive design for a user-friendly experience across devices.
Database: PostgreSQL (or SQLite for development) for reliable and efficient data management.
Authentication: Django's authentication system with potential for OAuth integration (e.g., Google, LinkedIn) for simplified sign-ups.

Future Enhancements
Messaging System: Enable direct communication between users for seamless collaboration.
Review & Rating System: Allow users to rate and review collaborators after completing projects, fostering trust and credibility.
Payment Integration: Add a secure payment gateway to facilitate smooth transactions between users.

Getting Started
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

Contributions
We welcome contributions from developers and designers alike! If you have ideas for improvements or want to report issues, please feel free to open an issue or submit a pull request.
