# Introduction

> API Endpoint

```html
[[api_endpoint]]
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
curl "[[api_endpoint]]/v4.0/address/search/?country_code=USA&search_term=1+Infinite+Loop" \
  -H "Authorization: ApiKey [[public_key]]:"
```

```objective_c
[OLKitePrintSDK setAPIKey:@"[[public_key]]" withEnvironment:kOLKitePrintSDKEnvironmentSandbox];
```

```java
KitePrintSDK.initialize("[[public_key]]", KitePrintSDK.Environment.TEST, getApplicationContext());
```

> <span ng-if="authenticated">One of your test API keys has been filled into all the examples on the page, so you can test out any example right away.</span>

> <span ng-if="!authenticated">A sample test API key has been provided so you can test out all the examples straight away. You should replace `[[public_key]]` with one of your own found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.</span>

You authenticate with the Kite API by providing your API key in the request. You can manage your API keys in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard. You can have multiple API keys active at one time. Your API keys carry many privileges, so be sure to keep them secret!

To authenticate you include the HTTP `Authorization` header in your request. All API requests must be made over [HTTPS](http://en.wikipedia.org/wiki/HTTPS). Calls made over plain HTTP will fail. You must authenticate for all requests.

In some scenarios it's also desirable to include your secret key in the `Authorization` header. If you're building a mobile application this is not normally needed, but if you're placing orders from your own server it usually makes sense. See [payment workflows](#payment-workflows) for more details.

# Payment Workflows
Your customers can either pay you directly when they place an order for a product or we can take payment on your behalf and automatically transfer your revenue into an account of your choosing. 

## Kite takes payment
In this scenario we take payment from customers on your behalf. This will occur entirely within your app or website in a way that's totally branded to you, your customers don't even need to know we were involved. We then automatically transfer funds we owe you directly into a bank or a PayPal account of your choosing. You can setup the account into which you want to receive payments in the [billing]([[website_endpoint]]/settings/billing/) section of the dashboard.

This is the easiest approach to using the Kite platform as it means you don't need to run your own server and it's baked into several of our SDKs. 

## You take payment

> Example Request

```shell
curl "[[api_endpoint]]/v4.0/address/search/?country_code=USA&search_term=1+Infinite+Loop" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>"
```

```objective_c
// Our iOS SDK does not support this payment workflow directly as it would require embedding your secret key into the app. Instead use our REST API
```

```java
// Our Android SDK does not support this payment workflow directly as it would require embedding your secret key into the app. Instead use our REST API
```

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.

In this scenario you take payment directly from your customer in any manner of your choosing. You'll need your own server infrastructure in order to take care of the payment processing, payment validation and to submit [product order requests](#placing-orders) to the Kite platform. 

You'll need to add a card to be charged for any orders you place with Kite. This can be done in the [billing]([[website_endpoint]]/settings/billing/) section of the dashboard.

Any request you make to Kite that would result in you incurring a charge (i.e. [product order requests](#placing-orders)) will need to include both your API key and your secret key in the HTTP `Authorization` header. Your secret key can be found alongside your API key in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard. 

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
curl "[[api_endpoint]]/v4.0/order/?offset=30&limit=5" \
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
curl "[[api_endpoint]]/v4.0/asset/sign/?mime_types=image/jpeg&client_asset=true" \
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

`GET [[api_endpoint]]/v4.0/asset/sign/`

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

Which products you display to your customers within our mobile SDKs and their associated retail prices can be configured within the [products]([[website_endpoint]]/dashboard/products) section of the dashboard


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
shipping_class<span class="attribute-type">integer</span> | *Optional* field to specify a non standard delivery method. See our [Shipping methods](#shipping-methods) section for more information.
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
customer_payment<span class="attribute-type">dictionary</span> | A dictionary containing the amount paid by the customer. In instances where Kite does not take payment (i.e you are using your secret key in the [Authorization header](#authentication) to validate orders), this field is required to give an accurate representation on the profit made on the sale within the [orders]([[website_endpoint]]/settings/credentials) section of the Kite dashboard.
jobs<span class="attribute-type">list</span> | A list of one or more [job objects](#the-job-object) to be created and delivered to `shipping_address`

## Placing orders

> Example Order Request

```shell
curl "[[api_endpoint]]/v4.0/print/" \
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
    "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
    },
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

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

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

`POST [[api_endpoint]]/v4.0/print/`

### Arguments

          | |
--------- | -----------
proof_of_payment<span class="optional-argument">optional, either **proof_of_payment** or a secret key in [Authorization header](#authentication) is required</span> | The proof of payment is a either a PayPal REST payment id for a payment/transaction made to the Kite PayPal account or a Stripe token created using Kite’s Stripe publishable key. This field is optional if you opted for [taking payment yourself](#you-take-payment)
shipping_address<span class="required-argument">required</span> | An [address object](#the-address-object) indicating the address to which the order will be delivered
customer_email<span class="optional-argument">optional</span> | The customer's email address. Automated order status update emails (you can brand these) can optionally be sent to this address i.e. order confirmation email, order dispatched email, etc. You can configure these in the Kite dashboard
customer_phone<span class="required-argument">required</span> | The customer's phone number. Certain postage companies require this to be provided e.g. FedEx
user_data<span class="optional-argument">optional</span> | A dictionary containing any application or user specific meta data that you might want associated with the order
customer_payment<span class="optional-argument">optional</span> | A dictionary containing the amount paid by the customer. In instances where Kite does not take payment (i.e you are using your secret key in the [Authorization header](#authentication) to validate orders), this field is required to give an accurate representation on the profit made on the sale within the [orders]([[website_endpoint]]/settings/credentials) section of the Kite dashboard.
jobs<span class="required-argument">required</span> | A list of one or more [job objects](#the-job-object) to be created and delivered to `shipping_address`

### Returns

Returns a dictionary containing the order id

## Ordering print products

> Example Order Request

```shell
curl "[[api_endpoint]]/v4.0/print/" \
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
    "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
    },
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

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

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
curl "[[api_endpoint]]/v4.0/print/" \
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
    "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
    },
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

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

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
iPhone 6s+ Case<span class="attribute-type">i6splus_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/phone_cases/IP6SP-CS/IP6SP-CS_mask.png">Case Mask</a></span> | iPhone 6s snap case constructed to the highest quality design, material & coating
iPhone 6s+ Tough Case<span class="attribute-type">i6splus_tough_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/tough_cases/IP6SP-TCB-CS/IP6SP-TCB-CS_mask.png">Case Mask</a></span> | iPhone 6s + tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 6+ Case<span class="attribute-type">i6plus_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP6P-CS.png">Case Mask</a></span> | iPhone 6+ snap case constructed to the highest quality design, material & coating
iPhone 6+ Tough Case<span class="attribute-type">i6plus_tough_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP6P-TC-CS.png">Case Mask</a></span> | iPhone 6+ tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 6s Case<span class="attribute-type">i6s_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/phone_cases/IP6S-CS/IP6S-CS_mask.png">Case Mask</a></span> | iPhone 6s snap case constructed to the highest quality design, material & coating
iPhone 6s Tough Case<span class="attribute-type">i6s_tough_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/tough_cases/IP6S-TCB-CS/IP6S-TCB-CS_mask.png">Case Mask</a></span> | iPhone 6s tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 6 Case<span class="attribute-type">i6_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP6-CS.png">Case Mask</a></span> | iPhone 6 snap case constructed to the highest quality design, material & coating
iPhone 6 Tough Case<span class="attribute-type">i6_tough_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP6-TC-CS.png">Case Mask</a></span> | iPhone 6 tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 5/5S Case<span class="attribute-type">i5_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP5-CS.png">Case Mask</a></span> | iPhone 5 snap case constructed to the highest quality design, material & coating
iPhone 5/5S Tough Case<span class="attribute-type">i5_tough_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP5-TC-CS.png">Case Mask</a></span> | iPhone 5 tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 5C Case<span class="attribute-type">i5c_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP5C-CS.png">Case Mask</a></span> | iPhone 5c snap case constructed to the highest quality design, material & coating
iPhone 5C Tough Case<span class="attribute-type">i5c_tough_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP5C-TC-CS.png">Case Mask</a></span> | iPhone 5c tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPhone 4/4S Case<span class="attribute-type">i4_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP4-CS.png">Case Mask</a></span> | iPhone 4 snap case constructed to the highest quality design, material & coating
iPhone 4/4S Tough Case<span class="attribute-type">i4_tough_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IP4-TC-CS.png">Case Mask</a></span> | iPhone 4 tough case constructed to the highest quality design, material & coating.  Durable two layered case that offer the best solution for protecting your phone
iPad Mini Case<span class="attribute-type">ipad_mini_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IPADMI-CS.png">Case Mask</a></span> | iPad Mini snap case constructed to the highest quality design, material & coating
iPad Air Case<span class="attribute-type">ipad_air_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_IPAD-A-CS.png">Case Mask</a></span> | iPad Air snap case constructed to the highest quality design, material & coating
iPad 2,3,4 Case<span class="attribute-type">ipad_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/ipad_cases/IPAD2-CS/IPAD2-CS_mask.png">Case Mask</a></span> | iPad 2,3,4 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S7 Edge Case<span class="attribute-type">samsung_s7e_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/phone_cases/SGS7E-CS/SGS7E-CS_mask.png">Case Mask</a></span> | Samsung Galaxy S6 Edge snap case constructed to the highest quality design, material & coating
Samsung Galaxy S7 Case<span class="attribute-type">samsung_s7_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/phone_cases/SGS7-CS/SGS7-CS_mask.png">Case Mask</a></span> | Samsung Galaxy S6 Edge snap case constructed to the highest quality design, material & coating
Samsung Galaxy S6 Edge Case<span class="attribute-type">samsung_s6e_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/phone_cases/SGS6E-CS/SGS6E-CS_mask.png">Case Mask</a></span> | Samsung Galaxy S6 Edge snap case constructed to the highest quality design, material & coating
Samsung Galaxy S6 Case<span class="attribute-type">samsung_s6_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/phone_cases/SGS6-CS/SGS6-CS_mask.png">Case Mask</a></span> | Samsung Galaxy S6 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S5 Case<span class="attribute-type">samsung_s5_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_SGS5-CS.png">Case Mask</a></span> | Samsung Galaxy S5 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S5 Mini Case<span class="attribute-type">samsung_s5_mini_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_SGS5M-CS.png">Case Mask</a></span> | Samsung Galaxy S5 Mini snap case constructed to the highest quality design, material & coating
Samsung Galaxy S4 Case<span class="attribute-type">samsung_s4_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_SGS4-CS.png">Case Mask</a></span> | Samsung Galaxy S4 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S4 Mini Case<span class="attribute-type">samsung_s4_mini_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_SGS4M-CS.png">Case Mask</a></span> | Samsung Galaxy S4 Mini snap case constructed to the highest quality design, material & coating
Samsung Galaxy S3 Case<span class="attribute-type">samsung_s3_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_SGS3-CS.png">Case Mask</a></span> | Samsung Galaxy S3 snap case constructed to the highest quality design, material & coating
Samsung Galaxy S3 Mini Case<span class="attribute-type">samsung_s3_mini_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_SGS3M-CS.png">Case Mask</a></span> | Samsung Galaxy S3 Mini snap case constructed to the highest quality design, material & coating
Samsung Galaxy Note 4 Case<span class="attribute-type">samsung_n4_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/phone_cases/SGN4-CS/SGN4-CS_mask.png">Case Mask</a></span> | Samsung Galaxy Note 4 snap case constructed to the highest quality design, material & coating
Samsung Galaxy Note 3 Case<span class="attribute-type">samsung_n3_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_GN3-CS.png">Case Mask</a></span> | Samsung Galaxy Note 3 snap case constructed to the highest quality design, material & coating
Sony Xperia Z1 Case<span class="attribute-type">sony_x_z1_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_SXZ1-CS.png">Case Mask</a></span> | Sony Xperia Z1 snap case constructed to the highest quality design, material & coating
Sony Xperia C Case<span class="attribute-type">sony_x_c_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_SXC-CS.png">Case Mask</a></span> | Sony Xperia Z1 snap case constructed to the highest quality design, material & coating
LG G2 Case<span class="attribute-type">lg_g2_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_LGG2-CS.png">Case Mask</a></span> | LG G2 snap case constructed to the highest quality design, material & coating
Nexus 7 Case<span class="attribute-type">nexus_7_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/phone_masks/phone_cases/NEX7-CS/NEX7-CS_mask.png">Case Mask</a></span> | Nexus 7 snap case constructed to the highest quality design, material & coating
Nexus 5 Case<span class="attribute-type">nexus_5_case</span><span class=attribute-secondary><a href="https://s3.amazonaws.com/sdk-static/mask_NEX5-CS.png">Case Mask</a></span> | Nexus 5 snap case constructed to the highest quality design, material & coating


### Options Arguments

          | |
--------- | -----------
case_style<span class="optional-argument">optional</span> | Either `matte` or `gloss`. Defaults to `gloss` if not present. `matte` style only valid for `i4_case`, `i5_case`, `i5c_case`, `i6_case`, `i6s_case`, `i6plus_case`, `i6splus_case`, `samsung_s4_case`, `samsung_s5_case`, `samsung_s6_case` , `samsung_s6e_case`, `samsung_s7_case` and `samsung_s7e_case`.

## Ordering DTG apparel

> Example Order Request

```shell
curl "[[api_endpoint]]/v4.0/print/" \
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
    "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
    },
    "jobs": [{
      "options": {
        "garment_size": "M",
        "garment_color": "white"
      },
      "assets": {
        "center_chest": "http://psps.s3.amazonaws.com/sdk_static/1.jpg"
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

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

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
American Apparel Mens T-Shirt<span class="attribute-type">aa_mens_tshirt</span> | The softest, smoothest, best-looking short sleeve tee shirt available anywhere! Fine Jersey (100% Cotton) construction (Heather Grey contains 10% Polyester) • Durable rib neckband
American Apparel Womens T-Shirt<span class="attribute-type">aa_womens_tshirt</span> |  A classic cut ladies t shirt that suits all ages and can be worn in lots of ways. The fabric of this t-shirt is ultra-soft and it is slim fitted with a durable rib neckline. Fabric: 100% Cotton
American Apparel Zip Fleece Hoodie<span class="attribute-type">aa_zip_hoodie</span> | A bestselling fitted hooded top by this favourite America brand. Features a full white zip, white draw cords and kangaroo pouch pockets. Fabric: 50% Cotton 50% Polyester
American Apparel Fleece Pullover Hoodie<span class="attribute-type">aa_fleece_pullover_hoodie</span> | The American Apparel Unisex Fleece Pullover Hoody is a unisex hoodie which is both a warm and comfortable piece of clothing. Raglan cut sleeves, ribbed cuffs and hem. Fabric: 100% Cotton
American Apparel Fine Jersey Zip Hoodie <span class="attribute-type">aa_fine_zip_hoodie</span> | A lightweight fine jersey hoody with a matching nylon zipper closure and a matching finished polyester drawcord. Kangaroo pockets. Fabric : 100% Cotton
American Apparel Tank Top  <span class="attribute-type">aa_tank_top</span> |  A bright and fashionable jersey tank, which suits customers old and young. It is soft and comfortable to wear. It is sleeveless and hangs loosely; it has contrasting piping round the neck and arm openings. Fabric: 100% Cotton
AWD Hooded Sweatshirt  <span class="attribute-type">awd_hooded_sweatshirt</span> |  The AWDis College Hoodie boasts twin needle stitching detailing, a double fabric hood, and self coloured cords. Also with a ribbed cuff and hem and a kangaroo pouch pocket containing an opening for earphone cord feed. Fabric: 80% Cotton / 20% Polyester (280gsm).
AWD Ladies Tank Top  <span class="attribute-type">awd_ladies_tank_top</span> |  The Girlie Cool Vest from AWD is tailor made to fit the contours of the female form and comes a range of fantastic colours. There is a curved back hem for extra comfort  and AWDis's own Neoteric textured fabric has great wicking properties.  Fabric: 100% Polyester.
AWD Men's Muscle Vest <span class="attribute-type">awd_mens_muscle_vest</span> | Gym fit. Thin shoulder straps, for ease of movement. AWDis's own NeotericTM textured fabric with inherent wickability. Straight front and back hem. Fabric: 100% Polyester.
Gildan Adult Cotton T-Shirt  <span class="attribute-type">gildan_adult_cotton_tshirt</span> |  High quality Gildan t-shirt which keeps it's shape wash after wash. Taped neck and shoulders with a quarter turn to eliminate centre crease. Fabric 100% Cotton
Gildan Adult Dryblend Crew Neck Sweatshirt  <span class="attribute-type">gildan_dry_blend_sweatshirt</span> | Air Jet yarn, softer feel and no pilling. DryBlend wicking performance. Heat transfer label. Twin needle stitching. 1x1 athletic rib with Spandex. Quarter turned to eliminate centre crease.
Gildan Adult Full Zip Hooded Sweatshirt  <span class="attribute-type">gildan_zip_hooded_sweatshirt</span> | The Gildan HeavyBlend Adult Full Zip Hoodie features an unlined hood with matching drawstring, double-needle stitching, and set-in sleeves. Fabric: 50% Cotton, 50% Polyester
Gildan Adult Hooded Sweatshirt  <span class="attribute-type">gildan_hooded_sweatshirt</span> | The Gildan HeavyBlend Adult Hoodie features a double lined hood with matching drawstring, pouch pocket, and twin needle stitching. Fabric: 50% Cotton, 50% Polyester
Gildan Heavyblend Adult Crew Neck Sweatshirt  <span class="attribute-type">gildan_heavy_blend_sweatshirt</span> | The Gildan HeavyBlend Adult Crew Neck Sweatshirt is manufactured with an Air Jet yarn which gives a much softer feel and no pilling even after extended use. Constructed with double needle stitching, 1x1 athletic rib with Spandex & Quarter turned to eliminate centre crease. Fabric: 50% Cotton, 50% Polyester
Gildan Soft Style Tank Top  <span class="attribute-type">gildan_tank_top</span> | Gildan Soft Style Tank Top has deluxe 30's Softstyle yarns, wide straps and a rib knit trim applied to neckline and armholes. Twin needle bottom hem. Quarter-turned to eliminate centre crease. Fabric: 100% Cotton

### Required Options Arguments

          | |
--------- | -----------
garment_size<span class="required-argument">required</span> | The size of garment you want created. Must be one of the following: `S`, `M`, `L`, `XL`, `XXL` corresponding to small, medium, large, extra large & extra extra large respectively
garment_color<span class="required-argument">required</span> | The base material/fabric colour of the garment you want created. See our [available garment colors table](#available-garment-colours) to review fabric colours.

### Available Garment Colours

<table class="apparel-positions">
    <thead>
		<tr>
			<th>Color</th>
			<th></th>
			<th>Hexadecimal Code</th>
		</tr>
	</thead>
	<tbody>
	    <tr>
			<td>Blue</td>
			<td> <span style="background-color:#004EA8">&nbsp&nbsp&nbsp&nbsp</span></td>
			<td>004EA8</td>
		</tr>
	    <tr>
			<td>Light Blue</td>
			<td> <span style="background-color:#A3B3CB">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>A3B3CB</td>
		</tr>
		<tr>
			<td>Navy</td>
			<td>  <span style="background-color:#263147">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>263147</td>
		</tr>
		<tr>
			<td>Carolina Blue</td>
			<td> <span style="background-color:#7BA4DB">&nbsp&nbsp&nbsp&nbsp</span></td>
			<td>7BA4DB</td>
		</tr>
		<tr>
			<td>Airforce Blue</td>
			<td> <span style="background-color:#486682">&nbsp&nbsp&nbsp&nbsp</span></td>
			<td>486682</td>
		</tr>
        <tr>
			<td>Coral</td>
			<td> <span style="background-color:#FF5A60">&nbsp&nbsp&nbsp&nbsp</span></td>
			<td>FF5A60</td>
		</tr>
		<tr>
			<td>Baby Pink</td>
			<td><span style="background-color:#E8BCD1">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>E8BCD1</td>
		</tr>
		<tr>
			<td>Red</td>
			<td> <span style="background-color:#D60024">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>D60024</td>
		</tr>
		<tr>
			<td>Cherry Red</td>
			<td> <span style="background-color:#AC2B37">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>AC2B37</td>
		</tr>
		<tr>
			<td>Truffle</td>
			<td> <span style="background-color:#6C333A">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>6C333A</td>
		</tr>
		<tr>
			<td>Brick Red</td>
			<td><span style="background-color:#560B14">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>560B14</td>
		</tr>
		<tr>
			<td>Maroon</td>
			<td><span style="background-color:#5B2B42">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>5B2B42</td>
		</tr>
		<tr>
			<td>Purple</td>
			<td><span style="background-color:#5B2B42">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>531D8A</td>
		</tr>
		<tr>
			<td>Yellow</td>
			<td> <span style="background-color:#FBDE4A">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>EDD35E</td>
		</tr>
		<tr>
			<td>Sunshine</td>
			<td> <span style="background-color:#FBDE4A">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>FBDE4A</td>
		</tr>
        <tr>
			<td>Gold</td>
			<td><span style="background-color:#EEAD1A">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>EEAD1A</td>
		</tr>
		<tr>
			<td>Dark Heather</td>
			<td> <span style="background-color:#3F4444">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>3F4444</td>
		</tr>
		<tr>
			<td>Green</td>
			<td><span style="background-color:#1C704D">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>1C704D</td>
		</tr>
		<tr>
			<td>Kelly Green</td>
			<td> <span style="background-color:#00805E">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>00805E</td>
		</tr>
		<tr>
			<td>Grass</td>
			<td><span style="background-color:#5AAD52">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>5AAD52</td>
		</tr>
		<tr>
			<td>Peppermint</td>
			<td><span style="background-color:#8CD2BF">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>8CD2BF</td>
		</tr>
		<tr>
			<td>Ash</td>
			<td> <span style="background-color:#D4D3D9">&nbsp&nbsp&nbsp&nbsp</span> </td>
			<td>D4D3D9</td>
		</tr>
		<tr>
			<td>Heather Grey</td>
			<td><span style="background-color:#ADBDBF">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>ADBDBF</td>
		</tr>
		<tr>
			<td>Charcoal</td>
			<td><span style="background-color:#66676C">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>66676C</td>
		</tr>
		<tr>
			<td>Grey</td>
			<td><span style="background-color:#B0B0B2">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>B0B0B2</td>
		</tr>
		<tr>
			<td>Asphalt</td>
			<td><span style="background-color:#353146">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>353146</td>
		</tr>
		<tr>
			<td>Jet Black</td>
			<td><span style="background-color:#1A2424">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>1A2424</td>
		</tr>
		<tr>
			<td>Black</td>
			<td><span style="background-color:#25282B">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>25282B</td>
		</tr>
		<tr>
			<td>White</td>
			<td><span style="background-color:#FFFFFF">&nbsp&nbsp&nbsp&nbsp</span>  </td>
			<td>FFFFFF</td>
		</tr>
	</tbody>
</table>


### Available Print Areas

<table class="apparel-positions">
    <thead>
		<tr>
			<th>Position</th>
			<th></th>
			<th>Dimensions</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>center_chest<span class="optional-argument">optional</span></td>
			<td class="img-tshirt"><img alt="T-Shirt Print API Centre Chest" src="{% static "docs/images/centre_chest.jpg" %}"></td>
			<td>2100 x 2400 px (30x40cm) </td>
		</tr>
		<tr>
			<td>center_back<span class="optional-argument">optional</span></td>
			<td class="img-tshirt"><img alt="T-Shirt Print API Centre Back" src="{% static "docs/images/centre_back.jpg" %}"></td>
			<td>2100 x 2400 px (30x40cm)</td>
		</tr>
	</tbody>
</table>


### Assets Position Arguments

All apparel orders must be made with options and sizes that correspond to the product ordered as detailed in the below table.

<table class="apparel-positions">
	<thead>
		<tr>
			<th>Product Template</th>
			<th>Applicable Positions </th>
			<th>Available Colors</th>
            <th>Available Sizes</th>
		</tr>
	</thead>
	<tbody>
		<tr>
		    <td>
		        <code class="prettyprint">aa_mens_tshirt</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black, white, heather_grey
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">aa_womens_tshirt</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black, white, heather_grey
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">aa_zip_hoodie</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black, white
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">aa_tank_top</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black, white, red, heather_grey, navy, coral, sunshine, grass
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">aa_fleece_pullover_hoodie</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  grey, navy, truffle, kelly_green, asphalt
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">aa_fine_zip_hoodie</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black, white
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">gildan_adult_cotton_tshirt	</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black, white, grey
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">gildan_tank_top</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  red, white, heather_grey, navy, charcoal
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">gildan_hooded_sweatshirt</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  cherry_red, carolina_blue, black, gold, charcoal
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">gildan_dry_blend_sweatshirt</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black, blue, green, grey, red
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">gildan_heavy_blend_sweatshirt</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black, blue, green, grey, red
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">gildan_zip_hooded_sweatshirt</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black, dark_heather, maroon, navy, carolina_blue, ash
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">awd_hooded_sweatshirt</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  heather_grey, ash, gold, airforce_blue, baby_pink, peppermint, jet_black, brick_red
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">awd_ladies_tank_top</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  white, yellow, purple, sapphire_blue
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">awd_mens_muscle_vest</code>
            </td>
			<td>center_chest, center_back</td>
			<td>
			  black
			</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
	</tbody>
</table>


## Ordering sublimation apparel

> Example Order Request

```shell
curl "[[api_endpoint]]/v4.0/print/" \
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
    "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
    },
    "jobs": [{
      "options": {
        "garment_size": "M"
      },
      "assets": {
        "front_image": "http://psps.s3.amazonaws.com/sdk_static/1.jpg",
        "back_image": "http://psps.s3.amazonaws.com/sdk_static/2.jpg"
      },
      "template_id": "awd_sublimation_tshirt"
    }]
  }'
```

```objective_c
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
#import <Kite-Print-SDK/OLKitePrintSDK.h>

NSArray *assets = @{
    @"front_image": [OLAsset assetWithURL:[NSURL URLWithString:@"http://psps.s3.amazonaws.com/sdk_static/1.jpg"]]
};

id<OLPrintJob> tshirt = [OLPrintJob printJobWithTemplateId:@"awd_sublimation_tshirt" OLAssets:assets];
[tshirt setValue:@"M" forOption:@"garment_size"];

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
assets.put("front_image", new Asset(new URL("http://psps.s3.amazonaws.com/sdk_static/1.jpg"))));

PrintJob tshirt = PrintJob.createPrintJob(assets, "awd_sublimation_tshirt");
tshirt.setOption("garment_size", "M");

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

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

> Example Response

```shell
{
  "print_order_id": "PS96-996634811"
}
```


If you haven't already, see [Placing orders](#placing-orders) for a general overview of the order request & response which is applicable to all product orders.

Sublimation printing allows for an image asset to be printed anywhere on the entire garment and is well suited to printing of patterned designs. All t-shirts are printed on a white t-shirts and are made of 100% Polyester which ensures the best colour transfer to the garment during the printing process.

The example request on the right would result in a sublimation t-shirt being created (with a front and back image) and shipped to the specified address.

Many more products and brands available in the very near future.

### products & template_ids

          | |
--------- | -----------
AWD Sublimation T-Shirt<span class="attribute-type">awd_sublimation_tshirt</span> | Just Sub shirts are made from 175 gsm 100% Polyester Jersey fabric durable enough to do justice to a permanent printing process. They retain all of the advantages of quick drying, easy care polyester, but when Sublimation printed at 190-200 degrees Centigrade exhibit minimal and very acceptable levels of marking which all but disappear in steaming or washing,
AWD Kids Sublimation T-Shirt<span class="attribute-type">awd_kids_sublimation_tshirt</span> | Just Sub shirts are made from 175 gsm 100% Polyester Jersey fabric durable enough to do justice to a permanent printing process. They retain all of the advantages of quick drying, easy care polyester, but when Sublimation printed at 190-200 degrees Centigrade exhibit minimal and very acceptable levels of marking which all but disappear in steaming or washing,
Subli Sublimation T-Shirt<span class="attribute-type">roly_sublimation_tshirt</span> | Short sleeve t-shirt with ribbed round collar in the same fabric and side seams. Made of polyester fabric with cotton touch. 100% polyester, cotton touch, 140 gsm.
American Apparel Sublimation T-shirt<span class="attribute-type">aa_sublimation_tshirt</span> | A comfortable and lightweight 100% Polyester T-shirt with Durable rib neckband. Made of a fine count yarn giving superior sublimation results
American Apparel Sublimation Vest<span class="attribute-type">aa_sublimation_vest</span> | Our American Apparel Unisex sublimation tanks are 100% polyester jersey tanks designed especially for sublimation. Ultra-soft to touch and are sleeveless with a scooped neck.

### Required Options Arguments

          | |
--------- | -----------
garment_size<span class="required-argument">required</span> | The size of garment you want created. Must be one of the following for adult apparel: `S`, `M`, `L`, `XL`, `XXL` corresponding to small, medium, large, extra large & extra extra large respectively. Alternate sizing options are detailed for childrens apparel below.


### Available Print Areas

<table class="apparel-positions">
    <thead>
		<tr>
			<th>Position</th>
			<th></th>
			<th>Dimensions</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>front_image<span class="optional-argument">optional</span></td>
			<td></td>
			<td>4500 x 3985 px (76x67cm) </td>
		</tr>
		<tr>
			<td>back_image<span class="optional-argument">optional</span></td>
            <td></td>
			<td>4500 x 3985 px (76x67cm) </td>
		</tr>
	</tbody>
</table>


### Assets Position Arguments

All apparel orders must be made with options and sizes that correspond to the product ordered as detailed in the below table.

<table class="apparel-positions">
	<thead>
		<tr>
			<th>Product Template</th>
			<th>Applicable Positions </th>
            <th>Available Sizes</th>
		</tr>
	</thead>
	<tbody>
		<tr>
		    <td>
		        <code class="prettyprint">awd_sublimation_tshirt</code>
            </td>
			<td>front_image, back_image</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">awd_kids_sublimation_tshirt</code>
            </td>
			<td>front_image, back_image</td>
			<td>
			    3to4, 5to6, 7to8, 9to10, 12to13
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">roly_sublimation_tshirt</code>
            </td>
			<td>front_image, back_image</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">aa_sublimation_tshirt</code>
            </td>
			<td>front_image, back_image</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
		<tr>
		    <td>
		        <code class="prettyprint">aa_sublimation_vest</code>
            </td>
			<td>front_image, back_image</td>
			<td>
			    s,m,l,xl
			</td>
		</tr>
	</tbody>
</table>


## Ordering photobooks

> Example Order Request (JSON route)

```shell
curl "[[api_endpoint]]/v4.0/print/" \
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
   "customer_email": "deon@kite.ly",
   "customer_phone": "+44 (0)784297 1234",
   "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
   },
   "jobs": [{
      "template_id": "rpi_wrap_280x210_sm",
      "assets": {
      	 "front_cover": "https://s3.amazonaws.com/sdk-static/TestImages/front.png",
      	 "back_cover": "https://s3.amazonaws.com/sdk-static/TestImages/back.png",      	
         "pages": [
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/1.png"
            }, 
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/2.png"
            },
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/3.png"
            },
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/4.png"
            },         
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/5.png"
            },         
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/6.png"
            },         
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/7.png"
            },                                                         
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/8.png"
            },   
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/9.png"
            },   
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/10.png"
            },   
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/11.png"
            }, 
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/12.png"
            },
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/13.png"
            },
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/14.png"
            },         
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/15.png"
            },         
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/16.png"
            },         
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/17.png"
            },                                                         
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/18.png"
            },   
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/19.png"
            },   
            {
               "layout": "single_centered",
               "asset": "https://s3.amazonaws.com/sdk-static/TestImages/20.png"
            }
         ]
      }
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

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

> Example Response

```shell
{
  "print_order_id": "PS96-996634811"
}
```


If you haven't already, see [Placing orders](#placing-orders) for a general overview of the order request & response which is applicable to all product orders. 

There are two options for ordering photobooks: (1) via our JSON representation or (2) using pre-constructed PDFs.

### Photobook JSON representation 

The easiest approach for placing photo book orders is to describe the book using our JSON interface. 
In this way, you can define the layouts and photos for each page without actually creating the PDF yourself.
 
The first example request on the right would result in a hardcover landscape photobook being created and shipped to the specified address.

### assets object
          | |
--------- | -----------
front_cover | An image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. This image will be used as the front cover.
back_cover | An image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. This image will be used as the back cover.
pages<span class="required-argument">required</span> | An array of page objects. You must submit at least 20 pages. Thereafter, you may increment the count in multiples of 4.

### page object
          | |
--------- | -----------
layout<span class="required-argument">required</span> | String name of one of the supported layouts.
asset<span class="required-argument">required</span> | An image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite.

### Supported layouts
          | |
--------- | -----------
single_centered | A single image taking up the entire page.

*More layouts coming soon!*

### Photobook PDF route

> Example Order Request (PDF route)

```shell
curl "[[api_endpoint]]/v4.0/print/" \
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
   "customer_email": "deon@kite.ly",
   "customer_phone": "+44 (0)784297 1234",
   "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
   },
   "jobs": [{
      "template_id": "rpi_wrap_280x210_sm",
      "assets": {
      	 "inside_pdf": "https://s3.amazonaws.com/sdk-static/TestImages/inside.pdf",
      	 "cover_pdf": "https://s3.amazonaws.com/sdk-static/TestImages/cover.pdf"   	
      }
   }]
}'
```

You may want more flexibility in designing your book, in which case you can send through a pre-made PDF.
You will need to send through two PDFs, one for the inner block of pages and one for the front/back cover spread.
It is important that your PDFs match the sizes in the below specs exactly:

[Book Specifications](https://s3-eu-west-1.amazonaws.com/co.oceanlabs.ps/kite_book_specs.pdf)

[Cover Example](https://s3-eu-west-1.amazonaws.com/co.oceanlabs.ps/kite_cover_example.pdf)


### products & template_ids

          | |
--------- | -----------
Landscape Hardcover<span class="attribute-type">rpi_wrap_280x210_sm</span> | 28cm x 21cm hardcover landscape photobook. Our books are perfectly bound with images printed on glossy 200gsm paper
Portrait Hardcover<span class="attribute-type">rpi_wrap_210x280_sm</span> | 21cm x 28cm hardcover portrait photobook. Our books are perfectly bound with images printed on glossy 200gsm paper
Small Square Hardcover<span class="attribute-type">rpi_wrap_140x140_sm</span> | 14cm x 14cm hardcover square photobook. Our books are perfectly bound with images printed on glossy 200gsm paper
Medium Square Hardcover<span class="attribute-type">rpi_wrap_210x210_sm</span> | 21cm x 21cm hardcover square photobook. Our books are perfectly bound with images printed on glossy 200gsm paper
Large Square Hardcover<span class="attribute-type">rpi_wrap_300x300_sm</span> | 30cm x 30cm hardcover square photobook. Our books are perfectly bound with images printed on glossy 200gsm paper

### assets object
          | |
--------- | -----------
inside_pdf | An image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. This image will be used as the inside block.
cover_pdf | An image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. This image will be used as the front / back cover spread.


## Ordering postcards

> Example Order Request

```shell
curl "[[api_endpoint]]/v4.0/print/" \
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
    "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
    },
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

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

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
curl "[[api_endpoint]]/v4.0/print/" \
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
    "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
    },
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

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

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

## Ordering invitations

> Example Order Request

```shell
curl "[[api_endpoint]]/v4.0/print/" \
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
    "customer_payment": {
      "amount": 3.99,
      "currency": "USD"
    },
    "jobs": [{
      "assets": {
        "front_image": "https://s3.amazonaws.com/kite-samples/invitation/front.png",
        "back_image": "https://s3.amazonaws.com/kite-samples/invitation/back.png"
      },
      "template_id": "square_invitations_15x15cm"
    }]
  }'
```

```objective_c
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions
// See https://github.com/OceanLabs/iOS-Print-SDK#custom-user-experience for full step by step instructions

```

```java
// See https://github.com/OceanLabs/Android-Print-SDK#custom-checkout for full step by step instructions

```

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

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
Square Invitation <span class="attribute-type">square_invitations_15x15cm</span> | Double sided square invitation printed on 350gsm quality gloss card. Shipped within an addressed envelope and dispatched worldwide.
Square Invitation 10 pack <span class="attribute-type">square_invitations_15x15cm_10pack</span> | Pack of 10 double sided square invitation printed on 350gsm quality gloss card. Shipped within an addressed envelope and dispatched worldwide.

### Assets Arguments

          | |
--------- | -----------
front_image<span class="required-argument">required</span> | A image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. It will form the front of the invitation.
back_image<span class="required-argument">required</span> | A image URL accessible to the Kite servers or an [asset object](#the-asset-object) identifier that you have received by [uploading an asset](#uploading-an-asset) to Kite. It will form the front of the invitation.


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

<div class="optional-asset-dimensions" ng-show="isPhotoboxUser">
<h3 id="optimal-photobox-asset-dimensions">OPTIMAL PHOTOBOX ASSET DIMENSIONS</h3>
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

<div class="optional-asset-dimensions" ng-show="isAlbelliUser">
<h3 id="optimal-albelli-asset-dimensions">OPTIMAL ALBELLI ASSET DIMENSIONS</h3>
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


# Orders

It's easy to fetch the list of orders and associated order details that you or your customers are placing against the Kite platform. 

## Getting a list of orders


> Example Order List Request

```shell
curl "[[api_endpoint]]/v4.0/order/?order_by=-time_submitted&test_order=false&error_exclude=true" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>"
```

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

> Example Order List Response

```shell
{
  "meta": {
    "limit": 20,
    "next": "/v4.0/order/?offset=20&limit=20",
    "offset": 0,
    "previous": null,
    "total_count": 960914
  },
  "objects": [
    {
      "attributed_to_notification": null,
      "customer_email": "deon@kite.ly",
      "customer_payment": {
        "amount": "25.59",
        "currency": "GBP",
        "formatted": "£25.59"
      },
      "jobs": [
        "/v4.0/job/36819/"
      ],
      "order_id": "PS243-825654811",
      "person_id": 71283,
      "refund_request": null,
      "resource_uri": "/v4.0/order/PS243-825654811/",
      "status": "Processed",
      "test_order": false,
      "time_processed": "2015-08-31T13:09:01.670462",
      "time_submitted": "2015-08-31T13:09:01.670462"
    },
    ...
  ]
}
```

### HTTP Request

`GET [[api_endpoint]]/v4.0/order/`

### Arguments

          | |
--------- | -----------
order_by<span class="maybe-argument">optional</span> | Controls the ordering of the returned orders, valid options are `time_submitted` & `status`. A `-` can be added to the front of any option i.e. `-time_submitted` to reverse the ordering.
test_order<span class="maybe-argument">optional</span> | If `true` then the results will be be filtered to only include test orders, if `false` then only live orders will be returned
error_exclude<span class="maybe-argument">optional</span> | If `true` then results will be filtered to only include successful orders, if `false` then only orders for which an error has occured will be returned
refund_requested<span class="maybe-argument">optional</span> | If `true` then results will be filtered to only include orders for which the customer has requested a refunded, if `false` then only orders for which there has been no refund request
time_submitted__lte<span class="maybe-argument">optional</span> | An ISO 8601 UTC formatted date time value i.e. `2016-03-23T11:01:28.710Z`. Orders will be filtered to only include those that were placed _before_ this date & time
time_submitted__gte<span class="maybe-argument">optional</span> | An ISO 8601 UTC formatted date time value i.e. `2016-03-23T11:01:28.710Z`. Orders will be filtered to only include those that were placed _after_ this date & time

### Returns
Returns a list of optionally filtered orders

## Getting an order's status


> Example Order Detail Request

```shell
curl "[[api_endpoint]]/v4.0/order/PS320-236374811" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>"
```

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

> Example Order Detail Response

```shell
{
  "jobs": [
    {
      "job_id": "PS320-23637481101-S9-MAGNETS-M",
      "shipped_time": null,
      "status": "Received by Printer",
      "template": {
        "id": "s9_magnets_mini",
        "name": "Medium Photo Magnets"
      }
    }
  ],
  "order_id": "PS320-236374811",
  "status": "Processed",
  "test_order": false,
  "time_processed": "2015-11-16T20:04:12.209495",
  "time_submitted": "2015-11-16T20:04:12.209495"
}
```

### HTTP Request

`GET [[api_endpoint]]/v4.0/order/<order_id>`

### Arguments

          | |
--------- | -----------
order_id<span class="required-argument">required</span> | The kite order id received in the response of a previous [order submission](#placing-orders)

### Returns
An order object detailing the order

# Shipping Methods

Within versions of the Kite API v4.0 and upwards, it is possible to place orders with particular expedited and tracked shipping methods.

Each product has a 'Standard' shipping class which in most cases will be an untracked delivery. Tracked and expedited delivery for a product can be retrieved from Kite and placed within the print order request to enable alternative shipping methods.

## Getting shipping options for a product

> Example Product response

```shell
curl "[[api_endpoint]]/v4.0/shipping_methods/a3_poster" \
  -H "Authorization: ApiKey [[public_key]]:"
```

> Example Shipping Response

```shell
{
  "shipping_classes": {
    "ROW": [
      {
        "class_name": "International Tracked",
        "costs": [
          {
            "amount": 6.35,
            "currency": "USD"
          },
          {
            "amount": 5.96,
            "currency": "EUR"
          },
          {
            "amount": 5.22,
            "currency": "GBP"
          }
        ],
        "display_name": "Royal Mail",
        "id": 2,
        "max_delivery_time": 10,
        "min_delivery_time": 3,
        "tracked": true
      },
      {
        "class_name": "Standard",
        "costs": [
          {
            "amount": 2.91,
            "currency": "USD"
          },
          {
            "amount": 2.73,
            "currency": "EUR"
          },
          {
            "amount": 2.39,
            "currency": "GBP"
          }
        ],
        "display_name": "Guernsey Post",
        "id": 1,
        "max_delivery_time": 10,
        "min_delivery_time": 3,
        "tracked": false
      }
    ],
    "UK": [
      {
        "class_name": "UK Signed",
        "costs": [
          {
            "amount": 6.35,
            "currency": "USD"
          },
          {
            "amount": 5.96,
            "currency": "EUR"
          },
          {
            "amount": 5.22,
            "currency": "GBP"
          }
        ],
        "display_name": "Royal Mail",
        "id": 3,
        "max_delivery_time": 2,
        "min_delivery_time": 1,
        "tracked": true
      },
      {
        "class_name": "Standard",
        "costs": [
          {
            "amount": 2.91,
            "currency": "USD"
          },
          {
            "amount": 2.73,
            "currency": "EUR"
          },
          {
            "amount": 2.39,
            "currency": "GBP"
          }
        ],
        "display_name": "Guernsey Post",
        "id": 1,
        "max_delivery_time": 3,
        "min_delivery_time": 1,
        "tracked": false
      }
    ]
  },
  "shipping_regions": {
    "ABW": "ROW",
    "FLK": "ROW",
    "FRA": "ROW",
    "FRO": "ROW",
    "FSM": "ROW",
    "GAB": "ROW",
    "GBR": "UK",
    "GEO": "ROW",
    "GGY": "ROW",
    "GHA": "ROW",
    "GIB": "ROW",
    "GIN": "ROW",
    "GLP": "ROW",
    "GMB": "ROW",
    "USA": "ROW",
  },
  "template_id": "a3_poster",
}
```

### HTTP List Request

`GET [[api_endpoint]]/v4.0/shipping_methods/`

### HTTP Detail Request

`GET [[api_endpoint]]/v4.0/shipping_methods/<template_id>`

### Returns
Returns a list of shipping options for the product. The shipping methods available are dependent on the destination country that you want to send the order too.

### Determining your shipping region

The shipping region of your destination country can be found by looking up it's 3 letter ISO country code within the `shipping_regions` dictionary of the response.

In the example on the right, a delivery to the United States ("USA") would fall within the "ROW" shipping region while a delivery to the United Kingdom ("GBR") would fall in the "GB" shipping region.

## Retrieving available shipping methods

The available shipping methods to that country can then be looked up within the `shipping_classes` field of the shipping response.

The available shipping methods for a delivery to the United States (which is in the "ROW" shipping region) is shown on the right.

In this case there are two available options, International Tracked and Standard shipping.

### Shipping response fields

> Example Shipping Classes available for a delivery to the United States

```shell
{
  "shipping_classes": {
    "ROW": [
      {
        "class_name": "International Tracked",
        "costs": [
          {
            "amount": 6.35,
            "currency": "USD"
          },
          {
            "amount": 5.96,
            "currency": "EUR"
          },
          {
            "amount": 5.22,
            "currency": "GBP"
          }
        ],
        "display_name": "Royal Mail",
        "id": 2,
        "max_delivery_time": 10,
        "min_delivery_time": 3,
        "tracked": true
      },
      {
        "class_name": "Standard",
        "costs": [
          {
            "amount": 2.91,
            "currency": "USD"
          },
          {
            "amount": 2.73,
            "currency": "EUR"
          },
          {
            "amount": 2.39,
            "currency": "GBP"
          }
        ],
        "display_name": "Guernsey Post",
        "id": 1,
        "max_delivery_time": 10,
        "min_delivery_time": 3,
        "tracked": false
      }
    ],
  },
}
```

          | |
--------- | -----------
id | The unique identifier of that shipping method
costs | A dictionary of the associated postage cost of placing a order with that shipping method.
display_name| The name of the mail carrier. Example carriers include Royal Mail, USPS or FedEx.
tracked| Whether the delivery method includes order tracking. Tracking details can be retrieved once the order is dispatched from the Orders endpoint.
min_delivery_time| The estimated earliest delivery time (in working days) once the order has been dispatched.
max_delivery_time| The estimated latest delivery time (in working days) once the order has been dispatched.

## Placing an order with a specified shipping method

> Example Order Request

```shell
curl "[[api_endpoint]]/v4.0/print/" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>" \
  --data '{
    "shipping_address": {
    "recipient_name": "Deon Botha",
    "address_line_1": "The White House",
    "address_line_2": "1600 Pennsylvania Ave NW",
    "city": "Washington",
    "county_state": "Washington D.C",
    "postcode": "20500",
    "country_code": "USA"
    },
    "customer_email": "[[user_email]]",
    "customer_phone": "+44 (0)784297 1234",
    "customer_payment": {
      "amount": 29.99,
      "currency": "USD"
    },
    "jobs": [{
      "assets": ["http://psps.s3.amazonaws.com/sdk_static/2.jpg"],
      "shipping_class": 2,
      "template_id": "a3_poster"
    }]
  }'
```

By default, orders placed for products will default to it's `Standard` shipping method. However you can specify an alternate shipping method if it exists for delivery to your destination country.

For example the request on the right would result in an A3 Poster being created and shipped to the United States using the `International Tracked` shipping method.

If an incorrect shipping_class is included within the order request that does not correspond to any available methods for that product, the job will fall back to the default `Standard` shipping method without raising an error.

The job object is covered in more detail within the [job objects](#the-job-object) section of the documentation.

### Specifying the shipping method with the job object

          | |
--------- | -----------
id <span class="optional-argument">optional </span> | The unique identifier of the shipping method that you would like to use for your ordered product


# Customers

Rich customer profiles are built automatically for you when you or your users place an order. Our powerful filtering tools then allow you to segment your user base in all kinds of ways - to the point where you can single out individual users if you want.

## Getting a list of people


> Example Customer List Request

```shell
curl "[[api_endpoint]]/v4.0/person/?customer=true" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>"
```

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

> Example Customer List Response

```shell
{
  "meta": {
    "limit": 20,
    "next": "/v4.0/person/?customer=true&limit=20&offset=20",
    "offset": 0,
    "previous": null,
    "total_count": 44737
  },
  "objects": [
    {
      "address": {
        "city": "London",
        "country": "United Kingdom",
        "country_code": "GBR",
        "county_state": "Kent",
        "line1": "27-28 Eastcastle House",
        "line2": "Eastcastle Street",
        "line3": "",
        "line4": "",
        "postcode": "W1W 8DH",
        "recipient_name": "Deon Botha"
      },
      "country": {
        "country_code_2": "GB",
        "country_code_3": "GBR",
        "id": 13,
        "name": "United Kingdom",
        "resource_uri": "/v2.1/country/13/"
      },
      "created": "2016-02-27T22:45:28.629607",
      "email": "deon@kite.ly",
      "first_name": "Deon",
      "full_name": "Deon Botha",
      "id": 530395,
      "ip": "86.185.46.67",
      "last_name": "Botha",
      "last_seen": "2016-02-27T22:45:37.283464",
      "live_person": true,
      "meta_data": "{u'environment': u'Live', u'platform': u'iOS', u'Order Count': 1}",
      "orders": [
        "PS58-942265811"
      ],
      "phone": "",
      "region": "United Kingdom",
      "resource_uri": "/v2.1/person/530395/",
      "revenue": {
        "amount": "22.99",
        "currency": "GBP"
      },
      "timezone": "Europe/London",
      "timezone_utc_offset": 0,
      "uuid": "7EFB2CA8-8EFB-4FC3-88AB-2F02E6003731"
    },
    ...
    ]
}
```

### HTTP Request

`GET [[api_endpoint]]/v4.0/person/`

### Arguments

          | |
--------- | -----------
customer<span class="maybe-argument">optional</span> | If `true` then the resulting people list will be filtered to only include those who have placed an order, if `false` then the resulting list will only include people who have not placed an order
country<span class="maybe-argument">optional</span> | A comma separated list of 3 digit country codes i.e. `GBR,USA` that will filter the resulting person list to only include people coming from the specified countries
order_count__gt<span class="maybe-argument">optional</span> | Filters the resulting list to only include customers who have ordered more than the specified number of times
order_count__lt<span class="maybe-argument">optional</span> | Filters the resulting list to only include customers who have ordered less than the specified number of times
last_ordered_date__lt<span class="maybe-argument">optional</span> | Filters the resulting person list to only include people that have ordered more recently that the value. Valid values include `Ndays`, `Nweeks`, `Nmonths` where `N` is a number i.e. `last_ordered_date__lt=1days` will filter the resulting list to only include customers who ordered within the last 1 day
last_ordered_date__gt<span class="maybe-argument">optional</span> | Filters the resulting person list to only include people that have ordered less recently that the value. Valid values include `Ndays`, `Nweeks`, `Nmonths` where `N` is a number i.e. `last_ordered_date__gt=1days` will filter the resulting list to only include customers who have ordered more than 1 day ago
push_token__isset<span class="maybe-argument">optional</span> | If `true` filters the resulting list to only include people with push notification tokens, if `false` filters the resulting list to only include people without push notification tokens
created__lte<span class="maybe-argument">optional</span> | An ISO 8601 UTC formatted date time value i.e. `2016-03-23T11:01:28.710Z`. It filters the resulting list to only include those people created before the specified date time
live_person<span class="maybe-argument">optional</span> | If `true` filters the resulting person list to only include people created in the live environment, if `false` filters the resulting person list to only include people created in the test environment


### Returns
Returns a list of optionally filtered people

## Getting a person's details


> Example Person Detail Request

```shell
curl "[[api_endpoint]]/v4.0/person/?id=196" \
  -H "Authorization: ApiKey [[public_key]]:<your_secret_key>"
```

> Replace `<your_secret_key>` with the one found in the [credentials]([[website_endpoint]]/settings/credentials) section of the dashboard.<br /><br />

> Example Person Detail Response

```shell
{
  "meta": {
    "limit": 20,
    "next": null,
    "offset": 0,
    "previous": null,
    "total_count": 1
  },
  "objects": [
    {
      "address": {
        "city": "London",
        "country": "United Kingdom",
        "country_code": "GBR",
        "county_state": "",
        "line1": "Eastcastle House",
        "line2": "27-28 Eastcastle Street",
        "line3": "",
        "line4": "",
        "postcode": "W1W 8DH",
        "recipient_name": "Deon Botha"
      },
      "country": {
        "country_code_2": "GB",
        "country_code_3": "GBR",
        "id": 233,
        "name": "United Kingdom",
        "resource_uri": "/v2.1/country/233/"
      },
      "created": "2015-06-02T20:24:39.519890",
      "email": "deon@kite.ly",
      "first_name": "Deon",
      "full_name": "Deon Botha",
      "id": 196,
      "ip": "10.84.20.98",
      "last_name": "Botha",
      "last_seen": "2015-06-02T20:47:25.434205",
      "live_person": true,
      "meta_data": "{u'environment': u'Development', u'platform': u'iOS', u'Order Count': 2}",
      "orders": [
        "PS153-474134811",
        "PS153-374134811",
        "PS153-164134811",
        "PS153-064134811",
        "PS153-964134811",
        "PS153-864134811"
      ],
      "phone": "",
      "region": "London",
      "resource_uri": "/v2.1/person/196/",
      "revenue": {
        "amount": "180.84",
        "currency": "GBP"
      },
      "timezone": "Europe/London",
      "timezone_utc_offset": 0,
      "uuid": "DF944EDC-90BE-470B-914E-1250E8DD1585"
    }
  ]
}
```

### HTTP Request

`GET [[api_endpoint]]/v4.0/person/?id=<person_id>`

### Arguments

          | |
--------- | -----------
person_id<span class="required-argument">required</span> | The kite person id

### Returns
A person object



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
curl "[[api_endpoint]]/v4.0/address/search/?country_code=GBR&search_term=10+Downing+Street,London" \
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
curl "[[api_endpoint]]/v4.0/address/search/?country_code=GBR&address_id=GBR|PR|23747771|0|0|0||Retrieve" \
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

`GET [[api_endpoint]]/v4.0/address/search/`

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


# Webhooks

Kite allows partners to specify a remote URL to which they can receive status updates of orders placed by their customers. This allows our partners to maintain their own CRM (confirmation & dispatch e-mails, SMS services etc) or accounting systems that exist outside the Kite platform ecosystem.

When an order is placed and any of it's associated print jobs status is updated, we'll send a HTTP POST request to the partner's configured webhook URL. This request will be sent as a JSON payload that includes a range of information about the customer's order.


## Configuring Webhook

A webhook url can be added to your account within the [notifications]([[website_endpoint]]/settings/notifications) section of the dashboard.

Clicking Test Webhook within this section will trigger an example POST request, which will return a success if your endpoint responds with a HTTP 200 response.

Your endpoint should be configured to receive a JSON payload in the format shown on the right.


> Example JSON

```json
{
    "environment": "TEST",
    "time_submitted": "2016-5-1 23:12:30",
    "order_id" : "PS-KITE-WEBHOOK-TEST",
    "job_id" : "PS-KITE-WEBHOOK-TEST01-MS",
    "status" : "Shipped",
    "is_reprint": false,
    "product" : {
        "name": "Squares",
        "id": "squares"
    },
    "customer_details" : {
        "name": "Joe Bloggs",
        "email": "joe@bloggs.com"
    },
    "address": {
        "shipping_address_1": "123 Kite Avenue",
        "shipping_address_2": "",
        "shipping_address_3": "London",
        "shipping_address_4": "",
        "shipping_address_5": "",
        "shipping_postcode": "123 ABD",
        "shipping_country": "United Kingdom",
        "shipping_country_code": "GB"
    }
}
```

## Order status updates

A HTTP POST request will be triggered when a print job within an order is updated to one of the following status's :

### Job Status

 | |
--------- | -----------
Received by Printer | Your order has been received and is awaiting fulfilment
Shipped | Your customer's order has been dispatched and is on it's way
Cancelled | Your customer's order has been cancelled
On Hold | The fulfilment of your customer's order has been put on hold
Fulfilment failed | An error has occurred while processing your order. (See [errors](#errors))
