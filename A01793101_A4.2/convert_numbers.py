"""
    Program to convert numbers to binary and hexadecimal base.
    The results shall be print on a screen and on a file named
    ConvertionResults.txt.
"""
import sys
import os
import re
import time
import copy

def decimal_a_binario(numero_decimal, bit_width=8):
    """Function para convertir decimales a binarios."""
    if numero_decimal < 0:
        numero_decimal = 2**bit_width + numero_decimal

    num_binario = ""

    while numero_decimal > 0:
        resto = numero_decimal % 2
        num_binario = str(resto) + num_binario
        numero_decimal = numero_decimal // 2

    # Rellenar con ceros a la izquierda para alcanzar el ancho de bits deseado
    while len(num_binario) < bit_width:
        num_binario = "0" + num_binario

    return num_binario

def decimal_a_hexadecimal(numero_decimal, bit_width=8):
    """Function para convertir decimales a hexadecimales."""
    my_decimal = copy.copy(numero_decimal)
    if numero_decimal < 0:
        numero_decimal = (1 << bit_width) + numero_decimal

    hexadecimal_result = ""

    while numero_decimal > 0:
        restante = numero_decimal % 16
        # Convertir los restos mayores a 7 a letras (A-F)
        if restante < 10:
            hexadecimal_result = str(restante) + hexadecimal_result
        else:
            hexadecimal_result = chr(ord('A') + restante - 10) + hexadecimal_result
        numero_decimal = numero_decimal // 16

    # Rellenar con 'F' a la izquierda en numeros negativos
    if my_decimal < 0:
        while len(hexadecimal_result) < bit_width:
            hexadecimal_result = "F" + hexadecimal_result
    elif my_decimal == 0:
        hexadecimal_result = "0"

    return hexadecimal_result.upper()

def main():
    """Main program function definition."""
    start_time = time.time()
    with open(sys.argv[1], 'r', encoding="UTF-8") as test_file:
        contents = test_file.readlines()

    test_case_key = f"{re.split(r'(TC[0-9])',sys.argv[1])[1]}"
    r_file_path = f"{re.split(r'(TC[0-9])',sys.argv[1])[0]}\\ConvertionResults_{test_case_key}.txt"
    # If file exists, delete its content first.
    if os.path.isfile(r_file_path):
        with open(r_file_path, 'w', encoding="UTF-8") as result_file:
            result_file.close()
    with open(r_file_path, 'w', encoding="UTF-8") as result_file:
        # Crear el archivo with line of headers
        result_file.write(f"{test_case_key}\n")
        result_file.write("Numero Original\t\t\tNumero Binario\t\t\tNumero Hexadecimal\n")

    print("Numero Original\t\tNumero Binario\t\tNumero Hexadecimal")
    for line in contents:
        try:
            binario = decimal_a_binario(int(line))
            hexadecimal = decimal_a_hexadecimal(int(line))
            print(f"{int(line)}\t\t\t{binario}\t\t\t{hexadecimal}")
            with open(r_file_path, 'a', encoding="UTF-8") as result_file:
                result_file.write(f"\t{int(line)}\t\t\t{binario}\t\t\t{hexadecimal}\n")
        except ValueError:
            print(f"{line} is not numeric type")

    end_time = time.time()
    print(f"\nTiempo de ejecución total: {end_time - start_time:.5f} segundos")

    # Agregar el tiempo de ejecución al final del archivo de resultados
    with open(r_file_path, 'r', encoding="UTF-8") as result_file:
        contents = result_file.readlines()

    with open(r_file_path, 'w', encoding="UTF-8") as result_file:
        for line in contents[:-1]:  # Copiar todo excepto la última línea
            result_file.write(line)
        result_file.write(f"Tiempo de ultima ejecucion: {end_time - start_time:.5f}\n")

if __name__ == "__main__":
    main()
