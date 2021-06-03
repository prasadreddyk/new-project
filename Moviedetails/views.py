import json

from django.http import Http404
from django.views import View
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Movies
from rest_framework.filters import SearchFilter,OrderingFilter
from .serializers import MovieSerializer
from reportlab.pdfgen import canvas
from django.http import HttpResponse


class Movies_list(GenericAPIView):
    """
    List of all movies.

    """
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer

    def get(self, request, format=None):
        snippets = Movies.objects.all()
        serializer = MovieSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Movies_detail(GenericAPIView):
    """
    Retrieve, update or delete a Movie instance.
    """
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer

    def get_object(self, pk):
        try:
            return Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MovieSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MovieSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Movies_search(ListAPIView):
    """
    search with name
        """
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    pagination_class = PageNumberPagination
    #filter_backends = (SearchFilter,OrderingFilter)
    SearchFilter = 'name'

class Movies_search_odering(ListAPIView):
    """
    if no result found it will show nothing in response
    """
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,OrderingFilter)



from django.http import HttpResponse


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def write_pdf_view(request):
    doc = SimpleDocTemplate("sample.pdf")
    styles = getSampleStyleSheet()
    Story = [Spacer(1,2*inch)]
    style = styles["Normal"]
    data=Movies.objects.all()
    for i in data:
       bogustext = ("This is movie name is %s.  " % i)
       p = Paragraph(bogustext, style)
       Story.append(p)
       Story.append(Spacer(1,0.2*inch))
    doc.build(Story)
    with open("sample.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sample.pdf"'
        return response

    return response