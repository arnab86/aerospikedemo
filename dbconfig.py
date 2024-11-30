import os

class Config:
    # Database URL
    NLB_URL = os.getenv("NLB_URL", "it is not set")
    NAMESPACE = os.getenv("NAMESPACE", "mydemo")
    SET_NAME = os.getenv("SET_NAME", "demo")

