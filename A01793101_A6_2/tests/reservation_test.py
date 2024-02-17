"""
Unit tests para verificar la funcionalidad de la clase Customer
"""
import unittest
import os
import json
from manage_bookings.reservation.reservation import Reservation
from manage_bookings.customer.customer import Customer
from manage_bookings.hotel.hotel import Hotel


class CustomerTest(unittest.TestCase):
    """
    Test cases diseñados para la clase Customer
    """
    @classmethod
    def setUpClass(cls):
        """Configuracion de los datos de prueba para todos los casos"""
        reserv_test_data_file = f"{os.getcwd()}\\test_data\\reservations_1.json"
        hotel_data = [
            {
                "hotel_id": 1,
                "hotel_name": "Sheraton Plaza Inn",
                "hotel_addr": "Av. Siempre Viva 785, Guadalajara Jalisco",
                "habitaciones": [
                    {
                        "room_number": 1,
                        "tipo": "single",
                        "precio": 54.0,
                        "disponible": True
                    },
                    {
                        "room_number": 2,
                        "tipo": "double",
                        "precio": 64.0,
                        "disponible": True
                    },
                    {
                        "room_number": 3,
                        "tipo": "king",
                        "precio": 70.0,
                        "disponible": False
                    }
                ]
            },
            {
                "hotel_id": 2,
                "hotel_name": "RIU GDL",
                "hotel_addr": "Lazaro Cardenaz 2545, Guadalajara Jalisco",
                "habitaciones": [
                    {
                        "room_number": 101,
                        "tipo": "double",
                        "precio": 45.0,
                        "disponible": False
                    },
                    {
                        "room_number": 102,
                        "tipo": "family",
                        "precio": 80.0,
                        "disponible": True
                    },
                    {
                        "room_number": 103,
                        "tipo": "double",
                        "precio": 45.0,
                        "disponible": True
                    }
                ]
            }
        ]
        customer_data = cls.get_json_data_from_file(customer_file)
        
        if os.path.isfile(reserv_test_data_file):
            with open(reserv_test_data_file, 'r', encoding="UTF-8") as archivo:
                reservations = json.load(archivo)
        
        for reserv in reservations:
            Reservation.create_reservacion(reserv)
    
    @classmethod
    def get_json_data_from_file(file):
        """Funcion para obtener los elementos de un archivo json"""
        if os.path.isfile(file):
            with open(file, 'r', encoding="UTF-8") as archivo:
                return json.load(archivo)
        return []

    # def test_create_reservation(self):
    #     """Prueba la creacion de una nueva Reservacion y lo añade a un archivo"""
    #     print("\nCREATE RESERVATION TEST:\n")
    #     reserv_id = Reservation.create_reservacion(new_reserv)
    #     print(f"Customer Saved in file with ID: {customer_id}\n")
    #     ids_on_file = map(lambda ctm: ctm["customer_id"],
    #                       Customer.get_existing_data())
    #     exp = customer_id in ids_on_file
    #     self.assertTrue(exp, "No encontre el customer en\
    #         el archivo de Customers\n")

    # def test_delete_customer(self):
    #     """Prueba la eliminacion de un customer por email y
    #     que no se encuentre en el archivo"""
    #     email_to_delete = "itHam@mail.com"
    #     Customer.delete_customer(email_to_delete)
    #     customers_on_file = Customer.get_existing_data()
    #     customers_emails = map(lambda ctm: ctm["customer_email"],
    #                            customers_on_file)
    #     self.assertTrue(email_to_delete not in customers_emails,
    #                     "Encontre el customer en el archivo de Customers,\
    #                         no fue eliminado")

if __name__ == '__main__':
    unittest.main()
