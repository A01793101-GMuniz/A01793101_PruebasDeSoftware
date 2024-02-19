"""Abstraccion de clase para la informacion de Hoteles."""
import json
import os
from random import randint

hotel_file = f"{os.getcwd()}\\hotel_data.json"


class Hotel:
    """
    Atributos:
        hotel_id (str): Identificador de reservacion.
        habitaciones (list): Lista de habitaciones disponibles
        y su informacion.

        hotel_name (str): Nombre del hotel.
        hotel_addr (str): Direccion del Hotel.
    """
    def __init__(self, **kwargs):
        """Inicializar objeto Hotel definiendo sus attributos"""
        self.habitaciones = kwargs.get("habitaciones")
        self.hotel_name = kwargs.get("hotel_name")
        self.hotel_id = self.get_next_id()
        self.hotel_addr = kwargs.get("hotel_addr")

    def save_hotel(self):
        """Guarda un nuevo hotel al archivo de hoteles"""
        data = {
            "hotel_id": self.hotel_id,
            "hotel_name": self.hotel_name,
            "hotel_addr": self.hotel_addr,
            "habitaciones": self.habitaciones
        }
        existing_data = self.get_existing_data()
        if isinstance(existing_data, dict):
            existing_data = [existing_data]
        names = map(lambda htl: htl["hotel_name"], existing_data)
        addre = map(lambda htl: htl["hotel_addr"], existing_data)
        exp = data["hotel_name"] in names and data["hotel_addr"] in addre
        if not exp:
            existing_data.append(data)
            Hotel.save_to_file(existing_data)
            return self.hotel_id
        indx = self.get_hotel_idx("hotel_addr",
                                  self.hotel_addr, existing_data)
        return existing_data[indx].get("hotel_id")

    @staticmethod
    def save_to_file(data):
        """Guardar un arreglo de objetos archivo a un json"""
        with open(hotel_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def get_next_id(self):
        """Obtener el siguiente ID disponible en el archivo"""
        existing_data = Hotel.get_existing_data()
        if len(existing_data) > 0:
            list_of_ids = sorted(map(lambda x: x["hotel_id"], existing_data))
            new_id = list_of_ids[-1] + 1
            return new_id
        return 1

    @staticmethod
    def create_hotel(nuevo_hotel):
        """Este metodo crea un nuevo Hotel y lo almacena en el archivo"""
        new_hotel = Hotel(**nuevo_hotel)
        return new_hotel.save_hotel()

    @staticmethod
    def delete_hotel(delete_hotel_id):
        """Funcion para eliminar un hotel y actualizar el archivo"""
        existing_data = Hotel.get_existing_data()
        idx_to_delete = Hotel.get_hotel_idx("hotel_id",
                                            delete_hotel_id,
                                            existing_data)
        if idx_to_delete >= 0:
            del existing_data[idx_to_delete]
            Hotel.save_to_file(existing_data)
            return True
        return False

    @staticmethod
    def display_hotel(searched_id):
        """Funcion para mostrar el hotel con el ID enviado"""
        hotels_on_file = Hotel.get_existing_data()
        info_idx = Hotel.search_hotel_idx(searched_id, hotels_on_file)
        if info_idx >= 0:
            for attr, valor in hotels_on_file[info_idx].items():
                if attr == "habitaciones":
                    print("\nHabitaciones:")
                    for hab in valor:
                        print(f"\n{hab}")
                else:
                    print(f"\n{attr.replace('_', ' ').capitalize()}: {valor}")
            return True
        return False

    @staticmethod
    def search_hotel_idx(searched_id, hotels_on_file):
        """Funcion para buscar el indice del hotel en el archivo"""
        info_idx = -1
        for idx, hotel in enumerate(hotels_on_file):
            if hotel.get("hotel_id") == searched_id:
                info_idx = idx
        return info_idx

    @staticmethod
    def get_hotel_idx(field, field_value, file_data):
        """Funcion para buscar el indice del hotel en el archivo"
        usando otro campo"""
        found_idx = -1
        for idx, hotel in enumerate(file_data):
            if hotel.get(field) == field_value:
                found_idx = idx
        return found_idx

    @staticmethod
    def get_existing_data():
        """Funcion para obtener los elementos del archivo"""
        if os.path.isfile(hotel_file):
            with open(hotel_file, 'r', encoding="UTF-8") as archivo:
                return json.load(archivo)
        return []

    @staticmethod
    def modify_hotel(hotel_id, new_data):
        """Funcion para modificar el hotel con el ID enviado"""
        hotels_on_file = Hotel.get_existing_data()
        info_idx = Hotel.search_hotel_idx(hotel_id, hotels_on_file)
        if info_idx >= 0:
            for key in new_data.keys():
                hotels_on_file[info_idx][key] = new_data[key]
            Hotel.save_to_file(hotels_on_file)
            return True
        return False

    @staticmethod
    def reserve_room(hotel_id, room_number):
        """Funcion para reservar una habitacion en el hotel"""
        hotels_on_file = Hotel.get_existing_data()
        info_idx = Hotel.search_hotel_idx(hotel_id, hotels_on_file)
        if info_idx >= 0:
            for habit in hotels_on_file[info_idx]["habitaciones"]:
                if habit["room_number"] == room_number:
                    if habit["disponible"]:
                        habit["disponible"] = False
                        room_res_id = randint(10000, 99999)
                        Hotel.save_to_file(hotels_on_file)
                        return room_res_id
            # Si no encontro la habitacion o no esta disponible
            return -1
        # Si no esta en el archivo
        return -2

    @staticmethod
    def cancel_room(hotel_id, room_number):
        """Funcion para reservar una habitacion en el hotel"""
        hotels_on_file = Hotel.get_existing_data()
        info_idx = Hotel.search_hotel_idx(hotel_id, hotels_on_file)
        if info_idx >= 0:
            for habit in hotels_on_file[info_idx]["habitaciones"]:
                if habit["room_number"] == room_number:
                    if not habit["disponible"]:
                        habit["disponible"] = True
                        Hotel.save_to_file(hotels_on_file)
                        return 0
                    # Si la habitacion  ya esta disponible
                    return -1
            # Si no encontro la habitacion
            return -2
        # Si el hotel no esta en el archivo
        return -3
