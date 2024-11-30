# aerospikedemo
Demo CRUD operation and data loader in Aerospike cluster in AWS with RF=2

Steps:
* Create the CFN stack from cfnstack.yaml
* Update the /etc/aerospike/aerospike.conf to add the other node IPs of the cluster.
* Start Aerospike in all three nodes.
* In the app server, add NLB_URL, SET_NAME environment variables.
* From the app directory, run aerospike_fakedata.py
* Start the CRUD APIs from aerospike_crud.py
