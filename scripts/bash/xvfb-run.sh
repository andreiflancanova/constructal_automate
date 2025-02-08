#!/bin/bash
# Inicia o Xvfb e mantém em segundo plano
Xvfb :99 -screen 0 1024x768x24 &

# Exporta a variável DISPLAY
export DISPLAY=:99

# Executa o comando que foi passado para o entrypoint
exec "$@"