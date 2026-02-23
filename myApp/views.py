import json
import time

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

try:
    import razorpay
except Exception:
    razorpay = None

from .models import Certificate, Education, Project
from .razorpay_config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

HARD_CODED_PROJECT_ASSETS = {
    "arya-z-tech": {
        "image_path": "/static/images/projects/img/arya-z-tech.png",
        "source_code_url": "/static/source_code/arya-z-tech.zip",
    },
    "old-portfolio": {
        "image_path": "/static/images/projects/img/portfolio.png",
        "source_code_url": "/static/source_code/portfolio01.zip",
    },
    "new-portfolio": {
        "image_path": "/static/images/projects/img/new-portfolio.png",
        "source_code_url": "/static/source_code/myPortfolio_2025.zip",
    },
    "school-management-system": {
        "image_path": "/static/images/projects/img/school.png",
        "source_code_url": "",
    },
    "agro-trade-portal": {
        "image_path": "/static/images/projects/img/agrotrade.png",
        "source_code_url": "/static/source_code/agro-trade-portal.zip",
    },
}

FALLBACK_EDUCATION = [
    {
        "title": "Primary Schooling",
        "institution": "Holy Child Convent High School",
        "date_range": "UKG - Class 5 (Till 2015)",
        "description": (
            "Started early education from Holy Child Convent High School from UKG to Class 2. "
            "Completed Class 3 from Rastra Pita Mahatma Gandhi Bal Vidyalaya. "
            "Then attended Class 4 and 5 at a Government School in my village (Madhya Pradesh)."
        ),
    },
    {
        "title": "Schooling (Class 6th to 9th)",
        "institution": "Jawahar Navodaya Vidyalaya",
        "date_range": "2015 - 2019",
        "description": "Completed foundational education, focusing on core subjects and overall development.",
    },
    {
        "title": "Class 10th (CBSE)",
        "institution": "Jawahar Navodaya Vidyalaya",
        "date_range": "2020",
        "description": (
            "Passed Class 10th with a strong academic record and participation in co-curricular activities."
        ),
    },
    {
        "title": "Class 12th (PCM + Computer Science)",
        "institution": "Jawahar Navodaya Vidyalaya",
        "date_range": "2022",
        "description": (
            "Completed Higher Secondary Education with major subjects Physics, Chemistry, Mathematics, "
            "and Computer Science."
        ),
    },
    {
        "title": "B.Tech in Computer Science & Engineering",
        "institution": "AKS University",
        "date_range": "2022 - 2026",
        "description": (
            "Currently pursuing undergraduate degree, focusing on software engineering, data structures, "
            "and emerging technologies."
        ),
    },
]

FALLBACK_CERTIFICATES = [
    {
        "title": "Python Bootcamp 2025",
        "issuer": "Code With Harry",
        "issued_date": "November 2025",
        "drive_link": "certificates/Python_from_Scratch_Certificate.pdf",
    },
    {
        "title": "Data Science and AI",
        "issuer": "Code With Harry",
        "issued_date": "October 2025",
        "drive_link": "certificates/Data_Science_CWH.pdf",
    },
    {
        "title": "Junior Software Developer",
        "issuer": "Skill India",
        "issued_date": "November 2024",
        "drive_link": "certificates/Junior_Software_Developer_By_Skill_India.jpg",
    },
    {
        "title": "A Novel Electromagnetic Pulse Repeater Design",
        "issuer": "IC-ASTSDGs",
        "issued_date": "March 2024",
        "drive_link": "certificates/Electromagnetic_Pulse_Repeater.pdf",
    },
    {
        "title": "Data Science & Analytics",
        "issuer": "HP Foundation",
        "issued_date": "October 2024",
        "drive_link": "certificates/Data_Analytics_by_HP.pdf",
    },
    {
        "title": "Code Cubicle Hackathon",
        "issuer": "Geek Room",
        "issued_date": "September 2024",
        "drive_link": "certificates/CubicCode.pdf",
    },
    {
        "title": "ThrillX 1.0 Hackathon",
        "issuer": "AKS University",
        "issued_date": "September 2024",
        "drive_link": "certificates/Thrill-X_By_AKS.pdf",
    },
]

FALLBACK_PROJECTS = [
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
        "image_path": "images/projects/img/arya-z-tech.png",
        "demo_url": "https://aryaztech.vercel.app/",
        "source_code_price_inr": 1,   #1499
        "source_code_zip": "source_code/zip_files/arya-z-tech.zip",
        "source_code_url": "/static/source_code/arya-z-tech.zip",
        "is_featured": True,
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
        "image_path": "images/projects/img/portfolio.png",
        "demo_url": "https://ayushpatelportfolio.netlify.app/",
        "source_code_price_inr": 1,
        "source_code_zip": "source_code/zip_files/portfolio01.zip",
        "source_code_url": "/static/source_code/portfolio01.zip",
        "is_featured": True,
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
        "image_path": "images/projects/img/school.png",
        "demo_url": "https://example.com",
        "source_code_price_inr": 0,
        "source_code_zip": "",
        "source_code_url": "",
        "is_featured": True,
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
        "image_path": "images/projects/img/new-portfolio.png",
        "demo_url": "https://ayushcodespy.vercel.app",
        "source_code_price_inr": 1,
        "source_code_zip": "source_code/zip_files/myPortfolio_2025.zip",
        "source_code_url": "/static/source_code/myPortfolio_2025.zip",
        "is_featured": True,
    },
]


def _apply_project_assets(project):
    slug = project.get("slug", "") if isinstance(project, dict) else getattr(project, "slug", "")
    mapped = HARD_CODED_PROJECT_ASSETS.get(slug)
    if not mapped:
        return project

    if isinstance(project, dict):
        project["image_path"] = mapped.get("image_path", project.get("image_path", ""))
        project["source_code_url"] = mapped.get("source_code_url", project.get("source_code_url", ""))
    else:
        project.image_path = mapped.get("image_path", getattr(project, "image_path", ""))
        project.source_code_url = mapped.get("source_code_url", "")

    return project


def _get_education_items():
    try:
        items = list(Education.objects.all())
        return items or FALLBACK_EDUCATION
    except Exception:
        return FALLBACK_EDUCATION


def _get_certificates():
    try:
        items = list(Certificate.objects.all())
        return items or FALLBACK_CERTIFICATES
    except Exception:
        return FALLBACK_CERTIFICATES


def _get_projects():
    try:
        items = list(Project.objects.all())
        source = items or FALLBACK_PROJECTS
        return [_apply_project_assets(item) for item in source]
    except Exception:
        return [_apply_project_assets(item) for item in FALLBACK_PROJECTS]


def _get_featured_projects():
    try:
        items = list(Project.objects.filter(is_featured=True))
        source = items or [item for item in FALLBACK_PROJECTS if item.get("is_featured")]
        return [_apply_project_assets(item) for item in source]
    except Exception:
        source = [item for item in FALLBACK_PROJECTS if item.get("is_featured")]
        return [_apply_project_assets(item) for item in source]


def _find_project(slug):
    try:
        return _apply_project_assets(Project.objects.get(slug=slug))
    except Project.DoesNotExist:
        for item in FALLBACK_PROJECTS:
            if item.get("slug") == slug:
                return _apply_project_assets(item)
        return None
    except Exception:
        for item in FALLBACK_PROJECTS:
            if item.get("slug") == slug:
                return _apply_project_assets(item)
        return None

def homePage(request):
    education_items = _get_education_items()
    certificates = _get_certificates()
    featured_projects = _get_featured_projects()
    return render(
        request,
        "index.html",
        {
            "education_items": education_items,
            "certificates": certificates,
            "featured_projects": featured_projects,
        },
    )


def projectsPage(request):
    projects = _get_projects()
    return render(request, "projects.html", {"projects": projects})


def projectDetail(request, slug):
    project = _find_project(slug)
    if not project:
        raise Http404("Project not found")
    return render(
        request,
        "project_detail.html",
        {
            "project": project,
            "razorpay_key_id": RAZORPAY_KEY_ID,
        },
    )


@csrf_exempt
@require_POST
def create_razorpay_order(request, slug):
    if razorpay is None:
        return JsonResponse({"error": "Razorpay SDK not installed"}, status=500)

    key_id = RAZORPAY_KEY_ID
    key_secret = RAZORPAY_KEY_SECRET
    if not key_id or not key_secret:
        return JsonResponse({"error": "Razorpay keys are not configured"}, status=500)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        payload = {}
    buyer_email = (payload.get("email") or "").strip()
    if not buyer_email or "@" not in buyer_email:
        return JsonResponse({"error": "Valid email is required"}, status=400)

    project = _find_project(slug)
    if not project:
        return JsonResponse({"error": "Project not found"}, status=404)

    if isinstance(project, dict):
        price_inr = int(project.get("source_code_price_inr") or 0)
        project_title = project.get("title", "Project")
        has_source = bool(project.get("source_code_url"))
    else:
        price_inr = int(project.source_code_price_inr or 0)
        project_title = project.title
        has_source = bool(getattr(project, "source_code_url", ""))
    if price_inr <= 0:
        return JsonResponse({"error": "Invalid price"}, status=400)
    if not has_source:
        return JsonResponse({"error": "Source code file not available"}, status=400)

    client = razorpay.Client(auth=(key_id, key_secret))
    order = client.order.create(
        {
            "amount": price_inr * 100,
            "currency": "INR",
            "receipt": f"{slug}-{int(time.time())}",
            "payment_capture": 1,
            "notes": {"buyer_email": buyer_email, "project": project_title},
        }
    )

    return JsonResponse(
        {
            "order_id": order.get("id"),
            "amount": order.get("amount"),
            "currency": order.get("currency"),
            "project": project_title,
            "buyer_email": buyer_email,
        }
    )


@csrf_exempt
@require_POST
def verify_razorpay_payment(request):
    if razorpay is None:
        return JsonResponse({"error": "Razorpay SDK not installed"}, status=500)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        payload = {}

    payment_id = payload.get("payment_id")
    order_id = payload.get("order_id")
    signature = payload.get("signature")
    buyer_email = (payload.get("email") or "").strip()
    project_slug = payload.get("project_slug")

    if not all([payment_id, order_id, signature, buyer_email, project_slug]):
        return JsonResponse({"error": "Missing payment details"}, status=400)

    key_id = RAZORPAY_KEY_ID
    key_secret = RAZORPAY_KEY_SECRET
    if not key_id or not key_secret:
        return JsonResponse({"error": "Razorpay keys are not configured"}, status=500)

    client = razorpay.Client(auth=(key_id, key_secret))
    try:
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
        )
    except Exception:
        return JsonResponse({"error": "Payment verification failed"}, status=400)

    project = _find_project(project_slug)
    if not project:
        return JsonResponse({"error": "Project not found"}, status=404)

    if isinstance(project, dict):
        project_title = project.get("title", "Project")
        source_code_url = project.get("source_code_url", "")
    else:
        project_title = project.title
        source_code_url = getattr(project, "source_code_url", "")

    if not source_code_url:
        _notify_admin(
            project_title,
            buyer_email,
            payment_id,
            order_id,
            "Source code URL missing",
        )
        return JsonResponse(
            {"error": "Payment received, but source URL is missing. We will contact you."},
            status=500,
        )

    try:
        _send_purchase_emails(project_title, buyer_email, payment_id, order_id, source_code_url)
    except Exception as err:
        return JsonResponse(
            {"error": f"Email failed: {err}"},
            status=500,
        )

    return JsonResponse({"status": "success"})


def _send_purchase_emails(project_title, buyer_email, payment_id, order_id, source_code_url):
    if source_code_url.startswith("/"):
        base_url = (getattr(settings, "SITE_URL", "") or "").rstrip("/")
        source_code_url = f"{base_url}{source_code_url}" if base_url else source_code_url

    subject = f"Your source code - {project_title}"
    context = {
        "project_title": project_title,
        "buyer_email": buyer_email,
        "payment_id": payment_id,
        "order_id": order_id,
        "source_code_url": source_code_url,
        "site_url": getattr(settings, "SITE_URL", ""),
        "logo_url": getattr(settings, "EMAIL_LOGO_URL", ""),
        "sender_name": "Ayush Patel",
    }
    html_body = render_to_string("emails/purchase_email.html", context)
    text_body = strip_tags(html_body)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[buyer_email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)

    _notify_admin(project_title, buyer_email, payment_id, order_id, "Source link sent to buyer")


def _notify_admin(project_title, buyer_email, payment_id, order_id, status_note):
    admin_email = getattr(settings, "PORTFOLIO_ADMIN_EMAIL", "") or settings.DEFAULT_FROM_EMAIL
    if not admin_email:
        return

    subject = f"New Project Purchase - {project_title}"
    context = {
        "project_title": project_title,
        "buyer_email": buyer_email,
        "payment_id": payment_id,
        "order_id": order_id,
        "status_note": status_note,
        "site_url": getattr(settings, "SITE_URL", ""),
        "logo_url": getattr(settings, "EMAIL_LOGO_URL", ""),
        "sender_name": "Ayush Patel",
    }
    html_body = render_to_string("emails/admin_notification.html", context)
    text_body = strip_tags(html_body)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[admin_email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)
