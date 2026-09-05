# Codificador_Educativo_Instrucciones_-RISC_V

## Preparación del Entorno

Para ejecutar y validar el Codificador Educativo de Instrucciones RISC-V, se debe configurar el entorno de ejecución según el sistema operativo.

### 1. Requisitos de Software y Dependencias

* **Python 3.x:** El codificador utiliza únicamente la biblioteca estándar de Python (`sys`, `re`), por lo que **no se requieren dependencias externas ni instalación mediante `pip`**.
* **Intérprete de Bash:** Necesario para ejecutar la interfaz `./run.sh` (nativo en Linux/macOS, Git Bash en Windows).
* **PowerShell:** Necesario en Windows para la ejecución del script de validación `validar.ps1`.

### 2. Configuración en Windows (Git Bash)

#### Configuración del alias de Python en Git Bash
Si al ejecutar `./run.sh` se presenta un error indicando que no se encuentra `python3`, cree un enlace simbólico al ejecutable de Python desde la terminal de Git Bash:

```bash
mkdir -p ~/bin
cp $(which python) ~/bin/python3
```

## Configuración del Toolchain xPack (Validación de Ensamblador)
Dado que la carpeta `riscv_toolchain_scr/Tools/` fue excluida del repositorio debido al tamaño, siga estos pasos para habilitar el entorno de prueba:

1. Descargue el toolchain **xPack GNU RISC-V Embedded GCC** (versión `15.2.0-1` para arquitectura de 64 bits). Descargado de: https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases
2. Extraiga el contenido comprimido manteniendo la siguiente estructura de directorios:

```text
riscv_toolchain_scr/
└── Tools/
    └── xpack/
        └── xpack-riscv-none-elf-gcc-15.2.0-1/
```
3. Validación automatizada con el Toolchain: Para ejecutar los casos de prueba y comparar las salidas codificadas contra el ensamblador oficial desde PowerShell utilice: 
```bash
.\riscv_toolchain_scr\validar.ps1
```

## Instrucciones de Ejecución de la herramienta desarrollada
### Ejecución individual de una instrucción
Para codificar una instrucción desde la terminal Bash:

```bash
./run.sh "add x5, x6, x7"
```

## Organización del Repositorio

A continuación se describe la estructura general del proyecto y el contenido de sus carpetas principales:

```text
Codificador_Educativo_Instrucciones_-RISC_V/
├── docs/
│   ├── imags/
│   └── Desarrollo.md                 
├── isa-encoder-riscv-scr/
│   ├── encoder_skeleton.py            
│   ├── README.md                     
│   └── run.sh                          
└── riscv_toolchain_scr/
    ├── casos_prueba.txt                
    ├── validar.ps1                     
    └── Tools/
        └── xpack/
            └── xpack-riscv-none-elf-gcc-15.2.0-1/  # Toolchain oficial xPack GCC (excluido en .gitignore)
```

### Descripción de Componentes

* **`isa-encoder-riscv-scr/`**: Contiene los archivos de ejecución del codificador. Incluye `encoder_skeleton.py` (Código fuente principal del codificador en Python) y `run.sh` (Script de entrada para ejecutar la herramienta desde Bash).
* **`riscv_toolchain_scr/`**: Alberga el entorno de pruebas automatizadas. Contiene el script `validar.ps1` que compara las salidas del codificador contra la compilación oficial de xPack GNU RISC-V GCC, así como el archivo `casos_prueba.txt`.
* **`docs/`**: Incluye la documentación técnica en formato Markdown (`.md`) que detalla el diseño, la arquitectura y las decisiones tomadas durante el desarrollo del proyecto. En el archivo `Desarrollo.md`.