import json
import logging
import time
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

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

FALLBACK_DATA_DIR = Path(__file__).resolve().parent / "fallback_data"
logger = logging.getLogger(__name__)
_fallback_mtimes = {}


def _read_fallback_json(filename):
    file_path = FALLBACK_DATA_DIR / filename
    if settings.DEBUG:
        current_mtime = file_path.stat().st_mtime
        previous_mtime = _fallback_mtimes.get(filename)
        if previous_mtime is None:
            logger.info("Loaded fallback data file: %s", file_path.name)
        elif previous_mtime != current_mtime:
            logger.info("Detected change in fallback data file: %s", file_path.name)
        _fallback_mtimes[filename] = current_mtime
    with file_path.open(encoding="utf-8") as file_obj:
        return json.load(file_obj)


@lru_cache(maxsize=None)
def _load_fallback_json_cached(filename):
    return _read_fallback_json(filename)


def _load_fallback_json(filename):
    if settings.DEBUG:
        return _read_fallback_json(filename)
    return _load_fallback_json_cached(filename)


def _get_fallback_education():
    return deepcopy(_load_fallback_json("education.json"))


def _get_fallback_certificates():
    return deepcopy(_load_fallback_json("certificates.json"))


def _get_fallback_projects():
    return deepcopy(_load_fallback_json("projects.json"))


@lru_cache(maxsize=1)
def _get_fallback_project_map():
    return {item.get("slug"): item for item in _load_fallback_json_cached("projects.json")}


def _load_fallback_project_map():
    if settings.DEBUG:
        return {item.get("slug"): item for item in _load_fallback_json("projects.json")}
    return _get_fallback_project_map()


def _static_path_exists(relative_path):
    if not relative_path:
        return False
    normalized_path = relative_path.lstrip("/").removeprefix("static/")
    return (Path(settings.BASE_DIR) / "static" / normalized_path).exists()


def _resolve_project_image_path(slug, image_path):
    if image_path and image_path.startswith(("http://", "https://")):
        return image_path

    if image_path and image_path.startswith("/static/"):
        if _static_path_exists(image_path):
            return image_path

    if image_path and not image_path.startswith("/"):
        if _static_path_exists(image_path):
            return image_path

    slug = (slug or "").strip()
    slug_no_dash = slug.replace("-", "")
    candidate_paths = [
        f"images/projects/img/{slug}.png",
        f"images/projects/img/{slug}.jpg",
        f"images/projects/img/{slug}.jpeg",
        f"images/projects/img/{slug_no_dash}.png",
        f"images/projects/img/{slug_no_dash}.jpg",
        f"images/projects/img/{slug_no_dash}.jpeg",
    ]

    if image_path:
        candidate_paths.insert(0, image_path)

    for candidate in candidate_paths:
        if candidate.startswith("/"):
            if _static_path_exists(candidate):
                return candidate
        elif _static_path_exists(candidate):
            return candidate

    logger.warning("No valid image found for project slug '%s'. Using placeholder.", slug)
    return "images/projects/img/project-placeholder.svg"


def _apply_project_assets(project):
    slug = project.get("slug", "") if isinstance(project, dict) else getattr(project, "slug", "")
    mapped = _load_fallback_project_map().get(slug)
    if not mapped:
        if isinstance(project, dict):
            project["image_path"] = _resolve_project_image_path(slug, project.get("image_path", ""))
        else:
            project.image_path = _resolve_project_image_path(slug, getattr(project, "image_path", ""))
        return project

    if isinstance(project, dict):
        if not project.get("image_path"):
            project["image_path"] = mapped.get("image_path", "")
        if not project.get("source_code_url"):
            project["source_code_url"] = mapped.get("source_code_url", "")
        if not project.get("source_code_zip"):
            project["source_code_zip"] = mapped.get("source_code_zip", "")
        project["image_path"] = _resolve_project_image_path(slug, project.get("image_path", ""))
    else:
        if not getattr(project, "image_path", ""):
            project.image_path = mapped.get("image_path", "")
        if not getattr(project, "source_code_url", ""):
            project.source_code_url = mapped.get("source_code_url", "")
        if not getattr(project, "source_code_zip", ""):
            project.source_code_zip = mapped.get("source_code_zip", "")
        project.image_path = _resolve_project_image_path(slug, getattr(project, "image_path", ""))

    return project


def _get_item_value(item, field_name, default=""):
    if isinstance(item, dict):
        return item.get(field_name, default)
    return getattr(item, field_name, default)


def _merge_items(primary_items, fallback_items, key_builder):
    merged = []
    seen_keys = set()

    for item in primary_items + fallback_items:
        item_key = key_builder(item)
        if item_key in seen_keys:
            continue
        seen_keys.add(item_key)
        merged.append(item)

    return sorted(
        merged,
        key=lambda item: (
            int(_get_item_value(item, "order", 0) or 0),
            str(_get_item_value(item, "title", _get_item_value(item, "slug", ""))),
        ),
    )


def _get_education_items():
    try:
        items = list(Education.objects.all())
        fallback_items = _get_fallback_education()
        return _merge_items(
            items,
            fallback_items,
            lambda item: (
                _get_item_value(item, "title"),
                _get_item_value(item, "institution"),
                _get_item_value(item, "date_range"),
            ),
        )
    except Exception:
        return _get_fallback_education()


def _get_certificates():
    try:
        items = list(Certificate.objects.all())
        fallback_items = _get_fallback_certificates()
        return _merge_items(
            items,
            fallback_items,
            lambda item: (
                _get_item_value(item, "title"),
                _get_item_value(item, "issuer"),
                _get_item_value(item, "issued_date"),
            ),
        )
    except Exception:
        return _get_fallback_certificates()


def _get_projects():
    try:
        items = list(Project.objects.all())
        source = _merge_items(
            items,
            _get_fallback_projects(),
            lambda item: _get_item_value(item, "slug"),
        )
        return [_apply_project_assets(item) for item in source]
    except Exception:
        return [_apply_project_assets(item) for item in _get_fallback_projects()]


def _get_featured_projects():
    try:
        items = list(Project.objects.filter(is_featured=True))
        source = _merge_items(
            items,
            [item for item in _get_fallback_projects() if item.get("is_featured")],
            lambda item: _get_item_value(item, "slug"),
        )
        return [_apply_project_assets(item) for item in source]
    except Exception:
        source = [item for item in _get_fallback_projects() if item.get("is_featured")]
        return [_apply_project_assets(item) for item in source]


def _find_project(slug):
    try:
        return _apply_project_assets(Project.objects.get(slug=slug))
    except Project.DoesNotExist:
        for item in _get_fallback_projects():
            if item.get("slug") == slug:
                return _apply_project_assets(item)
        return None
    except Exception:
        for item in _get_fallback_projects():
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
