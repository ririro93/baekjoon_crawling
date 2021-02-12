from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

from celery.result import AsyncResult
from tasks.sample_tasks import create_task

def home_page(request):
    # show home page of the whole website
    context = {'page': 'home'}
    return render(request, 'home_page.html', context)

# celery test
@csrf_exempt
def run_task(request):
    if request.POST:
        task_type = request.POST.get("type")
        task = create_task.delay(int(task_type))
        return JsonResponse({"task_id": task.id}, status=202)


@csrf_exempt
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)