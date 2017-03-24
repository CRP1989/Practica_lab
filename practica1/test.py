from django.contrib.auth.models import User
from django.test import TestCase

from sistema.models import Credito, Debito, PagoServicio, Servicio, UserProfile, Transferencia


class ServicioTest(TestCase):
    def setUp(self):
        User.objects.create(password="1234", username="prueba")
        usuario = User.objects.get(username = "prueba")
        User.objects.create(password="12345", username="prueba2")
        usuario2 = User.objects.get(username = "prueba2")
        Transferencia.objects.create(user_cuenta = "prueba", user_cuenta2 = "prueba2", monto = '25.00')
        UserProfile.objects.create(correo="hola@gmail.com", nombre="hola", user = usuario, saldo = '10.00')
        UserProfile.objects.create(correo="hola2@gmail.com", nombre="hola2", user = usuario2, saldo = '10.00')
        Servicio.objects.create(servicio="luz")
        Servicio.objects.create(servicio="cable")
        cable = Servicio.objects.get(servicio = "cable")
        PagoServicio.objects.create(cuenta_servicio="cuenta", tipo_servicio = cable, user_cuenta = "hola", monto='10.00')        
        user_cuenta = UserProfile.objects.get(correo = "hola@gmail.com")
        Debito.objects.create(monto='10.00', descripcion="prueba", user_cuenta=user_cuenta)
        Credito.objects.create(monto='10.00', descripcion="prueba", user_cuenta=user_cuenta)

    def test_login(self):
        usuarios = User.objects.get(username="prueba")
        self.assertIsNotNone(usuarios.username) 
        self.assertEqual(usuarios.username, "prueba")
        self.assertEqual(usuarios.password, "1234")

    def test_signup(self):
        usuarios = User.objects.get(username="prueba")
        usuario = User.objects.get(password="1234")
        self.assertEquals(usuarios.username,"prueba") and self.assertNotEqual(usuario.password,"")

    def test_pago_de_servicios(self):
        pago = PagoServicio.objects.get(user_cuenta = "hola")
        cable = Servicio.objects.get(servicio = "cable")
        usuarios = UserProfile.objects.get(nombre = pago.user_cuenta)
        self.assertNotEqual(pago.monto, '0.00')
        self.assertEqual(pago.monto, usuarios.saldo)
        self.assertIsNotNone(pago.user_cuenta)

    def test_credito(self):
        credit = Credito.objects.get(descripcion="prueba")
        self.assertNotEqual(credit.monto, '0.00')
        self.assertIsNotNone(credit.user_cuenta)

    def test_debito(self):
        debit = Debito.objects.get(descripcion="prueba")
        self.assertNotEqual(debit.monto, '0.00')
        self.assertIsNotNone(debit.user_cuenta)
