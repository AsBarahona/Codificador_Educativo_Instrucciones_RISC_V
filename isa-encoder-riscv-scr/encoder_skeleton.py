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

    # TODO: implementar. Sugerencia: parsear el mnemónico y los operandos,
    # despachar según el formato (R/I/S/B), y ensamblar los campos con
    # operaciones de bits.
    raise NotImplementedError("encode_instruction: pendiente de implementar")


def explain_instruction(instruction: str, word: int) -> str:
    """
    Debe retornar un texto (para imprimirse en pantalla) que muestre, de
    forma visual, los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    """
    # TODO: implementar.
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
        parsed_data.update({
            "rd": reg_to_int(tokens[1]),
            "rs1": reg_to_int(tokens[2]),
            "rs2": reg_to_int(tokens[3])
        })

    # Tipo I Aritmético: addi, andi -> mnemonic rd, rs1, imm
    elif fmt_inst == "I":
        if len(tokens) != 4:
            raise ValueError(f"Formato incorrecto para {mnemonic}. Estructura adecuada: {mnemonic} rd, rs1, imm")
        parsed_data.update({
            "rd": reg_to_int(tokens[1]),
            "rs1": reg_to_int(tokens[2]),
            "imm": int(tokens[3])
        })

    # Tipo I Carga: lw, lb -> mnemonic rd, imm(rs1)
    elif fmt_inst == "I_LOAD":
        # Espera algo como: lw x5, 8(x6) -> tokens: ['lw', 'x5', '8(x6)']
        if len(tokens) != 3:
            raise ValueError(f"Formato incorrecto para {mnemonic}. Estructura adecuada: {mnemonic} rd, imm(rs1)")
        match = re.match(r"^(-?\d+)\((x\d+)\)$", tokens[2]) #Verifica que tokens[2] sea de la forma imm(rs1)
        if not match:
            raise ValueError(f"Formato de memoria inválido: '{tokens[2]}'")
        parsed_data.update({
            "rd": reg_to_int(tokens[1]),
            "imm": int(match.group(1)),
            "rs1": reg_to_int(match.group(2))
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
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()
