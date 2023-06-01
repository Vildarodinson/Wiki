from . import util
from django.shortcuts import render, redirect
from django.urls import reverse
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, 'encyclopedia/error.html', {
            'error_message': f'The page "{title}" does not exist.'
        })
    else:
        entry_html = markdown2.markdown(entry)
        edit_url = reverse('edit_page', kwargs={'title': title})
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'entry': entry_html,
            'edit_url': edit_url
        })

def search(request):
    query = request.GET.get('q') if request.method == 'GET' else request.POST.get('q')
    entry = util.get_entry(query)
    if entry:
        return redirect('entry', title=query)
    else:
        matching_entries = util.list_entries_matching_query(query)
        if len(matching_entries) == 1:
            return redirect('entry', title=matching_entries[0])
        else:
            return render(request, "encyclopedia/search_results.html", {
                "query": query,
                "matching_entries": matching_entries
                })

def new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        entry = util.get_entry(title)

        if entry is not None:
            error_message = f'The page "{title}" already exists.'
            return render(request, 'encyclopedia/new_page.html', {
                'error_message': error_message,
                'title': title,
                'content': content
            })
        else:
            util.save_entry(title, content)
            return redirect('entry', title=title)
    else:
        return render(request, 'encyclopedia/new_page.html')


def edit_page(request, title):
    entry = util.get_entry(title)

    if request.method == 'POST':
        content = request.POST.get('content')
        util.save_entry(title, content)
        return redirect('entry', title=title)
    else:
        return render(request, 'encyclopedia/edit_page.html', {
            'title': title,
            'content': entry
        })

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect('entry', title=random_title)

def remove_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        util.delete_entry(title)
        return redirect('index')
    else:
        entries = util.list_entries()
        return render(request, 'encyclopedia/remove_page.html', {
            'entries': entries
        })

