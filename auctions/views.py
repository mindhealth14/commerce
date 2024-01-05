from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from django.template import loader
from .forms import ProductForm, AddCategoryForm, BidsForm,checkForm
from django.core.files.base import ContentFile  # Import ContentFile
from .models import User, Product, Category, Bid, Watchlist, Comment , Winner
from django.db.models import Count, Max
from django.utils import timezone
from django.contrib import messages  # Import messages for feedback
from datetime import timedelta
from django.contrib.auth.decorators import login_required
import requests
from requests.exceptions import RequestException



# Product List

def products(request):
    # get category from the link. I called the request cat when i loop through it
    cates = request.GET.get('cat')
    if cates== None:
        products = Product.objects.all().order_by('-id')
    else:
        products = Product.objects.filter(category__name=cates).order_by('-id')

    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "products": products,
        "categories": categories,
          
    })

# Active listing 

def active(request):
    active = Product.objects.filter(is_active=True).order_by('-id')


    categories = Category.objects.all()
    return render (request, 'auctions/active_listing.html', {
        'active': active,
        'categories': categories
    })

# Select all close listing 

# Select all close listings and their corresponding winners
def close(request):
    username = request.user
    close_list = Product.objects.filter(is_active=False)
    
    # Create a dictionary to store winners by product
    close_data = []
    for product in close_list:
        winners = Winner.objects.filter(product=product)
        close_data.append((product, winners))

    categories = Category.objects.all()
    return render(request, 'auctions/close_listing.html', {

        'categories': categories,
         'close_data': close_data,
    })



     


# Stop bid by closing the listing 
@login_required(login_url='login')
def close_bid(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]
        product = get_object_or_404(Product, pk=product_id)
        product.is_active = False
        product.save()

        bid_count = Bid.objects.filter(product=product_id).count()
        bids = Bid.objects.filter(product=product_id).exists()
        winner = None  # Initialize winner as None

        if bid_count > 0:
            max_bid = Bid.objects.filter(product=product_id).aggregate(max_bid=Max('bid_amount'))
            max_bid = max_bid['max_bid']
            bid_winner = Bid.objects.get(product=product_id, bid_amount=max_bid)
            winner = bid_winner.user  # Access the user who placed the winning bid


        # Create a Winner object only if there is a winner
        #check if the product has already be won
         
        if bids:
            messages.error(request, 'This product has already be won.')

        if winner:
            Winner.objects.create(product=product, user=winner)
            messages.success(request, f"{winner} has successfully won the bid.")


        return HttpResponseRedirect(reverse('details', args=[product_id]))





def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
# Product Details
@login_required(login_url='login')
def prod_details(request, product_id):
    
    
    product = get_object_or_404(Product, id=product_id)
    all_bids = Bid.objects.filter(product_id=product_id).order_by('-timestamp')
    bid_count = all_bids.count()
    cp = product.price
    current_bid = product.current_bid


    # Extract bid amounts and calculate the total bid amount
    bid_amounts = [bid.bid_amount for bid in all_bids]
    total_bid = sum(bid_amounts)

    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = BidsForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            # Check if bid amount is greater than the current bid
            if current_bid is None or (bid_amount > current_bid and bid_amount > cp):
                # Create and save the new bid
                bid = Bid(
                    user=request.user,
                    product=product,
                    bid_amount=bid_amount,
                )
                bid.save()
                # Update the product's current_bid
                product.current_bid = bid_amount if current_bid is None else  bid_amount
                product.save()
                
                messages.success(request, "Bid placed successfully.")
            else:
                messages.warning(request, "Bid amount must be greater than the current bid.")
                
            return redirect('details', product_id=product_id)
    else:
        form = BidsForm()
        
        
    # I am checking this watchlist here to be able to use it as condition for toggle 
    watch = Watchlist.objects.filter(user=request.user, product=product).exists()

    return render(request, "auctions/prod_detail.html", {
        "product": product,
        'categories': categories,
        'all_bids': all_bids,
        "bid_count": bid_count,
        "cp": cp,
        "bam": current_bid,
        "bid_form": form,  # Pass the bid form to the template
        "total_bid": total_bid,
        "watch": watch,
        
    })


# to be updated
def placebid(request):
    pass

# Category
@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # Assign the logged-in user to the category
            category.save()
            return redirect('index')
    else:
        form = AddCategoryForm()
    
    return render(request, 'auctions/add_cats.html', {'form': form})


# Add product listing 
@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Product instance and populate it with form data
            product = Product(
                product=form.cleaned_data['product'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                current_bid = form.cleaned_data['price'],
                category=form.cleaned_data['category'],
                image = form.cleaned_data['image'],
                seller=request.user,
                listed_date=timezone.now(),
                is_active=form.cleaned_data['is_active']
            )

            product.save()  # Save the product instance to the database
            messages.success(request, 'Product added successfully!')
            return redirect('index')  # Redirect to the product list page or any other page
    else:
        form = ProductForm()

    return render(request, 'auctions/addproduct.html', {'form': form})





@login_required(login_url='login')
def watchlist_toggle(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Check if the user is already watching the product
    watch = Watchlist.objects.filter(user=request.user, product=product).exists()
    if watch:
        # User is watching the product; remove it from the watchlist
        Watchlist.objects.filter(user=request.user, product=product).delete()
        messages.warning(request, "This product has been removed from your watchlist.")
       
    else:
        # User is not watching the product; add it to the watchlist
        Watchlist.objects.create(user=request.user, product=product)
        messages.success(request, 'Product added to your watchlist')
       
    return redirect('details', product_id=product_id)












def watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    
    return render(request, 'auctions/watchlist.html', {
        "watchlist": watchlist,
        "user": user,
    })


@login_required(login_url='login')
def remove_watchlist(request, product_id):
    # Get the product using the product_id
    product = get_object_or_404(Product, pk=product_id)

    # Check if the product is in the user's watchlist
    watchlist_entry = Watchlist.objects.filter(user=request.user, product=product).first()

    if watchlist_entry:
        # Delete the product from the user's watchlist
        watchlist_entry.delete()

    # Redirect back to the watchlist page or any other desired page
    return redirect('watchlist')


# create comments
def comments(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'GET':
        comment_text = request.GET.get("comment")
        if comment_text:
            username = request.user.username

            # Create a new comment
            new_comment = Comment(user=username, product=product, comment=comment_text)
            new_comment.save()


    # Get the URL for the details page with the product_id
    details_url = reverse('details', args=[product_id])

    return redirect(details_url)

@login_required(login_url='login')
def delete_comments(request):
    if request.method == 'POST':
        comment_id = request.POST['comment_id']
        product_id = request.POST['product_id']

        try:
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
            messages.success(request, 'You have successfully deleted the comment')
        except:
            messages.warning(request, 'The comment could not be deleted.')

        # Assuming you want to redirect back to the product details page
        return redirect('details', product_id=product_id)

    # Handle cases where the request method is not POST
    return redirect('details')  # You may need to adjust this if needed


# select winners
@login_required(login_url='login')
def winner(request):
    username = request.user
    winner = Winner.objects.filter(user=username).exists()
    wins = Winner.objects.filter(user=username)


    if winner:
        messages.success(request , 'Congratulations you won a bid')
    else:
        messages.success(request , 'There is no listing ')

    return render(request, 'auctions/winner.html', {
       
        'wins': wins,
        
        })