from django.contrib import messages
from django.shortcuts import render, HttpResponse,redirect
from .models import Book

# Create your views here.



# FBV -Function Based View

def welcome_page(request):
    return render(request, 'welcome.html')


def show_all_books(request):
    books = Book.objects.filter(is_active = True )     # only active record are shown
    return render(request, 'showbooks.html', {'allbooks': books})

def show_single_book(request, bid): 
    try:
        book_obj = Book.objects.get(id=bid) 
    except Book.DoesNotExist:
        return HttpResponse("Book does not exist..!")
    return render(request=request, template_name="bookdetail.html", context={"book": book_obj})

def common_var(req):
    
        final_dict = req.POST
        print(final_dict)
        book_name = final_dict.get("nm")
        book_price= final_dict.get("pri")
        book_qty= final_dict.get("qty")
        book_is_pub = final_dict.get("ispub")
        return book_name,book_price, book_qty, book_is_pub

def add_single_book(request):
    if request.method == "POST":
        book_name,book_price, book_qty, book_is_pub = common_var(request)
        if book_is_pub =="YES":
            is_pub = True
        else: 
            is_pub = False

        
        Book.objects.create(name = book_name, price = book_price, qty = book_qty, in_published = is_pub)   
        messages.success(request, "Book added successfully")
        return redirect("show_books")   


    elif request.method =="GET":
        return render(request, "addbook.html")   
    
def edit_single_book(request,bid):
    book_object = Book.objects.get(id =bid)
    if request.method =="GET":
        return render(request , "bookedit.html",{"single_book": book_object})
    elif request.method =="POST":
        book_name,book_price, book_qty, book_is_pub = common_var(request)
        if book_is_pub =="YES":
            is_pub = True
        else: 
            is_pub = False

        book_object.name = book_name    # update data in database
        book_object.price = book_price 
        book_object.qty = book_qty 
        book_object.in_published = is_pub

        book_object.save()
        messages.success(request, "Book edited dsuccessfully")
        return redirect("show_books")   



def delete_single_book(request,bid ):
    book_object = Book.objects.get(id =bid)     
    book_object.delete()        # hard delete means delte from database
    return redirect("show_books") 

def soft_delete_single_book(request, bid):
    book_object = Book.objects.get(id =bid)     
    book_object.is_active= False        # soft  delete means flag of isactive false from database
    book_object.save()
    return redirect("show_books") 


def inactive_book(request, bid):
    book_object = Book.objects.get(id =bid)
    books = Book.objects.filter(is_active = False )     # only active record are shown
    return render(request, 'showbooks.html', {'allbooks': books})


#----------------------------form view-----------------------------



from .forms import GeeksForm, BookForm,AddressForm
  
# Create your views here.
# def form_view(request):
#     context ={}
#     context['form']= GeeksForm()
#     return render(request, "test.html", context)


# def form_view(request):
#     context ={}
#     context['form']= BookForm()
#     return render(request, "test.html", context)

def form_view(request):
    context ={}
    context['form']= AddressForm()
    return render(request, "test.html", context)