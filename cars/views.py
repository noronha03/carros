from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelFrom
from django.views import View
from django.views.generic import ListView
        
        
class CarsListView(ListView):# Esta view exibe uma lista de objetos do modelo Car usando o ListView do Django
    model = Car  # Define o modelo que será listado
    template_name = 'cars.html'  # Define o template que será renderizado
    context_object_name = 'cars'  # Nome da variável usada no template para acessar a lista

    def get_queryset(self):# Este método retorna a lista de objetos que será exibida
        cars = super().get_queryset().order_by('model') # Primeiro, busca todos os carros e ordena pelo campo 'model'
        search = self.request.GET.get('search')# Pega o valor do parâmetro 'search' na URL, se existir
        if search: # Se o usuário buscou algo, filtra os carros pelo modelo
            cars = cars.filter(model__icontains=search)   
        return cars# Retorna a lista (filtrada ou não)

class NewCarView(View):
    
    def get(self, request):
        new_car_form = CarModelFrom()
        return render(request, 'new_car.html', {'new_car_form' : new_car_form})
    
    def post(self, request):
        new_car_form = CarModelFrom(request.POST, request.FILES)
        if new_car_form.is_valid():
            new_car_form.save()
            return redirect('cars_list')
        return render(request, 'new_car.html', {'new_car_form' : new_car_form})
    