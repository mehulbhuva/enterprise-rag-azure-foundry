#!/bin/bash
set -e

RESOURCE_GROUP=${1:-"rg-enterprise-rag"}
LOCATION=${2:-"eastus"}

echo "Creating resource group: $RESOURCE_GROUP in $LOCATION"
az group create --name $RESOURCE_GROUP --location $LOCATION

echo "Deploying Bicep..."
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file infra/main.bicep \
  --parameters infra/parameters.json

echo "Done! Outputs:"
az deployment group show \
  --resource-group $RESOURCE_GROUP \
  --name main \
  --query properties.outputs
