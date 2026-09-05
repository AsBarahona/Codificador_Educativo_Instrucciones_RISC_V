$toolchainPath = ".\Tools\xpack\xpack-riscv-none-elf-gcc-15.2.0-1\bin"
$gcc = "$toolchainPath\riscv-none-elf-gcc.exe"
$objdump = "$toolchainPath\riscv-none-elf-objdump.exe"
$encoderPath = "..\isa-encoder-riscv-scr\encoder_skeleton.py"

Write-Host ""
Write-Host "VALIDACION CONTRA TOOLCHAIN OFICIAL" -ForegroundColor Cyan

function Get-ToolchainHex {
    param([string]$Instruccion)

    # Ajustar sintaxis de branches para GCC (convertir offset en .+X / .-X para inst de formato B)
    $instruccionGCC = $Instruccion
    if ($Instruccion -match '^(beq|bne|blt|bge|bltu|bgeu)\s+([^,]+,\s*[^,]+,\s*)([+-]?\d+)$') {
        $opYRegs = $Matches[2]
        $offset = [int]$Matches[3]
        if ($offset -ge 0) {
            $instruccionGCC = "$($Matches[1]) ${opYRegs}.+$offset"
        } else {
            $instruccionGCC = "$($Matches[1]) ${opYRegs}.$offset"
        }
    }

    $tempFile = "temp_asm_$(Get-Random)"

    Set-Content -Path "$tempFile.s" -Value ".text" -Encoding ASCII
    Add-Content -Path "$tempFile.s" -Value $instruccionGCC -Encoding ASCII

    & $gcc -march=rv32i -mabi=ilp32 -c "$tempFile.s" -o "$tempFile.o" 2>$null
    $hex = & $objdump -d "$tempFile.o" | Select-String -Pattern '\s+([0-9a-f]{8})\s+' | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1
    Remove-Item -Force "$tempFile.s", "$tempFile.o" -ErrorAction SilentlyContinue

    return $hex
}

$casos = Get-Content casos_prueba.txt | Where-Object { $_ -notmatch '^#' -and $_.Trim() -ne '' }
$total = 0
$correctos = 0

foreach ($linea in $casos) {
    $partes = $linea -split ';'
    if ($partes.Count -lt 2) { continue }
    
    $inst = $partes[0].Trim()
    $esp = $partes[1].Trim().ToLower()
    $total++
    
    $hTool = Get-ToolchainHex $inst
    if ($hTool) { $hTool = "0x$($hTool.ToLower())" } else { $hTool = "ERROR" }
    
    $salida = python $encoderPath "$inst" 2>$null
    $hEnc = $salida | Select-String 'HEX: (0x[0-9a-fA-F]+)' | ForEach-Object { $_.Matches.Groups[1].Value }
    if ($hEnc) { $hEnc = $hEnc.ToLower() } else { $hEnc = "ERROR" }
    
    Write-Host "Caso $total : $inst" -ForegroundColor Yellow
    Write-Host "  Esperado:    $esp"
    Write-Host "  Toolchain:   $hTool"
    Write-Host "  Herramienta: $hEnc"
    
    if ($hEnc -eq $hTool) {
        Write-Host "  CORRECTO" -ForegroundColor Green
        $correctos++
    } else {
        Write-Host "  INCORRECTO" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "RESUMEN: $correctos de $total correctos" -ForegroundColor Cyan
if ($correctos -eq $total) {
    Write-Host "TODOS LOS CASOS PASARON!" -ForegroundColor Green
} else {
    Write-Host "ALGUNOS CASOS FALLARON" -ForegroundColor Red
}