from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, reverse

from .models import Product, Comment
from .forms import CommentForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    # model = Product
    queryset = Product.objects.filter(active=True)
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.auther = self.request.user
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        obj.product = product
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('product_list')