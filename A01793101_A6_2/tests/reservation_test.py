"""
Unit tests para verificar la funcionalidad de la clase Reservacion
"""
import unittest
import os
import json
from manage_bookings.reservation.reservation import Reservation
from manage_bookings.hotel.hotel import Hotel

reservation_file = f"{os.getcwd()}\\reservation_data.json"

hotel_test = {
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
      },
      {
        "room_number": 201,
        "tipo": "single",
        "precio": 35.0,
        "disponible": True
      },
      {
        "room_number": 202,
        "tipo": "suite",
        "precio": 100.0,
        "disponible": True
      }
    ],
    "hotel_name": "RIU GDL",
    "hotel_addr": "Lazaro Cardenaz 2545, Guadalajara Jalisco"
  }


class CustomerTest(unittest.TestCase):
    """
    Test cases diseñados para la clase Customer
    """
    @classmethod
    def setUpClass(cls):
        """Configuracion de los datos de prueba para todos los casos"""
        tst_reserv = \
            cls.get_data(f"{os.getcwd()}\\test_data\\reservations_1.json")

        hotel_data_file = f"{os.getcwd()}\\hotel_data.json"

        reserv_data = cls.get_data(reservation_file)
        clean_idx = Reservation.get_reserv_idx("hotel_name",
                                               "RIU GDL",
                                               reserv_data)
        if clean_idx >= 0:
            del reserv_data[clean_idx]
            Reservation.save_to_file(reserv_data)

        if os.path.isfile(hotel_data_file):
            with open(hotel_data_file, 'r', encoding="UTF-8") as archivo:
                htl_name = hotel_test["hotel_name"]
                ext_htl = json.load(archivo)
                if htl_name not in [htl["hotel_name"] for htl in ext_htl]:
                    Hotel.create_hotel(hotel_test)

                else:
                    # Obtener el índice del elemento que tenga el
                    # hotel_name_buscado
                    idx = next((i for i, hotel in enumerate(ext_htl)
                                if hotel["hotel_name"] ==
                                hotel_test["hotel_name"]), None)
                    if idx is not None:
                        habit = ext_htl[idx]["habitaciones"][2]
                        if habit["disponible"] is False:
                            habit["disponible"] = True
                    # Reset Valores para las pruebas
                    Hotel.save_to_file(ext_htl)

        for reserv in tst_reserv:
            Reservation.create_reservacion(reserv)

    @classmethod
    def get_data(cls, file):
        """Funcion para obtener los elementos de un archivo json"""
        if os.path.isfile(file):
            with open(file, 'r', encoding="UTF-8") as archivo:
                return json.load(archivo)
        return []

    def test_create_reservation(self):
        """Prueba la creacion de una nueva Reservacion y
        lo añade a un archivo"""
        print("\nCREATE RESERVATION TEST:\n")
        new_reserv = {
            "hotel_name": "RIU GDL",
            "room_number": 103,
            "customer_email": "exRchd782@hotmail.com",
            "in_date": "15-10-2024",
            "out_date": "17-10-2024"
        }
        reserv_id = Reservation.create_reservacion(new_reserv)

        self.assertNotEqual(reserv_id, -1,
                            f"Numero de Habitacion: {new_reserv['room_number']} no\
                                disponible o inexistente en el Hotel:\
                                    {new_reserv['hotel_name']}")
        self.assertNotEqual(reserv_id, -2,
                            f"Hotel: {new_reserv['hotel_name']}\
                                no disponible en el archivo")

        print(f"Room {new_reserv['room_number']} in Hotel : {new_reserv['hotel_name']}\
            was reserved with ID: {reserv_id}")
        ids_on_file = map(lambda rsv: rsv["reserv_id"],
                          self.get_data(reservation_file))
        exp = reserv_id in ids_on_file
        self.assertTrue(exp, f"No encontre la reservacion {reserv_id} en\
            el archivo de Reservas\n")

    def test_delete_reservation(self):
        """Prueba la eliminacion de una reserva por ID de reserva"""
        # Obtener el primer ID del archivo existente
        reserv_data = self.get_data(reservation_file)[0]
        can_code = Reservation.delete_reserv_by_id(reserv_data['reserv_id'])
        self.assertNotEqual(can_code, -1,
                            f"Habitacion: {reserv_data['room_number']}\
                                Ya estaba disponible")
        self.assertNotEqual(can_code, -2,
                            f"Numero de Habitacion: {reserv_data['room_number']}\
                                No encontrado en Hotel\
                                    {reserv_data['hotel_id']}")
        self.assertNotEqual(can_code, -3,
                            f"Hotel ID: {reserv_data['hotel_id']}\
                                no disponible en el archivo de hoteles")
        ids_on_file = map(lambda rsv: rsv["reserv_id"],
                          self.get_data(reservation_file))
        self.assertTrue(can_code not in ids_on_file,
                        "Encontre el customer en el archivo de Customers,\
                            no fue eliminado")

    def test_delete_not_existing_reserve(self):
        """Prueba la eliminacion de una reserva por ID que no existe"""
        print("\nBORRAR RESERVA INEXISTENTE TEST:\n")
        cancel_code = Reservation.delete_reserv_by_id("_NEC_345566_")
        self.assertEqual(cancel_code, -4, "Reservacion con codigo:\
                         _NEC_345566_ no Deberia existir en archivo")

    def test_reserve_non_existing_room(self):
        """Prueba el intento de reservar una habitacion no existente"""
        print("\nHABITACION NO EXISTE TEST:\n")
        new_reserv = {
            "hotel_name": "RIU GDL",
            "room_number": 2,
            "customer_email": "exRchd782@hotmail.com",
            "in_date": "25-08-2024",
            "out_date": "30-08-2024"
        }
        reserv_id = Reservation.create_reservacion(new_reserv)

        self.assertEqual(reserv_id, -1, f"Numero de Habitacion:\
            {new_reserv['room_number']} no deberia existir en el Hotel:\
                {new_reserv['hotel_name']}")

    def test_reserve_non_existing_hotel(self):
        """Prueba el intento de reservar una habitacion
        en un hotel no existente"""
        print("\nHOTEL NO EXISTE TEST:\n")
        new_reserv = {
            "hotel_name": "__NE_TEST_HOTEL__",
            "room_number": 1,
            "customer_email": "exRchd782@hotmail.com",
            "in_date": "25-08-2024",
            "out_date": "30-08-2024"
        }
        reserv_id = Reservation.create_reservacion(new_reserv)

        self.assertEqual(reserv_id, -2, "Hotel: __NE_TEST_HOTEL__ fue\
            encontrado en base de datos")


if __name__ == '__main__':
    unittest.main()
