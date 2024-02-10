"""
    Program to compute the total cost for all sales
    included in the JSON archives. The results shall
    be print on a screen and on a file named SalesResults.txt.

    The total cost should include all items in the sale considering
    the cost for every item.
"""
import sys
import os
import re
import time
import json
import pandas as pd
from tabulate import tabulate


def create_results_file(r_file_path, test_case_key):
    """Funcion para crear un archivo de resultados
    con cada ejecucion"""
    if os.path.isfile(r_file_path):
        with open(r_file_path, 'w', encoding="UTF-8") as result_file:
            result_file.close()
    with open(r_file_path, 'w', encoding="UTF-8") as result_file:
        # Crear el archivo con headers
        result_file.write(f"{test_case_key}\n")


def main():
    """Main program function definition."""
    start_time = time.time()
    if not os.path.isfile(sys.argv[1]):
        raise Exception(f"{sys.argv[1]} is not a file")
    with open(sys.argv[1], 'r', encoding="UTF-8") as archivo:
        cat_df = json.load(archivo)
    cat_df = pd.DataFrame(cat_df)
    cat_df = cat_df.rename(columns={"title": "product"})

    if not os.path.isfile(sys.argv[2]):
        raise Exception(f"{sys.argv[2]} is not a file")
    with open(sys.argv[2], 'r', encoding="UTF-8") as archivo:
        sales_df = json.load(archivo)
    sales_df = pd.DataFrame(sales_df)
    sales_df = sales_df.rename(columns={"Product": "product",
                                        "SALE_Date": "sale_date",
                                        "Quantity": "quantity"})

    # Obtener el numero de TC del archivo de Sales
    test_case_key = f"{re.split(r'(TC[0-9])',sys.argv[2])[1]}"
    path_to_file = f"{re.split(r'(TC[0-9])',sys.argv[1])[0]}"
    r_file_path = f"{path_to_file}\\SalesResults_{test_case_key}.txt"
    create_results_file(r_file_path, test_case_key)
    total_cost = 0
    det_ventas = []
    for _, product in sales_df.iterrows():
        if product["product"] in cat_df["product"].values:
            item_price = cat_df.loc[cat_df["product"] ==
                                    product["product"], "price"].values[0]
            if product["quantity"] > 0:
                det_ventas.append([product["product"], product["quantity"],
                                   item_price,
                                   item_price * product["quantity"]])
            total_cost += (item_price * product["quantity"])
        else:
            print(f"Not Found item on catalog: \n{product}\n")

    print(tabulate(det_ventas, headers=['Producto', 'Cantidad',
                                        'Valor Unitario', 'Subtotal']))
    print("\n-----------------------------------------------------------\n")
    print(f"TOTAL\t\t\t\t\t\t\t\t{total_cost:.2f}\n")

    with open(r_file_path, 'a', encoding="UTF-8") as result_file:
        result_file.write(tabulate(det_ventas,
                                   headers=['Producto', 'Cantidad',
                                            'Valor Unitario', 'Subtotal']))
        result_file.write("\n--------------------------------------------\n")
        result_file.write(f"\nTOTAL:\t\t\t\t\t\t\t\t{total_cost:.2f}\n\n")

    end_time = time.time()
    print(f"\nTiempo de ejecución total: {end_time - start_time:.5f} segundos")

    # Agregar el tiempo de ejecución al final del archivo de resultados
    with open(r_file_path, 'r', encoding="UTF-8") as result_file:
        contents = result_file.readlines()

    with open(r_file_path, 'w', encoding="UTF-8") as result_file:
        for line in contents[:-1]:  # Copiar todo excepto la última línea
            result_file.write(line)
        result_file.write(f"\nTiempo de ultima ejecucion:\
            {end_time - start_time:.5f}\n")


if __name__ == "__main__":
    main()
