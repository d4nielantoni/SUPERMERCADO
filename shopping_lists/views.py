from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ItemForm, ShoppingListForm
from .models import Item, ShoppingList


class SimpleUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirme a senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ("username",)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Escolha um nome de usuário'

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
        form = ItemForm(request.POST, request.FILES)
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
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, shopping_list__user=request.user)
    shopping_list = item.shopping_list

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado com sucesso!')
            return redirect('list_detail', pk=shopping_list.pk)
    else:
        form = ItemForm(instance=item)

    return render(request, 'shopping_lists/edit_item.html', {
        'form': form,
        'item': item,
        'shopping_list': shopping_list
    })

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

def register(request):
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo!')
            return redirect('home')
    else:
        form = SimpleUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def export_pdf(request, pk):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    from reportlab.lib import colors

    shopping_list = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    items = shopping_list.items.all()

    response = HttpResponse(content_type='application/pdf')
    filename = f"lista_compras_{shopping_list.title.replace(' ', '_')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=1
    )

    story.append(Paragraph(f"{shopping_list.title}", title_style))

    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=20,
        alignment=1
    )
    story.append(Paragraph(f"Gerada em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", date_style))
    story.append(Spacer(1, 0.2*inch))

    if items:
        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.whitesmoke,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        data = [[Paragraph('Item', header_style), Paragraph('Quantidade', header_style), Paragraph('Unidade<br/>(se aplicável)', header_style)]]

        for item in items:
            quantidade = str(item.quantity) if item.quantity else '-'
            unidade = item.unit if item.unit else '-'

            data.append([item.name, quantidade, Paragraph(unidade, styles['Normal'])])

        table = Table(data, colWidths=[4*inch, 1.2*inch, 1.3*inch])

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))

        story.append(table)
    else:
        story.append(Paragraph("Nenhum item adicionado nesta lista.", styles['Normal']))

    doc.build(story)

    return response
