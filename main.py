#U CAN CONNECT TO THE SERVER, YOU STILL NEED TO GET AN AUTH URI FROM MONGODB CLUSTERfrom fastapi import FastAPI
from handler.handler import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Crea un'istanza di FastAPI con specifiche configurazioni per i percorsi di documentazione
app = FastAPI(
    # Imposta il percorso personalizzato per il documento OpenAPI JSON
    # Questo è il documento che descrive formalmente l'intera API.
    openapi_url="/documentation/json",

    # Specifica un URL personalizzato per la documentazione interattiva di Swagger UI.
    # Swagger UI permette di esplorare e testare l'API in un'interfaccia grafica.
    docs_url="/documentation/",

    # Disabilita ReDoc, un'altra interfaccia di documentazione.
    # Impostando questo valore a None, l'endpoint ReDoc non sarà disponibile.
    redoc_url=None
)

# Decoratori per definire una rota
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List of origins allowed to access the API
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(router)
