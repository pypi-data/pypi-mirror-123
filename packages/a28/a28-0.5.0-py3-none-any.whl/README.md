# Developer Toolkit

Developer Toolkit providing developers with the tools and documentation necessary to build packages for the Area28 Application.

## Python version

Area28 follows the [VFX Reference Platform](https://vfxplatform.com/) which restricts Python to 3.7.x currently.

## Interfaces

-   IPlugin
-   IApiExtension
-   IApplicationExtension
-   IChatExtension
-   IEventExtension
-   IInteractionExtension
-   ILoggerExtension
-   IMetadataExtension
-   IPreferencesExtension
-   IRealtimeExtension
-   IUiExtension
-   IUnitsExtension

## Plugins

Plugins are decorators that can be used to manipulate the payload before being processed or before getting returned.

## Extensions

Extension are used to add additional functionality to the Area28 application. Extensions are broken up into multiple types, defined within the Interfaces list.

## Packaging

Each package has a unique identifier associated with it and is compressed into a .a28 file. Please look at the a28 development kit for details.

### Package structure

```sh
@{provider}
|-- {package}
    |-- extensions
    |   |-- {extensions[]}.py
    |-- scripts
    |   |-- install.py
    |   |-- postinstall.py
    |   |-- preinstall.py
    |   |-- uninstall.py
    |-- plugin
    |   |-- {application specific plugin}
    |-- plugins
    |   |-- {plugin[]}.py
    |-- bin
    |   |--{executable[]}.py
    |-- package.json
```

### Package.json structure

```json
{
    "name": "@area28/unity-application",
    "version": "0.0.4",
    "description": "Detect is running within Unity3D.",
    "homepage": "https://area28.io",
    "keywords": ["area28", "chat", "lowercase", "transform"],
    "repository": {
        "type": "git",
        "url": "git+https://github.com/area28/area28.git",
        "directory": "packages/unity-application"
    },
    "author": "Gary Stidston-Broadbent",
    "license": "MIT",
    "bugs": {
        "url": "https://github.com/area28/area28/issues"
    },
    "bin": {
        "myapp": "./bin/lowercase.py"
    },
    "os": ["darwin", "linux"],
    "cpu": ["x64", "ia32", "!mips"],
    "scripts": {
        "preinstall": "scripts/preinstall.py",
        "install": "scripts/install.py",
        "postinstall": "scripts/postinstall.py",
        "uninstall": "scripts/uninstall.py"
    }
}
```

### Building a package

-   `a28 build --src @area28/chat-logger --dest dist`

### Installing a package locally

-   `a28 install --pkg dist/00000000-0000-0000-0000-00000000-0.0.1.a28`
