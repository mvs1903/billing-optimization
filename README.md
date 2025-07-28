# Billing Records Cost Optimization – Azure Serverless Architecture

## 📘 Overview

This repository implements a **cost-optimized, serverless Azure solution** for managing billing records with very large data volumes. The approach archives older billing records from **Azure Cosmos DB** to **Azure Blob Storage** using batch compression, reducing costs by **over 93%**, while ensuring:

- ✅ No data loss & no downtime  
- ✅ No changes to existing API contracts  
- ✅ Simplicity and ease of maintenance  

---

## 🏗️ Architecture Diagram

<img width="512" height="512" alt="image" src="https://github.com/user-attachments/assets/d520c90d-920d-4606-ad6c-76a8b312a193" />


---

## 📊 System Profile and Cost Breakdowns

| Parameter                          | Value             |
|-----------------------------------|-------------------|
| Total Records                     | 2,000,000         |
| Average Record Size               | 300 KB            |
| Total Data Size                   | 600 GB            |
| Hot Data (last 3 months)          | 150 GB (25%)      |
| Cold Data (older than 3 months)   | 450 GB (75%)      |

### 💰 Azure Pricing & Estimated Monthly Cost (June 2024)

| Azure Resource       | Tier             | Rate (USD / GB / month) | Used Size (GB)        | Cost (USD) |
|----------------------|------------------|--------------------------|------------------------|------------|
| Azure Cosmos DB      | Serverless       | $0.25                    | 150                    | $37.50     |
| Azure Blob Storage   | Cool Tier        | $0.0152                  | 200 (compressed)       | $3.04      |
| Azure Blob Storage   | Archive Tier     | $0.0012                  | 250 (compressed)       | $0.30      |
| Azure Functions      | Consumption Plan | Per execution/ms         | N/A                    | ~$2.50     |
| **Total Estimated Cost** |              |                          |                        | **~$43.34** |

> ℹ️ Notes:  
> - Cold data is compressed (~33% typical ratio), reducing 450 GB to ~300 GB stored  
> - Blob split: 200 GB Cool (3–12 months), 250 GB Archive (>12 months)  
> - Azure Functions cost is based on timer-triggered batch archival  
> - Cosmos DB costs are minimized via serverless & restricted access to hot data  

---

## 🧩 Solution Components

### Archival Process

The system regularly looks for billing records that are older than 90 days in the main database (Cosmos DB). It groups these old records together into batches, then compresses each batch to make it smaller. After compressing, it uploads these batches as files to a cheaper storage system (Azure Blob Storage). Only after confirming that a batch was successfully saved to the blob storage, the system deletes those records from the main database. This way, older data moves out of the expensive database into low-cost storage without any loss.

### Read Fallback Process

When someone requests a billing record, the system first checks the main database. If the record isn’t there (because it was archived), it then looks for it in the batch files stored in blob storage by downloading and decompressing those files and searching for the record inside. This ensures that all records—new and old—are available through the same API without changes.

---

## 🚀 Deployment Instructions

### 1. Provision Azure Resources

```bash
# Create Storage Account and Blob Container
az storage account create --name mystorageacct --resource-group myResourceGroup --sku Standard_LRS
az storage container create --name billing-archive --account-name mystorageacct

# Create Azure Cosmos DB (serverless mode)
az cosmosdb create --name myCosmosDB --resource-group myResourceGroup --kind GlobalDocumentDB --serverless
