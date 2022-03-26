# History of Jainism

## Instructions to run the project
1. cd into the directory
2. Create a virtualenv using 
    ```
    python3 -m venv
    ````
3. Install all the dependencies using
    ```
    pip3 install -r requirements.txt
    ```
4. Create the following environmental variables
    ```
    export DJANGO_SETTINGS_MODULE="settings"
    export APP_ENVIRONMENT="localhost"
    export CLOUDINARY_URL="<Cloudinary URL>"
    export CONTENTFUL_URL="<Contentful URL>"
    export CONTENTFUL_AUTHORIZATION_TOKEN="<CONTENTFUL_AUTHORIZATION_TOKEN>"
    export STORYBLOK_URL="<STORYBLOK_URL>"
    export STORYBLOCK_AUTHORIZATION_TOKEN="<STORYBLOCK_AUTHORIZATION_TOKEN>"
    ```
4. Run the project using 
    ```
    python3 manage.py runserver
    ```

## Development Setup Guidelines
1. Use `EditorConfig` Extension https://editorconfig.org to maintain consistent coding styles for multiple developers.
2. Lint using the following command if on Linux/Mac
    ```bash
    find . -type f -name "*.py" | xargs pylint
    TODO: Find equivalent command on Windows.
    ```
