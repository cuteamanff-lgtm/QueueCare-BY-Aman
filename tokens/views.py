from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Token

SERVICES = [
    "College Office – Certificate", "Admission Enquiry",
    "Fee Department", "Document Verification",
]

def _next_number():
    today_prefix = f"A-{timezone.localdate():%y%m%d}-"
    last = Token.objects.filter(token_number__startswith=today_prefix).order_by("-id").first()
    seq = int(last.token_number.rsplit("-", 1)[-1]) + 1 if last else 1
    return f"{today_prefix}{seq:03d}"

def _queue_context():
    waiting = Token.objects.filter(status="WAITING").order_by("-priority", "created_at")
    serving = Token.objects.filter(status="SERVING").order_by("-updated_at").first()
    return waiting, serving

def home(request):
    waiting, serving = _queue_context()
    return render(request, "tokens/home.html", {"waiting_count": waiting.count(), "serving": serving})

def services(request):
    return render(request, "tokens/services.html", {"services": SERVICES})

def about(request):
    return render(request, "tokens/about.html")

def register_token(request):
    token = None
    if request.method == "POST":
        name = request.POST.get("full_name", "").strip()
        mobile = request.POST.get("mobile_number", "").strip()
        service = request.POST.get("service", "")
        priority = request.POST.get("priority") == "on"
        if not name or len(mobile) != 10 or not mobile.isdigit() or service not in SERVICES:
            messages.error(request, "Please enter a valid name, 10-digit mobile number, and service.")
        else:
            token = Token.objects.create(
                token_number=_next_number(), full_name=name, mobile_number=mobile,
                service=service, priority=priority
            )
            messages.success(request, "Your token has been generated.")
    waiting, serving = _queue_context()
    ahead = waiting.filter(created_at__lt=token.created_at).count() if token else 0
    return render(request, "tokens/register.html", {
        "services": SERVICES, "token": token, "people_ahead": ahead,
        "estimated_minutes": max(6, (ahead + 1) * 6)
    })

def live_queue(request):
    waiting, serving = _queue_context()
    next_tokens = waiting[:5]
    today = timezone.localdate()
    completed = Token.objects.filter(status="COMPLETED", updated_at__date=today).count()
    return render(request, "tokens/live.html", {
        "waiting": next_tokens, "waiting_count": waiting.count(),
        "serving": serving, "completed": completed
    })

def staff_login(request):
    if request.user.is_authenticated:
        return redirect("staff_dashboard")
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("staff_dashboard")
        messages.error(request, "Invalid staff credentials.")
    return render(request, "tokens/staff_login.html")

def staff_logout(request):
    logout(request)
    return redirect("home")

@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return redirect("home")
    today = timezone.localdate()
    waiting = Token.objects.filter(status="WAITING").order_by("-priority", "created_at")
    serving = Token.objects.filter(status="SERVING").first()
    completed = Token.objects.filter(status="COMPLETED", updated_at__date=today).count()
    cancelled = Token.objects.filter(status__in=["CANCELLED", "SKIPPED"], updated_at__date=today).count()
    all_tokens = Token.objects.exclude(status__in=["COMPLETED", "CANCELLED", "SKIPPED"]).order_by("-priority", "created_at")
    return render(request, "tokens/dashboard.html", {
        "waiting": waiting, "serving": serving, "completed": completed,
        "cancelled": cancelled, "all_tokens": all_tokens,
        "waiting_count": waiting.count()
    })

@login_required
def token_action(request, token_id, action):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not request.user.is_staff:
        return redirect("home")
    token = get_object_or_404(Token, pk=token_id)
    actions = {"call": "SERVING", "complete": "COMPLETED", "skip": "SKIPPED", "cancel": "CANCELLED"}
    if action not in actions:
        messages.error(request, "Unknown queue action.")
    else:
        if action == "call":
            Token.objects.filter(status="SERVING").update(status="WAITING")
        token.status = actions[action]
        token.save()
        messages.success(request, f"{token.token_number} updated: {token.get_status_display()}.")
    return redirect("staff_dashboard")
