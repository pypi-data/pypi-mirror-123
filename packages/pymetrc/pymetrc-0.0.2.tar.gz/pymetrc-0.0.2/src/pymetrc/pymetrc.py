from datetime import datetime, timedelta
import urllib.parse
from .apicaller import APICaller

# Currently only utilizing the Montana state Metrc API. Future plans include ability to choose endpoint in a more
# effective manner.
API_BASE_URL = 'https://api-mt.metrc.com'


class Metrc:
    '''
    A class to represent a Metrc client object. Contained within is a both a vendor API key and a unique user API key
    required for authentication with the Metrc REST API service. This allows for segmentation if using with multiple
    keys which may be necessary for a variety of reasons.

    Parameters
    ----------
    vendor_api_key : str
        Software vendor API key provided by Metrc upon validating that correct queries can be made.
    user_api_key : str
        API key tied to an individual which allows for access control and permissions for various subsets of related
        tasks within the state traceability system.

    Attributes
    ----------
    endpoints : dict
        Contains endpoint type (key) and a list of the associated endpoint url stubs (value). Several contain "{id}"
        which is modified via a string replace method to insert individual IDs.
    vendor_api_key : str
        Description in Parameters section above.
    user_api_key : str
        Description in Parameters section above.
    facility_data : list[dict]
        Facilities and all associated information as returned via the API.
    facilities : list[str]
        Facilities parsed from facility_data for easy access.
    dispensaries : list[str]
        Facilities that are identified as dispensaries.
    mipps : list[str]
        Facilities that are identified for manufacturing and processing.
    '''

    def __init__(self, vendor_api_key, user_api_key):
        # As states can dictate the features available to clients, future plans include the abiltiy to dynamically
        # provide a list of valid endpoints.
        self.endpoints = {'facilities': ['/facilities/v1'],
                          'packages': ['/packages/v1/active', '/packages/v1/inactive'],
                          'harvests': ['/harvests/v1/active', '/harvests/v1/inactive'],
                          'lab_results': ['/labtests/v1/results'],
                          'outgoing_transfers': ['/transfers/v1/outgoing'],
                          'deliveries': ['/transfers/v1/{id}/deliveries'],
                          'sales_receipts': ['/sales/v1/receipts/active'],
                          'sales_transactions': ['/sales/v1/receipts/{id}']}

        self.vendor_api_key = vendor_api_key
        self.user_api_key = user_api_key
        self.api = APICaller(self.vendor_api_key, self.user_api_key)
        self.init_facilities()

    def get_user_id(self):
        '''
        Return the fist seven (7) digits of the user API key. This can be used for creating unique database files,
        Elasticsearch indicies, etc. for each user/provider.

        Returns
        -------
        str
            First seven (7) characters of the user API key.
        '''
        return self.user_api_key[0:7]

    def get_facility_start_date(self, facility):
        '''
        Return the start date of the provided facility in ISO 8601 format (All praise the sanity of 8601). The start
        date is when the facility's state has blessed it as valid and legally allowed to operate. This can be used when
        obtaining records from "the beginning of time" from the persepective of that facility. For example, when
        initializing a database of all sales transactions, use the facility start date as the last modified start date.

        Many inconsistencies exist with the Metrc REST API. The first we'll note here -- start dates are provided as a
        calendar date. This is unacceptable. To provide them a helping hand, we append a time and offset string to make
        this useful for direct use in queries and for my own sanity.

        Parameters
        ----------
        facility : str
            The facility for which to fetch the start date.

        Returns
        -------
        str
        '''
        try:
            assert(facility in self.facilities)
        except AssertionError:
            print(f"Facility {facility} not available.")
            return None

        for f in self.facility_data:
            if f['License']['Number'] == facility:
                start_date = f['License']['StartDate']
                start_date += 'T00:00:00+00:00'
                break

        return start_date

    def _get_from_urls(self, urls):
        '''
        Take a list of urls and pass them to the APICaller, getting back a list of responses in dictionaries. To be
        precise, we get back a list of lists of dictionaries, i.e.:

          |--------- 24 hr period ---------|  |--------- 24 hr period ---------|  |- 24 hr period -|
        [ [ { package: 1 }, { package: 2 } ], [ { package: 3 }, { package: 4 } ], [ { package: 5 } ] ]

        The above example assumes we have made a request from the packages endpoint for packages last modified within
        three (3) 24 hour periods. Since we get the JSON data back converted to a Python dictionary object, and we must
        make a separate call for each 24 hour period, we get a list of lists of dictionaries.

        As many requests can be required, either for time-based queries or for ID-based queries such as when first
        initializing your database, this is done concurrently using AIOHTTP.

        Parameters
        ----------
        urls: list[str]
            URLs from which to make get requests.

        Returns
        -------
        list[list[dict]]
            The outer list contains all individual endpoint queries. The inner list contains all the entities returned
            an individual endpoint query. The dict is the dictionary representing the JSON object returned.
        '''
        response_json = self.api.get_from_url_list(urls)
        return response_json

    def get_24_hour_periods(self, start_date, end_date):
        try:
            # Verify the strings passed are ISO 8601 format and that the end date is greater than the start date.
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            assert((end_dt - start_dt).total_seconds() >= 0)
        except AssertionError:
            print("End date must be greater than start date.")
        except ValueError:
            print("One or more dates not in valid ISO format.")

        period_tuples = []

        while(1):
            # Calculate the difference in hours between the start and end date.
            difference = end_dt - start_dt
            difference = difference.total_seconds() / 3600

            if difference > 24:
                # Use the counter to create increments of < 24 hours. In this case, we subtract 1 millisecond to avoid
                # overlap when calculating subsequent 24 hour periods.
                end_date_counter = (start_dt + timedelta(days=1)) - timedelta(milliseconds=1)
                period_tuples.append((start_dt.isoformat(), end_date_counter.isoformat()))
                start_dt += timedelta(days=1)
            else:
                # If the original start and end represent a period of 24 hours or less, no modification is necessary.
                # This is also true when arriving at the end of the datetime iteration process above.
                period_tuples.append((start_dt.isoformat(), end_dt.isoformat()))
                break

        return period_tuples

    # Make a request for the users available facilities.
    def init_facilities(self):
        print('Initializing facility list...')
        ep = self.endpoints['facilities'][0]
        url = f"{API_BASE_URL}{ep}"
        self.facility_data = self.api.get_from_url_list([url])[0]

        self.facilities.clear()
        self.facilities = [facility['License']['Number'] for facility in self.facility_data]

        # List all dispensaries using the boolean property in the facility data, CanSellToPatients.
        self.dispensaries = [facility['License']['Number'] for facility in self.facility_data
                             if facility['FacilityType']['CanSellToPatients']]

        # List all manufacturing licenses using the boolean property in the facility data, CanInfuseProducts.
        self.mipps = [facility['License']['Number'] for facility in self.facility_data
                      if facility['FacilityType']['CanInfuseProducts']]

    # This method is a catch all for making queries. I know this is a clunky approach. This will change with more
    # experience and better knowledge of design priciples and best-practices.
    def get_data(self, endpoint, license_number, start_date, end_date, **kwargs):
        try:
            assert(license_number in self.facilities)
        except AssertionError:
            print('Invalid license: User must have access to facility.')

        if endpoint == 'sales_transactions':
            return self.get_sales_transactions(license_number=license_number,
                                               sales_date_start=start_date,
                                               sales_date_end=end_date,
                                               receipt_ids=kwargs.get('receipt_ids'),
                                               flatten=kwargs.get('flatten'))
        elif endpoint == 'packages':
            return self.get_packages(license_number=license_number,
                                     last_modified_start=start_date,
                                     last_modified_end=end_date,
                                     flatten=kwargs.get('flatten'))
        elif endpoint == 'harvests':
            return self.get_harvests(license_number=license_number,
                                     last_modified_start=start_date,
                                     last_modified_end=end_date)

    def _generate_urls(self, endpoint, license_number, last_modified_start, last_modified_end):
        date_ranges = self.get_24_hour_periods(last_modified_start, last_modified_end)
        urls = []

        for ep in self.endpoints[endpoint]:
            for period in date_ranges:
                query_dict = {'licenseNumber': license_number,
                              'lastModifiedStart': period[0],
                              'lastModifiedEnd': period[1]}
                query = urllib.parse.urlencode(query_dict)
                urls.append(f"{API_BASE_URL}{ep}?{query}")

        return urls

    # Return a list of packages as dictionaries.
    def get_harvests(self, license_number, last_modified_start, last_modified_end):
        endpoint = 'harvests'
        self._print_get_message(endpoint, license_number, last_modified_start, last_modified_end)

        urls = self._generate_urls(endpoint, license_number, last_modified_start, last_modified_end)

        response = self._get_from_urls(urls)
        harvests = [harvest for period in response if period for harvest in period]
        return harvests

    # Return a list of packages as dictionaries.
    def get_packages(self, license_number, last_modified_start, last_modified_end, flatten=True):
        endpoint = 'packages'
        self._print_get_message(endpoint, license_number, last_modified_start, last_modified_end)

        urls = self._generate_urls(endpoint, license_number, last_modified_start, last_modified_end)

        response = self._get_from_urls(urls)
        packages = [package for period in response if period for package in period]

        if flatten:
            print('Flattening packages...')
            flattened_packages = []

            for package in packages:
                item = package.pop('Item')
                new_item = {}

                for key, value in item.items():
                    key = 'Item' + key
                    new_item.update({key: value})

                package.update(new_item)
                flattened_packages.append(package)

            return flattened_packages
        else:
            return packages

    # Return a tuple containing a list of receipt IDs and list of receipts as dictionaries.
    def get_sales_receipts(self, license_number, sales_date_start, sales_date_end):
        endpoint = 'sales_receipts'
        self._print_get_message(endpoint, license_number, sales_date_start, sales_date_end)

        date_ranges = self.get_24_hour_periods(sales_date_start, sales_date_end)
        urls = []

        for ep in self.endpoints['sales_receipts']:
            for period in date_ranges:
                query_dict = {'licenseNumber': license_number, 'salesDateStart': period[0], 'salesDateEnd': period[1]}
                query = urllib.parse.urlencode(query_dict)
                urls.append(f"{API_BASE_URL}{ep}?{query}")

        response = self._get_from_urls(urls)

        # We get a list of lists from the async url request -- a list of receipts for each period requested, all
        # within the top-level list. Here we flatten this and extract a list of receipt IDs for easy integration with
        # other endpoints (transactions).
        receipts = [receipt for period in response if period for receipt in period]
        ids = [receipt['Id'] for receipt in receipts if isinstance(receipt, dict)]

        return (ids, receipts)

    # Return a list of transaction information using a list of receipt IDs for lookup. If flatten is true, return
    # a list of elements containing transaction information per individual package. Multiple elements
    # (transactions) can share a receipt ID. If flatten is false, return a list of receipts containing a nested list
    # of individual packages involved. First, if no IDs are provided, get them automatically for the date range
    # provided. This requires calling get_sales_reciepts().
    def get_sales_transactions(self, license_number, sales_date_start=None, sales_date_end=None, receipt_ids=None,
                               flatten=True):
        if not receipt_ids:
            try:
                assert(sales_date_start)
                assert(sales_date_end)
            except AssertionError:
                print('No receipt IDs provided: start and end date required.')

            print('No IDs provided when getting transactions...')
            receipt_ids = self.get_sales_receipts(license_number, sales_date_start, sales_date_end)[0]
            if not receipt_ids:
                print("No receipts in time period specified. Skipping transaction lookup.")
                return []

        print(f'Getting {len(receipt_ids)} sales transactions...')
        urls = []

        for ep in self.endpoints['sales_transactions']:
            for i in receipt_ids:
                query_dict = {'licenseNumber': license_number}
                query = urllib.parse.urlencode(query_dict)
                ep_with_id = ep.replace('{id}', str(i))
                urls.append(f"{API_BASE_URL}{ep_with_id}?{query}")

        response = self._get_from_urls(urls)

        # Flattening is useful for use in flat files, single database tables, and Elasticsearch indicies. Otherwise, the
        # returned dictionary includes a sub-list of transactions.
        if flatten:
            print('Flattening transactions...')
            doc_list = []

            # Extract relevant information that would otherwise not be included when isolating an individual
            # transaction and append it.
            for receipt in response:
                receipt_info = {
                    'ReceiptNumber': receipt['ReceiptNumber'],
                    'SalesDateTime': receipt['SalesDateTime'],
                    'SalesCustomerType': receipt['SalesCustomerType'],
                    'PatientLicenseNumber': receipt['PatientLicenseNumber'],
                    'IsFinal': receipt['IsFinal'],
                    'ArchivedDate': receipt['ArchivedDate'],
                    'RecordedDateTime': receipt['RecordedDateTime'],
                    'RecordedByUserName': receipt['RecordedByUserName'],
                    'ReceiptLastModified': receipt['LastModified']
                }

                for transaction in receipt['Transactions']:
                    transaction.update(receipt_info)
                    doc_list.append(transaction)

            return doc_list
        else:
            return response

    def _print_get_message(self, endpoint, license_number, start_date, end_date):
        print(f'Getting {endpoint} for {license_number} between {start_date} and {end_date}')


if __name__ == '__main__':
    import os

    vendor_api_key = os.environ['METRC_VENDOR_API_KEY']
    user_api_key = os.environ['METRC_USER_API_KEY']
    m = Metrc(vendor_api_key, user_api_key)
