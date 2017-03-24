from django.contrib.auth.models import User
from django.test import TestCase

from sistema.models import Credito, Debito, PagoServicio, Servicio, UserProfile, Transferencia


class ServicioTest(TestCase):
    def setUp(self):
        User.objects.create(password="1234", username="prueba")
        usuario = User.objects.get(username = "prueba")
        Transferencia.objects.create(user_cuenta = "usuario1", user_cuenta2 = "usuario2", monto = '25.00')
        UserProfile.objects.create(correo="hola@gmail.com", nombre="hola", user = usuario)
        Servicio.objects.create(servicio="luz")
        Servicio.objects.create(servicio="cable")
        cable = Servicio.objects.get(servicio = "cable")
        PagoServicio.objects.create(cuenta_servicio="cuenta", tipo_servicio = cable, user_cuenta = "prueba", monto='10.00')        
        user_cuenta = UserProfile.objects.get(correo = "hola@gmail.com")
        Debito.objects.create(monto='10.00', descripcion="prueba", user_cuenta=user_cuenta)
        Credito.objects.create(monto='10.00', descripcion="prueba", user_cuenta=user_cuenta)


    def test_servicio(self):
        luz = Servicio.objects.get(servicio="luz")
        self.assertEqual(luz.servicio, "luz")

    def test_credito(self):
        credit = Credito.objects.get(descripcion="prueba")
        self.assertNotEqual(credit.monto, '0.00')
        self.assertIsNotNone(credit.user_cuenta)

    def test_debito(self):
        debit = Debito.objects.get(descripcion="prueba")
        self.assertNotEqual(debit.monto, '0.00')
        self.assertIsNotNone(debit.user_cuenta)

    def test_pago(self):
        pago = PagoServicio.objects.get(user_cuenta = "prueba")
        cable = Servicio.objects.get(servicio = "cable")
        self.assertNotEqual(pago.monto, '0.00')
        self.assertIsNotNone(pago.user_cuenta)

    def test_user(self):
        usuarios = User.objects.get(username="prueba")
        usuario = User.objects.get(password="1234")
        self.assertEquals(usuarios.username,"prueba") and self.assertNotEqual(usuario.password,"")

    def test_transfer(self):
        transferencia = Transferencia.objects.get(user_cuenta="usuario1")
        self.assertNotEqual(transferencia.user_cuenta, transferencia.user_cuenta2)
        self.assertNotEqual(transferencia.monto, '0.00')
