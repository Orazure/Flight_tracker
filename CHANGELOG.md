# Change Log

## [1.0.4] 2022-01-16
### Improvements

- Bump Flask Codebase to [v2stable.0.1](https://github.com/app-generator/boilerplate-code-flask-dashboard/releases)
- Dependencies update (all packages) 
  - Flask==2.0.2 (latest stable version)
  - flask_wtf==1.0.0
  - jinja2==3.0.3
  - flask-restx==0.5.1
- Forms Update:
  - Replace `TextField` (deprecated) with `StringField`

## [1.0.3] 2021-12-09
### Improvements

- Bump UI: Soft UI Dashboard **v1.0.3**

## [1.0.2] 2021-11-08
### Improvements

- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v2.0.0
  - Dependencies update (all packages) 
    - Flask==2.0.1 (latest stable version)
- Better Code formatting
- Improved Files organization
- Optimize imports
- Docker Scripts Update
- Gulp Tooling  (SASS Compilation)
- Fix **ImportError: cannot import name 'TextField' from 'wtforms'**
  - Problem caused by `WTForms-3.0.0`
  - Fix: use **WTForms==2.3.3**

## [1.0.1] 2021-05-16
### Dependencies Update

- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v1.0.6
- Freeze used versions in `requirements.txt`
    - jinja2 = 2.11.3

## [1.0.0] 2021-05-12
### Initial Release

- UI: [Jinja Soft UI](https://github.com/app-generator/jinja-soft-ui-dashboard) v1.0.0
- Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v1.0.5
