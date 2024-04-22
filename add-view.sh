#!/bin/bash

# Definições de URL e autenticação
HOST="http://127.0.0.1:5984"
DBNAME="relatorios"
USERNAME="admin"
PASSWORD="teste"
DESIGN_DOC_ID="_design/vulnerabilities"

# Função para verificar se o documento de design já existe
function check_design_doc() {
    curl -s -X GET "$HOST/$DBNAME/$DESIGN_DOC_ID" \
         -u "$USERNAME:$PASSWORD"
}

# JSON para o design document
read -r -d '' DESIGN_DOC <<EOF
{
    "_id": "$DESIGN_DOC_ID",
    "views": {
        "all_vulnerabilities": {
            "map": "function(doc) { if (doc.type === 'vulnerability') emit(doc._id, doc); }"
        }
    }
}
EOF

# Verificar se o documento de design já existe
response=$(check_design_doc)
if echo "$response" | grep -q 'error'; then
    echo "Design document does not exist, creating one..."
    # Enviar o design document para o CouchDB
    curl -X PUT "$HOST/$DBNAME/$DESIGN_DOC_ID" \
         -u "$USERNAME:$PASSWORD" \
         -H "Content-Type: application/json" \
         -d "$DESIGN_DOC"
    echo "Design document created successfully."
else
    echo "Design document already exists, updating..."
    # Extrair o campo _rev do documento de design existente para atualização
    rev=$(echo "$response" | grep '"_rev"' | awk -F'"' '{print $4}')
    # Atualizar o documento de design
    updated_design_doc=$(echo "$DESIGN_DOC" | jq --arg rev "$rev" '._rev = $rev')
    curl -X PUT "$HOST/$DBNAME/$DESIGN_DOC_ID" \
         -u "$USERNAME:$PASSWORD" \
         -H "Content-Type: application/json" \
         -d "$updated_design_doc"
    echo "Design document updated successfully."
fi

