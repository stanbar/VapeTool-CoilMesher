#!/bin/sh

curl http://localhost:5000/generate-mesh \
-X POST \
-H "Content-Type: application/json" \
-d '{"wraps": 5, "innerDiameter": 3.2 , "wireDiameter": 0.322, "legsLength": 15 }'
