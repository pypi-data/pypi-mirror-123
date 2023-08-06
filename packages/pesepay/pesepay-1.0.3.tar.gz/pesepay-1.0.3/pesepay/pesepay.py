import base64
import string
import jsonpickle
import requests
from Crypto.Cipher import AES

from pesepay.payments import (TransactionDetailsHolder,
                              InitiateTransactionResponse,
                              PesepaySeamlessTransactionResponse, Transaction, Customer, Payment, Amount,
                              PesepayPaymentProcessingResponse)

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1:])]

BASE_URL = 'https://api.test.pesepay.com/api/payments-engine'
CHECK_PAYMENT_URL = BASE_URL + '/v1/payments/check-payment'
MAKE_SEAMLESS_PAYMENT_URL = BASE_URL + '/v2/payments/make-payment'
MAKE_PAYMENT_URL = BASE_URL + '/v1/payments/make-payment/secure'
INITIATE_PAYMENT_URL = BASE_URL + '/v1/payments/initiate'


class Pesepay:
    # https://api.test.pesepay.com/api/payments-engine
    BASE_URL = 'https://api.test.pesepay.com/api/payments-engine'
    result_url: string = None
    return_url: string = None

    def __init__(self, integration_key: string, encryption_key: string):
        self.integration_key = integration_key
        self.encryption_key = encryption_key
        self.headers = {'key': integration_key, 'Content-Type': 'application/json'}

    def initiate_transaction(self, transaction: Transaction):
        if self.result_url is None:
            raise 'Result url has not been specified'

        if self.return_url is None:
            raise 'Return url has not been specified'

        transaction.resultUrl = self.result_url
        transaction.returnUrl = self.return_url

        raw_request = jsonpickle.encode(transaction.__dict__)

        encrypted_request = TransactionDetailsHolder(self.__encrypt(raw_request))

        server_response = requests.post(INITIATE_PAYMENT_URL, data=jsonpickle.encode(encrypted_request),
                                        headers=self.headers)
        server_response_json = server_response.json()

        if server_response.status_code == 200:
            raw_response = self.__decrypt(server_response_json.get('payload'))
            return InitiateTransactionResponse.from_json(jsonpickle.decode(raw_response))
        else:
            raise InvalidRequestException(server_response_json.get('message'))

    def make_payment(self, payment: Payment, reference_number: string, required_fields: dict = None,
                     merchant_reference: string = None):
        payment.referenceNumber = reference_number
        payment.merchantReference = merchant_reference
        payment.paymentRequestFields = required_fields

        raw_request = jsonpickle.encode(payment.__dict__)

        encrypted_request = TransactionDetailsHolder(self.__encrypt(raw_request))

        server_response = requests.post(MAKE_PAYMENT_URL, data=jsonpickle.encode(encrypted_request),
                                        headers=self.headers)
        server_response_json = server_response.json()

        if server_response.status_code == 200:
            return PesepayPaymentProcessingResponse.from_json(server_response_json)
        else:
            raise InvalidRequestException(server_response_json.get('message'))

    def make_seamless_payment(self, payment: Payment, reason_for_payment: string, amount: float,
                              required_fields: dict = None):
        if self.result_url is None:
            raise 'Result url has not been specified'

        payment.resultUrl = self.result_url
        payment.returnUrl = self.return_url
        payment.reasonForPayment = reason_for_payment
        payment.amountDetails = Amount(amount, payment.currencyCode)
        payment.paymentMethodRequiredFields = required_fields

        raw_request = jsonpickle.encode(payment.__dict__)

        print(raw_request)

        encrypted_request = TransactionDetailsHolder(self.__encrypt(raw_request))

        server_response = requests.post(MAKE_SEAMLESS_PAYMENT_URL, data=jsonpickle.encode(encrypted_request),
                                        headers=self.headers)
        server_response_json = server_response.json()

        if server_response.status_code == 200:
            raw_response = self.__decrypt(server_response_json.get('payload'))
            return PesepaySeamlessTransactionResponse.from_json(jsonpickle.decode(raw_response))
        else:
            raise InvalidRequestException(server_response_json.get('message'))

    def check_payment(self, reference_number: string):
        url = CHECK_PAYMENT_URL + '?referenceNumber=' + reference_number
        return self.poll_transaction(url)

    def poll_transaction(self, poll_url):
        server_response = requests.get(poll_url, headers=self.headers)
        server_response_json = server_response.json()

        if server_response.status_code == 200:
            raw_response = self.__decrypt(server_response_json.get('payload'))
            return PesepaySeamlessTransactionResponse.from_json(raw_response)
        else:
            raise InvalidRequestException(server_response_json.get('message'))

    def create_payment(self, currency_code: string, payment_method_code: string, email: string = None,
                       phone: string = None, name: string = None):
        if email == None and phone == None:
            raise InvalidRequestException('Email and/or phone number should be provided')

        customer = Customer(email, phone, name)
        return Payment(currency_code, payment_method_code, customer)

    def create_transaction(self, app_id: int, app_code: string, app_name: string, amount: float, currency_code: string,
                           payment_reason: string, merchant_reference: string = None):
        return Transaction(app_id, app_code, app_name, amount, currency_code, payment_reason, merchant_reference)

    def __encrypt(self, payload):
        init_vector = self.encryption_key[0:16]
        cryptor = AES.new(self.encryption_key.encode("utf8"), AES.MODE_CBC, init_vector.encode("utf8"))
        ciphertext = cryptor.encrypt(bytes(pad(payload), encoding="utf8"))
        return base64.b64encode(ciphertext).decode('utf-8')

    def __decrypt(self, payload):
        decode = base64.b64decode(payload)
        init_vector = self.encryption_key[0:16]
        cryptor = AES.new(self.encryption_key.encode("utf8"), AES.MODE_CBC, init_vector.encode("utf8"))
        plain_text = cryptor.decrypt(decode)
        return unpad(plain_text).decode('utf-8')


class InvalidRequestException(Exception):
    def __init__(self, message):
        super(InvalidRequestException, self).__init__(message)
