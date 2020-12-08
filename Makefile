.PHONY: data

data: data/hashed.xlsx

data/hashed.xlsx:
	aws s3 cp s3://cscie29-data/hashed.xlsx data/ --request-payer=requester