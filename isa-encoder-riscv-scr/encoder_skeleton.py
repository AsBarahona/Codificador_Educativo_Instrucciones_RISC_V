#!/usr/bin/env python3
"""
Esqueleto del Codificador Educativo de Instrucciones RISC-V.
CE4301 Arquitectura de Computadores I — Proyecto Individual — 2026-II

Elaborado y facilitado por Dr.-Ing. Jeferson González Gómez
"""
import sys
import re # Para manipular la intrucción de entrada y buscar los patrones según el formato 

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",
              "lw", "lb", "sw", "sb", "beq", "bne"]

FORMAT_MAP = { # Diccionario para asociar los mnemónicos a un formato 
    # Tipo R
    "add": "R", 
    "sub": "R", 
    "and": "R", 
    "or": "R",
    # Tipo I 
    "addi": "I", 
    "andi": "I", 
    "lw": "I_LOAD", 
    "lb": "I_LOAD",
    # Tipo S 
    "sw": "S", 
    "sb": "S",
    # Tipo B 
    "beq": "B", 
    "bne": "B"
}

def encode_instruction(instruction: str) -> int:
    """
    Recibe una instrucción como texto, p. ej. "add x5, x6, x7", y debe
    retornar su codificación de 32 bits como entero (0 <= valor < 2**32).

    Debe soportar únicamente las instrucciones en SOPORTADAS.
    """
    data = parse_instruction(instruction)
    if data == {}:
        raise NotImplementedError("encode_instruction: pendiente de implementar")
    else: 
        inst_32_bits = explain_instruction(data)
        #print(inst_32_bits)

def explain_instruction(instruction_dict: dict) -> int:
    """
    Imprime en pantalla los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    Devuelve la instrucción en 32 bits
    """
    # Tipo R
    if instruction_dict.get("format_type") == "R":
        m = instruction_dict["mnemonic"]
        rd, rs1, rs2 = instruction_dict["rd"], instruction_dict["rs1"], instruction_dict["rs2"]
        rd_b, rs1_b, rs2_b = instruction_dict["rd_binary"], instruction_dict["rs1_binary"], instruction_dict["rs2_binary"]
        funct7 = instruction_dict["funct7"]
        funct3 = instruction_dict["funct3"]
        opcode_b = f"{instruction_dict['opcode']:07b}"

        #32 bits según el orden del formato R
        word_32bit = f"{funct7}{rs2_b}{rs1_b}{funct3}{rd_b}{opcode_b}"

        print("  ")
        print("=== Desglose del Formato Tipo R ===")
        print(f"Campos:  | funct7  |  rs2  |  rs1  | funct3 |   rd  | opcode  |")
        print(f"Rangos:  | [31:25] |[24:20]|[19:15]| [14:12]| [11:7]|  [6:0]  |")
        print(f"Bits:    | {funct7} | {rs2_b} | {rs1_b} |  {funct3}   | {rd_b} | {opcode_b} |")
        print(f"Valores: | {instruction_dict['mnemonic']:<7} | x{instruction_dict['rs2']:<4} | x{instruction_dict['rs1']:<4} | {funct3}    | x{instruction_dict['rd']:<3} | 0x33    |\n")

        print(
            f"\n--- Explicación de los campos de la intrucción {m}) ---\n"
            f"- opcode (0110011): Define que es una instrucción de formato R.\n"
            f"- rd (x{rd} en binario {rd_b}): Registro destino donde se almacenará el resultado.\n"
            f"- rs1 (x{rs1} en binario {rs1_b}) y rs2 (x{rs2} en binario {rs2_b}): Registros fuentes con los operandos de entrada.\n"
            f"- funct3 ({funct3}) y funct7 ({funct7}): Códigos de control que especifican la operación '{m}'.\n"
            f"- Inmediato: No aplica (solo opera con registros)."
        )

        print("  ")
        print(f"Instrucción completa (32 bits): {word_32bit}")
        return int(word_32bit, 2)

    # Tipo I (Aritmético y Carga)
    elif instruction_dict.get("format_type") in ("I", "I_LOAD"):
        m = instruction_dict["mnemonic"]
        rd, rs1, imm = instruction_dict["rd"], instruction_dict["rs1"], instruction_dict["imm"]
        
        # Representaciones en binario
        rd_b = f"{rd:05b}"
        rs1_b = f"{rs1:05b}"
        imm_b = str(num_to_binary(imm, 12))
        funct3 = instruction_dict["funct3"]
        opcode_val = instruction_dict["opcode"]
        opcode_b = f"{opcode_val:07b}"

        # 32 bits según el orden del formato I
        word_32bit = f"{imm_b}{rs1_b}{funct3}{rd_b}{opcode_b}"

        # Determinar si es de carga o aritmética para la explicación textual
        is_load = (instruction_dict.get("format_type") == "I_LOAD" or opcode_val == 0x03)
        op_desc = "de Carga (Load)" if is_load else "I Aritmética"
        imm_desc = f"Offset de memoria ({imm})" if is_load else f"Valor constante inmediato ({imm})"

        print(" ")
        print("=== Desglose del Formato Tipo I ===")
        print(f"Campos:  |    imm[11:0]   |   rs1   | funct3 |   rd    | opcode  |")
        print(f"Rangos:  |    [31:20]     | [19:15] | [14:12]|  [11:7] |  [6:0]  |")
        print(f"Bits:    |  {imm_b}  |  {rs1_b}  |  {funct3}   |  {rd_b}  | {opcode_b} |")
        print(f"Valores: | {imm:<14} | x{rs1:<6} | {funct3}    | x{rd:<6} | {hex(opcode_val):<7} |\n")

        print(
            f"\n--- Explicación de los campos de la instrucción {m} ---\n"
            f"- opcode ({opcode_b}): Define que es una instrucción {op_desc}.\n"
            f"- rd (x{rd} en binario {rd_b}): Registro destino donde se guardará el resultado/dato.\n"
            f"- rs1 (x{rs1} en binario {rs1_b}): Registro base (dirección base o primer operando).\n"
            f"- funct3 ({funct3}): Código de control que especifica la operación exacta '{m}'.\n"
            f"- imm[11:0] ({imm} en binario {imm_b}): {imm_desc} en complemento a dos."
        )

        print(" ")
        print(f"Instrucción completa (32 bits): {word_32bit}")
        return int(word_32bit, 2)

    else:
        raise NotImplementedError("explain_instruction: pendiente de implementar")

def reg_to_int(reg_str: str) -> int:
    """Convierte cadenas como 'x5' o 'x10' a su número de registro (en un entero)."""

    reg_str = reg_str.strip() # Quitar espacios
    if not reg_str.startswith('x'): #Valida formatos válidos en la entrada
        raise ValueError(f"Registro inválido: '{reg_str}'. Debe iniciar con 'x'.")
    num = int(reg_str[1:]) 
    if not (0 <= num <= 31):
        raise ValueError(f"Número de registro fuera de rango (0-31): {num}")
    return num

def num_to_binary(num_reg: int, bits: int) -> int:
    """Convierte un numero entero decimal a un número binario con una cant. determinada de bits"""
    num_masked = num_reg & ((1 << bits) - 1) # Aplicar complemento a dos si num_reg es negativo
    binary = bin(num_masked)[2:].zfill(bits) #Pasar a binario con cierta cant. de bits   
    return binary

def parse_instruction(instruction: str) -> dict:
    """
    Parsea la instrucción dada como texto y retorna un diccionario
    con la información estructurada.
    """
    # Limpiar comas y espacios redundantes (add, x5, x6, x7 -> addx5x6x7)
    clean_inst = instruction.strip().replace(",", " ")
    tokens = clean_inst.split()
    
    if not tokens:
        raise ValueError("Instrucción vacía.")
        
    mnemonic = tokens[0].lower()
    
    if mnemonic not in FORMAT_MAP:
        raise ValueError(f"Instrucción no soportada: '{mnemonic}'")
        
    fmt_inst = FORMAT_MAP[mnemonic] #Busca la pareja del mnemónico en el diccionario (el formato)
    parsed_data = {"mnemonic": mnemonic, "format_type": fmt_inst.replace("_LOAD", "")} #Deja el tipo I_LOAD como I

    # Tipo R: add, sub, and, or -> mnemonic rd, rs1, rs2
    if fmt_inst == "R":
        if len(tokens) != 4:
            raise ValueError(f"Formato incorrecto para {mnemonic}. Estructura adecuada: {mnemonic} rd, rs1, rs2")
        
        #funct3 y funct7 para tipo R
        funct3_map = {"add": "000", "sub": "000", "and": "111", "or": "110"}
        funct7_map = {"add": "0000000", "sub": "0100000", "and": "0000000", "or": "0000000"}
        rd = reg_to_int(tokens[1])
        rs1 = reg_to_int(tokens[2])
        rs2 = reg_to_int(tokens[3])

        parsed_data.update({
            "rd": rd,
            "rs1": rs1,
            "rs2": rs2,
            "opcode": 0b0110011,
            "funct3": funct3_map[mnemonic],
            "funct7": funct7_map[mnemonic],
            "rd_binary": num_to_binary(rd, 5),
            "rs1_binary": num_to_binary(rs1, 5),
            "rs2_binary": num_to_binary(rs2, 5)
        })

    # Tipo I Aritmético: addi, andi -> mnemonic rd, rs1, imm
    elif fmt_inst == "I":
        if len(tokens) != 4:
            raise ValueError(f"Formato incorrecto para {mnemonic}. Estructura adecuada: {mnemonic} rd, rs1, imm")

        funct3_map_i = {"addi": "000", "andi": "111"}
        rd, rs1, imm = reg_to_int(tokens[1]), reg_to_int(tokens[2]), int(tokens[3])

        parsed_data.update({
            "rd": rd,
            "rs1": rs1,
            "imm": imm,
            "opcode": 0b0010011,
            "funct3": funct3_map_i[mnemonic],
            "rd_binary": num_to_binary(rd, 5),
            "rs1_binary": num_to_binary(rs1, 5),
            "imm_binary": num_to_binary(imm, 12)
        })

    # Tipo I Carga: lw, lb -> mnemonic rd, imm(rs1)
    elif fmt_inst == "I_LOAD":
        # Espera algo como: lw x5, 8(x6) -> tokens: ['lw', 'x5', '8(x6)']
        if len(tokens) != 3:
            raise ValueError(f"Formato incorrecto para {mnemonic}. Estructura adecuada: {mnemonic} rd, imm(rs1)")
        match = re.match(r"^(-?\d+)\((x\d+)\)$", tokens[2]) #Verifica que tokens[2] sea de la forma imm(rs1)
        if not match:
            raise ValueError(f"Formato de memoria inválido: '{tokens[2]}'")

        funct3_map_load = {"lb": "000", "lw": "010"}
        rd = reg_to_int(tokens[1])
        imm = int(match.group(1))
        rs1 = reg_to_int(match.group(2))

        parsed_data.update({
            "rd": rd,
            "rs1": rs1,
            "imm": imm,
            "opcode": 0b0000011,
            "funct3": funct3_map_load[mnemonic],
            "rd_binary": num_to_binary(rd, 5),
            "rs1_binary": num_to_binary(rs1, 5),
            "imm_binary": num_to_binary(imm, 12)
        })

    # Tipo S Memoria: sw, sb -> mnemonic rs2, imm(rs1)
    elif fmt_inst == "S":
        if len(tokens) != 3:
            raise ValueError(f"Formato incorrecto para {mnemonic}. Estructura adecuada: {mnemonic} rs2, imm(rs1)")
        match = re.match(r"^(-?\d+)\((x\d+)\)$", tokens[2]) #Verifica que tokens[2] sea de la forma imm(rs1) y separa en grupos
        if not match:
            raise ValueError(f"Formato de memoria inválido: '{tokens[2]}'")
        parsed_data.update({
            "rs2": reg_to_int(tokens[1]),
            "imm": int(match.group(1)),
            "rs1": reg_to_int(match.group(2))
        })

    # Tipo B Salto: beq, bne -> mnemonic rs1, rs2, imm
    elif fmt_inst == "B":
        if len(tokens) != 4:
            raise ValueError(f"Formato incorrecto para {mnemonic}. Estructura adecuada: {mnemonic} rs1, rs2, imm")
        parsed_data.update({
            "rs1": reg_to_int(tokens[1]),
            "rs2": reg_to_int(tokens[2]),
            "imm": int(tokens[3])
        })

    # Imprimir descomposición en consola
    print("")
    print("=== Descomposición de la Instrucción ===")
    for k, v in parsed_data.items():
        print(f"  {k}: {v}")
    print("========================================")

    return parsed_data

def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) 

    ##print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()
