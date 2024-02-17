"""
Unit tests para verificar la funcionalidad de la clase Customer
"""
import unittest
import os
import json
from manage_bookings.customer.customer import Customer

new_customer = {
    "customer_name": "Ritus Octavious",
    "customer_email": "miRitus@hotmail.com",
    "customer_phone": "3312457865"
}


class CustomerTest(unittest.TestCase):
    """
    Test cases diseñados para la clase Customer
    """
    @classmethod
    def setUpClass(cls):
        """Configuracion de los datos de prueba para todos los casos"""
        customer_data_file = f"{os.getcwd()}\\test_data\\customers_1.json"
        if os.path.isfile(customer_data_file):
            with open(customer_data_file, 'r', encoding="UTF-8") as archivo:
                customers = json.load(archivo)
        for customer in customers:
            Customer.create_customer(customer)

    def test_create_customer(self):
        """Prueba la creacion de un nuevo customer y lo añade a un archivo"""
        print("\nCREATE CUSTOMER TEST:\n")
        customer_id = Customer.create_customer(new_customer)
        print(f"Customer Saved in file with ID: {customer_id}\n")
        ids_on_file = map(lambda ctm: ctm["customer_id"],
                          Customer.get_existing_data())
        exp = customer_id in ids_on_file
        self.assertTrue(exp, "No encontre el customer en\
            el archivo de Customers\n")

    def test_display_customer(self):
        """Prueba el despliegue de la informacion del customer
        por su email"""
        print("\nDISPLAY CUSTOMER TEST:")
        srch_email = "exRchd782@hotmail.com"
        disp = Customer.display_customer(srch_email)
        self.assertTrue(disp,
                        f"Customer ID: {srch_email}\
                            no fue encontrado en el archivo\n")

    def test_delete_customer(self):
        """Prueba la eliminacion de un customer por email y
        que no se encuentre en el archivo"""
        email_to_delete = "itHam@mail.com"
        Customer.delete_customer(email_to_delete)
        customers_on_file = Customer.get_existing_data()
        customers_emails = map(lambda ctm: ctm["customer_email"],
                               customers_on_file)
        self.assertTrue(email_to_delete not in customers_emails,
                        "Encontre el customer en el archivo de Customers,\
                            no fue eliminado")

    def test_modify_customer(self):
        """Prueba la modificacion de un customer y
        que no se vea reflejado en el archivo"""
        print("\nMODIFY CUSTOMER TEST:")
        modified_customer_info = {
            "customer_name": "Octavious Maiz Ritus",
            "customer_phone": "1112223334"
        }
        srch_email = "theMaiz@mail.com"
        mod = Customer.modify_customer(srch_email, modified_customer_info)
        self.assertTrue(mod,
                        f"Customer ID: {srch_email} no fue Modificado")
        customers_on_file = Customer.get_existing_data()
        idx = Customer.get_customer_idx("customer_email",
                                        srch_email, customers_on_file)
        for key, value in modified_customer_info.items():
            self.assertEqual(customers_on_file[idx][key], value,
                             f"El valor de {key}:{value}\
                                 no fue modificado en el archivo.\
                                     Valor en archivo:\
                                         {customers_on_file[idx][key]}")
        print("\nModified Customer Data:")
        Customer.display_customer(srch_email)


if __name__ == '__main__':
    unittest.main()
