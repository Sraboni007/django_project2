from django.shortcuts import render, redirect
from .models import Task, Book, Author
from django.http import HttpResponse, JsonResponse
from .form import TaskForm
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

# Create your views here.

def task_list(request):
    tasks = Task.objects.all()
    completed = request.GET.get("completed")
    if completed == '1':
        tasks = tasks.filter(completed=True)
    elif completed == '0':
        tasks = tasks.filter(completed=False)
    return render(request, 'task_list.html', {"tasks":tasks})

def task_details(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'task_detail.html', {"task":task})

def add_task(request):
    _title = "Let's have dinner together X"
    _description = "Dinner invitation at Chef Table X"
    _completed = False
    _due_date = "2024-08-28"
    task = Task(title=_title, description=_description, completed=_completed)
    task.save() 
    #return HttpResponse("Adding Task");
    return redirect('task_list')

def delete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.delete()
        return redirect('task_list')
    except Task.DoesNotExist:
        return HttpResponse("Task does not exist")
    
    
def update_task(request):
    task=Task.objects.get(pk=5)
    task.title = "This is a modified title";  
    task.save() 
    return redirect('task_list') 

def add_task_form(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect("task_list")
        
    else:    
       form = TaskForm()
       return render(request,"add_task.html", {"formx":form})
   
def task_by_user_id(request, user_id):
    #tasks = Task.objects.filter(user_id=user_id).values()
    #return JsonResponse({"tasks": list(tasks)}) 
      
    #tasks = Task.objects.filter(user_id=user_id)
    #result = []
    #for task in tasks:
        #result.append({
            #"title": task.title,
            #"description": task.description,
            #"completed": task.completed,
            #"created_at": task.created_at,
            #"due_date": task.due_date,
            #"use_id": task.user.id,
            #"user": task.user.username
        #})
        
    #return JsonResponse({"tasks":  result})    
    user = User.objects.get(pk=user_id)
    tasks = user.tasks.all().values()
    return JsonResponse({"tasks": list(tasks)})

def all_books(request):
    books = Book.objects.all().values()
    #return JsonResponse({"books":list(books)})
    result = []
    for book in books:
        result.append({
            "title":book.title,
        "description":book.description,
        "publication_date":book.publication_date,
        "author":f'{book.author.first_name} {book.author.last_name}'
            
        })
    return JsonResponse({"books":result})

def book(request, book_id):
    book = Book.objects.get(pk=book_id)
    book_details = {
        "title":book.title,
        "description":book.description,
        "publication_date":book.publication_date,
        "author":f'{book.author.first_name} {book.author.last_name}'
    }
    return JsonResponse({"book": book_details})

def author(request, author_id):
    author = Author.objects.get(pk=author_id)
    author_details= {
        "first_name":author.first_name,
        "last_name":author.last_name,
        "bio":author.bio,
        "book":author.books.title
    }
    return JsonResponse({"author": author_details})

