"""Abstraccion de clase para las reservaciones realizadas en el hotel."""
import json
import os
from random import randint

reserv_file = f"{os.getcwd()}\\reservation_data.json"


class Reservation:
    """
    Atributos:
        reserv_id (int): Identificador de reservacion.
        customer_id (str): Identificador del cliente que realiza la reserva.
        hotel_id (int):  Identificador del Hotel donde se realiza la reserva.
        num_habit (int): Numero de habitacion reservado.
        in_date (str): Fecha de check in de la reserva.
        out_date (str): Fecha de check out de la reserva.
    """
    def __init__(self, **kwargs) -> None:
        """Inicializar una reservacion definiendo sus attributos de clase"""
        self.customer_id = kwargs.get("customer_id")
        self.num_habit = kwargs.get("num_habit")
        self.in_date = kwargs.get("in_date")
        self.out_date = kwargs.get("out_date")
        self.reserv_id = self.generate_id()
    
    def guardar_reservacion(self):
        """Guarda una nueva reservacion al archivo de Reservaciones"""
        data = {
            "reserv_id": self.reserv_id,
            "customer_id": self.customer_id,
            "num_habit": self.num_habit,
            "in_date": self.in_date,
            "in_date": self.in_date,
        }
        existing_data = self.get_existing_data()
        if self.reserv_id is not False:
            if isinstance(existing_data, dict):
                existing_data = [existing_data]
            existing_data.append(data)
            Reservation.save_to_file(existing_data)
            return self.reserv_id
        indx = self.get_reserv_idx("customer_id",
                                     self.customer_id, existing_data)
        return existing_data[indx].get("reserv_id")
    
    @staticmethod
    def create_reservacion(reserv_data):
        """Este metodo crea una nueva reserva y la almacena"""
        nueva_reserv = Reservation(**reserv_data)
        return nueva_reserv.guardar_reservacion()
    
    @staticmethod
    def get_existing_data():
        """Funcion para obtener los elementos del archivo"""
        if os.path.isfile(reserv_file):
            with open(reserv_file, 'r', encoding="UTF-8") as archivo:
                return json.load(archivo)
        return []
    
    def generate_id(self):
        """Obtener el ID de la nueva reservacion"""
        existing_data = Reservation.get_existing_data()
        str_id = "".join([word[0] for word in self.customer_name.split(" ")])
        rnd_id = str(randint(10000, 99999))
        generated_id = f"{str_id}_{rnd_id}"
        # Validar si el email de usuario se encuentra en el archivo.
        if len(existing_data) > 0:
            list_of_emails = list(map(
                lambda x: x["customer_email"].lower(), existing_data))
            if self.customer_email.lower() in list_of_emails:
                # Si ya se encuentra presente. Regresamos False
                return False
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
        return found_idx
