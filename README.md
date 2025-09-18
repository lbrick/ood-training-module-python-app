# Python Training Workshop Downloader

A simple web application built with Python and WSGI that allows users to clone or update training workshops from Git repositories via a web interface.

## Description

This application provides a web-based interface to download and update machine learning and HPC training workshops developed by NeSI. It supports the following workshops:

- **ml101**: Machine Learning 101 Workshop
- **ml102**: Machine Learning 102 Workshop
- **hpc-training**: High Performance Computing Training

The app clones repositories into the `~/reannz_training` directory and can update existing clones to the latest version.

## Features

- Web-based form for selecting and downloading workshops
- Automatic cloning or updating of Git repositories
- Support for shallow cloning (--depth 1) for faster downloads
- Error handling and feedback through the web interface
- Compatible with Passenger WSGI server for deployment

## Requirements

- Python 3.x
- Git
- Passenger WSGI server (for production deployment)

## Setup

1. Clone this repository:
   ```
   git clone <this-repo-url>
   cd python-training-workshop-downloader
   ```

2. Ensure Git and Python are installed on your system.

3. For development/testing, you can run the WSGI app directly or deploy with a WSGI server.

4. For production deployment with Passenger:
   - Place the files in your web server's document root.
   - Configure Passenger to serve `passenger_wsgi.py` as the application entry point.

## Usage

1. Access the web application in your browser.
2. Select a workshop from the dropdown menu.
3. Click "Clone / Update" to download or update the selected workshop.
4. The application will display the output of the Git commands and confirm the action.

## Configuration

The workshops are defined in `passenger_wsgi.py` in the `WORKSHOPS` dictionary. You can add more workshops by modifying this dictionary:

```python
WORKSHOPS = {
    "new-workshop": "https://github.com/organization/new-workshop.git",
}
```

The base directory for cloning can be changed by modifying `TARGET_BASE` in the same file.

## Deployment

This app is designed to be deployed using Passenger WSGI. The `manifest.yml` file provides configuration for deployment platforms that support it (e.g., Cloud Foundry).

## License

[Specify license if applicable]

## Contributing

[Guidelines for contributing]