from django.shortcuts import render


def test(request):
    context = {
        'name': '',
    }
    return render(request, 'register.html', context)
