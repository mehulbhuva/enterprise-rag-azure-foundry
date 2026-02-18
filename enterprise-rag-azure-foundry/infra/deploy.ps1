param(
    [string]$ResourceGroup = "rg-enterprise-rag",
    [string]$Location = "eastus"
)

Write-Host "Creating resource group: $ResourceGroup"
az group create --name $ResourceGroup --location $Location

Write-Host "Deploying Bicep..."
az deployment group create `
    --resource-group $ResourceGroup `
    --template-file infra/main.bicep `
    --parameters infra/parameters.json

Write-Host "Deployment complete!"
