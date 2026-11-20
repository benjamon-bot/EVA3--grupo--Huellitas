
1. Primero creamos el entorno : 
python -m venv entorno

2. activamos el entorno virtual via powershell
.\entorno\Scripts\Activate.ps1

2.1. si surje un error ejecupar este comando y luego nuevamente ejecupar el paso numero 2 :
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

3. intalacion de los requerimientos del entrono: 
pip install -r requirements.txt

4. cambiar el ".env.example" a ".env" 

5. validar tus credenciales en el ".env"

6. validar tus credenciales en la extencion  "sql developer" 

7. una vez validado todo precionar "test" y luego "connect"

8. verificacion de la base de datos:
python manage.py check --database negocio

9. inspeccion de la base de datos para traer el modelo :
python manage.py inspectdb --database negocio atenciones detalle_atencion duenos mascotas servicios

10. cambiar el ".env" a ".env.example" antes de hacer el comit 