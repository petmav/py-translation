@echo off                     

echo WARNING: THIS WILL NOT RUN PROPERLY WITHOUT THE PRE-INSTALLATION REQUIREMENTS LISTED IN THE README.md
timeout /t 1

python -m pip install -r requirements.txt
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

if not exist settings mkdir settings

set /p CHATGPT=What is your OpenAI GPT API key (leave blank if none):
echo GPT key is : %CHATGPT%
echo CHATGPT=%CHATGPT% > settings\keys.txt

set /p MICROSOFT=What is your Microsoft Translator key (leave blank if none): 
echo Microsoft key is: %MICROSOFT%
echo MICROSOFT=%MICROSOFT% >> settings\keys.txt

echo Completed.
timeout /t 3
