# Pc3-Proyecto2--Repo-Compliance-

#  Proyecto 2 – Repo-Compliance

##  Objetivo de nuestro proyecto
Auditor automatizado para validar políticas **12-Factor / Seguridad** en repositorios.  
Verifica cumplimiento de buenas prácticas: secretos, licencias, Makefile estándar, cobertura ≥90 %, etc.

---

## Pasos para la  instalación

```bash
# Clonar el repositorio
git clone https://github.com/<tu-usuario>/repo-compliance.git
cd repo-compliance

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
