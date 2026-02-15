# Project Structure

## Directory Layout
```
project-name/
├── src/                    # Source code
│   ├── components/        # Reusable components
│   ├── services/          # Business logic
│   ├── utils/             # Helper functions
│   └── config/            # Configuration
├── tests/                 # Test files
├── docs/                  # Documentation
├── .kiro/                 # Kiro CLI configuration
│   ├── steering/          # Project knowledge
│   └── prompts/           # Custom commands
└── [config files]         # package.json, etc.
```

## File Naming Conventions
- **Components**: [e.g., PascalCase - UserProfile.tsx]
- **Services**: [e.g., camelCase - authService.ts]
- **Utils**: [e.g., camelCase - formatDate.ts]
- **Tests**: [e.g., *.test.ts, test_*.py]
- **Config**: [e.g., kebab-case - app-config.json]

## Module Organization
[How code is organized into modules]
- Module pattern 1
- Module pattern 2
- Import/export conventions

## Configuration Files
[Key configuration files and their purposes]
- `package.json` / `pyproject.toml` - Dependencies
- `tsconfig.json` / `setup.py` - Language config
- `.env` - Environment variables
- `[build config]` - Build configuration

## Documentation Structure
- **README.md** - Project overview and setup
- **docs/** - Detailed documentation
- **API.md** - API documentation (if applicable)
- **CONTRIBUTING.md** - Contribution guidelines

## Asset Organization
[If applicable - images, fonts, static files]
- `assets/images/` - Image files
- `assets/fonts/` - Font files
- `public/` - Static assets

## Build Artifacts
[Generated files and directories]
- `dist/` or `build/` - Production builds
- `node_modules/` or `venv/` - Dependencies
- `.cache/` - Build cache
- `coverage/` - Test coverage reports

## Environment-Specific Files
- `.env.development` - Development config
- `.env.production` - Production config
- `.env.test` - Test config
