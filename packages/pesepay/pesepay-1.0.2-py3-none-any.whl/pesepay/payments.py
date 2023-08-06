import string

import jsonpickle


class Customer:
    def __init__(self, email: string = None, phone_number: string = None, name: string = None):
        self.email = email
        self.phoneNumber = phone_number
        self.name = name


class Amount:
    def __init__(self, amount: float, currency_code: string):
        self.amount = amount
        self.currencyCode = currency_code

    @staticmethod
    def from_json(json_string):
        return Amount(json_string.get("amount"), json_string.get("currencyCode"))


class Transaction:
    resultUrl: string
    returnUrl: string

    def __init__(self, application_id: int, application_code: string, application_name: string, amount: float,
                 currency_code: string,
                 reason_for_payment: string, merchant_reference: string = None):
        self.applicationId = application_id
        self.applicationCode = application_code
        self.applicationName = application_name
        self.amountDetails = Amount(amount, currency_code)
        self.transactionType = "BASIC"
        self.reasonForPayment = reason_for_payment
        self.merchantReference = merchant_reference


class Payment:
    referenceNumber: string
    amountDetails: Amount
    reasonForPayment: string
    paymentRequestFields: dict
    paymentMethodRequiredFields: dict
    merchantReference: string
    returnUrl: string
    resultUrl: string

    def __init__(self, currencyCode: string, paymentMethodCode: string, customer: Customer):
        self.currencyCode = currencyCode
        self.paymentMethodCode = paymentMethodCode
        self.customer = customer


class TransactionDetailsHolder:
    def __init__(self, payload: string):
        self.payload = payload


class InitiateTransactionResponse:
    def __init__(self, reference_number, poll_url, redirect_url):
        self.reference_number = reference_number
        self.poll_url = poll_url
        self.redirect_url = redirect_url

    @staticmethod
    def from_json(json_string):
        ref_no = json_string.get('referenceNumber')
        poll_url = json_string.get('pollUrl')
        redirect_url = json_string.get('redirectUrl')
        return InitiateTransactionResponse(ref_no, poll_url, redirect_url)


class PesepayPaymentProcessingResponse:
    def __init__(self, reference_number: string, transaction_status: string, message: string, return_url: string,
                 redirection_required: bool, redirect_url: string):
        self.referenceNumber = reference_number
        self.transactionStatus = transaction_status
        self.message = message
        self.returnUrl = return_url
        self.redirectionRequired = redirection_required
        self.redirectUrl = redirect_url

    @staticmethod
    def from_json(json_string):
        return PesepayPaymentProcessingResponse(json_string.get("referenceNumber"),
                                                json_string.get("transactionStatus"),
                                                json_string.get("message"),
                                                json_string.get("returnUrl"),
                                                json_string.get("redirectionRequired"),
                                                json_string.get("redirectUrl"))


class PesepaySeamlessTransactionResponse:
    def __init__(self, reference_number, date_of_transaction, amount_details,
                 reason_for_payment, transaction_status,
                 result_url, return_url, poll_url, redirect_url):
        self.reference_number = reference_number
        self.date_of_transaction = date_of_transaction
        self.amount_details = amount_details
        self.reason_for_payment = reason_for_payment
        self.transaction_status = transaction_status
        self.result_url = result_url
        self.return_url = return_url
        self.poll_url = poll_url
        self.redirect_url = redirect_url

    @staticmethod
    def from_json(json_string):
        amount_details_json = jsonpickle.encode(json_string.get("amountDetails"))
        return PesepaySeamlessTransactionResponse(json_string.get("referenceNumber"),
                                                  json_string.get("dateOfTransaction"),
                                                  Amount.from_json(jsonpickle.decode(amount_details_json)),
                                                  json_string.get("reasonForPayment"),
                                                  json_string.get("transactionStatus"),
                                                  json_string.get("resultUrl"),
                                                  json_string.get("returnUrl"),
                                                  json_string.get("pollUrl"),
                                                  json_string.get("redirectUrl"))


class InvalidRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)
