# 🎮 Myrient ROM Manager - Intelligent ROM Downloader

**English** | [Español](#español)

---

## English

### 📖 Description

**Intelligent ROM downloader specifically designed for [Myrient](https://myrient.erista.me/) platform with advanced features:**

- 🔍 **Dual Search Mode**: Analyze entire collection OR search for specific titles
- 🌍 **Dynamic Language/Region Detection**: Automatically detects all available languages and regions
- 🎯 **Smart Priority System**: Select your preferred language and region with intelligent filtering
- 🎮 **Exclusive Games Detection**: Find games exclusive to specific regions with cross-country deduplication
- 📦 **Automatic ZIP Extraction**: Extract downloaded files automatically with progress tracking
- 🎨 **Enhanced Visual Interface**: Color-coded sections with clear step indicators
- 🔄 **Multi-disc Support**: Intelligent handling of multi-disc games
- ⚡ **Progress Tracking**: Real-time download progress with speed calculation

> **⚠️ Important**: This tool is **exclusive to Myrient platform**. It's designed specifically for Myrient's directory structure and HTML listing format.

### 🌐 About Myrient

[Myrient](https://myrient.erista.me/) is a comprehensive ROM archive hosting no-intro, redump, and other preservation sets. This tool is specifically optimized for downloading from their directory listings.

**Tested collections:**
- Sony PlayStation (Redump) - 10,000+ files
- Sega systems
- Other platforms available on Myrient

---

## 💝 Support Myrient - Please Donate!

**⚠️ IMPORTANT: Please support the Myrient platform!**

Myrient provides an **invaluable service** to the gaming preservation community by hosting and maintaining thousands of ROMs for free. Their work ensures that gaming history is preserved for future generations.

### 🎮 Why Support Myrient?

- **Free Access**: They provide free access to massive ROM collections
- **Game Preservation**: Actively preserving gaming history for everyone
- **Server Costs**: Hosting 10,000+ files requires significant infrastructure
- **Bandwidth**: Serving downloads to the community worldwide
- **Maintenance**: Continuous updates and maintenance of the archive

### 💰 How to Support

**Please consider donating to Myrient to help them continue their amazing work:**

🔗 **Donation Link**: Check [Myrient's website](https://myrient.erista.me/) for donation information

**Every contribution helps:**
- 💵 Keep servers running
- 💵 Maintain bandwidth for downloads
- 💵 Add new ROM collections
- 💵 Preserve gaming history

### 🙏 Thank You, Myrient!

**On behalf of the gaming community, we thank Myrient for:**
- Making game preservation accessible to everyone
- Maintaining one of the most comprehensive ROM archives
- Providing reliable and organized ROM collections
- Ensuring gaming history is preserved for future generations

**If you use this tool and benefit from Myrient's service, please consider giving back to support their incredible work!** 💖

---

## ⚖️ Legal Disclaimer

**IMPORTANT - READ BEFORE USING:**

### Copyright Notice

This tool is provided for **educational and game preservation purposes only**. Users must comply with all applicable copyright laws in their jurisdiction.

**Legal Status of ROMs:**

**LEGAL:**
- ROMs you created from your own physical cartridges/discs using legal dumping hardware
- Homebrew games and public domain software
- Games explicitly released as freeware by copyright holders

**LEGAL GRAY AREA (use at your own risk):**
- Abandonware from companies that no longer exist
- Very old systems (Atari, Commodore 64, etc.)
- Discontinued consoles without re-releases (Dreamcast, Sega Saturn)

**ILLEGAL in most jurisdictions:**
- Downloading ROMs of games you don't physically own
- Recent PlayStation, Xbox, or other modern console games
- Any copyrighted content without explicit permission

### User Responsibility

- **You are solely responsible** for ensuring your use complies with local laws
- Owning a physical copy does NOT legally entitle you to download ROMs in most countries
- This tool does NOT host, distribute, or endorse piracy
- The author assumes NO liability for how you use this software

### Recommended Legal Use Cases

- **Game preservation research** with proper academic credentials
- **Homebrew development** testing
- **Backup of your own legally dumped ROMs**
- **Analysis tools** for game preservation projects

**By using this tool, you acknowledge that you understand and accept these legal limitations.**

---

### 📁 Project Structure

**Production Files (for end users):**
- `myrient_manager.py` - **Main application** - Interactive mode with visual menu (all-in-one tool)
- `requirements.txt` - Python dependencies
- `build.py` - Universal build script for creating executables

**Source Code Files (for advanced users/developers):**
- `downloadroms.py` - Command-line download script (source code only)
- `preview_downloadroms.py` - Preview mode script (source code only)

**Development Files (not for production):**
- `tests/` - Testing suite for developers
- `debug_analysis.py` - Development debugging tools

> **📦 For releases**: Only `myrient-manager` executable is compiled. Advanced features require running from Python source code.

---

## 🚀 Installation & Requirements

### Option 1: 📦 Download Pre-built Executables (Easiest)

**No Python installation required!** Download ready-to-use executables:

- **Windows**: Download from [Releases](https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases)
- **macOS**: Download from [Releases](https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases)
- **Linux**: Download from [Releases](https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases)

**Available executable:**
- `myrient-manager` - **All-in-one interactive tool** with visual menu, preview mode, and download capabilities

> **Note**: For advanced command-line automation or preview-only mode, use the Python source code directly (see Option 2 below).

#### How to Run Executables:

**Windows:**
```cmd
# Download the executable and run directly:
myrient-manager.exe

# Or from Command Prompt:
.\myrient-manager.exe
```

**macOS:**
```bash
# Download the executable, make it executable, and run:
chmod +x myrient-manager
./myrient-manager

# If macOS blocks it (security), run:
xattr -d com.apple.quarantine myrient-manager
./myrient-manager
```

**Linux:**
```bash
# Download the executable, make it executable, and run:
chmod +x myrient-manager
./myrient-manager
```

#### ⚠️ Important - Download Location

**Downloaded ROMs are saved in the SAME DIRECTORY as the executable!**

By default, a `downloads` folder will be created next to the executable:

**Example directory structure:**
```
my-roms-folder/
├── myrient-manager          ← Your executable (all-in-one tool)
└── downloads/               ← ROMs downloaded here
    ├── Game1.zip
    ├── Game2.zip
    └── ...
```

**💡 Tip:** Place the executable in the folder where you want your ROMs stored!

**To specify a custom download folder:**

The interactive mode (`./myrient-manager`) will guide you through selecting the output directory.

> **For advanced command-line usage** (custom folders, automation, etc.), use the Python source code:
> ```bash
> python downloadroms.py "URL" my-custom-folder
> python preview_downloadroms.py "URL"
> ```

### Option 2: 🐍 Run from Python Source

### Python Requirements
- **Python 3.7+** (tested with Python 3.8+)
- **pip** (Python package manager)

### Dependencies Installation

**Option 1: Using requirements.txt (Recommended - like `npm install`)**
```bash
pip install -r requirements.txt
```

**Option 2: Individual packages**
```bash
pip install requests beautifulsoup4
```

**Option 3: Modern Python (using pyproject.toml)**
```bash
# Install in editable mode (like npm install for development)
pip install -e .
```

**Option 4: Using Poetry (modern package manager)**
```bash
# Install Poetry first: pip install poetry
poetry install
```

### System Requirements
- **Operating System**: Windows, macOS, Linux
- **Internet connection** for downloading ROMs
- **Disk space** depending on ROM collection size

---

## 🎯 Main Features

### 🔍 Dual Search Mode

When you start the tool, you can choose between:

1. **Analyze Entire Collection** (default)
   - Processes all files in the collection
   - Shows comprehensive statistics
   - Ideal for discovering all available games

2. **Search for Specific Title**
   - Filter by game title during preview
   - Faster processing for targeted downloads
   - Perfect when you know what you want

### 🌍 Dynamic Language & Region Detection

The tool automatically analyzes the entire collection and detects:

- **All available languages** (Japanese, English, Spanish, French, German, Italian, Dutch, Portuguese, Russian, Korean, Chinese)
- **All regions/continents** (Asia, Europe, Americas, Oceania, World)
- **File statistics** for each language and region

### 🎯 Smart Priority System

**Step 1: Select Language Priority**
- Choose your preferred language from detected options
- System shows number of files for each language
- Supports all major languages automatically detected

**Step 2: Select Region Priority**
- Choose continent/region preference
- System automatically maps to best specific country
- Example: Spanish → Spain, English → USA/UK, etc.

**Priority Levels:**
- **PRIORITY 1**: Exact country match (e.g., Spain files for Spanish)
- **PRIORITY 2**: Language match in region (e.g., Europe files with Spanish)

### 🎮 Exclusive Games Detection

Find games that are **exclusive to specific regions**:

- Intelligent keyword-based deduplication
- Cross-country duplicate removal
- Multi-disc support
- Numbered series detection
- Shows unique games per region with statistics

### 📦 Automatic ZIP Extraction

After downloads complete (or if files already exist):

- Automatically detects ZIP files in output directory
- Prompts for extraction with intuitive defaults
- Shows extraction progress for each file
- Handles errors gracefully

### 🎨 Enhanced Visual Interface

- Color-coded sections with 🟦 separators
- Clear step indicators (🔻 STEP 1, 🔻 STEP 2)
- Progress bars with real-time speed tracking
- Comprehensive statistics and summaries

---

## 🚀 Usage - Interactive Mode

**File**: `myrient_manager.py`

```bash
python myrient_manager.py
```

### Workflow:

1. **Enter Myrient URL**
   
   Visit [Myrient](https://myrient.erista.me/files/) to browse available collections and copy the URL of the collection you want to download.
   
   ```
   Example: https://myrient.erista.me/files/No-Intro/Sega%20-%20Mega%20Drive%20-%20Genesis/
   ```

2. **Choose Search Mode**
   - Option 1: Analyze entire collection
   - Option 2: Search for specific title

3. **Include Demos?** (optional)
   - yes/no prompt [default: no]

4. **Review Detected Languages & Regions**
   - See all available options with file counts

5. **Select Language Priority**
   - Choose from 11 detected languages or "no preference"

6. **Select Region Priority**
   - Choose from 5 continents or "no preference"
   - System auto-selects best specific country

7. **Exclusive Games (optional)**
   - Review region-exclusive games
   - Select multiple regions to include (e.g., 1,2,5)
   - Or skip with option 0

8. **Preview & Confirm**
   - Review complete file list with priorities
   - See size statistics
   - Confirm download

9. **Download**
   - Real-time progress tracking
   - Automatic file existence checking
   - Error handling with retries

10. **Automatic Extraction**
    - Prompts to extract ZIP files
    - Shows extraction progress
    - Creates organized folder structure

### Example Session:

```
📥 Enter Myrient URL: https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/

🔍 SEARCH MODE:
  1. Analyze entire collection (default)
  2. Search for specific title
Select option: 1

Include Demo files? [default: no]: no

⏳ Fetching directory listing...
✓ Found 10229 .zip files

🌍 LANGUAGES DETECTED:
  1. Jp - Japanese (Japan) (4,620 files)
  2. En - English (3,380 files)
  3. Es - Spanish (Spain) (880 files)
  ...

🔻 STEP 1: SELECT YOUR PREFERRED LANGUAGE
Select language priority (0-11): 5

🔻 STEP 2: SELECT YOUR PREFERRED REGION
Select region priority (0-5): 2

✅ Auto-selected: Spain (224 files)

📂 PRIORITY 1 - Spain: 224 files (82.5 GiB)
📂 PRIORITY 2 - Europe (Spanish): 503 files (159.5 GiB)

Do you want to proceed with download? [default: no]: yes

🚀 STARTING DOWNLOAD...
[Progress bars with real-time speed tracking]

✅ Download complete!

📦 Do you want to extract the ZIP files? [default: no]: yes
[Extraction progress...]
```

---

## � Building Executables (For Developers)

If you want to create your own executables from source:

### Quick Build (Universal Script)
```bash
# Works on Windows, Linux, and macOS
python build.py
```

### Platform-Specific Scripts
```bash
# Linux/macOS
chmod +x build_linux.sh
./build_linux.sh

# Windows
build_windows.bat
```

**Output**: Executables will be created in `dist/[system]/` folder

### Manual Build

> **Note**: The automated build script (`build.py`) only compiles `myrient-manager`. For other scripts, build manually:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the main executable (recommended)
pyinstaller --onefile --name="myrient-manager" myrient_manager.py

# Build other executables (optional - for advanced users)
pyinstaller --onefile --name="myrient-download" downloadroms.py
pyinstaller --onefile --name="myrient-preview" preview_downloadroms.py
```

---

## 🔍 Preview Mode & Advanced Usage

### Using the Compiled Executable

The `myrient-manager` executable includes a built-in preview mode accessible through the interactive menu.

### Using Python Source Code (Advanced)

For command-line automation and preview-only mode, use the Python source directly:

**Preview before downloading:**
```bash
python preview_downloadroms.py 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/'
```

**Command-line download with custom options:**
```bash
python downloadroms.py 'https://myrient.erista.me/files/...' output_folder --demos --quiet
```

### Manual Build
```bash
# Install PyInstaller
pip install pyinstaller

# Build individual executables
pyinstaller --onefile --name="myrient-manager" myrient_manager.py
pyinstaller --onefile --name="myrient-download" downloadroms.py
pyinstaller --onefile --name="myrient-preview" preview_downloadroms.py
```

---

## �🔍 Preview Mode (Optional)

Before downloading, you can preview what files will be selected:

```bash
python preview_downloadroms.py 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/'
```

This shows:
- ✅ Files that will be downloaded
- ⚠️ Files that will be discarded (duplicates)
- ❌ Files that will be ignored (wrong region/language)

---

## 📊 Technical Details

### Intelligent Filtering System

**Language Detection:**
- Automatically parses all filenames in collection
- Detects language codes from filenames
- Groups files by language with statistics

**Region/Country Detection:**
- Identifies specific countries (Spain, USA, Japan, France, Germany, etc.)
- Groups countries by continent
- Maps languages to best matching countries

**Priority System:**
- PRIORITY 1: Exact country match (e.g., Spain for Spanish)
- PRIORITY 2: Continental region with language match (e.g., Europe files with Spanish)
- Automatically filters Europe files to only include selected language

### Duplicate Detection

**Multi-level deduplication:**

1. **Within Priority Files:** Groups games by title, keeps only highest priority per game
2. **Keyword-Based Similarity:** Extracts meaningful keywords from titles
3. **Numbered Series Detection:** Identifies games with numbers (e.g., "FIFA 2000", "Final Fantasy VII")
4. **Multi-Disc Support:** Keeps all discs for the same game
5. **Cross-Country Deduplication:** Removes duplicates across different regions in exclusive games

### File Handling

**Download Features:**
- Checks existing files before downloading
- Real-time progress bars with speed tracking
- Automatic retry on network errors
- Preserves original Myrient filenames
- Creates output directory if needed

**Extraction Features:**
- Detects ZIP files automatically
- Extracts to game-named folders
- Progress tracking per file
- Error handling with detailed messages

---

## 📁 Output Structure

```
output_directory/
├── Game Title 1 (Spain).zip
├── Game Title 1 (Spain)/
│   ├── Game Title 1 (Spain).cue
│   └── Game Title 1 (Spain).bin
├── Game Title 2 (Europe) (En,Es,Fr,De,It).zip
├── Game Title 2 (Europe) (En,Es,Fr,De,It)/
│   ├── Game Title 2 (Europe) (En,Es,Fr,De,It).cue
│   └── Game Title 2 (Europe) (En,Es,Fr,De,It).bin
├── Multi-Disc Game (Spain) (Disc 1).zip
├── Multi-Disc Game (Spain) (Disc 1)/
│   ├── Multi-Disc Game (Spain) (Disc 1).cue
│   └── Multi-Disc Game (Spain) (Disc 1).bin
├── Multi-Disc Game (Spain) (Disc 2).zip
└── Multi-Disc Game (Spain) (Disc 2)/
    ├── Multi-Disc Game (Spain) (Disc 2).cue
    └── Multi-Disc Game (Spain) (Disc 2).bin
```

---

## 🛠️ Troubleshooting

### Common Issues

**Issue: "No files match the selected language criteria"**

- Try different language configuration
- Check if the URL contains ROMs for your selected regions
- Some collections may only have Japan/USA releases

**Issue: "Error fetching URL"**

- Verify the Myrient URL is correct and accessible
- Check your internet connection
- Ensure the URL starts with `https://myrient.erista.me/`

**Issue: "Permission denied" or download errors**

- Check disk space in output directory
- Verify write permissions in target folder
- Try a different output directory

**Issue: Python/dependency errors**

```bash
# Reinstall dependencies
pip install --upgrade requests beautifulsoup4

# Check Python version
python --version  # Should be 3.7+
```

### Performance Tips

- For large collections (10,000+ files), analysis may take 1-2 minutes
- Use specific title search for faster targeted downloads
- Close other network-intensive applications during download
- Extraction of large ZIP files may take several minutes

---

## 🧪 Development & Testing

### Test Mode

The tool includes a test mode (downloads only first 20 files):

```bash
# When prompted during interactive mode:
Download only first 20 files for testing? (yes/no): yes
```

Perfect for testing without downloading entire collections.

### Development Files

- `tests/test_downloadroms.py` - Unit tests for core functionality
- `debug_analysis.py` - Development debugging tools
- `preview_downloadroms.py` - Preview mode for testing URLs

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Fork for Other Platforms

This project is specifically designed for **Myrient platform**, but the core architecture can be adapted for other ROM download sites.

**Reusable components:**

- Download management system
- Interactive menu framework
- File filtering logic
- Progress tracking and error handling

**What needs modification:**

- HTML parsing logic (each site has different structure)
- URL patterns and navigation
- File naming conventions
- Region/language detection patterns

---

## 📄 License & Disclaimer

This tool is for **educational and personal use only**. Users are responsible for complying with copyright laws and terms of service of content providers.

**Responsible use:**

- Don't abuse Myrient's servers with excessive requests
- Support preservation efforts when possible
- Use responsibly and ethically
- When forking: Respect the target platform's terms of service

---

---

## Español

### 📖 Descripción

**Descargador inteligente de ROMs diseñado específicamente para [Myrient](https://myrient.erista.me/) con funcionalidades avanzadas:**

- 🔍 **Modo de Búsqueda Dual**: Analiza colección completa O busca títulos específicos
- 🌍 **Detección Dinámica de Idiomas/Regiones**: Detecta automáticamente todos los idiomas y regiones disponibles
- 🎯 **Sistema de Prioridades Inteligente**: Selecciona tu idioma y región preferidos con filtrado inteligente
- 🎮 **Detección de Juegos Exclusivos**: Encuentra juegos exclusivos de regiones específicas con deduplicación entre países
- 📦 **Extracción Automática de ZIP**: Extrae archivos descargados automáticamente con seguimiento de progreso
- 🎨 **Interfaz Visual Mejorada**: Secciones codificadas por colores con indicadores de pasos claros
- 🔄 **Soporte Multi-disco**: Manejo inteligente de juegos multi-disco
- ⚡ **Seguimiento de Progreso**: Progreso de descarga en tiempo real con cálculo de velocidad

---

## 💝 Apoya a Myrient - ¡Por Favor Dona!

**⚠️ IMPORTANTE: ¡Por favor apoya la plataforma Myrient!**

Myrient proporciona un **servicio invaluable** a la comunidad de preservación de videojuegos al alojar y mantener miles de ROMs de forma gratuita. Su trabajo asegura que la historia del gaming se preserve para las futuras generaciones.

### 🎮 ¿Por Qué Apoyar a Myrient?

- **Acceso Gratuito**: Proporcionan acceso gratuito a colecciones masivas de ROMs
- **Preservación de Juegos**: Preservan activamente la historia del gaming para todos
- **Costos de Servidor**: Alojar más de 10,000 archivos requiere infraestructura significativa
- **Ancho de Banda**: Sirven descargas a la comunidad en todo el mundo
- **Mantenimiento**: Actualizaciones y mantenimiento continuo del archivo

### 💰 Cómo Apoyar

**Por favor considera donar a Myrient para ayudarles a continuar su increíble trabajo:**

🔗 **Enlace de Donación**: Consulta [el sitio web de Myrient](https://myrient.erista.me/) para información sobre donaciones

**Cada contribución ayuda a:**
- 💵 Mantener los servidores funcionando
- 💵 Mantener el ancho de banda para descargas
- 💵 Añadir nuevas colecciones de ROMs
- 💵 Preservar la historia del gaming

### 🙏 ¡Gracias, Myrient!

**En nombre de la comunidad gamer, agradecemos a Myrient por:**
- Hacer la preservación de juegos accesible para todos
- Mantener uno de los archivos de ROMs más completos
- Proporcionar colecciones de ROMs confiables y organizadas
- Asegurar que la historia del gaming se preserve para futuras generaciones

**Si usas esta herramienta y te beneficias del servicio de Myrient, ¡por favor considera retribuir para apoyar su increíble trabajo!** 💖

---

## ⚖️ Aviso Legal

**IMPORTANTE - LEE ANTES DE USAR:**

### Aviso de Copyright

Esta herramienta se proporciona únicamente con **fines educativos y de preservación de juegos**. Los usuarios deben cumplir con todas las leyes de copyright aplicables en su jurisdicción.

**Estado Legal de las ROMs:**

**LEGAL:**
- ROMs que creaste desde tus propios cartuchos/discos físicos usando hardware de volcado legal
- Juegos homebrew y software de dominio público
- Juegos explícitamente liberados como freeware por los titulares de derechos de autor

**ZONA GRIS LEGAL (usa bajo tu propio riesgo):**
- Abandonware de empresas que ya no existen
- Sistemas muy antiguos (Atari, Commodore 64, etc.)
- Consolas descontinuadas sin relanzamientos (Dreamcast, Sega Saturn)

**ILEGAL en la mayoría de jurisdicciones:**
- Descargar ROMs de juegos que no posees físicamente
- Juegos recientes de PlayStation, Xbox u otras consolas modernas
- Cualquier contenido con copyright sin permiso explícito

### Responsabilidad del Usuario

- **Eres el único responsable** de asegurar que tu uso cumple con las leyes locales
- Poseer una copia física NO te da derecho legal a descargar ROMs en la mayoría de países
- Esta herramienta NO aloja, distribuye ni apoya la piratería
- El autor NO asume ninguna responsabilidad por cómo uses este software

### Casos de Uso Legal Recomendados

- **Investigación de preservación de juegos** con credenciales académicas apropiadas
- **Desarrollo de homebrew** para pruebas
- **Respaldo de tus propias ROMs volcadas legalmente**
- **Herramientas de análisis** para proyectos de preservación de juegos

**Al usar esta herramienta, reconoces que entiendes y aceptas estas limitaciones legales.**

---

---

## 🚀 Características Principales

### 🔍 Modo de Búsqueda Dual

Al iniciar la herramienta, puedes elegir entre:

1. **Analizar Colección Completa** (por defecto)
   - Procesa todos los archivos de la colección
   - Muestra estadísticas completas
   - Ideal para descubrir todos los juegos disponibles

2. **Buscar Título Específico**
   - Filtra por título de juego durante la vista previa
   - Procesamiento más rápido para descargas específicas
   - Perfecto cuando sabes lo que quieres

### 🌍 Detección Dinámica de Idiomas y Regiones

La herramienta analiza automáticamente toda la colección y detecta:

- **Todos los idiomas disponibles** (Japonés, Inglés, Español, Francés, Alemán, Italiano, Holandés, Portugués, Ruso, Coreano, Chino)
- **Todas las regiones/continentes** (Asia, Europa, Américas, Oceanía, Mundial)
- **Estadísticas de archivos** para cada idioma y región

### 🎯 Sistema de Prioridades Inteligente

**Paso 1: Seleccionar Prioridad de Idioma**
- Elige tu idioma preferido de las opciones detectadas
- El sistema muestra número de archivos para cada idioma
- Soporta todos los idiomas principales detectados automáticamente

**Paso 2: Seleccionar Prioridad de Región**
- Elige preferencia de continente/región
- El sistema mapea automáticamente al mejor país específico
- Ejemplo: Español → España, Inglés → USA/UK, etc.

**Niveles de Prioridad:**
- **PRIORIDAD 1**: Coincidencia exacta de país (ej., archivos de España para Español)
- **PRIORIDAD 2**: Coincidencia de idioma en región (ej., archivos de Europa con Español)

### 🎮 Detección de Juegos Exclusivos

Encuentra juegos que son **exclusivos de regiones específicas**:

- Deduplicación inteligente basada en palabras clave
- Eliminación de duplicados entre países
- Soporte multi-disco
- Detección de series numeradas
- Muestra juegos únicos por región con estadísticas

### 📦 Extracción Automática de ZIP

Después de completar las descargas (o si los archivos ya existen):

- Detecta archivos ZIP automáticamente en el directorio de salida
- Solicita extracción con valores predeterminados intuitivos
- Muestra progreso de extracción para cada archivo
- Maneja errores con mensajes detallados

---

## 🚀 Uso - Modo Interactivo

**Archivo**: `myrient_manager.py`

```bash
python myrient_manager.py
```

### Flujo de Trabajo

1. **Ingresar URL de Myrient**
   
   Visita [Myrient](https://myrient.erista.me/files/) para explorar las colecciones disponibles y copia la URL de la colección que deseas descargar.
   
   ```
   Ejemplo: https://myrient.erista.me/files/No-Intro/Sega%20-%20Mega%20Drive%20-%20Genesis/
   ```

2. **Elegir Modo de Búsqueda** (colección completa o título específico)
3. **¿Incluir Demos?** (opcional, predeterminado: no)
4. **Revisar Idiomas y Regiones Detectados**
5. **Seleccionar Prioridad de Idioma** (11 idiomas o "sin preferencia")
6. **Seleccionar Prioridad de Región** (5 continentes o "sin preferencia")
7. **Juegos Exclusivos** (opcional) - Seleccionar regiones o saltar
8. **Vista Previa y Confirmar** - Revisar lista completa con prioridades
9. **Descargar** - Seguimiento en tiempo real, verificación de existencia
10. **Extracción Automática** - Solicita extraer archivos ZIP con progreso

---

## 📊 Detalles Técnicos

### Sistema de Filtrado Inteligente

**Detección de Idiomas:**
- Analiza automáticamente todos los nombres de archivo en la colección
- Detecta códigos de idioma de los nombres de archivo
- Agrupa archivos por idioma con estadísticas

**Detección de Regiones/Países:**
- Identifica países específicos (España, USA, Japón, Francia, Alemania, etc.)
- Agrupa países por continente
- Mapea idiomas a los mejores países coincidentes

**Sistema de Prioridades:**
- PRIORIDAD 1: Coincidencia exacta de país (ej., España para Español)
- PRIORIDAD 2: Región continental con coincidencia de idioma (ej., archivos de Europa con Español)
- Filtra automáticamente archivos de Europa para incluir solo el idioma seleccionado

### Detección de Duplicados

**Deduplicación multi-nivel:**

1. **Dentro de Archivos Prioritarios:** Agrupa juegos por título, mantiene solo la mayor prioridad por juego
2. **Similitud Basada en Palabras Clave:** Extrae palabras clave significativas de los títulos
3. **Detección de Series Numeradas:** Identifica juegos con números (ej., "FIFA 2000", "Final Fantasy VII")
4. **Soporte Multi-Disco:** Mantiene todos los discos del mismo juego
5. **Deduplicación Entre Países:** Elimina duplicados entre diferentes regiones en juegos exclusivos

---

## 🛠️ Solución de Problemas

### Problemas Comunes

**"No files match the selected language criteria"**
- Prueba una configuración de idioma diferente
- Verifica si la URL contiene ROMs para tus regiones seleccionadas

**"Error fetching URL"**
- Verifica que la URL de Myrient sea correcta y accesible
- Comprueba tu conexión a internet

**Errores de Python/dependencias**

```bash
# Reinstalar dependencias
pip install --upgrade requests beautifulsoup4

# Verificar versión de Python
python --version  # Debe ser 3.7+
```

### Consejos de Rendimiento

- Para colecciones grandes (10,000+ archivos), el análisis puede tomar 1-2 minutos
- Usa búsqueda de título específico para descargas rápidas y dirigidas
- Cierra otras aplicaciones que usen la red intensivamente durante la descarga
- La extracción de archivos ZIP grandes puede tomar varios minutos

---

## 📄 Licencia y Descargo

Esta herramienta es solo para **uso educativo y personal**. Los usuarios son responsables de cumplir con las leyes de derechos de autor y términos de servicio.

**Uso responsable:**
- No abuses de los servidores de Myrient con solicitudes excesivas
- Apoya los esfuerzos de preservación cuando sea posible
- Usa de manera responsable y ética

## 🧪 Testing Files

The repository includes test files for development:
- `test_downloadroms.py`: Unit tests for core functionality
- `preview_downloadroms.py`: Preview-only mode for testing URLs

---

## 🍴 Contributing & Forking for Other Platforms

### Want to adapt this for other ROM platforms?

This project is specifically designed for **Myrient platform**, but the core architecture can be adapted for other ROM download sites. 

**🚀 We encourage you to fork this project if you want to:**
- Support other ROM platforms (Archive.org, ROM sites, etc.)
- Add different region prioritization systems
- Implement additional filtering logic
- Create platform-specific features

📚 **Detailed fork guidelines available in [CONTRIBUTING.md](CONTRIBUTING.md)**

### � Fork Guidelines

**Core components you can reuse:**
- ✅ **Download management** (`downloadroms.py` base structure)
- ✅ **Interactive menu system** (`myrient_manager.py` UI framework)
- ✅ **File filtering logic** (adapt region/language systems)
- ✅ **Progress tracking** and error handling

**What you'll need to modify:**
- 🔄 **HTML parsing logic** (each site has different structure)
- 🔄 **URL patterns** and navigation
- 🔄 **File naming conventions** 
- 🔄 **Region/language detection** patterns

### 🤝 Community Forks Welcome!

If you create a fork for another platform, feel free to:
1. **Link back** to this original project
2. **Share your fork** in discussions/issues
3. **Contribute improvements** back to the core architecture
4. **Document** your platform-specific adaptations

**Example fork ideas:**
- `archive-rom-manager` for Archive.org
- `emuparadise-downloader` (if still active)
- `regional-rom-manager` with different priority systems
- `multi-platform-rom-manager` supporting multiple sites

---

## �📄 License & Disclaimer

This tool is for educational and personal use only. Users are responsible for complying with copyright laws and terms of service of content providers.

**Respect the source:**
- Don't abuse Myrient's servers with excessive requests
- Support preservation efforts when possible
- Use responsibly and ethically
- **When forking**: Respect the target platform's terms of service

---

## Español

### 📖 Descripción

**Descargador inteligente de ROMs diseñado específicamente para la plataforma [Myrient](https://myrient.erista.me/).**

Esta herramienta ofrece **dos modos** para descargar y filtrar ROMs de la extensa colección de Myrient, con filtrado inteligente basado en regiones y priorización de idiomas.

---

## 🚀 Instalación y Requisitos

### Opción 1: 📦 Descargar Ejecutables Pre-compilados (Más Fácil)

**¡No requiere instalación de Python!** Descarga ejecutables listos para usar:

- **Windows**: Descarga desde [Releases](https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases)
- **macOS**: Descarga desde [Releases](https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases)
- **Linux**: Descarga desde [Releases](https://github.com/Tonymartos/DownloaderRomsMyrientManager/releases)

**Ejecutable disponible:**
- `myrient-manager` - **Herramienta todo-en-uno interactiva** con menú visual, modo vista previa y capacidades de descarga

> **Nota**: Para automatización avanzada por línea de comandos o modo solo vista previa, usa el código fuente Python directamente (ver Opción 2 abajo).

#### Cómo Ejecutar:

**Windows:**
```cmd
# Descarga el ejecutable y ejecútalo directamente:
myrient-manager.exe

# O desde el Símbolo del Sistema:
.\myrient-manager.exe
```

**macOS:**
```bash
# Descarga el ejecutable, dale permisos y ejecútalo:
chmod +x myrient-manager
./myrient-manager

# Si macOS lo bloquea (seguridad), ejecuta:
xattr -d com.apple.quarantine myrient-manager
./myrient-manager
```

**Linux:**
```bash
# Descarga el ejecutable, dale permisos y ejecútalo:
chmod +x myrient-manager
./myrient-manager
```

#### ⚠️ Importante - Ubicación de Descarga

**¡Las ROMs descargadas se guardan en el MISMO DIRECTORIO que el ejecutable!**

Por defecto, se creará una carpeta `downloads` junto al ejecutable:

**Estructura de directorios de ejemplo:**
```
mi-carpeta-roms/
├── myrient-manager          ← Tu ejecutable (herramienta todo-en-uno)
└── downloads/               ← ROMs descargadas aquí
    ├── Juego1.zip
    ├── Juego2.zip
    └── ...
```

**💡 Consejo:** ¡Coloca el ejecutable en la carpeta donde quieras almacenar tus ROMs!

**Para especificar una carpeta personalizada:**

El modo interactivo (`./myrient-manager`) te guiará en la selección del directorio de salida.

> **Para uso avanzado por línea de comandos** (carpetas personalizadas, automatización, etc.), usa el código fuente Python:
> ```bash
> python downloadroms.py "URL" mi-carpeta-personalizada
> python preview_downloadroms.py "URL"
> ```

### Opción 2: 🐍 Ejecutar desde Código Fuente Python

### Requisitos de Python
- **Python 3.7+** (probado con Python 3.8+)
- **pip** (gestor de paquetes de Python)

### Instalación de Dependencias

**Opción 1: Usando requirements.txt (Recomendado - como `npm install`)**
```bash
pip install -r requirements.txt
```

**Opción 2: Paquetes individuales**
```bash
pip install requests beautifulsoup4
```

**Opción 3: Python moderno (usando pyproject.toml)**
```bash
# Instalar en modo editable (como npm install para desarrollo)
pip install -e .
```

**Opción 4: Usando Poetry (gestor de paquetes moderno)**
```bash
# Instalar Poetry primero: pip install poetry
poetry install
```

---

## 🎯 Modos de Uso

### 1. 🖥️ Modo Interactivo (Recomendado para principiantes)
**Archivo**: `myrient_manager.py`

Menú interactivo con múltiples configuraciones de idioma y vista previa antes de descargar.

```bash
python myrient_manager.py
```

**Características:**
- ✅ **Menú visual** con opciones codificadas por colores
- ✅ **6 configuraciones de idioma**:
  - 🇪🇸 Español (España): España > Europa (Es) > Japón
  - 🇬🇧 Inglés (Europa/USA): Europa (En) > USA > Japón
  - 🇫🇷 Francés (Francia): Francia > Europa (Fr) > Japón
  - 🇩🇪 Alemán (Alemania): Alemania > Europa (De) > Japón
  - 🇮🇹 Italiano (Italia): Italia > Europa (It) > Japón
  - 🇯🇵 Japonés (Japón): Solo Japón
- ✅ **Tablas de vista previa** mostrando qué se descargará
- ✅ **Información de tamaño** de archivos y estadísticas
- ✅ **Opción de incluir demos**
- ✅ **Confirmaciones** antes de descargar

### 2. ⚡ Modo Línea de Comandos (Recomendado para automatización)
**Archivo**: `downloadroms.py`

Ejecución directa por línea de comandos con prioridad española (España > Europa > Japón).

```bash
python downloadroms.py "<URL>" [directorio_salida] [opciones]
```

**Ejemplos:**
```bash
# Uso básico
python downloadroms.py 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/' roms_psx

# Con demos incluidos
python downloadroms.py 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/' roms_psx --demos

# Modo silencioso
python downloadroms.py 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/' roms_psx --quiet
```

**Opciones de Línea de Comandos:**
- `--demos`: Incluir archivos Demo/Sample
- `--quiet`: Salida mínima (sin progreso detallado)

---

## 📊 Lógica de Filtrado

### Sistema de Prioridad de Regiones
**Configuración Española (Por defecto en CLI):**
1. **España** (prioridad más alta)
2. **Europa** (solo si contiene español o no especifica idioma)
3. **Japón** (prioridad más baja)

### Manejo de Duplicados
- **Un ROM por juego**: Si existen múltiples regiones, mantiene la de mayor prioridad
- **Coincidencia de títulos**: Agrupa juegos por título base
- **Limpieza automática**: Descarta duplicados de menor prioridad

---

## 🛠️ Resolución de Problemas

### Problemas Comunes

**1. "No files match the selected language criteria"**
- Prueba una configuración de idioma diferente
- Verifica si la URL contiene ROMs para tus regiones seleccionadas

**2. "Error fetching URL"**
- Verifica que la URL de Myrient sea correcta y accesible
- Comprueba tu conexión a internet

**3. Errores de Python/dependencias**
```bash
# Reinstalar dependencias
pip install --upgrade requests beautifulsoup4

# Verificar versión de Python
python --version  # Debe ser 3.7+
```

---

## 🍴 Contribuciones y Forks para Otras Plataformas

### ¿Quieres adaptar esto para otras plataformas de ROMs?

Este proyecto está específicamente diseñado para la **plataforma Myrient**, pero la arquitectura central puede adaptarse para otros sitios de descarga de ROMs.

**🚀 Te animamos a hacer fork de este proyecto si quieres:**
- Soportar otras plataformas de ROMs (Archive.org, sitios de ROMs, etc.)
- Añadir diferentes sistemas de priorización de regiones
- Implementar lógica de filtrado adicional
- Crear características específicas de plataforma

📚 **Guías detalladas para forks disponibles en [CONTRIBUTING.md](CONTRIBUTING.md)**

### 🔧 Guías para Forks

**Componentes centrales que puedes reutilizar:**
- ✅ **Gestión de descargas** (estructura base de `downloadroms.py`)
- ✅ **Sistema de menú interactivo** (framework UI de `myrient_manager.py`)
- ✅ **Lógica de filtrado de archivos** (adaptar sistemas de región/idioma)
- ✅ **Seguimiento de progreso** y manejo de errores

**Lo que necesitarás modificar:**
- � **Lógica de parsing HTML** (cada sitio tiene estructura diferente)
- 🔄 **Patrones de URL** y navegación
- 🔄 **Convenciones de nombres de archivos**
- 🔄 **Patrones de detección** de región/idioma

### 🤝 ¡Forks de la Comunidad Bienvenidos!

Si creas un fork para otra plataforma, siéntete libre de:
1. **Enlazar de vuelta** a este proyecto original
2. **Compartir tu fork** en discusiones/issues
3. **Contribuir mejoras** de vuelta a la arquitectura central
4. **Documentar** tus adaptaciones específicas de plataforma

**Ideas de ejemplo para forks:**
- `archive-rom-manager` para Archive.org
- `emuparadise-downloader` (si sigue activo)
- `regional-rom-manager` con diferentes sistemas de prioridad
- `multi-platform-rom-manager` soportando múltiples sitios

---

## �📄 Licencia y Descargo

Esta herramienta es solo para uso educativo y personal. Los usuarios son responsables de cumplir con las leyes de derechos de autor y términos de servicio.

**Respeta la fuente:**
- No abuses de los servidores de Myrient con solicitudes excesivas
- Apoya los esfuerzos de preservación cuando sea posible
- Usa de manera responsable y ética
- **Al hacer fork**: Respeta los términos de servicio de la plataforma objetivo
