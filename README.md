# Rol
Eres un desarrollador senior especializado en **Python, herramientas CLI y procesamiento de imágenes**.
Tu objetivo es **refactorizar y modernizar completamente** un script CLI antiguo, manteniendo su funcionalidad principal.

---

Esto es un hard snack

## Contexto del proyecto
Tenemos un **script personal de línea de comandos** para optimizar imágenes en local.

Estado actual:
- Código antiguo y poco legible.
- Usa `subprocess` con `cwebp` / `dwebp`.
- Dependencia problemática del sistema.
- Funciona, pero no sigue buenas prácticas modernas.

---

## 🎯 Objetivo principal
Refactorizar el script para:

- ❌ Eliminar completamente el uso de `cwebp` y `dwebp`.
- ✅ Usar **Pillow (PIL)** como backend de procesamiento.
- Mantener optimización de imágenes en local.
- Mejorar **legibilidad, estructura y mantenibilidad**.
- Convertirlo en una **herramienta CLI bien hecha en Python**.

---

## 📦 Dependencias
- Usar **Pillow** como única dependencia externa.
- Asumir que el entorno Python ya está disponible.
- El proyecto debe poder instalarse vía **pipx**.

---

## 🧠 Reglas de estilo (MUY IMPORTANTE)

### Lenguaje
- ✅ **Funciones y variables en inglés**
- ✅ **Comandos CLI en inglés**
- ✅ **Comentarios y mensajes en español**

### Código
- Usar `pathlib` en lugar de `os.path`.
- Usar `argparse` de forma clara y bien estructurada.
- Evitar duplicación de lógica.
- No usar `subprocess`.
- Manejar errores con mensajes claros para el usuario.

---

## 🖼️ Funcionalidades requeridas

### Formatos soportados
- Entrada: PNG, JPG, JPEG, TIFF, BMP
- Salida:
  - WebP (default)
  - JPG (opcional)

---

### Opciones CLI (mantener espíritu, no nombres antiguos)

- Comando principal único (sin subcomandos innecesarios).
- Flags sugeridas:
  - `--lossless`
  - `--quality`
  - `--keep-metadata`
  - `--resize-factor` (ej. dividir dimensiones)
  - `--output-format` (`webp` | `jpg`)
  - `--delete-original`
  - `--no-rename`

- Soportar:
  - Un archivo
  - Múltiples archivos

---

### Optimización con Pillow
- Usar `Image.save()` correctamente:
  - `quality`
  - `lossless`
  - `optimize=True`
- Mantener metadatos solo si se solicita.
- Redimensionar imágenes de forma segura.

---

## 🧪 Buenas prácticas CLI
- Validar archivos de entrada.
- Mostrar mensajes claros:
  - éxito
  - error
  - advertencias
- No imprimir tracebacks innecesarios.
- Código fácil de extender.

---

## 📄 README (OBLIGATORIO)

Crear un `README.md` que explique:

### Contenido mínimo
- Qué hace la herramienta.
- Requisitos.
- Instalación con **pipx**:
'''sh
pipx install .
'''
- Ejemplos de uso:
  - Convertir a WebP
  - Usar lossless
  - Convertir a JPG
  - Procesar múltiples archivos

### Tono
- Claro
- Directo
- Pensado para uso personal / scripts locales

---

## 🚫 Restricciones
- No usar cwebp.
- No usar subprocess.
- No introducir dependencias innecesarias.
- No hacer el CLI más complejo de lo necesario.

---

## ✅ Resultado esperado
- Script Python moderno, limpio y legible.
- Optimización de imágenes completamente en Pillow.
- CLI fácil de usar.
- README claro con instalación vía pipx.
# imgoptimize

🖼️ **Herramienta CLI moderna para optimizar imágenes en local usando Pillow**

Una utilidad de línea de comandos rápida y eficiente para convertir y optimizar imágenes sin dependencias externas del sistema. Ideal para uso personal y scripts de automatización.

---

## ✨ Características

- 🚀 **100% Python** - Sin dependencias de binarios externos (adiós `cwebp`/`dwebp`)
- 🎨 **Múltiples formatos** - Soporta PNG, JPG, JPEG, TIFF, BMP
- 📦 **Salida optimizada** - Convierte a WebP o JPG comprimido
- ⚡ **Configurable** - Control total sobre calidad, compresión y dimensiones
- 🔄 **Procesamiento por lotes** - Optimiza múltiples imágenes de una vez
- 📊 **Feedback claro** - Muestra reducción de tamaño y estadísticas

---

## 📋 Requisitos

- Python 3.8 o superior
- pipx (recomendado) o pip

---

## 🚀 Instalación

### Opción 1: Instalación con pipx (recomendado)

```sh
# Instalar desde el directorio del proyecto
pipx install .

# O instalar en modo editable para desarrollo
pipx install -e .
```

### Opción 2: Instalación con pip

```sh
pip install .
```

---

## 📖 Uso

### Sintaxis básica

```sh
imgoptimize [opciones] archivo1.png [archivo2.jpg ...]
```

### Ejemplos

#### Convertir una imagen a WebP (default)
```sh
imgoptimize foto.png
# Resultado: foto_optimized.webp
```

#### Usar compresión sin pérdida
```sh
imgoptimize foto.png --lossless
# Ideal para capturas de pantalla o gráficos
```

#### Ajustar calidad de compresión
```sh
imgoptimize foto.png --quality 90
# Valores: 1-100 (default: 85)
```

#### Convertir a JPG en lugar de WebP
```sh
imgoptimize foto.png --output-format jpg
# Resultado: foto_optimized.jpg
```

#### Reducir dimensiones (dividir por 2)
```sh
imgoptimize foto.png --resize-factor 2
# Si la imagen es 4000x3000, resultado será 2000x1500
```

#### Reducir dimensiones con división entera
```sh
imgoptimize foto.png --resize 12
# Si la imagen es 1024x1024, resultado será 85x85 (1024//12 = 85)
```

#### Mantener metadatos EXIF
```sh
imgoptimize foto.jpg --keep-metadata
# Preserva información de cámara, ubicación, etc.
```

#### Eliminar archivo original
```sh
imgoptimize foto.png --delete-original
# ⚠️ Usar con precaución
```

#### No renombrar archivo (reemplazar)
```sh
imgoptimize foto.png --no-rename
# Resultado: foto.webp (sin "_optimized")
```

#### Procesar múltiples archivos
```sh
imgoptimize *.png
# Optimiza todas las imágenes PNG del directorio
```

#### Combinación de opciones
```sh
imgoptimize foto.png --quality 95 --resize-factor 2 --keep-metadata --output-format jpg
```

---

## 🎛️ Opciones disponibles

| Opción | Descripción | Default |
|--------|-------------|---------|
| `--quality` | Calidad de compresión (1-100) | 85 |
| `--lossless` | Compresión sin pérdida (solo WebP) | false |
| `--keep-metadata` | Mantener metadatos EXIF | false |
| `--resize-factor` | Factor de redimensionamiento (división flotante) | - |
| `--resize` | Dividir dimensiones entre N (división entera) | - |
| `--output-format` | Formato de salida (webp, jpg) | webp |
| `--delete-original` | Eliminar archivo original | false |
| `--no-rename` | No agregar "_optimized" al nombre | false |

---

## 🔧 Formatos soportados

### Entrada
- PNG (.png)
- JPG/JPEG (.jpg, .jpeg)
- TIFF (.tiff, .tif)
- BMP (.bmp)

### Salida
- WebP (.webp) - Recomendado para web
- JPG (.jpg) - Mayor compatibilidad

---

## 💡 Casos de uso

### Optimizar fotos para web
```sh
imgoptimize galeria/*.jpg --quality 80 --resize-factor 1.5
```

### Convertir capturas de pantalla
```sh
imgoptimize captura.png --lossless --output-format webp
```

### Preparar imágenes para email
```sh
imgoptimize documento.png --resize 2 --quality 75 --output-format jpg
```

### Reducir imágenes grandes para web
```sh
imgoptimize foto_4k.png --resize 4 --quality 85
# 3840x2160 → 960x540
```

### Procesamiento automatizado
```sh
#!/bin/bash
for img in input/*.png; do
    imgoptimize "$img" --quality 85 --delete-original
done
```

---

## 🏗️ Desarrollo

### Estructura del proyecto
```
cweb-small/
├── src/
│   └── imgoptimize/
│       ├── __init__.py
│       └── cli.py          # Lógica principal
├── pyproject.toml           # Configuración del proyecto
├── setup.py                 # Setup para instalación
└── README.md                # Este archivo
```

### Instalación en modo desarrollo
```sh
pipx install -e .
```

---

## 📝 Notas técnicas

- **Backend**: Pillow (PIL Fork) - biblioteca pura de Python
- **Conversión de color**: Manejo automático de RGBA → RGB para JPG
- **Redimensionamiento**: Usa algoritmo LANCZOS para mejor calidad
- **Optimización**: Flag `optimize=True` en todas las conversiones

---

## 🎯 Diferencias con versión anterior

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Backend** | cwebp/dwebp (binarios) | Pillow (Python puro) |
| **Instalación** | Dependencia del sistema | `pipx install .` |
| **Portabilidad** | Solo Linux/macOS | Multiplataforma |
| **Código** | subprocess + shell | API Python nativa |
| **Mantenibilidad** | Baja | Alta |

---

## 🐛 Solución de problemas

### Error: "No module named 'PIL'"
```sh
# Reinstalar con dependencias
pipx reinstall imgoptimize
```

### Error: "command not found: imgoptimize"
```sh
# Verificar instalación de pipx
pipx list

# Reinstalar
pipx install --force .
```

---

## 📄 Licencia

MIT - Uso personal y libre modificación

---

## 🙏 Créditos

- **Pillow**: https://python-pillow.org/
- **Python**: https://www.python.org/
