# discord-gateway

## Initial setup
Create a configuration file as detailed in [readme-f1rewall.md](readme-f1rewall.md).

Create a gcloud secret from that file.
```
gcloud secrets create discord-gateway-config --data-file=config.yaml
```

Allow GCP Cloud run to access the secret.
Follow these steps https://cloud.google.com/run/docs/configuring/secrets#access-secret

## Deploy

From the repo root, this command will build and deploy a new container with your changes.

```
gcloud beta run deploy discord-gateway \
  --allow-unauthenticated \
  --source . \
  --port=5000 \
  --set-secrets=/secret/config.yaml=discord-gateway-config:latest \
  --region=us-east4
```

## Custom domain name

The random name assigned to the service is not desirable for engendering trust.

There are a few steps.

Create a permenant address, NEG, Service, and url-map.
```
gcloud compute addresses create discord-gateway \
    --network-tier=PREMIUM \
    --ip-version=IPV4 \
    --global

gcloud beta compute network-endpoint-groups create discord-gateway \
    --region=us-east4 \
    --network-endpoint-type=serverless  \
    --cloud-run-service=discord-gateway

gcloud beta compute backend-services create discord-gateway \
    --load-balancing-scheme=EXTERNAL_MANAGED \
    --global

gcloud beta compute backend-services add-backend discord-gateway \
    --global \
    --network-endpoint-group=discord-gateway \
    --network-endpoint-group-region=us-east4

gcloud beta compute url-maps create discord-gateway \
    --default-service discord-gateway
```

Choose your domain name and point it to the address created in the previous set
```
gcloud compute addresses describe discord-gateway --global
```

Now, issue the cert and attach it to a target proxy which is attached to the forwarding-rules.
```
gcloud beta compute ssl-certificates create discord-gateway \
    --domains discord-gateway.optimism.io

gcloud beta compute target-https-proxies create discord-gateway \
    --ssl-certificates=discord-gateway \
    --url-map=discord-gateway

gcloud beta compute forwarding-rules create discord-gateway \
    --load-balancing-scheme=EXTERNAL_MANAGED \
    --network-tier=PREMIUM \
    --address=discord-gateway \
    --target-https-proxy=discord-gateway \
    --global \
    --ports=443
```

Now, never think about it again :relieved: