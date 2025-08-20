from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# Libera CORS para qualquer origem durante o desenvolvimento.
# Em produção, troque '*' pela origem do seu front (ex.: 'https://seu-dominio.com').
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

tarefas = []

@app.route("/")
def health():
    return jsonify({"status": "ok"})

@app.route("/tarefas", methods=["GET", "POST", "OPTIONS"])  # OPTIONS cobre o preflight
@cross_origin(origin='*', methods=['GET','POST','OPTIONS'], headers=['Content-Type'])
def gerenciar_tarefas():
    # Preflight CORS
    if request.method == "OPTIONS":
        from flask import make_response
        resp = make_response("", 204)
        return resp

    if request.method == "POST":
        data = request.get_json(silent=True) or {} #vem do curl no terminal, transfomra em json
        animal = data.get("animal") #extrai só o campo tarefa do json criado acima - precisa estar no curl
        som = data.get("som")
        if not animal or not som:
            return jsonify({"erro": "campos 'animal' e 'som' são obrigatórios"}), 400
        tarefas.append(f"{animal} - {som}")
        return jsonify({"mensagem": "Animal e som adicionados"}), 201
    return jsonify(tarefas)



if __name__ == "__main__":
    # host='0.0.0.0' facilita rodar em containers; porta 5000 por padrão
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
