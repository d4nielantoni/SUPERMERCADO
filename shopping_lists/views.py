from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShoppingList, Item
from .forms import ShoppingListForm, ItemForm

@login_required
def home(request):
    shopping_lists = ShoppingList.objects.filter(user=request.user)
    return render(request, 'shopping_lists/home.html', {'shopping_lists': shopping_lists})

@login_required
def create_list(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            shopping_list = form.save(commit=False)
            shopping_list.user = request.user
            shopping_list.save()
            messages.success(request, 'Lista criada com sucesso!')
            return redirect('list_detail', pk=shopping_list.pk)
    else:
        form = ShoppingListForm()
    return render(request, 'shopping_lists/list_form.html', {'form': form})

@login_required
def list_detail(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    items = shopping_list.items.all()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.shopping_list = shopping_list
            item.save()
            messages.success(request, 'Item adicionado com sucesso!')
            return redirect('list_detail', pk=pk)
    else:
        form = ItemForm()
    return render(request, 'shopping_lists/list_detail.html', {
        'shopping_list': shopping_list,
        'items': items,
        'form': form
    })

@login_required
def toggle_item(request, pk):
    item = get_object_or_404(Item, pk=pk, shopping_list__user=request.user)
    item.purchased = not item.purchased
    item.save()
    return redirect('list_detail', pk=item.shopping_list.pk)

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk, shopping_list__user=request.user)
    list_pk = item.shopping_list.pk
    item.delete()
    messages.success(request, 'Item removido com sucesso!')
    return redirect('list_detail', pk=list_pk)

@login_required
def delete_list(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    shopping_list.delete()
    messages.success(request, 'Lista removida com sucesso!')
    return redirect('home')
