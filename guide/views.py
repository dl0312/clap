from django.shortcuts import render

def post_list(request):
    return render(request, 'guide/post_list.html', {})