# Introduction

> API Endpoint

```html
https://api.kite.ly
```

The Kite API is organized around [REST](http://en.wikipedia.org/wiki/Representational_state_transfer). Our API is designed to have predictable, resource-oriented URLs and to use HTTP response codes to indicate API errors. We use built-in HTTP features, like HTTP authentication and HTTP verbs, which can be understood by off-the-shelf HTTP clients. [JSON](http://www.json.org/) will be returned in all responses from the API, including errors (though if you're using API bindings, we will convert the response to the appropriate language-specific object).

To make the Kite API as explorable as possible, accounts have test-mode API keys as well as live-mode API keys. These keys can be active at the same time. Data created with test-mode credentials will never result in real products being created and shipped to addresses, will never hit the credit card networks and will never cost anyone money.

<span ng-if="authenticated">
**The requests in the sidebar actually work**. We'll perform the requests using your test-mode API key, `[[public_key]]`, which is linked to your account under the email address **[[user_email]]**.
</span>

# Libraries
Kite is built by developers for developers and we have SDKs spanning a range of languages and platforms. It's recommended that you use our SDKs where available as it will greatly simplify and speed up integration. In most cases you can be up an running sending through product orders within minutes.

Some of our SDKs are also bundled with optional checkout experiences proven to convert well with users.

* [iOS SDK](https://github.com/OceanLabs/iOS-Print-SDK)
* [Android SDK](https://github.com/OceanLabs/Android-Print-SDK)

# Authentication

> Example Request

```shell
curl "https://api.kite.ly/v2.0/address/search/?country_code=USA&search_term=1+Infinite+Loop" \
  -H "Authorization: ApiKey [[public_key]]:"
```

```objective_c
[OLKitePrintSDK setAPIKey:@"[[public_key]]" withEnvironment:kOLKitePrintSDKEnvironmentSandbox];
```

```java
KitePrintSDK.initialize("[[public_key]]", KitePrintSDK.Environment.TEST, getApplicationContext());
```

> <span ng-if="authenticated">One of your test API keys has been filled into all the examples on the page, so you can test out any example right away.</span>

> <span ng-if="!authenticated">A sample test API key has been provided so you can test out all the examples straight away. You should replace `[[public_key]]` with one of your own found in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard.</span>

You authenticate with the Kite API by providing your API key in the request. You can manage your API keys in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard. You can have multiple API keys active at one time. Your API keys carry many privileges, so be sure to keep them secret!

To authenticate you include the HTTP `Authorization` header in your request. All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTPS). Calls made over plain HTTP will fail. You must authenticate for all requests.

In some scenarios it's also desirable to include your secret key in the `Authorization` header. If you're building a mobile application this is not normally needed, but if you're placing orders from your own server it usually makes sense. See [payment workflows](#payment-workflows) for more details.

# Payment Workflows
Your customers can either pay you directly when they place an order for a product or we can take payment on your behalf and automatically transfer your revenue into an account of your choosing. 

## Kite takes payment
In this scenario we take payment from customers on your behalf. This will occur entirely within your app or website in a way that's totally branded to you, your customers don't even need to know we were involved. We then automatically transfer funds we owe you directly into a bank or a PayPal account of your choosing. You can setup the account into which you want to receive payments in the [billing](https://www.kite.ly/settings/billing/) section of the dashboard.

This is the easiest approach to using the Kite platform as it means you don't need to run your own server and it's baked into several of our SDKs. 

## You take payment

> Example Request

```shell
curl "https://api.kite.ly/v2.0/address/search/?country_code=USA&search_term=1+Infinite+Loop" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>"
```

```objective_c
// Our iOS SDK does not support this payment workflow directly as it would require embedding your secret key into the app. Instead use our REST API
```

```java
// Our Android SDK does not support this payment workflow directly as it would require embedding your secret key into the app. Instead use our REST API
```

> Replace `<your_secret_key>` with the one found in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard.

In this scenario you take payment directly from your customer in any manner of your choosing. You'll need your own server infrastructure in order to take care of the payment processing, payment validation and to submit [product order requests](#placing-orders) to the Kite platform. 

You'll need to add a card to be charged for any orders you place with Kite. This can be done in the [billing](https://www.kite.ly/settings/billing/) section of the dashboard.

Any request you make to Kite that would result in you incurring a charge (i.e. [product order requests](#placing-orders)) will need to include both your API key and your secret key in the HTTP `Authorization` header. Your secret key can be found alongside your API key in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard. 

The presence of your secret key in charge incurring requests (i.e. product order requests) removes the need for the `proof_of_payment` argument to be provided as the card associated with your account can be charged directly.

<aside class="warning">You should never embed your secret key in a client application, rather requests including your secret key should only be made from your own server.</aside>

# Errors

> Example Error Response

```json
{
  "error": {
  	"code": "01",
    "message": "JSON schema error: The request data does not match the required JSON schema"
  }
}
```

Kite uses conventional HTTP response codes to indicate success or failure of an API request. In general, codes in the 2xx range indicate success, codes in the 4xx range indicate an error that resulted from the provided information (e.g. a required parameter was missing, etc.), and codes in the 5xx range indicate an error with Kite's servers.

Where possible an error response will include an `error` object that provides further details in the form of a `code` and `message`.

### Error code summary
          | |
--------- | -----------
<span id="error-code-E00">00</span> | Failed to parse JSON from the body of the request. Please ensure you're sending data through as valid JSON and please check it can be decoded as UTF-8
<span id="error-code-E01">01</span> | The request data does not match the required JSON schema
<span id="error-code-E02">02</span> | Version not supported
<span id="error-code-E03">03</span> | Failed to add order to the processing queue
<span id="error-code-E10">10</span> | Cannot set email in both `user_data` and `customer_email`
<span id="error-code-E11">11</span> | Invalid delivery address
<span id="error-code-E12">12</span> | Invalid `customer_payment` field provided
<span id="error-code-E13">13</span> | Promo code provided does not exist
<span id="error-code-E14">14</span> | Invalid email address
<span id="error-code-E15">15</span> | Failed to add order to the fulfilment queue
<span id="error-code-E16">16</span> | No email address provided
<span id="error-code-E17">17</span> | Invalid email address provided
<span id="error-code-E18">18</span> | Customer payment required for given payment method
<span id="error-code-E19">19</span> | Unexpected order rejection
<span id="error-code-E20">20</span> | Payment confirmation already used on a successful order
<span id="error-code-E30">30</span> | Template does not exist
<span id="error-code-E31">31</span> | One or more products ordered is unavailable
<span id="error-code-E32">32</span> | Failed to save address for print job
<span id="error-code-E33">33</span> | One or more products ordered is missing a shipping address
<span id="error-code-E40">40</span> | Assets not provided
<span id="error-code-E41">41</span> | Malformed asset cropping instructions
<span id="error-code-E42">42</span> | One or more assets provided were neither an asset ID nor valid URL
<span id="error-code-E43">43</span> | Assets provided in an incorrect format for the product
<span id="error-code-E44">44</span> | Required named asset field missing
<span id="error-code-E45">45</span> | Invalid text object
<span id="error-code-E46">46</span> | Invalid request for Noncustomizable product
<span id="error-code-E50">50</span> | Product not available in given country
<span id="error-code-H00">H00</span> | User is blocked from sending orders
<span id="error-code-H01">H01</span> | User has no valid card on record
<span id="error-code-F01">F01</span> | Asset does not exist
<span id="error-code-F02">F02</span> | Supplied image is Corrupt and unprocessable
<span id="error-code-F03">F03</span> | Missing delivery address
<span id="error-code-F04">F04</span> | Missing postcode
<span id="error-code-F05">F05</span> | Missing city
<span id="error-code-F06">F06</span> | Missing county / state
<span id="error-code-F07">F07</span> | Missing address line 1
<span id="error-code-F08">F08</span> | Missing email address
<span id="error-code-F10">F10</span> | Unexpected fulfilment error
<span id="error-code-F20">F20</span> | Incorrect apparel asset format
<span id="error-code-F30">F30</span> | Incorrect Sticky9 affiliate name
<span id="error-code-P01">P01</span> | Unknown payment method
<span id="error-code-P02">P02</span> | Error looking up payment
<span id="error-code-P03">P03</span> | No proof of payment and no secret key provided
<span id="error-code-P04">P04</span> | Max number of echeques exceeded
<span id="error-code-P05">P05</span> | Cannot use discount codes without a card on record
<span id="error-code-P06">P06</span> | Confirmed payment does not cover order cost
<span id="error-code-P07">P07</span> | Unexpected PayPal intent
<span id="error-code-P08">P08</span> | Does not recognise modification area provided in request

# Pagination

> Example Request

```shell
curl "https://api.kite.ly/v2.0/order/?offset=30&limit=5" \
  -H "Authorization: ApiKey [[public_key]]:[[secret_key]]"
```

```objective_c
// Our iOS SDK encapsulates pagination through some high level abstractions so you don't need to worry about this
```

```java
// Our Android SDK encapsulates pagination through some high level abstractions so you don't need to worry about this
```

> Example Paginated Response

```shell 
{
  "meta": {
    "limit": 5,
	"next": null,
	"offset": 30,
	"previous": null,
	"total_count": 33
  },
  "objects": [
    {...},
	{...},
	{...}
  ]
}
```

```objective_c
// See above comment
```

```java
// See above comment
```


Several Kite API endpoints return paginated responses, for example the list orders endpoint. All paginated responses share the same common structure.

### Arguments

          | |
--------- | -----------
offset<span class="optional-argument">optional</span> | The offset into the result set of objects returned
limit<span class="optional-argument">optional</span> | By default, you get returned a paginated set of objects (20 per page is the default), by specifying the `limit` argument you can control the number of objects returned


# Assets
Assets are files, typically images (jpegs, pngs), PDFs & fonts that you use in your product & print order requests. There are two classes of assets: *remote* and *managed*.

**Remote assets** are those that you already host yourself. You can start submitting orders straight away with these as long as they have URLs that are accessible to the Kite servers.

**Managed assets** are those which we host on Amazon S3 on your behalf. Managed assets allow you to use our infrastructure to host your user's assets (and your own) without the need to pay for your own hosting.

## The asset object

> Example JSON

```json
{
  "asset_id": 1638,
  "client_asset": false,
  "description": "A very grumpy cat",
  "filename": "1.jpg",
  "mime_type": "image/jpeg",
  "stock_asset": false,
  "time_registered": "2014-03-14T14:37:51",
  "url": "http://psps.s3.amazonaws.com/sdk_static/1.jpg"
}
```

### Attributes
          | |
--------- | -----------
asset_id<span class="attribute-type">integer</span> | The unique identifier of the asset
client_asset<span class="attribute-type">boolean</span> | Client assets are dynamic assets typically uploaded by your users & customers. They are periodically purged (a short while after the customer has received their order) and are not displayed in your dashboard
description<span class="attribute-type">string</span> | An optional description of the asset
filename<span class="attribute-type">string</span> | The asset's filename
mime_type<span class="attribute-type">string</span> | The files mimetype, such as 'image/jpeg'. Optional and unused for remote assets
stock_asset<span class="attribute-type">string</span> | Indicates whether this is one of the default Kite assets provided on signup
time_registered<span class="attribute-type">string</span> | The time the asset registration request was received
url<span class="attribute-type">string</span> | The URL from which the asset can be fetched for display

## Uploading an asset

> Managed Asset Registration Request

```shell
curl "https://api.kite.ly/v2.0/asset/sign/?mime_types=image/jpeg&client_asset=true" \
  -H "Authorization: ApiKey [[public_key]]:"
```

```objective_c
#import <Kite-Print-SDK/OLAssetUploadRequest.h>

OLAssetUploadRequest *req = [[OLAssetUploadRequest alloc] init];
req.delegate = self; // assuming self conforms to OLAssetUploadRequestDelegate
[req uploadImageAsJPEG:[UIImage imageNamed:@"photo"]];

```

```java
import ly.kite.print.AssetUploadRequestListener;

AssetUploadRequest req = new AssetUploadRequest();
req.uploadAsset(new Asset(R.drawable.instagram1), getApplicationContext(), /*AssetUploadRequestListener:*/this);
```

> Example Response

```shell
{
  "signed_requests": [
    "https://s3-eu-west-1.amazonaws.com/...&Signature=0ls3p7BD3RGcAvsB0UNS3D"
  ],
  "asset_ids": [
    560227
  ],
  "urls": [
    "https://s3-eu-west-1.amazonaws.com/.../560227.jpeg"
  ]
}
```

```objective_c
#pragma mark OLAssetUploadRequestDelegate methods
- (void)assetUploadRequest:(OLAssetUploadRequest *)req didSucceedWithAssets:(NSArray/*<OLAsset>*/ *)assets {
	// Success, we're now hosting the asset for you and it has been successfully uploaded to S3
}

- (void)assetUploadRequest:(OLAssetUploadRequest *)req didFailWithError:(NSError *)error {
	// do something sensible with the error
}
```

```java
// AssetUploadRequestListener implementation:

@Override
public void onUploadComplete(AssetUploadRequest req, List<Asset> assets) {

}

@Override
public void onError(AssetUploadRequest req, Exception error) {

}

@Override
public void onProgress(AssetUploadRequest req, int totalAssetsUploaded, 
                       int totalAssetsToUpload,  long bytesWritten, 
                       long totalAssetBytesWritten, long totalAssetBytesExpectedToWrite) {
                
}

```

> S3 Asset Upload Request

```shell
curl --upload-file "<path/to/local/image.jpg>" \
    -H "Content-Type:image/jpeg" \
    -H "x-amz-acl:private" \
    "<signed_request_url>"
```

```objective_c
// Manual S3 upload is not required with the iOS SDK as it's taken care of automatically -- it's encapsulated within the OLAssetUploadRequest:upload* methods
```

```java
// Manual S3 upload is not required with the Android SDK as it's taken care of automatically -- it's encapsulated within the AssetUploadRequest.uploadAsset methods
```

> Replace `<path/to/local/image.jpg>` with the path to a local image to be uploaded and `<signed_request_url>` with a url found in the `signed_requests` property in the response from the previous Managed Asset Registration Request


Registering and uploading a managed asset is a two step process. First you make a request to the Kite servers to get a signed Amazon S3 URL to which you can upload the asset. Second you upload the file representing the asset to Amazon S3 using that signed URL.

### HTTP Request

`GET https://api.kite.ly/v2.0/asset/sign/`

### Arguments

          | |
--------- | -----------
mime_types<span class="required-argument">required</span> | A comma separated list of one or more [mime types](http://en.wikipedia.org/wiki/Internet_media_type) for the assets that you want to upload. The number of mime types you specify indicates the number of assets you are expected to upload to S3. Current supported mime types are: `image/jpeg`, `image/png`, `application/pdf`
client_asset<span class="optional-argument">optional</span> | A boolean indicating if this is a client/customer/user asset. This should always be `true` if the assets with specified mime types are being uploaded from a client application. Client assets are are periodically purged (a short while after a customer has received their order) and are not displayed in your dashboard

### Returns
Returns an object with `signed_requests`, `asset_ids` & `urls` list properties. Each list's length is the same and equal to the number of `mime_type`'s specified in the request.  The equivalent index in each list corresponds directly to the asset referred to by the mime type at the same index in the request's `mime_type` query parameter.

### Response Properties
          | |
--------- | -----------
signed_requests<span class="attribute-type">list</span> | A list of signed Amazon S3 URLs that can be used to upload the assets
asset_ids<span class="attribute-type">list</span> | A list of [asset object](#the-asset-object) id's that can be used in product & print order requests
urls<span class="attribute-type">list</span> | A list of Amazon S3 URLs where the uploaded assets will reside. These are not publically accessible but can be used in various requests

# Products

With a single API request to Kite you can have personalised products created, packaged and shipped anywhere in the world. Our product range is second to none, and we're adding new ones all the time.

Packaging will carry your branding, not ours -- your customers never need to know we were involved!

We have a global product fulfilment and distribution network to get orders into your customers hands faster.

When you initially create your Kite account, the product template id's listed in this section are immediately available for you to order from.

Additional products SKU's are also available from our exclusive suppliers such as Photobox, please do [get in touch](mailto:hello@kite.ly) for further information about getting access to these product ranges.

Which products you display to your customers within our mobile SDKs and their associated retail prices can be configured within the [products](https://www.kite.ly/dashboard/products) section of the dashboard


## The job object

> Example JSON

```json
{
  "template_id": "magnets",
  "assets": [
    "http://psps.s3.amazonaws.com/sdk_static/1.jpg", 
    "http://psps.s3.amazonaws.com/sdk_static/2.jpg",
    "http://psps.s3.amazonaws.com/sdk_static/3.jpg",
    "http://psps.s3.amazonaws.com/sdk_static/4.jpg"
  ]
}
```

A job encapsulates the details to create a single personalised product. For example the job represented by the JSON to the right would result in a set of magnets being created where each magnet has one of four images printed on the front.

### Attributes

          | |
--------- | -----------
template_id<span class="attribute-type">string</span> | The identifier for the product you want created. A full list of template identifiers for products can be found below in the relevant product ordering sections
assets<span class="attribute-type">list</span> | A list of image URLs accessible to the Kite servers or a list of [asset object](#the-asset-object) identifiers that you have received by [uploading an asset](#uploading-an-asset) to Kite. These assets will be used in the creation of the personalised product indicated by `template_id`
options<span class="attribute-type">object</span> | *Optional* object only applicable for certain products. It contains product specific modifiers; for example for [t-shirts](#ordering-apparel) you can specify the color and size amongst other things in here, for [phone cases](#ordering-phone-cases) you can specify gloss or matte finish, etc.
pdf<span class="attribute-type">string</span> | *Optional* object only applicable for certain products such as [photobooks](#ordering-photobooks). A PDF URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite.

## The order object

> Example JSON

```json
{
  "proof_of_payment": "PAY-4M676136DK539691RKURJ7QY",
  "shipping_address": {
    "recipient_name": "Deon Botha",
    "address_line_1": "Eastcastle House",
	"address_line_2": "27-28 Eastcastle Street",
	"city": "London",
	"county_state": "Greater London",
	"postcode": "W1W 8DH",
	"country_code": "GBR"
  },
  "customer_email": "[[user_email]]",
  "customer_phone": "+44 (0)784297 1234",
  "user_data": {
  	"foo": "bar",
  	"pi": 3.14
  },
  "customer_payment": {
    "amount": 9.99,
    "currency": "USD"
  },
  "jobs": [{
    "assets": ["http://psps.s3.amazonaws.com/sdk_static/1.jpg"],
	"template_id": "i6_case"
  }, {
    "assets": ["http://psps.s3.amazonaws.com/sdk_static/2.jpg"],
	"template_id": "a1_poster"
  }]
}
```
An order encapsulates all the details required to create & deliver one or more personalised products (described by [job objects](#the-job-object)) to an address. For example the order represented by the JSON on the right would result in an *iPhone 6 Case* and an *A1 Poster* being created and shipped to the specified address.

### Attributes

          | |
--------- | -----------
proof_of_payment<span class="attribute-type">string</span> | The proof of payment is a either a PayPal REST payment id for a payment/transaction made to the Kite PayPal account or a Stripe token created using Kite's Stripe publishable key. This field will be absent if you opted for [taking payment yourself](#you-take-payment)
shipping_address<span class="attribute-type">[address object](#the-address-object)</span> | The address to which the order will be delivered
customer_email<span class="attribute-type">string</span> | The customer's email address. Automated order status update emails (you can brand these) can optionally be sent to this address i.e. order confirmation email, order dispatched email, etc. You can configure these in the Kite dashboard
customer_phone<span class="attribute-type">string</span> | The customer's phone number. Certain postage companies require this to be provided e.g. FedEx
user_data<span class="attribute-type">dictionary</span> | A dictionary containing any application or user specific meta data that you attached to the order.
customer_payment<span class="attribute-type">dictionary</span> | A dictionary containing the amount paid by the customer. In instances where Kite does not take payment (i.e you are using your secret key in the [Authorization header](#authentication) to validate orders), this field is required to give an accurate representation on the profit made on the sale within the [orders](https://www.kite.ly/settings/credentials) section of the Kite dashboard.
jobs<span class="attribute-type">list</span> | A list of one or more [job objects](#the-job-object) to be created and delivered to `shipping_address`

## Placing orders

> Example Order Request

```shell
curl "https://api.kite.ly/v2.0/print/" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>" \
  --data '{
    "shipping_address": {
      "recipient_name": "Deon Botha",
      "address_line_1": "Eastcastle House",
    "address_line_2": "27-28 Eastcastle Street",
    "city": "London",
    "county_state": "Greater London",
    "postcode": "W1W 8DH",
    "country_code": "GBR"
    },
    "customer_email": "[[user_email]]",
    "customer_phone": "+44 (0)784297 1234",
    "jobs": [{
      "assets": ["http://psps.s3.amazonaws.com/sdk_static/1.jpg"],
    "template_id": "i6_case"
    }, {
      "assets": ["http://psps.s3.amazonaws.com/sdk_static/2.jpg"],
    "template_id": "a1_poster"
    }]
  }'
```

```objective_c
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
#import <Kite-Print-SDK/OLKitePrintSDK.h>

NSArray *assets = @[
    [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/1.jpg"]]
];

id<OLPrintJob> iPhone6Case = [OLPrintJob printJobWithTemplateId:@"i6_case" OLAssets:assets];
id<OLPrintJob> poster = [OLPrintJob printJobWithTemplateId:@"a1_poster" OLAssets:assets];

OLPrintOrder *order = [[OLPrintOrder alloc] init];
[order addPrintJob:iPhone6Case];
[order addPrintJob:poster];

OLAddress *a    = [[OLAddress alloc] init];
a.recipientName = @"Deon Botha";
a.line1         = @"27-28 Eastcastle House";
a.line2         = @"Eastcastle Street";
a.city          = @"London";
a.stateOrCounty = @"Greater London";
a.zipOrPostcode = @"W1W 8DH";
a.country       = [OLCountry countryForCode:@"GBR"];

order.shippingAddress = a;

OLPayPalCard *card = [[OLPayPalCard alloc] init];
card.type = kOLPayPalCardTypeVisa;
card.number = @"4121212121212127";
card.expireMonth = 12;
card.expireYear = 2020;
card.cvv2 = @"123";

[card chargeCard:printOrder.cost currencyCode:printOrder.currencyCode description:@"A Kite order!" completionHandler:^(NSString *proofOfPayment, NSError *error) {
  // if no error occured set the OLPrintOrder proofOfPayment to the one provided and submit the order
  order.proofOfPayment = proofOfPayment;
  [self.printOrder submitForPrintingWithProgressHandler:nil
                   completionHandler:^(NSString *orderIdReceipt, NSError *error) {
    // If there is no error then you can display a success outcome to the user
  }];
}];

```

```java
// See https://github.com/OceanLabs/Android-Print-SDK#custom-checkout for full step by step instructions

import ly.kite.address.Address;
import ly.kite.payment.PayPalCard;
import ly.kite.print.Asset;
import ly.kite.print.PrintJob;
import ly.kite.print.PrintOrder;

ArrayList<Asset> assets = new ArrayList<Asset>();
assets.add(new Asset(R.drawable.photo));

PrintJob iPhone6Case = PrintJob.createPrintJob(assets, "i6_case");
PrintJob poster = PrintJob.createPrintJob(assets, "a1_poster");

PrintOrder order = new PrintOrder();
order.addPrintJob(iPhone6Case);
order.addPrintJob(poster);

Address a = new Address();
a.setRecipientName("Deon Botha");
a.setLine1("Eastcastle House");
a.setLine2("27-28 Eastcastle Street");
a.setCity("London");
a.setStateOrCounty("London");
a.setZipOrPostalCode("W1W 8DH");
a.setCountry(Country.getInstance("GBR"));

order.setShippingAddress(a);

PayPalCard card = new PayPalCard();
card.setNumber("4121212121212127");
card.setExpireMonth(12);
card.setExpireYear(2012);
card.setCvv2("123");

card.chargeCard(PayPalCard.Environment.SANDBOX, printOrder.getCost(), PayPalCard.Currency.GBP, "A Kite order!", new PayPalCardChargeListener() {
    @Override
    public void onChargeSuccess(PayPalCard card, String proofOfPayment) {
        // set the PrintOrder proofOfPayment to the one provided and submit the order
    }

    @Override
    public void onError(PayPalCard card, Exception ex) {
        // handle gracefully
        order.setProofOfPayment(proofOfPayment);
        printOrder.submitForPrinting(getApplicationContext(), /*PrintOrderSubmissionListener:*/this);
    }
});

```

> Replace `<your_secret_key>` with the one found in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard.<br /><br />

> Example Response

```shell
{
  "print_order_id": "PS96-996634811"
}
```

```objective_c
// See above submitForPrintingWithProgressHandler:completionHandler:
```

```java
// PrintOrderSubmissionListener implementation

@Override
public void onSubmissionComplete(PrintOrder printOrder, String orderIdReceipt) {
  // Print order was successfully submitted to the system, display success to the user
}

@Override
public void onError(PrintOrder printOrder, Exception error) {
  // Handle error gracefully
}
```


With a single API request to Kite you can have personalised products created, packaged and shipped anywhere in the world. Packaging will carry your branding, not ours – your customers never need to know we were involved! 

For example the request on the right would result in an iPhone 6 Case and an A1 Poster being created and shipped to the specified address.

Product identifiers and product specific request arguments (if any) are documented in dedicated sections following this one.

### HTTP Request

`POST https://api.kite.ly/v2.0/print/`

### Arguments

          | |
--------- | -----------
proof_of_payment<span class="optional-argument">optional, either **proof_of_payment** or a secret key in [Authorization header](#authentication) is required</span> | The proof of payment is a either a PayPal REST payment id for a payment/transaction made to the Kite PayPal account or a Stripe token created using Kite’s Stripe publishable key. This field is optional if you opted for [taking payment yourself](#you-take-payment)
shipping_address<span class="required-argument">required</span> | An [address object](#the-address-object) indicating the address to which the order will be delivered
customer_email<span class="optional-argument">optional</span> | The customer's email address. Automated order status update emails (you can brand these) can optionally be sent to this address i.e. order confirmation email, order dispatched email, etc. You can configure these in the Kite dashboard
customer_phone<span class="required-argument">required</span> | The customer's phone number. Certain postage companies require this to be provided e.g. FedEx
user_data<span class="optional-argument">optional</span> | A dictionary containing any application or user specific meta data that you might want associated with the order
customer_payment<span class="optional-argument">optional</span> | A dictionary containing the amount paid by the customer. In instances where Kite does not take payment (i.e you are using your secret key in the [Authorization header](#authentication) to validate orders), this field is required to give an accurate representation on the profit made on the sale within the [orders](https://www.kite.ly/settings/credentials) section of the Kite dashboard.
jobs<span class="required-argument">required</span> | A list of one or more [job objects](#the-job-object) to be created and delivered to `shipping_address`

### Returns

Returns a dictionary containing the order id

## Ordering print products

> Example Order Request

```shell
curl "https://api.kite.ly/v2.0/print/" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>" \
  --data '{
    "shipping_address": {
      "recipient_name": "Deon Botha",
      "address_line_1": "Eastcastle House",
      "address_line_2": "27-28 Eastcastle Street",
      "city": "London",
      "county_state": "Greater London",
      "postcode": "W1W 8DH",
      "country_code": "GBR"
    },
    "customer_email": "[[user_email]]",
    "customer_phone": "+44 (0)784297 1234",
    "jobs": [{
      "assets": [
        "http://psps.s3.amazonaws.com/sdk_static/1.jpg",
        "http://psps.s3.amazonaws.com/sdk_static/2.jpg",
        "http://psps.s3.amazonaws.com/sdk_static/3.jpg",
        "http://psps.s3.amazonaws.com/sdk_static/4.jpg"
      ],
      "template_id": "squares"
    }]
  }'
```

```objective_c
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
#import <Kite-Print-SDK/OLKitePrintSDK.h>

NSArray *assets = @[
    [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/1.jpg"]],
    [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/2.jpg"]],
    [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/3.jpg"]],
    [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/4.jpg"]]
];

id<OLPrintJob> squarePrints = [OLPrintJob printJobWithTemplateId:@"squares" OLAssets:assets];

OLPrintOrder *order = [[OLPrintOrder alloc] init];
[order addPrintJob:squarePrints];

OLAddress *a    = [[OLAddress alloc] init];
a.recipientName = @"Deon Botha";
a.line1         = @"27-28 Eastcastle House";
a.line2         = @"Eastcastle Street";
a.city          = @"London";
a.stateOrCounty = @"Greater London";
a.zipOrPostcode = @"W1W 8DH";
a.country       = [OLCountry countryForCode:@"GBR"];

order.shippingAddress = a;

OLPayPalCard *card = [[OLPayPalCard alloc] init];
card.type = kOLPayPalCardTypeVisa;
card.number = @"4121212121212127";
card.expireMonth = 12;
card.expireYear = 2020;
card.cvv2 = @"123";

[card chargeCard:printOrder.cost currencyCode:printOrder.currencyCode description:@"A Kite order!" completionHandler:^(NSString *proofOfPayment, NSError *error) {
  // if no error occured set the OLPrintOrder proofOfPayment to the one provided and submit the order
  order.proofOfPayment = proofOfPayment;
  [self.printOrder submitForPrintingWithProgressHandler:nil
                   completionHandler:^(NSString *orderIdReceipt, NSError *error) {
    // If there is no error then you can display a success outcome to the user
  }];
}];

```

```java
// See https://github.com/OceanLabs/Android-Print-SDK#custom-checkout for full step by step instructions

import ly.kite.address.Address;
import ly.kite.payment.PayPalCard;
import ly.kite.print.Asset;
import ly.kite.print.PrintJob;
import ly.kite.print.PrintOrder;

ArrayList<Asset> assets = new ArrayList<Asset>();
assets.add(new Asset(new URL("http://psps.s3.amazonaws.com/sdk_static/1.jpg"))));
assets.add(new Asset(new URL("http://psps.s3.amazonaws.com/sdk_static/2.jpg"))));
assets.add(new Asset(new URL("http://psps.s3.amazonaws.com/sdk_static/3.jpg"))));
assets.add(new Asset(new URL("http://psps.s3.amazonaws.com/sdk_static/4.jpg"))));

PrintJob squarePrints = PrintJob.createPrintJob(assets, "squares");

PrintOrder order = new PrintOrder();
order.addPrintJob(squarePrints);

Address a = new Address();
a.setRecipientName("Deon Botha");
a.setLine1("Eastcastle House");
a.setLine2("27-28 Eastcastle Street");
a.setCity("London");
a.setStateOrCounty("London");
a.setZipOrPostalCode("W1W 8DH");
a.setCountry(Country.getInstance("GBR"));

order.setShippingAddress(a);

PayPalCard card = new PayPalCard();
card.setNumber("4121212121212127");
card.setExpireMonth(12);
card.setExpireYear(2012);
card.setCvv2("123");

card.chargeCard(PayPalCard.Environment.SANDBOX, printOrder.getCost(), PayPalCard.Currency.GBP, "A Kite order!", new PayPalCardChargeListener() {
    @Override
    public void onChargeSuccess(PayPalCard card, String proofOfPayment) {
        // set the PrintOrder proofOfPayment to the one provided and submit the order
    }

    @Override
    public void onError(PayPalCard card, Exception ex) {
        // handle gracefully
        order.setProofOfPayment(proofOfPayment);
        printOrder.submitForPrinting(getApplicationContext(), /*PrintOrderSubmissionListener:*/this);
    }
});

```

> Replace `<your_secret_key>` with the one found in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard.<br /><br />

> Example Response

```shell
{
  "print_order_id": "PS96-996634811"
}
```

If you haven't already, see [Placing orders](#placing-orders) for a general overview of the order request & response which is applicable to all product orders. 

The example request on the right would result in a square prints being created and shipped to the specified address.

### print products & template_ids
          | |
--------- | -----------
Magnets<span class="attribute-type">magnets</span> | Our magnets are printed on a unique MagneCote substrate, providing photo quality imagery with a thin magnetic backing
Square Prints<span class="attribute-type">squares</span> | Amazing quality square prints printed on 350 GSM card completed with a matte finish
Mini Square Prints<span class="attribute-type">squares_mini</span> | Like our Square Prints, just smaller! Amazing quality printed on 350 GSM card completed with a matte finish
Retro Prints<span class="attribute-type">polaroids</span> | Polaroid style prints printed on 350 GSM card completed with a matte finish
Mini Retro Prints<span class="attribute-type">polaroids_mini</span> | Like our Retro Prints, just smaller! Mini Polaroid style prints printed on 350 GSM card completed with a matte finish
Classic Photo Prints<span class="attribute-type">photos_4x6</span> | Our classic photo 6x4 prints printed on 350 GSM card completed with a matte finish
Square Stickers<span class="attribute-type">stickers_square</span> | Fun personalised square stickers. Just peel them off and stick them on
Circle Stickers<span class="attribute-type">stickers_circle</span> | Fun personalised circle stickers. Just peel them off and stick them on
Greetings Cards<span class="attribute-type">greeting_cards</span> | Our greetings cards are printed on thick premium card stock and once folded, form a 14.8 cm square
Frames<span class="attribute-type">frames_50cm frames_50cm_2x2 frames_50cm_3x3 frames_50cm_4x4</span> | The perfect way to show off your most loved photos. They come in various configurations allowing between one and sixteen images to printed and enclosed within a wooden frame (Available UK only).
A1 Poster<span class="attribute-type">a1_poster<br />a1_poster_35<br />a1_poster_54<br />a1_poster_70</span> | Our large format poster prints are printed on 190 GSM sheets with a satin finish. Various templates are available from single images to photo collages. They are delivered worldwide in sturdy cardboard tubes
A2 Poster<span class="attribute-type">a2_poster<br />a2_poster_24<br />a2_poster_35<br />a2_poster_54</span> | Our large format poster prints are printed on 190 GSM sheets with a satin finish. Various templates are available from single images to photo collages. They are delivered worldwide in sturdy cardboard tubes
A3 Poster<span class="attribute-type">a3_poster</span> | Our large format poster prints are printed on 190 GSM sheets with a satin finish. They are delivered worldwide in sturdy cardboard tubes

## Ordering phone cases

> Example Order Request

```shell
curl "https://api.kite.ly/v2.0/print/" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>" \
  --data '{
    "shipping_address": {
      "recipient_name": "Deon Botha",
      "address_line_1": "Eastcastle House",
      "address_line_2": "27-28 Eastcastle Street",
      "city": "London",
      "county_state": "Greater London",
      "postcode": "W1W 8DH",
      "country_code": "GBR"
    },
    "customer_email": "[[user_email]]",
    "customer_phone": "+44 (0)784297 1234",
    "jobs": [{
      "assets": ["http://psps.s3.amazonaws.com/sdk_static/1.jpg"],
      "template_id": "ipad_air_case"
    }, {
      "options": {
      	"case_style": "matte"
      },
      "assets": ["http://psps.s3.amazonaws.com/sdk_static/2.jpg"],
      "template_id": "samsung_s5_case"      
    }]
  }'
```

```objective_c
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
#import <Kite-Print-SDK/OLKitePrintSDK.h>

NSArray *assets = @[
    [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/1.jpg"]]
];

id<OLPrintJob> ipadAirCase = [OLPrintJob printJobWithTemplateId:@"ipad_air_case" OLAssets:assets];
id<OLPrintJob> galaxyS5Case = [OLPrintJob printJobWithTemplateId:@"samsung_s5_case" OLAssets:assets];
[galaxyS5Case setValue:@"matte" forOption:@"case_style"];

OLPrintOrder *order = [[OLPrintOrder alloc] init];
[order addPrintJob:ipadAirCase];
[order addPrintJob:galaxyS5Case];

OLAddress *a    = [[OLAddress alloc] init];
a.recipientName = @"Deon Botha";
a.line1         = @"27-28 Eastcastle House";
a.line2         = @"Eastcastle Street";
a.city          = @"London";
a.stateOrCounty = @"Greater London";
a.zipOrPostcode = @"W1W 8DH";
a.country       = [OLCountry countryForCode:@"GBR"];

order.shippingAddress = a;

OLPayPalCard *card = [[OLPayPalCard alloc] init];
card.type = kOLPayPalCardTypeVisa;
card.number = @"4121212121212127";
card.expireMonth = 12;
card.expireYear = 2020;
card.cvv2 = @"123";

[card chargeCard:printOrder.cost currencyCode:printOrder.currencyCode description:@"A Kite order!" completionHandler:^(NSString *proofOfPayment, NSError *error) {
  // if no error occured set the OLPrintOrder proofOfPayment to the one provided and submit the order
  order.proofOfPayment = proofOfPayment;
  [self.printOrder submitForPrintingWithProgressHandler:nil
                   completionHandler:^(NSString *orderIdReceipt, NSError *error) {
    // If there is no error then you can display a success outcome to the user
  }];
}];

```

```java
// See https://github.com/OceanLabs/Android-Print-SDK#custom-checkout for full step by step instructions

import ly.kite.address.Address;
import ly.kite.payment.PayPalCard;
import ly.kite.print.Asset;
import ly.kite.print.PrintJob;
import ly.kite.print.PrintOrder;

ArrayList<Asset> assets = new ArrayList<Asset>();
assets.add(new Asset(new URL("http://psps.s3.amazonaws.com/sdk_static/1.jpg"))));

PrintJob ipadAirCase = PrintJob.createPrintJob(assets, "ipad_air_case");
PrintJob galaxyS5Case = PrintJob.createPrintJob(assets, "samsung_s5_case");
galaxyS5Case.setOption("case_style", "matte");

PrintOrder order = new PrintOrder();
order.addPrintJob(ipadAirCase);
order.addPrintJob(galaxyS5Case);

Address a = new Address();
a.setRecipientName("Deon Botha");
a.setLine1("Eastcastle House");
a.setLine2("27-28 Eastcastle Street");
a.setCity("London");
a.setStateOrCounty("London");
a.setZipOrPostalCode("W1W 8DH");
a.setCountry(Country.getInstance("GBR"));

order.setShippingAddress(a);

PayPalCard card = new PayPalCard();
card.setNumber("4121212121212127");
card.setExpireMonth(12);
card.setExpireYear(2012);
card.setCvv2("123");

card.chargeCard(PayPalCard.Environment.SANDBOX, printOrder.getCost(), PayPalCard.Currency.GBP, "A Kite order!", new PayPalCardChargeListener() {
    @Override
    public void onChargeSuccess(PayPalCard card, String proofOfPayment) {
        // set the PrintOrder proofOfPayment to the one provided and submit the order
    }

    @Override
    public void onError(PayPalCard card, Exception ex) {
        // handle gracefully
        order.setProofOfPayment(proofOfPayment);
        printOrder.submitForPrinting(getApplicationContext(), /*PrintOrderSubmissionListener:*/this);
    }
});

```

> Replace `<your_secret_key>` with the one found in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard.<br /><br />

> Example Response

```shell
{
  "print_order_id": "PS96-996634811"
}
```

If you haven't already, see [Placing orders](#placing-orders) for a general overview of the order request & response which is applicable to all product orders. 

The example request on the right would result in iPad Air & Samsung Galaxy 5 cases being created and shipped to the specified address.

### cases & template_ids

          | |
--------- | -----------
iPhone 6s+ Case<span class="attribute-type">i6splus_case</span> | iPhone 6s snap case constructed to the highest quality design, material & coating
iPhone 6s+ Tough Case<span class="attribute-type">i6splus_tough_case</span> | iPhone 6s + tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 6+ Case<span class="attribute-type">i6plus_case</span> | iPhone 6+ snap case constructed to the highest quality design, material & coating
iPhone 6+ Tough Case<span class="attribute-type">i6plus_tough_case</span> | iPhone 6+ tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 6s Case<span class="attribute-type">i6s_case</span> | iPhone 6s snap case constructed to the highest quality design, material & coating
iPhone 6s Tough Case<span class="attribute-type">i6s_tough_case</span> | iPhone 6s tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 6 Case<span class="attribute-type">i6_case</span> | iPhone 6 snap case constructed to the highest quality design, material & coating
iPhone 6 Tough Case<span class="attribute-type">i6_tough_case</span> | iPhone 6 tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 5/5S Case<span class="attribute-type">i5_case</span> | iPhone 5 snap case constructed to the highest quality design, material & coating
iPhone 5/5S Tough Case<span class="attribute-type">i5_tough_case</span> | iPhone 5 tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 5C Case<span class="attribute-type">i5c_case</span> | iPhone 5c snap case constructed to the highest quality design, material & coating
iPhone 5C Tough Case<span class="attribute-type">i5c_tough_case</span> | iPhone 5c tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 4/4S Case<span class="attribute-type">i4_case</span> | iPhone 4 snap case constructed to the highest quality design, material & coating
iPhone 4/4S Tough Case<span class="attribute-type">i4_tough_case</span> | iPhone 4 tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPad Mini Case<span class="attribute-type">ipad_mini_case</span> | iPad Mini snap case constructed to the highest quality design, material & coating
iPad Air Case<span class="attribute-type">ipad_air_case</span> | iPad Air snap case constructed to the highest quality design, material & coating
iPad 2,3,4 Case<span class="attribute-type">ipad_case</span> | iPad 2,3,4 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S6 Edge Case<span class="attribute-type">samsung_s6e_case</span> | Samsung Galaxy S6 Edge snap case constructed to the highest quality design, material & coating
Samsung Galaxy S6 Case<span class="attribute-type">samsung_s6_case</span> | Samsung Galaxy S6 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S5 Case<span class="attribute-type">samsung_s5_case</span> | Samsung Galaxy S5 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S5 Mini Case<span class="attribute-type">samsung_s5_mini_case</span> | Samsung Galaxy S5 Mini snap case constructed to the highest quality design, material & coating
Samsung Galaxy S4 Case<span class="attribute-type">samsung_s4_case</span> | Samsung Galaxy S4 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S4 Mini Case<span class="attribute-type">samsung_s4_mini_case</span> | Samsung Galaxy S4 Mini snap case constructed to the highest quality design, material & coating
Samsung Galaxy S3 Case<span class="attribute-type">samsung_s3_case</span> | Samsung Galaxy S3 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S3 Mini Case<span class="attribute-type">samsung_s3_mini_case</span> | Samsung Galaxy S3 Mini snap case constructed to the highest quality design, material & coating
Samsung Galaxy Note 4 Case<span class="attribute-type">samsung_n4_case</span> | Samsung Galaxy Note 3 snap case constructed to the highest quality design, material & coating
Samsung Galaxy Note 3 Case<span class="attribute-type">samsung_n3_case</span> | Samsung Galaxy Note 3 snap case constructed to the highest quality design, material & coating
Sony Xperia Z1 Case<span class="attribute-type">sony_x_z1_case</span> | Sony Xperia Z1 snap case constructed to the highest quality design, material & coating
Sony Xperia C Case<span class="attribute-type">sony_x_c_case</span> | Sony Xperia Z1 snap case constructed to the highest quality design, material & coating
LG G2 Case<span class="attribute-type">lg_g2_case</span> | LG G2 snap case constructed to the highest quality design, material & coating
Nexus 5 Case<span class="attribute-type">nexus_5_case</span> | Nexus 5 snap case constructed to the highest quality design, material & coating
Nexus 7 Case<span class="attribute-type">nexus_7_case</span> | Nexus 7 snap case constructed to the highest quality design, material & coating

### Options Arguments

          | |
--------- | -----------
case_style<span class="optional-argument">optional</span> | Either `matte` or `gloss`. Defaults to `gloss` if not present. `matte` style only valid for `i4_case`, `i5_case`, `i5c_case`, `i6_case`, `i6plus_case`, `samsung_s4_case`, `samsung_s5_case` and `samsung_s5_mini_case`.

## Ordering apparel

> Example Order Request

```shell
curl "https://api.kite.ly/v2.0/print/" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>" \
  --data '{
    "shipping_address": {
      "recipient_name": "Deon Botha",
      "address_line_1": "Eastcastle House",
      "address_line_2": "27-28 Eastcastle Street",
      "city": "London",
      "county_state": "Greater London",
      "postcode": "W1W 8DH",
      "country_code": "GBR"
    },
    "customer_email": "[[user_email]]",
    "customer_phone": "+44 (0)784297 1234",
    "jobs": [{
      "options": {
        "garment_size": "M",
        "garment_color": "white"
      },
      "assets": {
        "center_chest": "http://psps.s3.amazonaws.com/sdk_static/1.jpg",
      },
      "template_id": "aa_mens_tshirt"
    }]
  }'
```

```objective_c
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
#import <Kite-Print-SDK/OLKitePrintSDK.h>

NSArray *assets = @{
    @"center_chest": [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/1.jpg"]]
};

id<OLPrintJob> tshirt = [OLPrintJob printJobWithTemplateId:@"aa_mens_tshirt" OLAssets:assets];
[tshirt setValue:@"M" forOption:@"garment_size"];
[tshirt setValue:@"white" forOption:@"garment_color"];

OLPrintOrder *order = [[OLPrintOrder alloc] init];
[order addPrintJob:tshirt];

OLAddress *a    = [[OLAddress alloc] init];
a.recipientName = @"Deon Botha";
a.line1         = @"27-28 Eastcastle House";
a.line2         = @"Eastcastle Street";
a.city          = @"London";
a.stateOrCounty = @"Greater London";
a.zipOrPostcode = @"W1W 8DH";
a.country       = [OLCountry countryForCode:@"GBR"];

order.shippingAddress = a;

OLPayPalCard *card = [[OLPayPalCard alloc] init];
card.type = kOLPayPalCardTypeVisa;
card.number = @"4121212121212127";
card.expireMonth = 12;
card.expireYear = 2020;
card.cvv2 = @"123";

[card chargeCard:printOrder.cost currencyCode:printOrder.currencyCode description:@"A Kite order!" completionHandler:^(NSString *proofOfPayment, NSError *error) {
  // if no error occured set the OLPrintOrder proofOfPayment to the one provided and submit the order
  order.proofOfPayment = proofOfPayment;
  [self.printOrder submitForPrintingWithProgressHandler:nil
                   completionHandler:^(NSString *orderIdReceipt, NSError *error) {
    // If there is no error then you can display a success outcome to the user
  }];
}];

```

```java
// See https://github.com/OceanLabs/Android-Print-SDK#custom-checkout for full step by step instructions

import ly.kite.address.Address;
import ly.kite.payment.PayPalCard;
import ly.kite.print.Asset;
import ly.kite.print.PrintJob;
import ly.kite.print.PrintOrder;

Map<String, Asset> assets = new HashMap<String, Asset>();
assets.put("center_chest", new Asset(new URL("http://psps.s3.amazonaws.com/sdk_static/1.jpg"))));

PrintJob tshirt = PrintJob.createPrintJob(assets, "aa_mens_tshirt");
tshirt.setOption("garment_size", "M");
tshirt.setOption("garment_color", "white");

PrintOrder order = new PrintOrder();
order.addPrintJob(tshirt);

Address a = new Address();
a.setRecipientName("Deon Botha");
a.setLine1("Eastcastle House");
a.setLine2("27-28 Eastcastle Street");
a.setCity("London");
a.setStateOrCounty("London");
a.setZipOrPostalCode("W1W 8DH");
a.setCountry(Country.getInstance("GBR"));

order.setShippingAddress(a);

PayPalCard card = new PayPalCard();
card.setNumber("4121212121212127");
card.setExpireMonth(12);
card.setExpireYear(2012);
card.setCvv2("123");

card.chargeCard(PayPalCard.Environment.SANDBOX, printOrder.getCost(), PayPalCard.Currency.GBP, "A Kite order!", new PayPalCardChargeListener() {
    @Override
    public void onChargeSuccess(PayPalCard card, String proofOfPayment) {
        // set the PrintOrder proofOfPayment to the one provided and submit the order
    }

    @Override
    public void onError(PayPalCard card, Exception ex) {
        // handle gracefully
        order.setProofOfPayment(proofOfPayment);
        printOrder.submitForPrinting(getApplicationContext(), /*PrintOrderSubmissionListener:*/this);
    }
});

```

> Replace `<your_secret_key>` with the one found in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard.<br /><br />

> Example Response

```shell
{
  "print_order_id": "PS96-996634811"
}
```


If you haven't already, see [Placing orders](#placing-orders) for a general overview of the order request & response which is applicable to all product orders. 

The example request on the right would result in a t-shirt being created (with an photo on the front) and shipped to the specified address.

Many more products and brands available in the very near future.

### products & template_ids

          | |
--------- | -----------
T-Shirt<span class="attribute-type">aa_mens_tshirt</span> | The softest, smoothest, best-looking short sleeve tee shirt available anywhere! Fine Jersey (100% Cotton) construction (Heather Grey contains 10% Polyester) • Durable rib neckband
Hoodie<span class="attribute-type">aa_zip_hoodie</span> | Our hoodie offering from [Apparel](http://store.americanapparel.net/). A fitted, sporty unisex hoody in a unique Flex Fleece 50/50 cotton/poly blend, featuring a zipper closure

### Options Arguments

          | |
--------- | -----------
garment_size<span class="required-argument">required</span> | The size of garment you want created. Must be one of the following: `S`, `M`, `L`, `XL`, `XXL` corresponding to small, medium, large, extra large & extra extra large respectively
garment_color<span class="required-argument">required</span> | The base material/fabric colour of the garment you want created. See the [American Apparel color swatch](http://www.americanapparel.net/wholesaleresources/colors.asp) to review fabric colours. Must be one of the following:  `white`, `black`, `navy`, `heather grey`, `light blue`, `maroon`, `sports grey`, `dark heather`

### Assets Position Arguments
<table class="apparel-positions">
	<thead>
		<tr>
			<th>Position</th>
			<th></th>
			<th>Applicable Products</th>
			<th>Max Width</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>center_chest<span class="optional-argument">optional</span></td>
			<td class="img-tshirt"><img alt="T-Shirt Print API Centre Chest" src="{% static "docs/images/centre_chest.jpg" %}"></td>
			<td><code class="prettyprint">aa_mens_tshirt</code>, <code class="prettyprint">aa_zip_hoodie</code></td>
			<td>30cm</td>
		</tr>
		<tr>
			<td>center_back<span class="optional-argument">optional</span></td>
			<td class="img-tshirt"><img alt="T-Shirt Print API Centre Back" src="{% static "docs/images/centre_back.jpg" %}"></td>
			<td><code class="prettyprint">aa_mens_tshirt</code>, <code class="prettyprint">aa_zip_hoodie</code></td>
			<td>30cm</td>
		</tr>
		<tr>
			<td>top_chest<span class="optional-argument">optional</span></td>
			<td class="img-tshirt"><img alt="T-Shirt Print API Top Chest" src="{% static "docs/images/top_chest.jpg" %}"></td>
			<td><code class="prettyprint">aa_mens_tshirt</code>, <code class="prettyprint">aa_zip_hoodie</code></td>
			<td>30cm</td>
		</tr>
		<tr>
			<td>right_chest<span class="optional-argument">optional</span></td>
			<td class="img-tshirt"><img alt="T-Shirt Print API Right Chest" src="{% static "docs/images/right_chest.jpg" %}"></td>
			<td><code class="prettyprint">aa_mens_tshirt</code>, <code class="prettyprint">aa_zip_hoodie</code></td>
			<td>12cm</td>
		</tr>
		<tr>
			<td>left_chest<span class="optional-argument">optional</span></td>
			<td class="img-tshirt"><img alt="T-Shirt Print API Left Chest" src="{% static "docs/images/left_chest.jpg" %}"></td>
			<td><code class="prettyprint">aa_mens_tshirt</code>, <code class="prettyprint">aa_zip_hoodie</code></td>
			<td>12cm</td>
		</tr>
	</tbody>
</table>



## Ordering photobooks

> Example Order Request

```shell
curl "https://api.kite.ly/v2.0/print/" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>" \
  --data '{
    "shipping_address": {
      "recipient_name": "Deon Botha",
      "address_line_1": "Eastcastle House",
      "address_line_2": "27-28 Eastcastle Street",
      "city": "London",
      "county_state": "Greater London",
      "postcode": "W1W 8DH",
      "country_code": "GBR"
    },
    "customer_email": "[[user_email]]",
    "customer_phone": "+44 (0)784297 1234",
    "jobs": [
      "pdf": "https://s3.amazonaws.com/sdk-static/portrait_photobook.pdf",
      "template_id": "rpi_wrap_280x210_sm"
    }]
  }'
```

```objective_c
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
#import <Kite-Print-SDK/OLKitePrintSDK.h>

NSArray *assets = @[
    [OLAsset assetWithURL:[NSURL URLWithString:@"https://s3.amazonaws.com/sdk-static/portrait_photobook.pdf"]]
];

id<OLPrintJob> photobook = [OLPrintJob printJobWithTemplateId:@"rpi_wrap_280x210_sm" OLAssets:assets];

OLPrintOrder *order = [[OLPrintOrder alloc] init];
[order addPrintJob:photobook];

OLAddress *a    = [[OLAddress alloc] init];
a.recipientName = @"Deon Botha";
a.line1         = @"27-28 Eastcastle House";
a.line2         = @"Eastcastle Street";
a.city          = @"London";
a.stateOrCounty = @"Greater London";
a.zipOrPostcode = @"W1W 8DH";
a.country       = [OLCountry countryForCode:@"GBR"];

order.shippingAddress = a;

OLPayPalCard *card = [[OLPayPalCard alloc] init];
card.type = kOLPayPalCardTypeVisa;
card.number = @"4121212121212127";
card.expireMonth = 12;
card.expireYear = 2020;
card.cvv2 = @"123";

[card chargeCard:printOrder.cost currencyCode:printOrder.currencyCode description:@"A Kite order!" completionHandler:^(NSString *proofOfPayment, NSError *error) {
  // if no error occured set the OLPrintOrder proofOfPayment to the one provided and submit the order
  order.proofOfPayment = proofOfPayment;
  [self.printOrder submitForPrintingWithProgressHandler:nil
                   completionHandler:^(NSString *orderIdReceipt, NSError *error) {
    // If there is no error then you can display a success outcome to the user
  }];
}];

```

```java
// See https://github.com/OceanLabs/Android-Print-SDK#custom-checkout for full step by step instructions

import ly.kite.address.Address;
import ly.kite.payment.PayPalCard;
import ly.kite.print.Asset;
import ly.kite.print.PrintJob;
import ly.kite.print.PrintOrder;

ArrayList<Asset> assets = new ArrayList<Asset>();
assets.add(new Asset(new URL("https://s3.amazonaws.com/sdk-static/portrait_photobook.pdf"))));

PrintJob photobook = PrintJob.createPrintJob(assets, "rpi_wrap_280x210_sm");

PrintOrder order = new PrintOrder();
order.addPrintJob(ipadAirCase);
order.addPrintJob(galaxyS5Case);

Address a = new Address();
a.setRecipientName("Deon Botha");
a.setLine1("Eastcastle House");
a.setLine2("27-28 Eastcastle Street");
a.setCity("London");
a.setStateOrCounty("London");
a.setZipOrPostalCode("W1W 8DH");
a.setCountry(Country.getInstance("GBR"));

order.setShippingAddress(a);

PayPalCard card = new PayPalCard();
card.setNumber("4121212121212127");
card.setExpireMonth(12);
card.setExpireYear(2012);
card.setCvv2("123");

card.chargeCard(PayPalCard.Environment.SANDBOX, printOrder.getCost(), PayPalCard.Currency.GBP, "A Kite order!", new PayPalCardChargeListener() {
    @Override
    public void onChargeSuccess(PayPalCard card, String proofOfPayment) {
        // set the PrintOrder proofOfPayment to the one provided and submit the order
    }

    @Override
    public void onError(PayPalCard card, Exception ex) {
        // handle gracefully
        order.setProofOfPayment(proofOfPayment);
        printOrder.submitForPrinting(getApplicationContext(), /*PrintOrderSubmissionListener:*/this);
    }
});

```

> Replace `<your_secret_key>` with the one found in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard.<br /><br />

> Example Response

```shell
{
  "print_order_id": "PS96-996634811"
}
```


If you haven't already, see [Placing orders](#placing-orders) for a general overview of the order request & response which is applicable to all product orders. 

The example request on the right would result in a hardcover landscape photobook being created and shipped to the specified address.

### products & template_ids

          | |
--------- | -----------
Landscape Hardcover<span class="attribute-type">rpi_wrap_280x210_sm</span> | 28cm x 21cm hardcover landscape photobook. Our books are perfectly bound with images printed on glossy 200gsm paper
Portrait Hardcover<span class="attribute-type">rpi_wrap_210x280_sm</span> | 21cm x 28cm hardcover portrait photobook. Our books are perfectly bound with images printed on glossy 200gsm paper
Small Square Hardcover<span class="attribute-type">rpi_wrap_140x140_sm</span> | 14cm x 14cm hardcover square photobook. Our books are perfectly bound with images printed on glossy 200gsm paper
Medium Square Hardcover<span class="attribute-type">rpi_wrap_210x210_sm</span> | 21cm x 21cm hardcover square photobook. Our books are perfectly bound with images printed on glossy 200gsm paper
Large Square Hardcover<span class="attribute-type">rpi_wrap_300x300_sm</span> | 30cm x 30cm hardcover square photobook. Our books are perfectly bound with images printed on glossy 200gsm paper

### Job Arguments

          | |
--------- | -----------
pdf<span class="required-argument">required</span> | A PDF URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. The PDF itself should contain 24 pages. Each PDF page must have dimensions matching those specified by the chosen photobook template. The first and last pages of the PDF form the front and back covers for the photobook respectively.


## Ordering postcards

> Example Order Request

```shell
curl "https://api.kite.ly/v2.0/print/" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>" \
  --data '{
    "shipping_address": {
      "recipient_name": "Deon Botha",
      "address_line_1": "Eastcastle House",
      "address_line_2": "27-28 Eastcastle Street",
      "city": "London",
      "county_state": "Greater London",
      "postcode": "W1W 8DH",
      "country_code": "GBR"
    },
    "customer_email": "[[user_email]]",
    "customer_phone": "+44 (0)784297 1234",
    "jobs": [{
      "assets": {
        "front_image": "http://psps.s3.amazonaws.com/sdk_static/4.jpg"
      },
      "template_id": "postcard", 
      "message": "Hello World!"
    }]
  }'
```

```objective_c
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
#import <Kite-Print-SDK/OLKitePrintSDK.h>

OLAsset *frontImage = [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/4.jpg"]];
id<OLPrintJob> postcard = [OLPrintJob postcardWithTemplateId:@"postcard" frontImageOLAsset:frontImage message:@"Hello World!" address:/*Address*/];

OLPrintOrder *order = [[OLPrintOrder alloc] init];
[order addPrintJob:postcard];

OLPayPalCard *card = [[OLPayPalCard alloc] init];
card.type = kOLPayPalCardTypeVisa;
card.number = @"4121212121212127";
card.expireMonth = 12;
card.expireYear = 2020;
card.cvv2 = @"123";

[card chargeCard:printOrder.cost currencyCode:printOrder.currencyCode description:@"A Kite order!" completionHandler:^(NSString *proofOfPayment, NSError *error) {
  // if no error occured set the OLPrintOrder proofOfPayment to the one provided and submit the order
  order.proofOfPayment = proofOfPayment;
  [self.printOrder submitForPrintingWithProgressHandler:nil
                   completionHandler:^(NSString *orderIdReceipt, NSError *error) {
    // If there is no error then you can display a success outcome to the user
  }];
}];

```

```java
// See https://github.com/OceanLabs/Android-Print-SDK#custom-checkout for full step by step instructions

import ly.kite.address.Address;
import ly.kite.payment.PayPalCard;
import ly.kite.print.Asset;
import ly.kite.print.PrintJob;
import ly.kite.print.PrintOrder;

Address a = new Address();
a.setRecipientName("Deon Botha");
a.setLine1("Eastcastle House");
a.setLine2("27-28 Eastcastle Street");
a.setCity("London");
a.setStateOrCounty("London");
a.setZipOrPostalCode("W1W 8DH");
a.setCountry(Country.getInstance("GBR"));

Asset frontImage = new Asset(new URL("http://psps.s3.amazonaws.com/sdk_static/4.jpg")));
PrintJob postcard = PrintJob.createPostcardJob("postcard", frontImage, "Hello World", a);

PrintOrder order = new PrintOrder();
order.addPrintJob(postcard);

PayPalCard card = new PayPalCard();
card.setNumber("4121212121212127");
card.setExpireMonth(12);
card.setExpireYear(2012);
card.setCvv2("123");

card.chargeCard(PayPalCard.Environment.SANDBOX, printOrder.getCost(), PayPalCard.Currency.GBP, "A Kite order!", new PayPalCardChargeListener() {
    @Override
    public void onChargeSuccess(PayPalCard card, String proofOfPayment) {
        // set the PrintOrder proofOfPayment to the one provided and submit the order
    }

    @Override
    public void onError(PayPalCard card, Exception ex) {
        // handle gracefully
        order.setProofOfPayment(proofOfPayment);
        printOrder.submitForPrinting(getApplicationContext(), /*PrintOrderSubmissionListener:*/this);
    }
});

```

> Replace `<your_secret_key>` with the one found in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard.<br /><br />

> Example Response

```shell
{
  "print_order_id": "PS96-996634811"
}
```


If you haven't already, see [Placing orders](#placing-orders) for a general overview of the order request & response which is applicable to all product orders. 

The example request on the right would result in a postcard being created and shipped to the specified address.

### products & template_ids

          | |
--------- | -----------
Postcard<span class="attribute-type">postcard</span> | Our postcards are printed on high quality 350gsm card stock with a gloss finish and dispatched worldwide

### Job Arguments

          | |
--------- | -----------
message<span class="optional-argument">optional</span> | The text message that you want to appear on the back of the postcard

### Assets Arguments

          | |
--------- | -----------
front_image<span class="required-argument">required</span> | A image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. It will form the front of the postcard
back_image<span class="optional-argument">optional</span> | A image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. Specifying a `back_image` gives you near total control of the back of postcard layout. In doing so you are expected to insert the message & recipient address directly into the image according to our [guidelines](#postcard-guidelines)

## Ordering greeting cards

> Example Order Request

```shell
curl "https://api.kite.ly/v2.0/print/" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>" \
  --data '{
    "shipping_address": {
      "recipient_name": "Deon Botha",
      "address_line_1": "Eastcastle House",
      "address_line_2": "27-28 Eastcastle Street",
      "city": "London",
      "county_state": "Greater London",
      "postcode": "W1W 8DH",
      "country_code": "GBR"
    },
    "customer_email": "[[user_email]]",
    "customer_phone": "+44 (0)784297 1234",
    "jobs": [{
      "assets": {
        "front_image": "https://s3.amazonaws.com/kite-samples/greetings/front.png",
        "back_image": "https://s3.amazonaws.com/kite-samples/greetings/back.png",
        "inside_right_image": "https://s3.amazonaws.com/kite-samples/greetings/inside.png"
      },
      "template_id": "greeting_cards_a5"
    }]
  }'
```

```objective_c
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
#import <Kite-Print-SDK/OLKitePrintSDK.h>

OLAsset *frontImage = [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/1.jpg"]];
OLAsset *backImage = [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/2.jpg"]];
OLAsset *inLeftImage = [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/3.jpg"]];
OLAsset *inRightImage = [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/4.jpg"]];
id<OLPrintJob> card = [OLPrintJob greetingCardWithTemplateId:@"greeting_cards_a5" frontImageOLAsset:frontImage backImageOLAsset:backImage insideRightImageAsset:inRightImage insideLeftImageAsset:inLeftImage];

OLPrintOrder *order = [[OLPrintOrder alloc] init];
[order addPrintJob:card];

OLPayPalCard *card = [[OLPayPalCard alloc] init];
card.type = kOLPayPalCardTypeVisa;
card.number = @"4121212121212127";
card.expireMonth = 12;
card.expireYear = 2020;
card.cvv2 = @"123";

[card chargeCard:printOrder.cost currencyCode:printOrder.currencyCode description:@"A Kite order!" completionHandler:^(NSString *proofOfPayment, NSError *error) {
  // if no error occured set the OLPrintOrder proofOfPayment to the one provided and submit the order
  order.proofOfPayment = proofOfPayment;
  [self.printOrder submitForPrintingWithProgressHandler:nil
                   completionHandler:^(NSString *orderIdReceipt, NSError *error) {
    // If there is no error then you can display a success outcome to the user
  }];
}];


```

```java
// See https://github.com/OceanLabs/Android-Print-SDK#custom-checkout for full step by step instructions

```

> Replace `<your_secret_key>` with the one found in the [credentials](https://www.kite.ly/settings/credentials) section of the dashboard.<br /><br />

> Example Response

```shell
{
  "print_order_id": "PS96-996634811"
}
```


If you haven't already, see [Placing orders](#placing-orders) for a general overview of the order request & response which is applicable to all product orders.

The example request on the right would result in a greetings card being created and shipped to the specified address.

### products & template_ids

          | |
--------- | -----------
Greetings card A5 <span class="attribute-type">greeting_cards_a5</span> | Our greetings cards are 330gsm Fedrigoni one sided Symbol gloss and gloss UV varnished card. Dispatched worldwide.
Greetings card 7"x5" <span class="attribute-type">greeting_cards_7x5</span> | Our greetings cards are 330gsm Fedrigoni one sided Symbol gloss and gloss UV varnished card. Dispatched worldwide.
Greetings cards A5 (10 Pack) <span class="attribute-type">greeting_cards_a5_10pack</span> | Pack of 10 single design greetings cards printed on 330gsm Fedrigoni one sided Symbol gloss and gloss UV varnished card. Dispatched worldwide.
Greetings cards 7"x5" (10 Pack) <span class="attribute-type">greeting_cards_7x5_10pack</span> | Pack of 10 single design greetings cards printed on 330gsm Fedrigoni one sided Symbol gloss and gloss UV varnished card. Dispatched worldwide.

### Assets Arguments

          | |
--------- | -----------
front_image<span class="required-argument">required</span> | A image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. It will form the front of the greetings card
back_image<span class="optional-argument">optional</span> | A image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. Specifying a `back_image` gives you total control of the back of the greetings card.
inside_left_image<span class="optional-argument">optional</span> | A image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. Specifying an `inside_left_image` gives you total control of the inside of the greetings card.
inside_right_image<span class="optional-argument">optional</span> | A image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. Specifying a `inside_right_image` gives you total control of the inside of the greetings card.

## Dimension Reference

The tables below detail the optimal asset pixel dimensions for products in our range. Whilst assets you provide to Kite can be
smaller than this, it's recommended you try get as close to these dimensions as possible to guarantee high quality prints.


### OPTIMAL PRINT PRODUCT ASSET DIMENSIONS
<table class="apparel-positions"><thead><tr><th>product</th><th>pixels</th><th>cm</th><th>inches</th></tr></thead><tbody>
<tr><td>A1 Poster<span class="optional-argument">a1_poster</span></td><td><code class="prettyprint">7017&times;9933</code></td><td><code class="prettyprint">59.4&times;84.1</code></td><td><code class="prettyprint">23.4&times;33.1</code></td></tr>
<tr><td>A2 Poster<span class="optional-argument">a2_poster</span></td><td><code class="prettyprint">4962&times;7017</code></td><td><code class="prettyprint">42&times;59.4</code></td><td><code class="prettyprint">16.5&times;23.4</code></td></tr>
<tr><td>A3 Poster<span class="optional-argument">a3_poster</span></td><td><code class="prettyprint">3508&times;4961</code></td><td><code class="prettyprint">29.7&times;42</code></td><td><code class="prettyprint">11.7&times;16.5</code></td></tr>
<tr><td>A4 Poster<span class="optional-argument">a4_poster</span></td><td><code class="prettyprint">2481&times;3507</code></td><td><code class="prettyprint">21&times;29.7</code></td><td><code class="prettyprint">8.3&times;11.7</code></td></tr>
<tr><td>Classic prints (4x6)<span class="optional-argument">photos_4x6</span></td><td><code class="prettyprint">1760&times;1276</code></td><td><code class="prettyprint">14.9&times;10.8</code></td><td><code class="prettyprint">5.9&times;4.3</code></td></tr>
<tr><td>Magnets<span class="optional-argument">magnets</span></td><td><code class="prettyprint">815&times;815</code></td><td><code class="prettyprint">6.9&times;6.9</code></td><td><code class="prettyprint">2.7&times;2.7</code></td></tr>
<tr><td>Squares<span class="optional-argument">squares</span></td><td><code class="prettyprint">1152&times;1152</code></td><td><code class="prettyprint">9.8&times;9.8</code></td><td><code class="prettyprint">3.8&times;3.8</code></td></tr>
<tr><td>Mini squares<span class="optional-argument">squares_mini</span></td><td><code class="prettyprint">804&times;804</code></td><td><code class="prettyprint">6.8&times;6.8</code></td><td><code class="prettyprint">2.7&times;2.7</code></td></tr>
<tr><td>Retro style prints<span class="optional-argument">polaroids</span></td><td><code class="prettyprint">1027&times;1192</code></td><td><code class="prettyprint">8.7&times;10.1</code></td><td><code class="prettyprint">3.4&times;4</code></td></tr>
<tr><td>Mini retro style<span class="optional-argument">polaroids_mini</span></td><td><code class="prettyprint">739&times;832</code></td><td><code class="prettyprint">6.3&times;7</code></td><td><code class="prettyprint">2.5&times;2.8</code></td></tr>
<tr><td>Greeting Cards<span class="optional-argument">greeting_cards</span></td><td><code class="prettyprint">1069&times;1069</code></td><td><code class="prettyprint">9.1&times;9.1</code></td><td><code class="prettyprint">3.6&times;3.6</code></td></tr>
<tr><td>Greeting Cards A5<span class="optional-argument">greeting_cards_a5</span></td><td><code class="prettyprint">1749&times;2481</code></td><td><code class="prettyprint">14.8&times;21</code></td><td><code class="prettyprint">5.8&times;8.3</code></td></tr>
<tr><td>Greeting Cards 7x5<span class="optional-argument">greeting_cards_7x5</span></td><td><code class="prettyprint">1500&times;2100</code></td><td><code class="prettyprint">12.7&times;17.8</code></td><td><code class="prettyprint">5&times;7</code></td></tr>
<tr><td>Square Stickers<span class="optional-argument">stickers_square</span></td><td><code class="prettyprint">732&times;732</code></td><td><code class="prettyprint">6.2&times;6.2</code></td><td><code class="prettyprint">2.4&times;2.4</code></td></tr>
<tr><td>Circle Stickers<span class="optional-argument">stickers_circle</span></td><td><code class="prettyprint">779&times;779</code></td><td><code class="prettyprint">6.6&times;6.6</code></td><td><code class="prettyprint">2.6&times;2.6</code></td></tr>
<tr><td>Frames 50cm<span class="optional-argument">frames_50cm</span></td><td><code class="prettyprint">3426&times;3426</code></td><td><code class="prettyprint">29&times;29</code></td><td><code class="prettyprint">11.4&times;11.4</code></td></tr>
<tr><td>Postcard<span class="optional-argument">postcard</span></td><td><code class="prettyprint">1796&times;1288</code></td><td><code class="prettyprint">15.2&times;10.9</code></td><td><code class="prettyprint">6&times;4.3</code></td></tr>
</tbody></table>

### OPTIMAL PHONE CASE ASSET DIMENSIONS
<table class="apparel-positions"><thead><tr><th>product</th><th>pixels</th><th>cm</th><th>inches</th></tr></thead><tbody>
<tr><td>iPhone 6s Plus<span class="optional-argument">i6splus_tough_case</span></td><td><code class="prettyprint">1335&times;2132</code></td><td><code class="prettyprint">11.3&times;18.1</code></td><td><code class="prettyprint">4.5&times;7.1</code></td></tr>
<tr><td>iPhone 6s Plus<span class="optional-argument">i6splus_case</span></td><td><code class="prettyprint">1335&times;2132</code></td><td><code class="prettyprint">11.3&times;18.1</code></td><td><code class="prettyprint">4.5&times;7.1</code></td></tr>
<tr><td>iPhone 6s<span class="optional-argument">i6s_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>iPhone 6s<span class="optional-argument">i6s_tough_case</span></td><td><code class="prettyprint">1191&times;1896</code></td><td><code class="prettyprint">10.1&times;16.1</code></td><td><code class="prettyprint">4&times;6.3</code></td></tr>
<tr><td>iPhone 6 Plus<span class="optional-argument">i6plus_tough_case</span></td><td><code class="prettyprint">1335&times;2132</code></td><td><code class="prettyprint">11.3&times;18.1</code></td><td><code class="prettyprint">4.5&times;7.1</code></td></tr>
<tr><td>iPhone 6 Plus<span class="optional-argument">i6plus_case</span></td><td><code class="prettyprint">1335&times;2132</code></td><td><code class="prettyprint">11.3&times;18.1</code></td><td><code class="prettyprint">4.5&times;7.1</code></td></tr>
<tr><td>iPhone 6/6s Plus Folio<span class="optional-argument">i6plus_folio_case</span></td><td><code class="prettyprint">2228&times;2015</code></td><td><code class="prettyprint">18.9&times;17.1</code></td><td><code class="prettyprint">7.4&times;6.7</code></td></tr>
<tr><td>iPhone 6<span class="optional-argument">i6_tough_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
<tr><td>iPhone 6<span class="optional-argument">i6_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>iPhone 6/6s Folio<span class="optional-argument">i6_folio_case</span></td><td><code class="prettyprint">2002&times;1791</code></td><td><code class="prettyprint">17&times;15.2</code></td><td><code class="prettyprint">6.7&times;6</code></td></tr>
<tr><td>iPhone 6/6s BakPak 1<span class="optional-argument">i6_bakpak_1_case</span></td><td><code class="prettyprint">889&times;1731</code></td><td><code class="prettyprint">7.5&times;14.7</code></td><td><code class="prettyprint">3&times;5.8</code></td></tr>
<tr><td>iPhone 6/6s BakPak 3<span class="optional-argument">i6_bakpak_3_case</span></td><td><code class="prettyprint">972&times;1677</code></td><td><code class="prettyprint">8.2&times;14.2</code></td><td><code class="prettyprint">3.2&times;5.6</code></td></tr>
<tr><td>iPhone 5/5s<span class="optional-argument">i5_tough_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>iPhone 5/5s<span class="optional-argument">i5_case</span></td><td><code class="prettyprint">1032&times;1610</code></td><td><code class="prettyprint">8.7&times;13.6</code></td><td><code class="prettyprint">3.4&times;5.4</code></td></tr>
<tr><td>iPhone 5 Clik Clik<span class="optional-argument">i5_clik_case</span></td><td><code class="prettyprint">770&times;1542</code></td><td><code class="prettyprint">6.5&times;13.1</code></td><td><code class="prettyprint">2.6&times;5.1</code></td></tr>
<tr><td>iPhone 5C<span class="optional-argument">i5c_tough_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>iPhone 5C<span class="optional-argument">i5c_case</span></td><td><code class="prettyprint">1032&times;1610</code></td><td><code class="prettyprint">8.7&times;13.6</code></td><td><code class="prettyprint">3.4&times;5.4</code></td></tr>
<tr><td>iPhone 4/4s<span class="optional-argument">i4_tough_case</span></td><td><code class="prettyprint">1032&times;1610</code></td><td><code class="prettyprint">8.7&times;13.6</code></td><td><code class="prettyprint">3.4&times;5.4</code></td></tr>
<tr><td>iPhone 4/4s<span class="optional-argument">i4_case</span></td><td><code class="prettyprint">1032&times;1542</code></td><td><code class="prettyprint">8.7&times;13.1</code></td><td><code class="prettyprint">3.4&times;5.1</code></td></tr>
<tr><td>Galaxy S6 Edge<span class="optional-argument">samsung_s6e_tough_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
<tr><td>Galaxy S6 Edge<span class="optional-argument">samsung_s6e_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
<tr><td>Galaxy S6<span class="optional-argument">samsung_s6_tough_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
<tr><td>Galaxy S6<span class="optional-argument">samsung_s6_case</span></td><td><code class="prettyprint">1192&times;1896</code></td><td><code class="prettyprint">10.1&times;16.1</code></td><td><code class="prettyprint">4&times;6.3</code></td></tr>
<tr><td>Galaxy S5<span class="optional-argument">samsung_s5_tough_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
<tr><td>Galaxy S5<span class="optional-argument">samsung_s5_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
<tr><td>Galaxy S5 Mini<span class="optional-argument">samsung_s5_mini_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>Galaxy S4<span class="optional-argument">samsung_s4_tough_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>Galaxy S4<span class="optional-argument">samsung_s4_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>Galaxy S4 Mini<span class="optional-argument">samsung_s4_mini_tough_case</span></td><td><code class="prettyprint">1032&times;1610</code></td><td><code class="prettyprint">8.7&times;13.6</code></td><td><code class="prettyprint">3.4&times;5.4</code></td></tr>
<tr><td>Galaxy S4 Mini<span class="optional-argument">samsung_s4_mini_case</span></td><td><code class="prettyprint">1032&times;1610</code></td><td><code class="prettyprint">8.7&times;13.6</code></td><td><code class="prettyprint">3.4&times;5.4</code></td></tr>
<tr><td>Galaxy S3<span class="optional-argument">samsung_s3_tough_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>Galaxy S3<span class="optional-argument">samsung_s3_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>Galaxy S3 Mini<span class="optional-argument">samsung_s3_mini_case</span></td><td><code class="prettyprint">1844&times;2600</code></td><td><code class="prettyprint">15.6&times;22</code></td><td><code class="prettyprint">6.1&times;8.7</code></td></tr>
<tr><td>Samsung Note 4<span class="optional-argument">samsung_n4_tough_case</span></td><td><code class="prettyprint">1335&times;2132</code></td><td><code class="prettyprint">11.3&times;18.1</code></td><td><code class="prettyprint">4.5&times;7.1</code></td></tr>
<tr><td>Samsung Note 4<span class="optional-argument">samsung_n4_case</span></td><td><code class="prettyprint">1335&times;2132</code></td><td><code class="prettyprint">11.3&times;18.1</code></td><td><code class="prettyprint">4.5&times;7.1</code></td></tr>
<tr><td>Samsung Note 3<span class="optional-argument">samsung_n3_case</span></td><td><code class="prettyprint">1200&times;2040</code></td><td><code class="prettyprint">10.2&times;17.3</code></td><td><code class="prettyprint">4&times;6.8</code></td></tr>
<tr><td>Sony Xperia Z1<span class="optional-argument">sony_x_z1_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
<tr><td>Sony Xperia C<span class="optional-argument">sony_x_c_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
<tr><td>LG G2<span class="optional-argument">lg_g2_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
<tr><td>Motorola G<span class="optional-argument">moto_g_case</span></td><td><code class="prettyprint">1086&times;1736</code></td><td><code class="prettyprint">9.2&times;14.7</code></td><td><code class="prettyprint">3.6&times;5.8</code></td></tr>
<tr><td>Nexus 5<span class="optional-argument">nexus_5_case</span></td><td><code class="prettyprint">1182&times;1896</code></td><td><code class="prettyprint">10&times;16.1</code></td><td><code class="prettyprint">3.9&times;6.3</code></td></tr>
</tbody></table>

### OPTIMAL TABLET CASE DIMENSIONS
<table class="apparel-positions"><thead><tr><th>product</th><th>pixels</th><th>cm</th><th>inches</th></tr></thead><tbody>
<tr><td>iPad Mini 1<span class="optional-argument">ipad_mini_case</span></td><td><code class="prettyprint">1844&times;2600</code></td><td><code class="prettyprint">15.6&times;22</code></td><td><code class="prettyprint">6.1&times;8.7</code></td></tr>
<tr><td>iPad 2, 3 and 4<span class="optional-argument">ipad_case</span></td><td><code class="prettyprint">2472&times;3080</code></td><td><code class="prettyprint">20.9&times;26.1</code></td><td><code class="prettyprint">8.2&times;10.3</code></td></tr>
<tr><td>iPad Air<span class="optional-argument">ipad_air_case</span></td><td><code class="prettyprint">2472&times;3080</code></td><td><code class="prettyprint">20.9&times;26.1</code></td><td><code class="prettyprint">8.2&times;10.3</code></td></tr>
<tr><td>Nexus 7<span class="optional-argument">nexus_7_case</span></td><td><code class="prettyprint">1778&times;2841</code></td><td><code class="prettyprint">15.1&times;24.1</code></td><td><code class="prettyprint">5.9&times;9.5</code></td></tr>
</tbody></table>

### OPTIMAL PHOTOBOOK ASSET DIMENSIONS
<table class="apparel-positions"><thead><tr><th>product</th><th>pixels</th><th>cm</th><th>inches</th></tr></thead><tbody>
<tr><td>Large Landscape Hardcover<span class="optional-argument">rpi_wrap_321x270_sm</span></td><td><code class="prettyprint">3792&times;3190</code></td><td><code class="prettyprint">32.1&times;27</code></td><td><code class="prettyprint">12.6&times;10.6</code></td></tr>
<tr><td>Portrait Hardcover<span class="optional-argument">rpi_wrap_210x280_sm</span></td><td><code class="prettyprint">2481&times;3306</code></td><td><code class="prettyprint">21&times;28</code></td><td><code class="prettyprint">8.3&times;11</code></td></tr>
<tr><td>Landscape Hardcover<span class="optional-argument">rpi_wrap_280x210_sm</span></td><td><code class="prettyprint">3308&times;2481</code></td><td><code class="prettyprint">28&times;21</code></td><td><code class="prettyprint">11&times;8.3</code></td></tr>
<tr><td>Large Square Hardcover<span class="optional-argument">rpi_wrap_300x300_sm</span></td><td><code class="prettyprint">3544&times;3544</code></td><td><code class="prettyprint">30&times;30</code></td><td><code class="prettyprint">11.8&times;11.8</code></td></tr>
<tr><td>Medium Square Hardcover<span class="optional-argument">rpi_wrap_210x210_sm</span></td><td><code class="prettyprint">2481&times;2481</code></td><td><code class="prettyprint">21&times;21</code></td><td><code class="prettyprint">8.3&times;8.3</code></td></tr>
<tr><td>Small Square Hardcover<span class="optional-argument">rpi_wrap_140x140_sm</span></td><td><code class="prettyprint">1654&times;1654</code></td><td><code class="prettyprint">14&times;14</code></td><td><code class="prettyprint">5.5&times;5.5</code></td></tr>
</tbody></table>

<div ng-if="isPhotoboxUser">
### OPTIMAL PHOTOBOX ASSET DIMENSIONS
<table class="apparel-positions"><thead><tr><th>product</th><th>pixels</th><th>cm</th><th>inches</th></tr></thead><tbody>
<tr><td>iPhone 6 Plus Case<span class="optional-argument">i6ptc7</span></td><td><code class="prettyprint">1335&times;2320</code></td><td><code class="prettyprint">11.3&times;19.6</code></td><td><code class="prettyprint">4.5&times;7.7</code></td></tr>
<tr><td>iPhone 6 Case<span class="optional-argument">i6cc7</span></td><td><code class="prettyprint">1335&times;2257</code></td><td><code class="prettyprint">11.3&times;19.1</code></td><td><code class="prettyprint">4.5&times;7.5</code></td></tr>
<tr><td>iPhone 5/5S Case<span class="optional-argument">i5c4</span></td><td><code class="prettyprint">1335&times;2199</code></td><td><code class="prettyprint">11.3&times;18.6</code></td><td><code class="prettyprint">4.5&times;7.3</code></td></tr>
<tr><td>iPhone 5C Case<span class="optional-argument">iphone5c1</span></td><td><code class="prettyprint">1335&times;2199</code></td><td><code class="prettyprint">11.3&times;18.6</code></td><td><code class="prettyprint">4.5&times;7.3</code></td></tr>
<tr><td>iPhone 5/5S Clear Case<span class="optional-argument">i5ccc1</span></td><td><code class="prettyprint">1335&times;2734</code></td><td><code class="prettyprint">11.3&times;23.1</code></td><td><code class="prettyprint">4.5&times;9.1</code></td></tr>
<tr><td>iPhone 5 Clear Case Sticker<span class="optional-argument">stickeri5c1</span></td><td><code class="prettyprint">732&times;1500</code></td><td><code class="prettyprint">6.2&times;12.7</code></td><td><code class="prettyprint">2.4&times;5</code></td></tr>
<tr><td>iPhone 4/4S Case<span class="optional-argument">i4c9</span></td><td><code class="prettyprint">1335&times;2195</code></td><td><code class="prettyprint">11.3&times;18.6</code></td><td><code class="prettyprint">4.5&times;7.3</code></td></tr>
<tr><td>iPhone 4/4S Clear Case<span class="optional-argument">i4ccc1</span></td><td><code class="prettyprint">1335&times;2582</code></td><td><code class="prettyprint">11.3&times;21.9</code></td><td><code class="prettyprint">4.5&times;8.6</code></td></tr>
<tr><td>iPhone 4 Clear Case Sticker<span class="optional-argument">stickeri4c1</span></td><td><code class="prettyprint">715&times;1382</code></td><td><code class="prettyprint">6.1&times;11.7</code></td><td><code class="prettyprint">2.4&times;4.6</code></td></tr>
<tr><td>Galaxy S5 Case<span class="optional-argument">sgs5c1</span></td><td><code class="prettyprint">1335&times;2403</code></td><td><code class="prettyprint">11.3&times;20.3</code></td><td><code class="prettyprint">4.5&times;8</code></td></tr>
<tr><td>Galaxy S4 Case<span class="optional-argument">sgs4c3</span></td><td><code class="prettyprint">1335&times;2299</code></td><td><code class="prettyprint">11.3&times;19.5</code></td><td><code class="prettyprint">4.5&times;7.7</code></td></tr>
<tr><td>Galaxy S3 Case<span class="optional-argument">sgs3c4</span></td><td><code class="prettyprint">1335&times;2200</code></td><td><code class="prettyprint">11.3&times;18.6</code></td><td><code class="prettyprint">4.5&times;7.3</code></td></tr>
<tr><td>Galaxy S2 Case<span class="optional-argument">sgs2c1</span></td><td><code class="prettyprint">1335&times;2050</code></td><td><code class="prettyprint">11.3&times;17.4</code></td><td><code class="prettyprint">4.5&times;6.8</code></td></tr>
<tr><td>iPad 2/3/4 Case<span class="optional-argument">ipad_case_1</span></td><td><code class="prettyprint">1335&times;1588</code></td><td><code class="prettyprint">11.3&times;13.4</code></td><td><code class="prettyprint">4.5&times;5.3</code></td></tr>
<tr><td>iPad Mini Case<span class="optional-argument">ipadminic1</span></td><td><code class="prettyprint">1335&times;1808</code></td><td><code class="prettyprint">11.3&times;15.3</code></td><td><code class="prettyprint">4.5&times;6</code></td></tr>
<tr><td>iPad Smart Cover<span class="optional-argument">ipadsmartc6</span></td><td><code class="prettyprint">1335&times;1740</code></td><td><code class="prettyprint">11.3&times;14.7</code></td><td><code class="prettyprint">4.5&times;5.8</code></td></tr>
<tr><td>iPad Mini Smart Cover<span class="optional-argument">ipadminismartc1</span></td><td><code class="prettyprint">1335&times;1981</code></td><td><code class="prettyprint">11.3&times;16.8</code></td><td><code class="prettyprint">4.5&times;6.6</code></td></tr>
<tr><td>Canvas Print 20 cm x 30 cm<span class="optional-argument">pbx_canvas_20x30</span></td><td><code class="prettyprint">2363&times;3544</code></td><td><code class="prettyprint">20&times;30</code></td><td><code class="prettyprint">7.9&times;11.8</code></td></tr>
<tr><td>Canvas Print 30 cm x 20 cm<span class="optional-argument">pbx_canvas_30x20</span></td><td><code class="prettyprint">3544&times;2363</code></td><td><code class="prettyprint">30&times;20</code></td><td><code class="prettyprint">11.8&times;7.9</code></td></tr>
<tr><td>Canvas Print 30 cm x 30 cm<span class="optional-argument">pbx_canvas_30x30</span></td><td><code class="prettyprint">3544&times;3544</code></td><td><code class="prettyprint">30&times;30</code></td><td><code class="prettyprint">11.8&times;11.8</code></td></tr>
<tr><td>Classic Canvas 40 cm x 40 cm<span class="optional-argument">pbx_canvas_40x40</span></td><td><code class="prettyprint">4725&times;4725</code></td><td><code class="prettyprint">40&times;40</code></td><td><code class="prettyprint">15.8&times;15.8</code></td></tr>
<tr><td>12 Prints + Box<span class="optional-argument">pbx_polaroids_12</span></td><td><code class="prettyprint">1540&times;1580</code></td><td><code class="prettyprint">13&times;13.4</code></td><td><code class="prettyprint">5.1&times;5.3</code></td></tr>
<tr><td>24 Prints + Box<span class="optional-argument">pbx_polaroids_24</span></td><td><code class="prettyprint">1540&times;1580</code></td><td><code class="prettyprint">13&times;13.4</code></td><td><code class="prettyprint">5.1&times;5.3</code></td></tr>
<tr><td>36 Prints + Box<span class="optional-argument">pbx_polaroids_36</span></td><td><code class="prettyprint">1540&times;1580</code></td><td><code class="prettyprint">13&times;13.4</code></td><td><code class="prettyprint">5.1&times;5.3</code></td></tr>
<tr><td>A3 Poster<span class="optional-argument">pbx_a3</span></td><td><code class="prettyprint">3508&times;4961</code></td><td><code class="prettyprint">29.7&times;42</code></td><td><code class="prettyprint">11.7&times;16.5</code></td></tr>
<tr><td>Classic Prints<span class="optional-argument">pbx_6x4</span></td><td><code class="prettyprint">1800&times;1200</code></td><td><code class="prettyprint">15.2&times;10.2</code></td><td><code class="prettyprint">6&times;4</code></td></tr>
<tr><td>Large Classic Prints<span class="optional-argument">pbx_7x5</span></td><td><code class="prettyprint">2100&times;1500</code></td><td><code class="prettyprint">17.8&times;12.7</code></td><td><code class="prettyprint">7&times;5</code></td></tr>
<tr><td>Square Prints<span class="optional-argument">pbx_squares_5x5</span></td><td><code class="prettyprint">1500&times;1500</code></td><td><code class="prettyprint">12.7&times;12.7</code></td><td><code class="prettyprint">5&times;5</code></td></tr>
<tr><td>Square Prints<span class="optional-argument">pbx_squares_8x8</span></td><td><code class="prettyprint">2400&times;2400</code></td><td><code class="prettyprint">20.3&times;20.3</code></td><td><code class="prettyprint">8&times;8</code></td></tr>
<tr><td>Square Magnets<span class="optional-argument">pbx_magnets_8x8</span></td><td><code class="prettyprint">1250&times;1250</code></td><td><code class="prettyprint">10.6&times;10.6</code></td><td><code class="prettyprint">4.2&times;4.2</code></td></tr>
<tr><td>Classic Magnets<span class="optional-argument">pbx_magnets_13x9</span></td><td><code class="prettyprint">1536&times;1062</code></td><td><code class="prettyprint">13&times;9</code></td><td><code class="prettyprint">5.1&times;3.5</code></td></tr>
<tr><td>Classic Magnets<span class="optional-argument">pbx_magnets_15x10</span></td><td><code class="prettyprint">1773&times;1182</code></td><td><code class="prettyprint">15&times;10</code></td><td><code class="prettyprint">5.9&times;3.9</code></td></tr>
<tr><td>Reusable Stickers 13cm x 9cm<span class="optional-argument">pbx_stickers_13x9</span></td><td><code class="prettyprint">1536&times;1062</code></td><td><code class="prettyprint">13&times;9</code></td><td><code class="prettyprint">5.1&times;3.5</code></td></tr>
<tr><td>Pack of 10 Cards<span class="optional-argument">pbx_cards_a6_10pack</span></td><td><code class="prettyprint">1241&times;1749</code></td><td><code class="prettyprint">10.5&times;14.8</code></td><td><code class="prettyprint">4.1&times;5.8</code></td></tr>
<tr><td>Mug<span class="optional-argument">mgth10</span></td><td><code class="prettyprint">4725&times;4725</code></td><td><code class="prettyprint">40&times;40</code></td><td><code class="prettyprint">15.8&times;15.8</code></td></tr>
<tr><td>Bone China Mug<span class="optional-argument">mug_bone_wrap</span></td><td><code class="prettyprint">5850&times;2400</code></td><td><code class="prettyprint">49.5&times;20.3</code></td><td><code class="prettyprint">19.5&times;8</code></td></tr>
<tr><td>Timeless Framed Print 30cm x 30cm<span class="optional-argument">pbx_frame_30x30</span></td><td><code class="prettyprint">3544&times;3544</code></td><td><code class="prettyprint">30&times;30</code></td><td><code class="prettyprint">11.8&times;11.8</code></td></tr>
<tr><td>Classic Canvas 30 cm x 40 cm<span class="optional-argument">pbx_canvas_30x40</span></td><td><code class="prettyprint">3544&times;4725</code></td><td><code class="prettyprint">30&times;40</code></td><td><code class="prettyprint">11.8&times;15.8</code></td></tr>
<tr><td>3 Minute Book<span class="optional-argument">23540-3mbook_1</span></td><td><code class="prettyprint">4725&times;4725</code></td><td><code class="prettyprint">40&times;40</code></td><td><code class="prettyprint">15.8&times;15.8</code></td></tr>
</tbody></table>
</div>

<div ng-if="isAlbelliUser">
### OPTIMAL ALBELLI ASSET DIMENSIONS
<table class="apparel-positions"><thead><tr><th>product</th><th>pixels</th><th>cm</th><th>inches</th></tr></thead><tbody>
<tr><td>Aluminium Print<span class="optional-argument">ap_aluminium_400x400</span></td><td><code class="prettyprint">4725&times;4725</code></td><td><code class="prettyprint">40&times;40</code></td><td><code class="prettyprint">15.8&times;15.8</code></td></tr>
<tr><td>Aluminium Print<span class="optional-argument">ap_aluminium_300x400</span></td><td><code class="prettyprint">3544&times;4725</code></td><td><code class="prettyprint">30&times;40</code></td><td><code class="prettyprint">11.8&times;15.8</code></td></tr>
<tr><td>Aluminium Print<span class="optional-argument">ap_aluminium_400x300</span></td><td><code class="prettyprint">4725&times;3543</code></td><td><code class="prettyprint">40&times;30</code></td><td><code class="prettyprint">15.8&times;11.8</code></td></tr>
<tr><td>Mounted Print<span class="optional-argument">ap_mounted_400x400</span></td><td><code class="prettyprint">4725&times;4725</code></td><td><code class="prettyprint">40&times;40</code></td><td><code class="prettyprint">15.8&times;15.8</code></td></tr>
<tr><td>Mounted Print<span class="optional-argument">ap_mounted_400x300</span></td><td><code class="prettyprint">4725&times;3543</code></td><td><code class="prettyprint">40&times;30</code></td><td><code class="prettyprint">15.8&times;11.8</code></td></tr>
<tr><td>Mounted Print<span class="optional-argument">ap_mounted_300x400</span></td><td><code class="prettyprint">3544&times;4725</code></td><td><code class="prettyprint">30&times;40</code></td><td><code class="prettyprint">11.8&times;15.8</code></td></tr>
<tr><td>Canvas Print<span class="optional-argument">ap_canvas_400x300</span></td><td><code class="prettyprint">4725&times;3543</code></td><td><code class="prettyprint">40&times;30</code></td><td><code class="prettyprint">15.8&times;11.8</code></td></tr>
<tr><td>Canvas Print<span class="optional-argument">ap_canvas_300x400</span></td><td><code class="prettyprint">3544&times;4725</code></td><td><code class="prettyprint">30&times;40</code></td><td><code class="prettyprint">11.8&times;15.8</code></td></tr>
<tr><td>Canvas Print<span class="optional-argument">ap_canvas_400x400</span></td><td><code class="prettyprint">4725&times;4725</code></td><td><code class="prettyprint">40&times;40</code></td><td><code class="prettyprint">15.8&times;15.8</code></td></tr>
<tr><td>Wood Print<span class="optional-argument">ap_wood_400x300</span></td><td><code class="prettyprint">4725&times;3543</code></td><td><code class="prettyprint">40&times;30</code></td><td><code class="prettyprint">15.8&times;11.8</code></td></tr>
<tr><td>Wood Print<span class="optional-argument">ap_wood_300x400</span></td><td><code class="prettyprint">3544&times;4725</code></td><td><code class="prettyprint">30&times;40</code></td><td><code class="prettyprint">11.8&times;15.8</code></td></tr>
<tr><td>Wood Print<span class="optional-argument">ap_wood_400x400</span></td><td><code class="prettyprint">4725&times;4725</code></td><td><code class="prettyprint">40&times;40</code></td><td><code class="prettyprint">15.8&times;15.8</code></td></tr>
<tr><td>Acrylic Print<span class="optional-argument">ap_acrylic_300x400</span></td><td><code class="prettyprint">3544&times;4725</code></td><td><code class="prettyprint">30&times;40</code></td><td><code class="prettyprint">11.8&times;15.8</code></td></tr>
<tr><td>Acrylic Print<span class="optional-argument">ap_acrylic_400x300</span></td><td><code class="prettyprint">4725&times;3543</code></td><td><code class="prettyprint">40&times;30</code></td><td><code class="prettyprint">15.8&times;11.8</code></td></tr>
<tr><td>Acrylic Print<span class="optional-argument">ap_acrylic_400x400</span></td><td><code class="prettyprint">4725&times;4725</code></td><td><code class="prettyprint">40&times;40</code></td><td><code class="prettyprint">15.8&times;15.8</code></td></tr>
<tr><td>Square Photo Book<span class="optional-argument">ap_album_210x210</span></td><td><code class="prettyprint">2481&times;2481</code></td><td><code class="prettyprint">21&times;21</code></td><td><code class="prettyprint">8.3&times;8.3</code></td></tr>
<tr><td>Metallic Squares<span class="optional-argument">metallic_8x8</span></td><td><code class="prettyprint">2501&times;2501</code></td><td><code class="prettyprint">21.2&times;21.2</code></td><td><code class="prettyprint">8.3&times;8.3</code></td></tr>
</tbody></table>
</div>




# Addresses
Our address lookup services allows you to perform international address searches. You'll benefit from the most up to date and complete address information available as our databases are typically updated daily.

## The address object

A place where a person or business resides.

> Example JSON

```json
{
  "recipient_name": "Deon Botha",
  "address_line_1": "Eastcastle House",
  "address_line_2": "27-28 Eastcastle Street",
  "address_line_3": "",
  "address_line_4": "",
  "city": "London",
  "county_state": "",
  "postcode": "W1W 8DH",
  "country_code": "GBR"
}
```

### Attributes

          | |
--------- | -----------
recipient_name<span class="attribute-type">string</span> | The name of the person intended to receive the order
address_line_1<span class="attribute-type">string</span> | The first line of the address
address_line_2<span class="attribute-type">string</span> | The second line of the address
address_line_3<span class="attribute-type">string</span> | The third line of the address
address_line_4<span class="attribute-type">string</span> | The fourth line of the address
city<span class="attribute-type">string</span> | The city of the address
postcode<span class="attribute-type">string</span> | The ZIP/Postal code of the address
county_state<span class="attribute-type">string</span> | The state/county/province of the address
country_code<span class="attribute-type">string</span> | The [three letter country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) of the address


## The partial address object

> Example JSON

```json
{
  "address_id": "GBR|PR|25762481|0|0|0||Retrieve",
  "display_address": "Eastcastle House 27-28, Eastcastle Street, London, W1W... "
}
```

Partial address objects are typically returned when an ambiguous address search results in an list of potential matches. Typically the choice of partial addresses is presented to the user so they can refine the search. The `address_id` attribute of the chosen partial address can then be used to narrow the search down until a full address object is returned.


### Attributes

          | |
--------- | -----------
address_id<span class="attribute-type">string</span> | An identifier that can be used to perform further lookups until a full address object is found
display_address<span class="attribute-type">string</span> | A partial textual representation of the address

## Searching for an address

> Example Address Search Request

```shell
curl "https://api.kite.ly/v2.0/address/search/?country_code=GBR&search_term=10+Downing+Street,London" \
  -H "Authorization: ApiKey [[public_key]]:"
```

```objective_c
OLCountry *usa = [OLCountry countryForCode:@"USA"];
[OLAddress searchForAddressWithCountry:usa query:@"1 Infinite Loop" delegate:self];
```

```java
Address.search("1 Infinite Loop", Country.getInstance("USA"), /*AddressSearchRequestListener: */ this);
```

> Example List Response

```shell
{
  "choices": [
    {
      "address_id": "GBR|PR|23747771|0|0|0||Retrieve",
      "display_address": "Prime Minister & First Lord of the Treasury, 10 Downing Street, London, SW1A..."
    },
    {
      "address_id": "GBR|PR|26245117|0|0|0||Retrieve",
      "display_address": "Flat 10, Downing Court, Grenville Street, London, WC1N..."
    },
    {
      "address_id": "GBR|PR|25755770|0|0|0||Retrieve",
      "display_address": "Ove Arup & Partners, Downing House, 10 Maple Street, London, W1T..."
    }
  ]
}
```

```objective_c
#pragma mark - OLAddressSearchRequestDelegate methods

- (void)addressSearchRequest:(OLAddressSearchRequest *)req didSuceedWithMultipleOptions:(NSArray *)options {
    // present choice of OLAddress' to the user, then
    // perform further search if address.isSearchRequiredForFullDetails
}

- (void)addressSearchRequest:(OLAddressSearchRequest *)req didSuceedWithUniqueAddress:(OLAddress *)addr {
    // Search resulted in one unique address
}

- (void)addressSearchRequest:(OLAddressSearchRequest *)req didFailWithError:(NSError *)error {
    // Oops something went wrong
}
```

```java
// AddressSearchRequestListener implementation

@Override
public void onMultipleChoices(AddressSearchRequest req, List<Address> options) {
  // present choice of Address' to the user, then 
  // perform further search if address.isSearchRequiredForFullDetails() 
}

@Override
public void onUniqueAddress(AddressSearchRequest req, Address address) {
  // Search resulted in one unique address
}

@Override
public void onError(AddressSearchRequest req, Exception error) {
// Oops something went wrong
}
```

> Example Address Search Request

```shell
curl "https://api.kite.ly/v2.0/address/search/?country_code=GBR&address_id=GBR|PR|23747771|0|0|0||Retrieve" \
  -H "Authorization: ApiKey [[public_key]]:"
```

```objective_c
// Fetch full details for a partial OLAddress

if (address.isSearchRequiredForFullDetails) {
	[OLAddress searchForAddress:address delegate:self];
}
```

```java
// Fetch full details for a partial Address

if (address.isSearchRequiredForFullDetails()) {
	Address.search(/*Address:*/address, /*AddressSearchRequestListener:*/this);
}
```

> Example Unique Response

```shell
{
  "unique": {
    "address_line_1": "Prime Minister & First Lord of the Treasury",
    "address_line_2": "10 Downing Street",
    "address_line_3": "",
    "address_line_4": "",
    "city": "London",
    "county_state": "",
    "postcode": "SW1A 2AA",
    "country_code": "GBR"
  }
}
```

```objective_c
// See above OLAddressSearchRequestDelegate implementation
```

```java
// See above AddressSearchRequestListener implementation
```

You can perform a search on any part of the address not just the ZIP/Postal code and our smart sorting of results will order by nearest locations first. We also recognise common misspellings.

### HTTP Request

`GET https://api.kite.ly/v2.0/address/search/`

### Arguments

          | |
--------- | -----------
country_code<span class="required-argument">required</span> | [Three letter country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) to which the address search will be restricted
search_term<span class="maybe-argument">optional, either **search_term** or **address_id** is required</span> | A free text value, often encompassing the first line of address or ZIP/Postal code, on which the search is performed
address_id<span class="maybe-argument">optional, either **search_term** or **address_id** is required</span> | A parameter referencing a previously returned address search results list item that can be used to lookup a unique address 

### Returns
Returns either a dictionary with a `unique` property that is a [full address object](#the-address-object), or (if the search is ambiguous) a dictionary with a `choices` property that is a list of [partial address objects](#the-partial-address-object). 

In the case of a list response, additional calls to the address search endpoint are required to find a unique match. You can use the `address_id`'s from previous responses to narrow down the search until you eventually find a unique address.

<aside class="notice">Be sure to handle both unique and list responses from the address search endpoint.</aside>


# Postcard Guidelines
When you supply a back_image to Kite for postcard orders, you gain control of the design that is printed on the back of that postcard.

You are able to style your message whichever way you like, however the back of the card must adhere to certain style guidelines to maximise the chances of accurate dispatch and delivery of the postcard to your customers.

## Address formatting

Addresses must be eligible, be formatted on the right hand side of the postcard and include the delivery information with the following structure

### Fields

 | |
--------- | -----------
Recipients Name<span class="required-argument">required</span> | Name of receipient
Address Line 1<span class="required-argument">required</span> | Address Line 1
Address Line 2<span class="maybe-argument">optional</span> | Address Line 2
City<span class="required-argument">required</span> | City
Country<span class="required-argument">required</span> | Country
Postcode<span class="required-argument">required</span> | Postcode, The postcode should always be on the last line of the address

Avoid positioning any logo underneath the address text.

## Stamp Placement

A blank space must be reserved in the top right corner of the postcard so that Kite can place a stamp there.

This is because stamp designs must be pre-approved by the mail carrier before printing can take place. Designs which have not been approved will unfortunately not be accepted by the mail service for delivery.