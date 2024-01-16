from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, TemplateView, ListView, UpdateView, DeleteView

from catalog.forms import ProductForm, CategoryForm, VersionForm
from catalog.models import Product, Category, Contact, Version


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Главная страница',
    }
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {
        'title': 'Контакты',
    }

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}, phone: {phone}, message: {message}')
        return render(request, 'catalog/contacts.html', self.extra_context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('catalog:base', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': 'Товар',
    }
    template_name = 'catalog/product_detail.html'


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('product', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse_lazy('catalog:base', kwargs={'pk': self.object.pk})

    def toggle_active(request, slug):
        catalog = get_object_or_404(Category, slug=slug)
        if catalog.to_publish:
            catalog.to_publish = False
        else:
            catalog.to_publish = True
        catalog.save()
        return redirect('catalog:index', slug=catalog.slug)


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm

    def get_success_url(self):
        return reverse_lazy('catalog:index', kwargs={'pk': self.object.pk})


def product(request, pk):
    return render(request, 'catalog/product_list.html', {'product': Product.objects.get(pk=pk)})


def create_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_desc = request.POST.get('category_desc')
        Category.objects.create(name=category_name, description=category_desc)
        return redirect('index')
    return render(request, 'catalog/category_create.html')


def create_product(request):
    if request.method == 'POST':
        product_category = request.POST.get('product_category')
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        description = request.POST.get('prod_desc')
        image = request.FILES.get('prod_image')
        Product.objects.create(name=name, description=description, price=price,
                               image=image, category=Category.objects.get(id=product_category))
        print(f"Данные:\n"
              f"Название: {name}\n"
              f"Описание: {description}\n"
              f"Цена: {price}\n"
              f"Фото: {image}\n"
              f"Категория: {product_category}")
    return render(request, 'catalog/product_create.html', {'categories': Category.objects.all()})


class CategoryListView(ListView):
    """Главная старница со списком товаров"""
    model = Category
    extra_context = {
        'title': 'Категории',
    }
    template_name = 'catalog/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class CategoryView(ListView):
    model = Product
    template_name = 'category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        return Product.objects.filter(category=category)


class CategoryDetailView(DetailView):
    model = Category
    extra_context = {
        'title': 'Категория',
    }
    template_name = 'catalog/category_detail.html'


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm

    def get_success_url(self):
        return reverse_lazy('catalog:category_list', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category

    def get_success_url(self):
        return reverse_lazy('catalog:category_list', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.is_superuser
