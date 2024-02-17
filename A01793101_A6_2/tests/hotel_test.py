"""
Unit tests para verificar la funcionalidad de la clase Hotel
"""

import unittest
import os
import json
from manage_bookings.hotel.hotel import Hotel


new_hotel = {
    "hotel_name": "Hampton Inn",
    "hotel_addr": "Calle Siempre Viva 785",
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
            "disponible": False
        },
        {
            "room_number": 3,
            "tipo": "king",
            "precio": 70.0,
            "disponible": True
        }]
    }


class HotelTest(unittest.TestCase):
    """
    Test cases diseñados para la clase Hotel
    """
    @classmethod
    def setUpClass(cls):
        """Configuracion de los datos de prueba para todos los casos"""
        test_data_file = f"{os.getcwd()}\\test_data\\hoteles_1.json"
        if os.path.isfile(test_data_file):
            with open(test_data_file, 'r', encoding="UTF-8") as archivo:
                hoteles = json.load(archivo)

        hotel_data_file = f"{os.getcwd()}\\hotel_data.json"
        if os.path.isfile(hotel_data_file):
            with open(hotel_data_file, 'r', encoding="UTF-8") as archivo:
                existing_hotl = json.load(archivo)
                if existing_hotl[0]["habitaciones"][2]["disponible"] is False:
                    existing_hotl[0]["habitaciones"][2]["disponible"] = True
                    
                if existing_hotl[0]["habitaciones"][1]["disponible"]:
                    existing_hotl[0]["habitaciones"][1]["disponible"] = False

                # Reset Valores para las pruebas
                Hotel.save_to_file(existing_hotl)

        for hotel in hoteles:
            Hotel.create_hotel(hotel)

    def test_create_hotel(self):
        """Prueba la creacion de un nuevo hotel y lo añade a un archivo"""
        print("\nCREATE HOTEL TEST:\n")
        hotel_id = Hotel.create_hotel(new_hotel)
        print(f"Hotel Saved to file with ID: {hotel_id}\n")
        hotels_on_file = Hotel.get_existing_data()
        hotels_names = map(lambda htl: htl["hotel_name"], hotels_on_file)
        hotels_addre = map(lambda htl: htl["hotel_addr"], hotels_on_file)
        exp = new_hotel["hotel_name"] in hotels_names\
            and new_hotel["hotel_addr"] in hotels_addre
        self.assertTrue(exp, "No encontre el hotel en el archivo de Hoteles")

    def test_display_hotel(self):
        """Prueba el despliegue de la informacion del hotel
        con cierto ID"""
        print("\nDISPLAY HOTEL TEST:\n")
        srch_id = 1
        disp = Hotel.display_hotel(srch_id)
        self.assertTrue(disp,
                        f"Hotel ID: {srch_id} no fue encontrado en el archivo")

    def test_delete_hotel(self):
        """Prueba la eliminacion de un hotel y
        que no se encuentre en el archivo"""
        print("\nDELETE HOTEL TEST\n")
        id_to_delete = 3
        Hotel.delete_hotel(id_to_delete)
        hotels_on_file = Hotel.get_existing_data()
        hotels_ids = map(lambda htl: htl["hotel_id"], hotels_on_file)
        self.assertTrue(id_to_delete not in hotels_ids,
                        "Encontre el hotel en el archivo de Hoteles,\
                         no fue eliminado")
        print(f"Hotel with ID {id_to_delete} deleted\n")

    def test_modify_hotel(self):
        """Prueba la modificacion de un hotel y
        que no se vea reflejado en el archivo"""
        print("\nMODIFY HOTEL TEST\n")
        modified_hotel_info = {
            "hotel_name": "Hilton Inn Plaza",
            "habitaciones": [
                {
                    "room_number": 1,
                    "tipo": "double",
                    "precio": 85.0,
                    "disponible": True
                },
                {
                    "room_number": 2,
                    "tipo": "double",
                    "precio": 85.0,
                    "disponible": True
                },
                {
                    "room_number": 3,
                    "tipo": "family",
                    "precio": 105.0,
                    "disponible": True
                },
                {
                    "room_number": 4,
                    "tipo": "suite",
                    "precio": 154.0,
                    "disponible": True
                }
            ]
        }
        srch_id = 2
        mod = Hotel.modify_hotel(srch_id, modified_hotel_info)
        self.assertTrue(mod,
                        f"Hotel ID: {srch_id} no fue Modificado")
        hotels_on_file = Hotel.get_existing_data()
        idx = Hotel.search_hotel_idx(srch_id, hotels_on_file)
        for key, value in modified_hotel_info.items():
            self.assertEqual(hotels_on_file[idx][key], value,
                             f"El valor de {key}:{value}\
                                no fue modificado en el archivo.\
                                    Valor en archivo:\
                                        {hotels_on_file[idx][key]}")
        print("Modified Hotel Data:")
        Hotel.display_hotel(srch_id)

    def test_reserve_room(self):
        """Prueba que reserva una habitacion del hotel y
        cambia su disponibilidad"""
        print("\nRESERVE A ROOM TEST\n")
        room_number = 3
        hotel_id = 1

        room_res_id = Hotel.reserve_room(hotel_id, room_number)
        self.assertNotEqual(room_res_id, -1,
                            f"Numero de Habitacion: {room_number} no\
                                disponible o inexistente en el hotel ID\
                                    {hotel_id}")
        self.assertNotEqual(room_res_id, -2,
                            f"Hotel ID: {hotel_id}\
                                no disponible en el archivo")
        print(f"Room {room_number} in Hotel ID: {hotel_id}\
            was reserved with ID: {room_res_id}")

    def test_reserve_room_cancel(self):
        """Prueba que cancela una reserva de una habitacion del hotel y
        cambia su disponibilidad"""
        print("\nCANCEL A ROOM TEST\n")
        room_number = 2
        hotel_id = 1

        room_res_id = Hotel.cancel_room(hotel_id, room_number)
        self.assertNotEqual(room_res_id, -1,
                            f"Habitacion: {room_number}\
                                Ya estaba disponible")
        self.assertNotEqual(room_res_id, -2,
                            f"Numero de Habitacion: {room_number}\
                                No encontrado en Hotel {hotel_id}")
        self.assertNotEqual(room_res_id, -3,
                            f"Hotel ID: {hotel_id}\
                                no disponible en el archivo")
        print(f"Reservacion en la habitacion {room_number}\
            del Hotel ID: {hotel_id} fue cancelada")

if __name__ == '__main__':
    unittest.main()
