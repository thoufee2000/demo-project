from django.shortcuts import render
from shop.models import Product
from django.db.models import Q

def search_product(request):
        p=None
        s=''
        if (request.method == 'POST'):
            s=request.POST['s']
            if s:
                p=Product.objects.filter(name__icontains=s)
        return render(request,'search.html',{'p':p,'s':s})


