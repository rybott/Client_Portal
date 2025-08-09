from django.shortcuts import render, redirect, get_object_or_404
from .forms import CaseIntakeForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods, require_POST
from .forms import LawyerInlineForm, TaskForm
from .models import Lawyer, Case, CaseNote


def main(request):
    context = {}
    return render(request,'home.html', context)


def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    task_filter = request.GET.get("task_filter", "todo")

    if task_filter == "complete":
        tasks = case.tasks.filter(status="complete")
    else:
        tasks = case.tasks.exclude(status="complete")

    notes = case.notes.all()

    context = {
        "case": case,
        "notes": notes,
        "tasks": tasks,
        "task_filter": task_filter,
    }
    return render(request, "case.html", context)

def case_intake(request):
    if request.method == 'POST':
        form = CaseIntakeForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.plaintiff_lawyer_id = request.POST.get("plaintiff_lawyer")
            case.defense_lawyer_id = request.POST.get("defense_lawyer")
            case.save()
            return redirect('case_list')  # or wherever
    else:
        form = CaseIntakeForm()

    return render(request, 'intake_form.html', {'form': form})



@require_http_methods(["GET", "POST"])
def lawyer_create_form(request):
    if request.method == 'POST':
        form = LawyerInlineForm(request.POST)
        if form.is_valid():
            new_lawyer = form.save()

            return HttpResponse(
                f"""
                <script>
                    const newOption = new Option("{new_lawyer.name}", "{new_lawyer.id}", true, true);
                    document.querySelector('select[name="{request.GET.get("side")}_lawyer"]').appendChild(newOption);
                </script>
                """
            )
    else:
        form = LawyerInlineForm()

    return render(request, 'partials/lawyer_form.html', {
        'form': form,
        'side': request.GET.get('side', 'plaintiff'),
    })


def lawyer_autocomplete(request):
    query = request.GET.get("plaintiff_lawyer_search") or request.GET.get("defense_lawyer_search")
    matches = []

    if query:
        matches = Lawyer.objects.filter(name__icontains=query).order_by('name')[:10]

    html = render_to_string("partials/lawyer_autocomplete_results.html", {
        "lawyers": matches,
        "input_id": "plaintiff-lawyer-id" if "plaintiff_lawyer_search" in request.GET else "defense-lawyer-id"
    })

    return HttpResponse(html)

@require_POST
def case_note_create(request, case_id):
    case = get_object_or_404(Case, pk=case_id)
    note_text = request.POST.get('note_text', '').strip()

    if note_text:
        new_note = CaseNote.objects.create(case=case, note_text=note_text)

        # Return just one note (partial), not the full list
        return render(request, 'partials/note_single.html', {
            'note': new_note
        })

    return HttpResponse(status=204)  # No content if note_text was empty

def case_tasks_list(request, pk):
    case = get_object_or_404(Case, pk=pk)
    view_mode = request.GET.get("view", "todo")

    if view_mode == "complete":
        tasks = case.tasks.filter(completed=True).order_by("-due_date")
    else:
        tasks = case.tasks.filter(completed=False).order_by("due_date")

    return render(request, "partials/task_list.html", {"tasks": tasks})

def task_create_form(request, pk):
    case = get_object_or_404(Case, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.case = case
            task.save()
            return HttpResponse(
                f"""
                <script>
                  location.reload();
                </script>
                """
            )
    else:
        form = TaskForm()

    return render(request, "partials/task_form.html", {"form": form})


def task_modal_create(request, pk):
    case = get_object_or_404(Case, pk=pk)
    view_mode = request.GET.get("view", "todo")

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.case = case
            task.save()

            # Recompute the list for the active tab
            if view_mode == "complete":
                tasks = case.tasks.filter(status="complete").order_by("-end_time")
            else:
                tasks = case.tasks.exclude(status="complete").order_by("end_time")

            return render(request, "partials/task_list.html", {"tasks": tasks})

        # If invalid, re-render the modal with errors
        return render(
            request,
            "partials/task_modal_form.html",
            {"form": form, "case": case, "view_mode": view_mode, "mode": "create"},
            status=400,
        )

    # GET → just show the empty modal
    form = TaskForm()
    return render(
        request,
        "partials/task_modal_form.html",
        {"form": form, "case": case, "view_mode": view_mode, "mode": "create"},
    )