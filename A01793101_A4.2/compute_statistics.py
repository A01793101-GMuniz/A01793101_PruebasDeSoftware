"""
    Program to calculate all descriptive statistics
    The descriptive statistics are mean, median,
    mode, standard deviation, and variance.
"""
import sys
import os
import re
import time

def median(numbers_list):
    """Function to calculate the median of a list of numbers."""
    # Calcular el índice central.
    mid = len(numbers_list) // 2

    # Si el número de elementos es par, tomar el promedio
    # de los dos valores centrales.
    if len(numbers_list) % 2 == 0:
        return (sorted(numbers_list)[mid] + sorted(numbers_list)[~mid]) / 2
    # Si es impar, el valor central es la mediana.
    return numbers_list[mid]

def calculate_mode(numbers_list):
    """Function to calculate the mode of a list of numbers."""
    numbers_map = {}
    mode = numbers_list[0]
    for element in numbers_list:
        if element in numbers_map:
            numbers_map[element] += 1
            if numbers_map[element] > numbers_map[mode]:
                mode = element
        else:
            numbers_map[element] = 1
    return mode

def variance(numbers_sum, numbers_list):
    """Function to calculate the variance of a list of numbers."""
    mean = numbers_sum / len(numbers_list)
    # Calcular la suma de los cuadrados de las diferencias entre cada elemento y la media.
    dif_sum_square = sum((list_element - mean) ** 2 for list_element in numbers_list)
    # Regresar la Varianza.
    return dif_sum_square / len(numbers_list)

def calculate_sd(numbers_sum, numbers_list):
    """Function to calculate the standar deviation of a list of numbers."""
    var = variance(numbers_sum, numbers_list)
    return var ** 0.5

def main():
    """Main program function definition."""
    start_time = time.time()
    with open(sys.argv[1], 'r', encoding="UTF-8") as test_file:
        contents = test_file.readlines()

    list_of_numbers = []
    sum_of_numbers = 0
    i = 0
    test_case_key = f"{re.split(r'(TC[0-9])',sys.argv[1])[1]}"
    for line in contents:
        try:
            list_of_numbers.append(float(line))
            sum_of_numbers += list_of_numbers[i]
            i += 1
        except ValueError:
            print(f"{line} is not numeric type")

    mediana = median(list_of_numbers)
    moda = calculate_mode(list_of_numbers)
    desv_standar = calculate_sd(sum_of_numbers, list_of_numbers)
    varianza = variance(sum_of_numbers, list_of_numbers)

    r_file_path = f"{re.split(r'(TC[0-9])',sys.argv[1])[0]}\\StatisticsResults_{test_case_key}.txt"
    if os.path.isfile(r_file_path): # Clean all file content
        with open(r_file_path, 'w', encoding="UTF-8") as result_file:
            result_file.close()

    with open(r_file_path, 'a', encoding="UTF-8") as result_file:
        result_file.write(f"{test_case_key}\n")
        result_file.write(f"COUNT: {len(list_of_numbers)}\n")
        result_file.write(f"MEDIA: {sum_of_numbers / len(list_of_numbers):.5f}\n")
        result_file.write(f"MEDIANA: {mediana}\n")
        result_file.write(f"MODA: {moda}\n")
        result_file.write(f"SD: {desv_standar:.5f}\n")
        result_file.write(f"VARIANZA: {varianza:.5f}\n\n")

    print(f"COUNT: {len(list_of_numbers)}")
    print(f"MEDIA: {sum_of_numbers / len(list_of_numbers):.5f}")
    print(f"MEDIANA: {mediana}")
    print(f"MODA: {moda}")
    print(f"SD: {desv_standar:.5f}")
    print(f"VARIANZA: {varianza:.5f}")

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
