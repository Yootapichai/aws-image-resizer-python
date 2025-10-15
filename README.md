# Automated Serverless Image Resizer on AWS

This project is a fully serverless, event-driven image resizing service built on AWS. When an image is uploaded to an S3 bucket, an AWS Lambda function is automatically triggered to resize it, store the result in a separate S3 bucket, and log the metadata to a DynamoDB table.

## Tech Stack

*   **Cloud:** AWS (Lambda, S3, DynamoDB, IAM)
*   **Framework:** Serverless Framework
*   **Language:** Python 3.9
*   **Key Libraries:** Boto3, Pillow
*   **IaC:** YAML (via Serverless Framework)

## Getting Started

#### Prerequisites:
*   AWS CLI (configured with your asccess key)
*   Node.js & npm
*   Python 3.x

#### Deployment:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Yootapichai/aws-image-resizer-python.git
    cd aws-image-resizer-python
    ```
2.  **Install Serverless Framework and plugins:**
    ```bash
    npm install -g serverless

    # install plugin
    npm i -D serverless-python-requirements @serverless-aws/serverless-s3-remover
    ```
3.  **Deploy to AWS:**
    ```bash
    serverless deploy
    ```

## How to Test

1.  Navigate to the **AWS S3 Console**.
2.  **Upload** a `.jpg` or `.png` file to the bucket ending in `...-original-images-dev`.
3.  **Verify** the resized image in the `...-resized-images-dev` bucket.
4.  **Check** the new metadata entry in the corresponding **DynamoDB Table**.

## Cleanup

To remove all deployed resources from your AWS account and avoid further charges, run:
```bash
serverless remove
```