#!/usr/bin/env python3
"""
CLI para optimizar imágenes usando Pillow
Soporta conversión a WebP y JPG con múltiples opciones de optimización
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from PIL import Image, ExifTags


# Formatos de entrada soportados
SUPPORTED_INPUT_FORMATS = {'.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp'}

# Formatos de salida soportados
SUPPORTED_OUTPUT_FORMATS = {'webp', 'jpg', 'jpeg'}


class ImageOptimizer:
    """Clase para optimizar imágenes usando Pillow"""
    
    def __init__(
        self,
        quality: int = 85,
        lossless: bool = False,
        keep_metadata: bool = False,
        resize_factor: Optional[float] = None,
        resize: Optional[int] = None,
        output_format: str = 'webp',
        delete_original: bool = False,
        no_rename: bool = False
    ):
        self.quality = quality
        self.lossless = lossless
        self.keep_metadata = keep_metadata
        self.resize_factor = resize_factor
        self.resize = resize
        self.output_format = output_format.lower()
        self.delete_original = delete_original
        self.no_rename = no_rename
        
    def optimize_image(self, input_path: Path) -> Optional[Path]:
        """
        Optimiza una imagen y la guarda en el formato especificado
        
        Args:
            input_path: Ruta de la imagen de entrada
            
        Returns:
            Ruta de la imagen optimizada o None si hubo error
        """
        try:
            # Validar que el archivo existe
            if not input_path.exists():
                print(f"❌ Error: El archivo '{input_path}' no existe")
                return None
            
            # Validar formato de entrada
            if input_path.suffix.lower() not in SUPPORTED_INPUT_FORMATS:
                print(f"❌ Error: Formato no soportado '{input_path.suffix}'")
                print(f"   Formatos soportados: {', '.join(SUPPORTED_INPUT_FORMATS)}")
                return None
            
            # Abrir imagen
            print(f"📂 Procesando: {input_path.name}")
            img = Image.open(input_path)
            
            # Convertir a RGB si es necesario (WebP y JPG no soportan RGBA con transparencia)
            if self.output_format in ['jpg', 'jpeg']:
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Crear fondo blanco para JPG
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    if 'transparency' in img.info or img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                    else:
                        img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
            elif self.output_format == 'webp':
                # WebP soporta RGBA, pero convertir otros modos problemáticos
                if img.mode not in ('RGB', 'RGBA'):
                    if img.mode in ('LA', 'L'):
                        img = img.convert('RGBA' if 'transparency' in img.info else 'RGB')
                    elif img.mode == 'P':
                        img = img.convert('RGBA' if 'transparency' in img.info else 'RGB')
            
            # Redimensionar con --resize (división entera)
            if self.resize and self.resize > 0:
                new_width = img.width // self.resize
                new_height = img.height // self.resize
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"   ↔️  Redimensionado: {img.width}x{img.height} (1/{self.resize} del tamaño original)")
            # Redimensionar si se especificó factor
            elif self.resize_factor and self.resize_factor != 1.0:
                new_width = int(img.width / self.resize_factor)
                new_height = int(img.height / self.resize_factor)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"   ↔️  Redimensionado: {img.width}x{img.height}")
            
            # Preparar metadatos si se solicita
            exif_data = None
            if self.keep_metadata:
                try:
                    exif_data = img.info.get('exif')
                except Exception:
                    pass
            
            # Determinar nombre de archivo de salida
            if self.no_rename:
                # Mantener nombre original, solo cambiar extensión
                output_path = input_path.with_suffix(f'.{self.output_format}')
            else:
                # Agregar sufijo antes de la extensión
                stem = input_path.stem
                output_path = input_path.with_name(f"{stem}_optimized.{self.output_format}")
            
            # Preparar opciones de guardado
            save_kwargs = {
                'optimize': True,
            }
            
            if self.output_format == 'webp':
                save_kwargs['quality'] = self.quality
                save_kwargs['lossless'] = self.lossless
                if exif_data:
                    save_kwargs['exif'] = exif_data
            elif self.output_format in ['jpg', 'jpeg']:
                save_kwargs['quality'] = self.quality
                save_kwargs['format'] = 'JPEG'
                if exif_data:
                    save_kwargs['exif'] = exif_data
            
            # Guardar imagen optimizada
            img.save(output_path, **save_kwargs)
            
            # Calcular reducción de tamaño
            original_size = input_path.stat().st_size
            optimized_size = output_path.stat().st_size
            reduction = ((original_size - optimized_size) / original_size) * 100
            
            print(f"   ✅ Guardado: {output_path.name}")
            print(f"   📊 Tamaño: {original_size / 1024:.1f}KB → {optimized_size / 1024:.1f}KB ({reduction:+.1f}%)")
            
            # Eliminar original si se solicita
            if self.delete_original and output_path != input_path:
                input_path.unlink()
                print(f"   🗑️  Original eliminado")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error procesando '{input_path.name}': {str(e)}")
            return None


def parse_arguments() -> argparse.Namespace:
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Optimiza imágenes usando Pillow (PNG, JPG, TIFF, BMP → WebP/JPG)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s image.png                           # Convertir a WebP con calidad 85
  %(prog)s image.png --lossless                # Convertir a WebP sin pérdida
  %(prog)s image.png --quality 90              # Convertir con calidad 90
  %(prog)s image.png --output-format jpg       # Convertir a JPG
  %(prog)s image.png --resize-factor 2         # Reducir dimensiones a la mitad
  %(prog)s *.png                               # Procesar múltiples archivos
  %(prog)s image.png --delete-original         # Eliminar archivo original
  %(prog)s image.png --no-rename               # No agregar "_optimized" al nombre
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        type=str,
        help='Archivo(s) de imagen a optimizar'
    )
    
    parser.add_argument(
        '--quality',
        type=int,
        default=85,
        choices=range(1, 101),
        metavar='1-100',
        help='Calidad de compresión (1-100, default: 85)'
    )
    
    parser.add_argument(
        '--lossless',
        action='store_true',
        help='Usar compresión sin pérdida (solo WebP)'
    )
    
    parser.add_argument(
        '--keep-metadata',
        action='store_true',
        help='Mantener metadatos EXIF de la imagen original'
    )
    
    parser.add_argument(
        '--resize-factor',
        type=float,
        metavar='FACTOR',
        help='Factor de redimensionamiento (ej: 2 = mitad del tamaño, 0.5 = doble)'
    )
    
    parser.add_argument(
        '--resize',
        type=int,
        metavar='N',
        help='Dividir dimensiones entre N (ej: --resize 12 = 1/12 del tamaño original)'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['webp', 'jpg', 'jpeg'],
        default='webp',
        help='Formato de salida (default: webp)'
    )
    
    parser.add_argument(
        '--delete-original',
        action='store_true',
        help='Eliminar archivo original después de optimizar'
    )
    
    parser.add_argument(
        '--no-rename',
        action='store_true',
        help='No agregar "_optimized" al nombre del archivo'
    )
    
    return parser.parse_args()


def main():
    """Función principal del CLI"""
    args = parse_arguments()
    
    # Validar resize-factor
    if args.resize_factor is not None and args.resize_factor <= 0:
        print("❌ Error: --resize-factor debe ser mayor que 0")
        sys.exit(1)
    
    # Validar resize
    if args.resize is not None and args.resize <= 0:
        print("❌ Error: --resize debe ser un entero mayor que 0")
        sys.exit(1)
    
    # Validar que no se usen ambas opciones a la vez
    if args.resize is not None and args.resize_factor is not None:
        print("❌ Error: No se puede usar --resize y --resize-factor al mismo tiempo")
        sys.exit(1)
    
    # Crear optimizador
    optimizer = ImageOptimizer(
        quality=args.quality,
        lossless=args.lossless,
        keep_metadata=args.keep_metadata,
        resize_factor=args.resize_factor,
        resize=args.resize,
        output_format=args.output_format,
        delete_original=args.delete_original,
        no_rename=args.no_rename
    )
    
    # Convertir archivos a Path objects
    input_files: List[Path] = [Path(f) for f in args.files]
    
    # Procesar cada archivo
    print(f"\n🚀 Iniciando optimización de {len(input_files)} imagen(es)...\n")
    
    successful = 0
    failed = 0
    
    for input_file in input_files:
        result = optimizer.optimize_image(input_file)
        if result:
            successful += 1
        else:
            failed += 1
        print()  # Línea en blanco entre archivos
    
    # Resumen final
    print("=" * 50)
    print(f"✅ Exitosos: {successful}")
    if failed > 0:
        print(f"❌ Fallidos: {failed}")
    print("=" * 50)
    
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
