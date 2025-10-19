# Java-Processing4-Project

A Processing sketch implemented as a standard Java project with frame-rate independent animation. It could be a simple template for a start with Java and Processing 4 on Mac OS. I generated a javadoc file for the core lib, which is not available in the Processing 4.4.8 release (only via URL: https://processing.github.io/processing4-javadocs/)

## Project Structure

```
windsurf-project/
├── src/
│   └── WindsurfSketch.java         # Main Processing sketch
├── lib/
│   ├── core-4.4.8.jar              # Processing core library
│   ├── core-4.4.8-javadoc.jar      # Processing Javadoc (for enhanced hover hints)
│   ├── gluegen-rt-2.5.0.jar        # OpenGL bindings
│   ├── gluegen-rt-2.5.0-natives-macosx-universal.jar
│   ├── jogl-all-2.5.0.jar          # OpenGL library
│   └── jogl-all-2.5.0-natives-macosx-universal.jar
├── .vscode/
│   ├── settings.json               # Java configuration
│   └── launch.json                 # Run configuration
├── .classpath                      # Eclipse classpath (used by VS Code Java extension)
├── .project                        # Eclipse project file (used by VS Code Java extension)
├── .settings/                      # Eclipse settings (used by VS Code Java extension)
├── create_javadoc_jar.py           # Script to regenerate javadoc JAR
└── create_javadoc_jar.sh           # Shell script alternative
```

## Running the Sketch

1. Open `src/WindsurfSketch.java`
2. Right-click in the code
3. Select **"Run Java"**

Or click the "Run" button above the `main` method.

## Features

- **Frame-rate independent animation**: Uses delta time to ensure consistent animation speed regardless of processor speed or frame rate
- **Real-time FPS display**: Shows current frame rate in the top-left corner
- **Interactive controls**: Adjust wind speed and move the windsurfer

## Controls

- **UP Arrow**: Increase wind speed
- **DOWN Arrow**: Decrease wind speed
- **Mouse Drag**: Move the windsurfer

## Javadoc Integration

The project includes a custom Javadoc JAR (`lib/core-4.4.8-javadoc.jar`) created from Processing's online documentation at https://processing.github.io/processing4-javadocs/

### How it works

VS Code's Java Language Server automatically detects Javadoc JARs when they are:

1. Named with the pattern `<library-name>-javadoc.jar`
2. Located in the same directory as the library JAR, OR
3. In the project's lib directory

The hover hints you see come from:

- **Embedded Javadoc** in the Processing core JAR (method signatures, basic descriptions)
- **Custom Javadoc JAR** in `lib/` (enhanced documentation from Processing's website)

### Regenerating the Javadoc JAR

If you need to update the Javadoc JAR (e.g., for a new Processing version):

```bash
python3 create_javadoc_jar.py
mv core-4.4.8-javadoc.jar lib/
```

## Configuration

### Requirements

- this template is for using VS Code if you do not want use the Processing IDE
- **Java JDK 17** (Processing 4 is built on Java 17)
- Configure your JDK path in `.vscode/settings.json`

### Processing Library

- Version: 4.4.8 ("core-4.4.8.jar") and all the files needed when you want to use the P2D Processing renderer (JOGL, GLUE and Natives)
- Core library and dependencies located in `lib/`
- the natives are for Mac OS only. Windows or Linux have their own specific libs (also included in the Processing installation)

### IDE Configuration Files

The project uses Eclipse project files (`.classpath`, `.project`, `.settings/`) which are required by VS Code's Java extension. These files should **not** be deleted as they configure:

- Source paths (`src/`)
- Output directory (`bin/`)
- Library dependencies
- Java compiler settings


## Notes

- The Javadoc JAR is a standard ZIP/JAR file containing HTML documentation. VS Code's Java extension reads this to provide enhanced hover hints and documentation when you hover over Processing methods and classes.
- The animation uses delta time (`millis()`) to calculate frame-independent movement, ensuring consistent speed across different hardware and frame rates.
