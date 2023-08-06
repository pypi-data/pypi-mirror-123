from cord.client import CordClient, CordClientDataset

client: CordClientDataset = CordClient.initialise(
    '3e90e8e4-e8fe-4093-94d6-d38454fbb7ae',  # Dataset ID
    '78A-hLlxhPsf71JWCNcmMPTqu-jmVuV4wNIrRIEtDS8'  # API key
)
# Get and print dataset info (videos, image groups)
group = client.create_image_group(['tests/test_data/media/screen1.png', 'tests/test_data/media/screen2.png'])
