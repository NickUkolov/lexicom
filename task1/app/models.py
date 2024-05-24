from pydantic import ConfigDict, BaseModel, Field


class Phone(BaseModel):
    phone: str = Field(pattern=r'(^8|7|\+7)((\d{10})|(\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}))')

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "phone": "88005553535",
        }
    })


class Address(BaseModel):
    address: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "address": "Birobidzhan, Lenin str, etc",
        }
    })


class PhoneAddress(Address, Phone):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "phone": "88005553535",
            "address": "Birobidzhan, Lenin str, etc",
        }
    })
