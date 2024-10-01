from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import PDF, Category
from .forms import PDFUploadForm

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_instance = form.save()
            pdf_instance.convert_pdf_to_epub()  # Convert the uploaded PDF
            return redirect('epub_app:epub_view', pk=pdf_instance.pk)  # Redirect to the EPUB view
    else:
        form = PDFUploadForm()
    
    return render(request, 'upload_pdf.html', {'form': form})

def epub_view(request, pk):
    pdf_instance = get_object_or_404(PDF, pk=pk)
    return render(request, 'epub_view.html', {'pdf': pdf_instance})

def epub_list(request):
    query = request.GET.get('q')
    pdf_list = PDF.objects.all()

    # If there's a search query, filter by title or category
    if query:
        pdf_list = pdf_list.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Pagination setup
    paginator = Paginator(pdf_list, 15)  # Show 15 EPUBs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'epub_list.html', {
        'page_obj': page_obj,
        'query': query,
    })
