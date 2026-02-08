from django.core.management.base import BaseCommand

from myApp.models import Certificate, Education, Project


class Command(BaseCommand):
    help = "Seed portfolio data (education, certificates, projects)."

    def handle(self, *args, **options):
        education_data = [
            {
                "title": "Primary Schooling",
                "institution": "Holy Child Convent High School",
                "date_range": "UKG - Class 5 (Till 2015)",
                "description": (
                    "Started early education from Holy Child Convent High School from UKG to Class 2. "
                    "Completed Class 3 from Rastra Pita Mahatma Gandhi Bal Vidyalaya. "
                    "Then attended Class 4 and 5 at a Government School in my village (Madhya Pradesh)."
                ),
                "order": 1,
            },
            {
                "title": "Schooling (Class 6th to 9th)",
                "institution": "Jawahar Navodaya Vidyalaya",
                "date_range": "2015 - 2019",
                "description": (
                    "Completed foundational education, focusing on core subjects and overall development."
                ),
                "order": 2,
            },
            {
                "title": "Class 10th (CBSE)",
                "institution": "Jawahar Navodaya Vidyalaya",
                "date_range": "2020",
                "description": (
                    "Passed Class 10th with a strong academic record and participation in co-curricular activities."
                ),
                "order": 3,
            },
            {
                "title": "Class 12th (PCM + Computer Science)",
                "institution": "Jawahar Navodaya Vidyalaya",
                "date_range": "2022",
                "description": (
                    "Completed Higher Secondary Education with major subjects Physics, Chemistry, "
                    "Mathematics, and Computer Science."
                ),
                "order": 4,
            },
            {
                "title": "B.Tech in Computer Science & Engineering",
                "institution": "AKS University",
                "date_range": "2022 - 2026",
                "description": (
                    "Currently pursuing undergraduate degree, focusing on software engineering, data structures, "
                    "and emerging technologies."
                ),
                "order": 5,
            },
        ]

        cert_data = [
            {
                "title": "Python Bootcamp 2025",
                "issuer": "Code With Harry",
                "issued_date": "November 2025",
                "drive_link": "certificates/Python_from_Scratch_Certificate.pdf",
                "order": 1,
            },
            {
                "title": "Data Science and AI",
                "issuer": "Code With Harry",
                "issued_date": "October 2025",
                "drive_link": "certificates/Data_Science_CWH.pdf",
                "order": 2,
            },
            {
                "title": "Junior Software Developer",
                "issuer": "Skill India",
                "issued_date": "November 2024",
                "drive_link": "certificates/Junior_Software_Developer_By_Skill_India.jpg",
                "order": 3,
            },
            {
                "title": "A Novel Electromagnetic Pulse Repeater Design",
                "issuer": "IC-ASTSDGs",
                "issued_date": "March 2024",
                "drive_link": "certificates/Electromagnetic_Pulse_Repeater.pdf",
                "order": 4,
            },
            {
                "title": "Data Science & Analytics",
                "issuer": "HP Foundation",
                "issued_date": "October 2024",
                "drive_link": "certificates/Data_Analytics_by_HP.pdf",
                "order": 5,
            },
            {
                "title": "Code Cubicle Hackathon",
                "issuer": "Geek Room",
                "issued_date": "September 2024",
                "drive_link": "certificates/CubicCode.pdf",
                "order": 6,
            },
            {
                "title": "ThrillX 1.0 Hackathon",
                "issuer": "AKS University",
                "issued_date": "September 2024",
                "drive_link": "certificates/Thrill-X_By_AKS.pdf",
                "order": 7,
            },
        ]

        projects_data = [
            {
                "slug": "arya-z-tech",
                "title": "ARYA-Z-TECH",
                "short_description": (
                    "A business website offering website development and deployment services, built using "
                    "HTML, CSS, JS, Flask, and hosted on Vercel."
                ),
                "long_description": (
                    "ARYA-Z-TECH is a clean business website built to showcase services, highlight credibility, "
                    "and convert visitors into leads. It focuses on performance, strong CTAs, and a professional look."
                ),
                "tech_stack": ["HTML", "CSS", "JavaScript", "Flask"],
                "highlights": ["Responsive layout", "Service-focused landing pages", "Deployed on Vercel"],
                "image_path": "images/projects/arya-z-tech.png",
                "demo_url": "https://aryaztech.vercel.app/",
                "source_code_price_inr": 1499,
                "source_code_zip": "/projects/zip_files/dummy.zip",
                "is_featured": True,
                "order": 1,
            },
            {
                "slug": "old-portfolio",
                "title": "Old Portfolio",
                "short_description": (
                    "This was my earlier portfolio showcasing my journey, skills, and work using simple HTML, "
                    "CSS, and Bootstrap layout."
                ),
                "long_description": (
                    "This portfolio was my first polished personal site. It focuses on clarity, quick navigation, "
                    "and a simple layout to highlight projects, skills, and contact details."
                ),
                "tech_stack": ["HTML", "CSS", "Bootstrap"],
                "highlights": ["Simple and clean layout", "Fast load times", "Mobile-friendly"],
                "image_path": "images/projects/portfolio.png",
                "demo_url": "https://ayushpatelportfolio.netlify.app/",
                "source_code_price_inr": 999,
                "source_code_zip": "/projects/zip_files/dummy.zip",
                "is_featured": True,
                "order": 2,
            },
            {
                "slug": "school-management-system",
                "title": "School Management System",
                "short_description": (
                    "A complete Django-based school system to manage students, teachers, attendance, admissions, "
                    "fees, and more."
                ),
                "long_description": (
                    "A full-featured school management system that handles admissions, attendance, fees, and "
                    "reporting. It includes admin dashboards, role-based access, and data exports."
                ),
                "tech_stack": ["Django", "Python", "SQLite", "HTML", "CSS"],
                "highlights": ["Admin dashboards", "Attendance and fee tracking", "Role-based access"],
                "image_path": "images/projects/school.png",
                "demo_url": "https://example.com",
                "source_code_price_inr": 2999,
                "source_code_zip": "/projects/zip_files/dummy.zip",
                "is_featured": True,
                "order": 3,
            },
            {
                "slug": "new-portfolio",
                "title": "New Portfolio",
                "short_description": (
                    "This portfolio you're viewing now, crafted with advanced UI, modern effects, Swiper slider, "
                    "and highly optimized sections."
                ),
                "long_description": (
                    "My latest portfolio with modern UI effects, animated sections, sliders, and a clean layout. "
                    "It is designed to be bold, readable, and easy to navigate."
                ),
                "tech_stack": ["Django", "HTML", "CSS", "JavaScript", "Swiper"],
                "highlights": ["Modern UI effects", "Responsive sections", "Optimized performance"],
                "image_path": "images/projects/new-portfolio.png",
                "demo_url": "https://example.com",
                "source_code_price_inr": 1999,
                "source_code_zip": "/projects/zip_files/dummy.zip",
                "is_featured": True,
                "order": 4,
            },
        ]

        for item in education_data:
            Education.objects.update_or_create(
                title=item["title"],
                date_range=item["date_range"],
                defaults=item,
            )

        for item in cert_data:
            Certificate.objects.update_or_create(
                title=item["title"],
                issuer=item["issuer"],
                issued_date=item["issued_date"],
                defaults=item,
            )

        for item in projects_data:
            Project.objects.update_or_create(
                slug=item["slug"],
                defaults=item,
            )

        self.stdout.write(self.style.SUCCESS("Seeded education, certificates, and projects."))
