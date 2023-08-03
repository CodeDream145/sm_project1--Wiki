from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    md_content = util.get_entry(title)
    
    if md_content :
        html_content = markdown2.markdown(md_content)
    else:
        html_content = None

    return render(request, "encyclopedia/entry_page.html", {
        "content": html_content,
        "title": title 
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    print(random_entry)
    return HttpResponseRedirect(f"wiki/{random_entry}")

def search(request):
    word = str(request.GET["q"])
    entries = util.list_entries()
    search_result =[]

    for entry in entries:
        if word.lower() == entry.lower():
            return HttpResponseRedirect(f"/wiki/{word}")
        elif word.lower() in entry.lower():
            search_result.append(entry)

    return render(request, "encyclopedia/result_page.html", {
        "entries": search_result
    })

def new_entry(request):
    if request.method == "POST":
        title = str(request.POST["title"])
        content = str(request.POST["content"])
        
        entries = util.list_entries()
        
        if not title and not content:
            return render(request, "encyclopedia/new_entry.html", {
                "content": content,
                "title": title,
                "error_msg_c": "Must Provide Content",
                "error_msg_t": "Must Provide Title"
            })

        if not title:
            return render(request, "encyclopedia/new_entry.html", {
                "content": content,
                "error_msg_t": "Must Provide Title"
            })
        
        if not content:
            return render(request, "encyclopedia/new_entry.html", {
                "title": title,
                "error_msg_c": "Must Provide Content"
            })



        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/new_entry.html", {
                    "title": title,
                    "content": content,
                    "error_msg_t": "Title already Exists"
                })
        
        util.save_entry(title, content)

        return HttpResponseRedirect(f"/wiki/{title}")
    
    return render(request, "encyclopedia/new_entry.html")

def edit_entry(request,title):

    if request.method == "POST":
        content = request.POST["content"]

        if not content:
            return render(request, "encyclopedia/new_entry.html", {
                "title": title,
                "error_msg_c": "Must Provide Content"
            })

        util.save_entry(title, content)
        return redirect(f"/wiki/{title}")
    
    else:
        entry = util.get_entry(title)

        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "content": entry
        })