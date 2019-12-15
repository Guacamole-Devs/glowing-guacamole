if (-not (Test-Path -LiteralPath .\\venv\Scripts\Activate.ps1)) {
    py -m venv venv
}
.\\venv\Scripts\Activate.ps1
pip install flask
pip install pyrebase4