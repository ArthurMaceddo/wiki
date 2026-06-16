from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found"})
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })

def search(request):
    query = request.GET.get('q', '')
    if util.get_entry(query):
        return redirect('entry', title=query)
    
    # Busca por substring
    entries = util.list_entries()
    results = [e for e in entries if query.lower() in e.lower()]
    return render(request, "encyclopedia/search.html", {"results": results, "query": query})

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {"message": "A page with that title alrady exist"})
        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/new_page.html")

def edit(request, title):
    if request.method == "POST":
        util.save_entry(title, request.POST.get("content"))
        return redirect('entry', title=title)
    
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {"title": title, "content": content})

def random_page(request):
    entries = util.list_entries()
    return redirect('entry', title=random.choice(entries))