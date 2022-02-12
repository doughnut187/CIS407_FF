cd BackEnd; 
rm -rf ./venv;
python -m venv ./venv;
source venv/Scripts/activate;
pip3 install -r requirements.txt;
python app.py;