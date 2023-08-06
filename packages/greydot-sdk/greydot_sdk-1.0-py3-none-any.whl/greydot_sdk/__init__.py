"""Greydot SDK.

To make a call to the API use the URL : https://id.greydot.co.ke
You must use https and you can send data using GET or POST html method.
A transaction requires 2 steps.

Step 1 : Use function authorise to authorise a transaction

Step 2 : Complete the transaction using the link sent to the account holders mobile device.
All API functions will output XML by default.
To change this output to JSON simply add&datout=jsonto the end of any API URL calls.

Example :
URL :
https://id.greydot.co.ke/?key=000...000&par1=mobile_find_account&par2=27820000001&datout=json
"""

import requests
import xmltodict
import json


class APIClient:
    """Greydot API Client."""

    def __init__(
        self,
        api_key,
        base_url="https://id.greydot.co.ke",
    ):
        """Create new API client."""
        self.api_key = api_key
        self.base_url = base_url

    def _parse_xml(self, xml):
        """Parse xml to dict."""
        return json.loads(json.dumps(xmltodict.parse(xml))).get("reply")

    def _get_request(self, **params):
        """Send get request to remote url."""
        p = {}
        p.update(**params)
        response = requests.get(self.base_url, params=p)
        print(f"\033[32mGET: {response.url}\033[0m")
        return self._parse_xml(response.content.decode())

    def _post_request(self, **params):
        """Send post request to remote url."""
        p = {}
        p.update(**params)
        response = requests.post(self.base_url, params=p)
        print(f"\033[33mPOST: {response.url}\033[0m")
        return self._parse_xml(response.content.decode())

    def authorize(
        self,
        from_account_number,
        to_account_number,
        amount,
        description,
    ):
        """Authorise function create a funds reservation, that is completed by using the link sent to the account holders mobile device.

        https://id.greydot.co.ke?key=[yourAPIkey]&par1=[authorise]& par2=[AccountFrom]&par3=[AccountTo]&par4=[Amount]&par5=[Description]

        key = Your API key
        par1 = Function name
        par2 = From Account number
        par3 = To Account number
        par4 = Amount to transfer
        par5 = Description of transaction

        Example :
        URL :
        https://id.greydot.co.ke/?key=000...000&par1=authorise&par2=KES0000000000KE &par3=KES0000000001KE&par4=10.00&par5=Test_1
        Reply :
        .. code-block:: xml
            <?xml version="1.0" encoding="utf-8" ?>
            <reply>
            <function>enquire</function>
            <response_code>4</response_code>
            <message>approved</message>
            <payment_reference>8</payment_reference>
            </reply>
        """
        func_name = "authorise"
        params = {
            "key": self.api_key,
            "par1": func_name,
            "par2": from_account_number,
            "par3": to_account_number,
            "par4": amount,
            "par5": description,
        }
        return self._post_request(**params)

    def payment_enquire(
        self,
        payment_address,
    ):
        """Retrieve the details associated with a completed transaction.

        https://id.greydot.co.ke?key=[yourAPIkey]&par1=[payment_enquire]& par2=[payment address]

        key = Your API key
        par1 = Function name
        par2 = Payment address

        Example :
        URL :
        https://id.greydot.co.ke/?key=000...000&par1=payment_enquire&par2=8800000000001
        Reply :
        .. code-block:: xml
            <?xml version="1.0" encoding="utf-8" ?>
            <reply>
            <function>payment_enquire</function>
            <id>1</id>
            <date>2020-01-01 09:00:00</date>
            <status_id>4</status_id>
            <amount>10.00000</amount>
            <currency>ZAR</currency>
            <reference>Test_1</reference>
            </reply>
        """
        func_name = "payment_equire"
        params = {
            "key": self.api_key,
            "par1": func_name,
            "par2": payment_address,
        }
        return self._get_request(**params)

    def mobile_find_account(
        self,
        mobile_number,
    ):
        """Retrieve the account details associated with a mobile number.

        https://id.greydot.co.ke?key=[yourAPIkey]&par1=[mobile_find_account]

        key = Your API key
        par1 = Function name
        par2 = mobile number

        Example :
        URL :
        https://id.greydot.co.ke/?key=000...000&par1=mobile_find_account&par2=27820000001
        Reply :
        .. code-block:: xml
            <?xml version="1.0" encoding="utf-8" ?>
            <reply>
            <function>mobile_find_account</function>
            <response_code>1</response_code>
            <message>Success</message>
            <tokens>KES0000000001KE</tokens>
            <airtime>KES0000000002KE</airtime>
            </reply>
        """
        func_name = "mobile_find_account"
        params = {
            "key": self.api_key,
            "par1": func_name,
            "par2": mobile_number,
        }
        return self._get_request(**params)

    def voucher_get(
        self,
        from_account_number,
        amount,
    ):
        """Create a Greydot Voucher.

        https://id.greydot.co.ke?key=[yourAPIkey]&par1=[voucher_get]&par2=[FromAccount]&par3=[Amount]

        key = Your API key
        par1 = Function name
        par2 = From Account number
        par3 = Voucher Amount

        Example :
        URL :
        https://id.greydot.co.ke/?key=000...000&&par1=voucher_get&par2=KES0000000000KE&par3=2.00
        Reply :
        .. code-block:: xml
            <?xml version="1.0" encoding="utf-8" ?>
            <reply>
            <function>mobile_find_account</function>
            <response_code>1</response_code>
            <message>Success</message>
            <pin>893435779894</pin>
            <value>2.00</value>
            <exp_date>2020-01-01 09:00:00</exp_date>
            </reply>
        """
        func_name = "voucher_get"
        params = {
            "key": self.api_key,
            "par1": func_name,
            "par2": from_account_number,
            "par3": amount,
        }
        return self._post_request(**params)

    def server_authorize(
        self,
        from_account_number,
        to_account_number,
        amount,
        reference,
        reason_id,
        payment_id,
    ):
        """Create a funds reservation, which in turn is executed through either the server-to-server complete or void functions.

        https://id.greydot.co.ke?key=[yourAPIkey]&par1=[server_authorise]& par2=[AccountFrom]&par3=[AccountTo]&par4=[Amount]& par5=[YourReference]&par6=[PaymentReasonDeclaration]&par7=[PaymentID]

        key = Your API key
        par1 = Function name
        par2 = From Account number
        par3 = To Account number
        par4 = Amount to transfer
        par5 = Your Reference
        par6 = Payment Reason Declaration ID (see list below Example)
        par7 = Payment ID(your reference)

        After calling payment_equire we will send you the payment_address and your_reference using POST html form method to the url you set below.

        Set

        Example :
        URL :
        https://id.greydot.co.ke/?key=000...000&par1=server_authorise&
        par2=KES0000000000KE&par3=KES0000000001KE&par4=10.00&
        par5=Test_1&par6=2&par7=MyAcc8
        Reply :
        .. code-block:: xml
            <?xml version="1.0" encoding="utf-8" ?>
            <reply>
            <function>enquire</function>
            <response_code>4</response_code>
            <message>approved</message>
            <payment_reference>8</payment_reference>
            </reply>

        Payment Reason Declaration
        1 = Purchase of Physical Goods
        2 = Payment for Services
        3 = Donation
        4 = Payment for Intellectual Property
        5 = Rent
        6 = Interaccount Transfer
        7 = Unknown
        """
        func_name = "server_authorise"
        params = {
            "key": self.api_key,
            "par1": func_name,
            "par2": from_account_number,
            "par3": to_account_number,
            "par4": amount,
            "par5": reference,
            "par6": reason_id,
            "par7": payment_id,
        }
        return self._post_request(**params)

    def server_complete(
        self,
        payment_address,
    ):
        """Complete the transaction created by server_authorise.

        https://id.greydot.co.ke?key=[yourAPIkey]&par1=[server_complete]&par2=[PaymentAddress]

        key = Your API key
        par1 = Function name
        par2 = Payment Address (sent via URL POST by server_authorise)

        Example :
        URL :
        https://id.greydot.co.ke/?key=000...000&par1=server_complete&par2=8800000000001
        Reply :
        .. code-block:: xml
            <?xml version="1.0" encoding="utf-8" ?>
            <reply>
            <function>enquire</function>
            <response_code>4</response_code>
            <message>approved</message>
            </reply>
        """
        func_name = "server_complete"
        params = {
            "key": self.api_key,
            "par1": func_name,
            "par2": payment_address,
        }
        return self._post_request(**params)

    def server_void(
        self,
        payment_address,
        reason,
    ):
        """Void the transaction created by server_authorise.

        https://id.greydot.co.ke?key=[yourAPIkey]&par1=[server_void]&par2=[PaymentAddress]&par3=[ReasonForVoiding]

        key = Your API key
        par1 = Function name
        par2 = Payment Address (sent via URL POST by server_authorise)
        par3 = Reason For Voiding

        Example :
        URL :
        https://id.greydot.co.ke/?key=000...000&par1=server_void&par2=8800000000001&par3=service%20canceled
        Reply :
        .. code-block:: xml
            <?xml version="1.0" encoding="utf-8" ?>
            <reply>
            <function>enquire</function>
            <response_code>4</response_code>
            <message>approved</message>
            </reply>
        """
        func_name = "server_void"
        params = {
            "key": self.api_key,
            "par1": func_name,
            "par2": payment_address,
            "par3": reason,
        }
        return self._post_request(**params)
