# Analizador de PDF




## Configuracion

```
python -m venv venv
pip install -r requirement.txt
```
## Instalar Ollama
* https://github.com/ollama/ollama
```
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3
ollama pull nomic-embed-text
pip install llama-index-llms-ollama
pip install llama-index-embeddings-ollama
```

```
pip install traceloop-sdk
```
* https://github.com/hyperdxio/hyperdx


pip install EbookLib html2text


### Iniciar Aplicaciones


```
streamlit run app.py
```

```
me puedes contestar en espanol, que es data debt
me puedes contestar en espanol, cómo mitigar la deuda de datos
me puedes contestar en espanol, how to mitigate data debt
how to mitigate data debt
```

### Eliminar contenido generado

```
rm -rf datos/raws
rm -rf datos/textos
rm -rf datos/storage
```

