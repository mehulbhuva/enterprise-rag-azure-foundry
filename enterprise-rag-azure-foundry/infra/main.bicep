
targetScope = 'resourceGroup'

param searchServiceName string
param storageAccountName string
param functionAppName string
param openAiEndpoint string
param openAiKey string
param searchKey string

var location = resourceGroup().location

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: { accessTier: 'Hot' }
}

// Knowledge container
resource knowledgeContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/knowledge'
  properties: { publicAccess: 'None' }
}

// Azure AI Search S1
resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: searchServiceName
  location: location
  sku: { name: 'S1' }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
}

// App Service Plan for Functions
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'plan-${functionAppName}'
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  kind: 'functionapp'
}

// Function App
resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      pythonVersion: '3.11'
      appSettings: [
        { name: 'AzureWebJobsStorage', value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};AccountKey=${storageAccount.listKeys().keys[0].value}' }
        { name: 'FUNCTIONS_EXTENSION_VERSION', value: '~4' }
        { name: 'FUNCTIONS_WORKER_RUNTIME', value: 'python' }
        { name: 'SEARCH_ENDPOINT', value: 'https://${searchServiceName}.search.windows.net' }
        { name: 'SEARCH_KEY', value: searchKey }
        { name: 'OPENAI_ENDPOINT', value: openAiEndpoint }
        { name: 'OPENAI_KEY', value: openAiKey }
        { name: 'INDEX_NAME', value: 'enterprise-knowledge' }
        { name: 'EMBEDDING_MODEL', value: 'text-embedding-3-small' }
        { name: 'CHAT_MODEL', value: 'gpt-4o-mini' }
      ]
    }
  }
}

output searchEndpoint string = 'https://${searchServiceName}.search.windows.net'
output functionAppUrl string = 'https://${functionAppName}.azurewebsites.net'
output storageAccountName string = storageAccount.name
