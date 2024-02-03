"""
    Program to  identify all distinct words and the
    frequency of them (how many times the word “X” appears in
    the file). The results shall be print on a screen and on
    a file named WordCountResults.txt
"""
import sys
import os
import re
import time

def main():
    """Main program function definition."""
    start_time = time.time()
    with open(sys.argv[1], 'r', encoding="UTF-8") as test_file:
        contents = test_file.readlines()

    test_case_key = f"{re.split(r'(TC[0-9])',sys.argv[1])[1]}"
    r_file_path = f"{re.split(r'(TC[0-9])',sys.argv[1])[0]}\\WordCountResults_{test_case_key}.txt"
    if os.path.isfile(r_file_path):
        with open(r_file_path, 'w', encoding="UTF-8") as result_file:
            result_file.close()
    with open(r_file_path, 'w', encoding="UTF-8") as result_file:
        # Crear el archivo with line of headers
        result_file.write(f"{test_case_key}\n")
        result_file.write("Palabra\t\t\tNumero de apariciones\t\t\t\n")

    print("Palabra\t\tNumero de apariciones\t\t\n")
    mapa_de_palabras = {}
    for line in contents:
        try:
            palabra = line.strip()
            if palabra in mapa_de_palabras:
                mapa_de_palabras[palabra] += 1
            else:
                mapa_de_palabras[palabra] = 1
        except ValueError:
            print(f"{line} is not string type")

    mapa_de_palabras = dict(sorted(mapa_de_palabras.items(), key=lambda x:x[1], reverse=True))
    for palabra, num_de_apariciones in mapa_de_palabras.items():
        print(f"{palabra}\t\t{num_de_apariciones}\n")
        with open(r_file_path, 'a', encoding="UTF-8") as result_file:
            result_file.write(f"{palabra}\t\t\t{num_de_apariciones}\n")

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
