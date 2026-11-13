
1. Primero creamos el entorno : 
python -m venv entorno

2. activamos el entorno virtual via powershell
.\entorno\Scripts\Activate.ps1

3. intalacion de los requerimientos del entrono: 
pip install -r requirements.txt

4. verificacion de la base de datos:
python manage.py check --database negocio

5. inspeccion de la base de datos para traer el modelo :
python manage.py inspectdb --database negocio atenciones detalle_atencion duenos mascotas servicios

6. cambiar el ".env.example" a ".env" 