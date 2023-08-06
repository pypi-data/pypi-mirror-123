
from .schema import Schema, ObjectClass, Attribute, DistinguishedName


def inet_org_person_schema():
    return Schema(
        ObjectClass(
                "inetOrgPerson",
                Attribute("businessCategory"),
                Attribute("carLicense"),
                Attribute("cn"),
                Attribute("departmentNumber"),
                Attribute("description"),
                Attribute("destinationIndicator"),
                Attribute("displayName"),
                Attribute("employeeNumber"),
                Attribute("employeeType"),
                Attribute("givenName"),
                Attribute("jpegPhoto", bytes),
                Attribute("l"),
                Attribute("mail"),
                Attribute("o"),
                Attribute("objectClass"),
                Attribute("ou"),
                Attribute("postalAddress"),
                Attribute("postalCode"),
                Attribute("postOfficeBox"),
                Attribute("physicalDeliveryOfficeName"),
                Attribute("preferredDeliveryMethod"),
                Attribute("preferredLanguage"),
                Attribute("registeredAddress"),
                Attribute("seeAlso", DistinguishedName),
                Attribute("sn"),
                Attribute("st"),
                Attribute("street"),
                Attribute("telephoneNumber"),
                Attribute("title"),
                Attribute("uid"),
                Attribute("userCertificate", bytes),
                Attribute("userPKCS12", bytes),
                Attribute("userPassword"),
                Attribute("userSMIMECertificate", bytes),
        )
    )
