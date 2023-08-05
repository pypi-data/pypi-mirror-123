from django.test.testcases import TestCase
from inspect import ismethod


class ModelTestBase(TestCase):
    '''- Esta clase facilita la creacion de unit tests mediante el uso del metodo
       base_test_model. Dicho metodo ejecuta funciones concatenadas o no
       mediante un string separado por puntos, usando sus respectivos parametros.
       - Es necesario incluir el setUp declarando la instancia sobre la cual
       se aplicarán los metodos, como sigue:
            - def setUp(self):
                 - self.instance = SomeModel.objects.get(pk=some_pk)'''

    def base_test_model(self, metodo, assertion, **kwargs):
        metodos = metodo.split('.')
        for met in metodos:
            if metodos.index(met)==0:
                aux = getattr(self.instance, met)
            else:
                aux = getattr(aux, met)
            if ismethod(aux):
                aux = aux()
        if callable(aux):
            result = aux(**kwargs)
        else: result = aux
        if assertion:
            self.assertEqual(result, assertion)
        return result
