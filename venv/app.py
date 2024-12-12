from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<username>:<password>@localhost:5432/movilidaddb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Movilidad(db.Model):
    __tablename__ = 'movilidades'

    placa = db.Column(db.String(10), primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    nro_chasis = db.Column(db.String(50), nullable=False)
    tipo_movilidad = db.Column(db.String(10), nullable=False)
    propietario = db.Column(db.String(100), nullable=False)

    def __init__(self, placa, marca, modelo, nro_chasis, tipo_movilidad, propietario):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.nro_chasis = nro_chasis
        self.tipo_movilidad = tipo_movilidad
        self.propietario = propietario

@app.route('/movilidad', methods=['POST'])
def create_movilidad():
    data = request.get_json()
    nueva_movilidad = Movilidad(
        placa=data['placa'],
        marca=data['marca'],
        modelo=data['modelo'],
        nro_chasis=data['nro_chasis'],
        tipo_movilidad=data['tipo_movilidad'],
        propietario=data['propietario']
    )
    try:
        db.session.add(nueva_movilidad)
        db.session.commit()
        return jsonify({"message": "Movilidad registrada correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

@app.route('/movilidad', methods=['GET'])
def get_all_movilidades():
    movilidades = Movilidad.query.all()
    result = []
    for movilidad in movilidades:
        result.append({
            'placa': movilidad.placa,
            'marca': movilidad.marca,
            'modelo': movilidad.modelo,
            'nro_chasis': movilidad.nro_chasis,
            'tipo_movilidad': movilidad.tipo_movilidad,
            'propietario': movilidad.propietario
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
