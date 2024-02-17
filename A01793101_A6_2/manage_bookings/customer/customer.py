"""Abstraccion de clase para la informacion de Clientes."""
import json
import os
from random import randint

customer_file = f"{os.getcwd()}\\customer_data.json"


class Customer:
    """
    Atributos:
        customer_id (str): Identificador de cliente.
        customer_name (str): Nombre del cliente.
        customer_email (str): Correo del cliente.
    """
    def __init__(self, **kwargs) -> None:
        """Inicializar un objeto Customer definiendo sus attributos"""
        self.customer_name = kwargs.get("customer_name")
        self.customer_email = kwargs.get("customer_email")
        self.customer_phone = kwargs.get("customer_phone")
        self.customer_id = self.generate_id()

    def save_customer(self):
        """Guarda un nuevo customer al archivo de customers"""
        data = {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "customer_phone": self.customer_phone
        }
        existing_data = self.get_existing_data()
        if self.customer_id is not False:
            if isinstance(existing_data, dict):
                existing_data = [existing_data]
            existing_data.append(data)
            Customer.save_to_file(existing_data)
            return self.customer_id
        indx = self.get_customer_idx("customer_email",
                                     self.customer_email, existing_data)
        return existing_data[indx].get("customer_id")

    @staticmethod
    def save_to_file(save_data):
        """Guardar un arreglo de objetos archivo a un json"""
        with open(customer_file, 'w', encoding='utf-8') as file:
            json.dump(save_data, file, indent=4)

    def generate_id(self):
        """Obtener el siguiente ID disponible en el archivo"""
        existing_data = Customer.get_existing_data()
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
    def create_customer(nuevo_customer):
        """Este metodo crea un nuevo customer y lo almacena en el archivo"""
        new_customer = Customer(**nuevo_customer)
        return new_customer.save_customer()

    @staticmethod
    def delete_customer(delete_customer_email):
        """Funcion para eliminar un customer y actualizar el archivo"""
        existing_data = Customer.get_existing_data()
        idx_to_delete = Customer.get_customer_idx("customer_email",
                                                  delete_customer_email,
                                                  existing_data)
        if idx_to_delete >= 0:
            del existing_data[idx_to_delete]
            Customer.save_to_file(existing_data)

    @staticmethod
    def display_customer(searched_email):
        """Funcion para mostrar el customer con el ID enviado"""
        customers_on_file = Customer.get_existing_data()
        info_idx = Customer.get_customer_idx("customer_email",
                                             searched_email,
                                             customers_on_file)
        if info_idx >= 0:
            for attr, valor in customers_on_file[info_idx].items():
                print(f"\n{attr.replace('_', ' ').capitalize()}: {valor}")
            return True
        return False

    @staticmethod
    def search_customer_idx(searched_id, customers_on_file):
        """Funcion para buscar el indice del customer en el archivo"""
        info_idx = -1
        for idx, customer in enumerate(customers_on_file):
            if customer.get("customer_id") == searched_id:
                info_idx = idx
        return info_idx

    @staticmethod
    def get_customer_idx(field, field_value, file_data):
        """Funcion para buscar el indice del customer en el archivo"
        usando otro campo"""
        found_idx = -1
        for idx, customer in enumerate(file_data):
            if customer.get(field) == field_value:
                found_idx = idx
        return found_idx

    @staticmethod
    def get_existing_data():
        """Funcion para obtener los elementos del archivo"""
        if os.path.isfile(customer_file):
            with open(customer_file, 'r', encoding="UTF-8") as archivo:
                return json.load(archivo)
        return []

    @staticmethod
    def modify_customer(customer_email, new_data):
        """Funcion para modificar el customer con el ID enviado"""
        customers_on_file = Customer.get_existing_data()
        info_idx = Customer.get_customer_idx("customer_email",
                                             customer_email, customers_on_file)
        if info_idx >= 0:
            for key in new_data.keys():
                customers_on_file[info_idx][key] = new_data[key]
            Customer.save_to_file(customers_on_file)
            return True
        return False
