# aerospikedemo
Demo CRUD operation and data loader in Aerospike cluster in AWS with RF=2

* Steps:
*    1. Create the CFN stack from cfnstack.yaml
*    2. Update the /etc/aerospike/aerospike.conf to add the other node IPs of the cluster.
*    3. Start Aerospike in all three nodes.
*    4. In the app server, add NLB_URL, NAMESPACE and SET_NAME environment variables.
*    5. From the app directory, run aerospike_fakedata.py
*    6. Start the CRUD APIs from aerospike_crud.py
