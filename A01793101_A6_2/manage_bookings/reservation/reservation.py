"""Abstraccion de clase para las reservaciones realizadas en el hotel."""
import json
import os
from random import randint
from manage_bookings.customer.customer import Customer
from manage_bookings.hotel.hotel import Hotel

reserv_file = f"{os.getcwd()}\\reservation_data.json"
hotel_data_file = f"{os.getcwd()}\\hotel_data.json"
customer_data_file = f"{os.getcwd()}\\customer_data.json"


# pylint: disable=too-many-instance-attributes
class Reservation:
    """
    Atributos:
        reserv_id (int): Identificador de reservacion.
        hotel_id (int):  Identificador del Hotel donde se realiza la reserva.
        room_number (int): Numero de habitacion reservado.
        in_date (str): Fecha de check in de la reserva.
        out_date (str): Fecha de check out de la reserva.
        customer_email (str): Correo del cliente
        customer_id (str): Identificador del cliente que realiza la reserva.
    """
    def __init__(self, **kwargs) -> None:
        """Inicializar una reservacion definiendo sus attributos de clase"""
        self.room_number = kwargs.get("room_number")
        self.in_date = kwargs.get("in_date")
        self.out_date = kwargs.get("out_date")
        self.hotel_name = kwargs.get("hotel_name")
        self.hotel_id = self.get_hotel_id()
        self.customer_email = kwargs.get("customer_email")
        self.customer_id = self.get_customer_id()
        self.reserv_id = self.generate_id()

    def guardar_reservacion(self):
        """Guarda una nueva reservacion al archivo de Reservaciones"""
        if self.customer_id is False:
            return -1
        if self.hotel_id is False:
            return -2
        data = {
            "reserv_id": self.reserv_id,
            "room_number": self.room_number,
            "in_date": self.in_date,
            "out_date": self.out_date,
            "hotel_name": self.hotel_name,
            "hotel_id": self.hotel_id,
            "customer_email": self.customer_email,
            "customer_id": self.customer_id
        }

        existing_data = self.get_existing_data(reserv_file)
        room_rsv_id = Hotel.reserve_room(self.hotel_id, self.room_number)
        if room_rsv_id > 0:
            if isinstance(existing_data, dict):
                existing_data = [existing_data]
            data["reserv_id"] = f"{self.reserv_id}_{str(room_rsv_id)}"
            existing_data.append(data)
            Reservation.save_to_file(existing_data)
            return data["reserv_id"]
        # Return error code
        return room_rsv_id

    @staticmethod
    def create_reservacion(reserv_data):
        """Este metodo crea una nueva reserva y la almacena"""
        nueva_reserv = Reservation(**reserv_data)
        return nueva_reserv.guardar_reservacion()

    @staticmethod
    def get_existing_data(file):
        """Funcion para obtener los elementos del archivo"""
        if os.path.isfile(file):
            with open(file, 'r', encoding="UTF-8") as archivo:
                return json.load(archivo)
        return []

    def get_customer_id(self):
        """Funcion para obtener el id del cliente"""
        customer_data = Reservation.get_existing_data(customer_data_file)
        cstm_idx = Customer.get_customer_idx("customer_email",
                                             self.customer_email,
                                             customer_data)
        if cstm_idx >= 0:
            return customer_data[cstm_idx]["customer_id"]
        return False

    def get_hotel_id(self):
        """Funcion para obtener el id del hotel"""
        hotel_data = Reservation.get_existing_data(hotel_data_file)
        htl_idx = Hotel.get_hotel_idx("hotel_name",
                                      self.hotel_name,
                                      hotel_data)
        if htl_idx >= 0:
            return hotel_data[htl_idx]["hotel_id"]
        return False

    def generate_id(self):
        """Obtener el ID de la nueva reservacion"""
        str_id = "".join([word[0] for word in self.hotel_name.split(" ")])
        rnd_id = str(randint(100000, 999999))
        generated_id = f"{str_id}{rnd_id}"
        return generated_id

    @staticmethod
    def save_to_file(save_data):
        """Guardar un arreglo de objetos archivo a un json"""
        with open(reserv_file, 'w', encoding='utf-8') as file:
            json.dump(save_data, file, indent=4)

    @staticmethod
    def get_reserv_idx(field, field_value, file_data):
        """Funcion para buscar el indice de la reservacion guardada
        en el archivo usando otro campo"""
        found_idx = -1
        for idx, customer in enumerate(file_data):
            if customer.get(field) == field_value:
                found_idx = idx
                break
        return found_idx

    @staticmethod
    def delete_reserv_by_id(reserv_id):
        """Funcion para borrar una reservacion con determinado ID"""
        existing_data = Reservation.get_existing_data(reserv_file)
        reserv_idx = Reservation.get_reserv_idx("reserv_id",
                                                reserv_id,
                                                existing_data)
        if reserv_idx >= 0:
            reserv_dt = existing_data[reserv_idx]
            is_canceled = Hotel.cancel_room(reserv_dt["hotel_id"],
                                            reserv_dt["room_number"])
            if is_canceled == 0:
                del existing_data[reserv_idx]
                Reservation.save_to_file(existing_data)
            return is_canceled
        return -4
