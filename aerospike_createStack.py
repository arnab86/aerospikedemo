import boto3
import time
import sys

def create_stack(stack_name, template_file):
    # Create a CloudFormation client
    cf_client = boto3.client('cloudformation')

    # Read the template file
    with open(template_file, 'r') as template_file_obj:
        template_body = template_file_obj.read()

    try:
        # Create the CloudFormation stack
        response = cf_client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_NAMED_IAM']  # If your template creates IAM resources
        )

        print(f"Stack creation initiated. Stack ID: {response['StackId']}")

        # Wait until the stack is created
        waiter = cf_client.get_waiter('stack_create_complete')
        print(f"Waiting for stack {stack_name} to be created...")
        waiter.wait(StackName=stack_name)

        print(f"Stack {stack_name} has been created successfully!")

    except boto3.exceptions.SSLError as e:
        print(f"SSL error occurred: {e}")
        sys.exit(1)
    except boto3.exceptions.Boto3Error as e:
        print(f"Boto3 error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def delete_stack(stack_name):
    # Create a CloudFormation client
    cf_client = boto3.client('cloudformation')

    try:
        # Delete the CloudFormation stack
        response = cf_client.delete_stack(StackName=stack_name)
        print(f"Stack deletion initiated. Stack name: {stack_name}")

        # Wait until the stack is deleted
        waiter = cf_client.get_waiter('stack_delete_complete')
        print(f"Waiting for stack {stack_name} to be deleted...")
        waiter.wait(StackName=stack_name)

        print(f"Stack {stack_name} has been deleted successfully!")

    except boto3.exceptions.Boto3Error as e:
        print(f"Boto3 error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    stack_name = 'aerospike'
    template_file = 'cfnstack.yaml'
    action = input("Do you want to 'create' or 'delete'?")
    if (action == "create"):
        create_stack(stack_name, template_file)
    elif (action == "delete") :
        delete_stack(stack_name)
    else:
        print("Wrong Input")
