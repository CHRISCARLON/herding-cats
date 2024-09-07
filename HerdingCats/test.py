from typing import List, Dict, Any
from pprint import pprint

def extract_package_show_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extracts specific fields from the package data and creates a list of dictionaries,
    one for each resource, containing the specified fields.

    Args:
    data (Dict[str, Any]): The input package data dictionary.

    Returns:
    List[Dict[str, Any]]: A list of dictionaries, each containing the specified fields for a resource.
    """
    base_fields = {
        'name': data.get('name'),
        'notes_markdown': data.get('notes_markdown')
    }

    resource_fields = ['url', 'name', 'format', 'created', 'last_modified']

    result = []
    for resource in data.get('resources', []):
        resource_data = base_fields.copy()
        for field in resource_fields:
            resource_data[f'resource_{field}'] = resource.get(field)
        result.append(resource_data)

    return result

# Example usage...
if __name__ == "__main__":

    data = {'author': 'VRU Contracts & Commissioning Team',
    'author_email': 'VRUCommissioning@london.gov.uk',
    'creator_user_id': None,
    'email_notify_author': False,
    'email_notify_maintainer': False,
    'groups': [{'description': '',
                'display_name': 'Transparency',
                'id': '1d5852ed-0315-4472-927a-3d1bdaa4f630',
                'image_display_url': 'https://airdrive-images.s3-eu-west-1.amazonaws.com/london/img/topic/2018-11-01T18%3A46%3A24.62/transparency.png',
                'name': 'transparency',
                'title': 'Transparency'}],
    'id': 'e307e8f6-02b8-4e13-95e4-1f5b7499e5f7',
    'isopen': None,
    'license_id': 'ogl-v3',
    'license_text': None,
    'license_title': 'UK Open Government Licence (OGL v3)',
    'maintainer': 'Group Collaboration – Grants Project Team',
    'maintainer_email': 'Datastore@london.gov.uk',
    'metadata_created': '2023-06-01T10:25:12.848Z',
    'metadata_modified': '2024-09-04T13:44:38.691Z',
    'name': 'violence-reduction-unit',
    'notes': '<p>\n'
            '<span style="color: black;">The Royal Docks Team is a '
            'multi-disciplinary team that brings together officers from across '
            'the Greater London Authority, the London Borough of Newham and the '
            'London Economic Action Partnership.&nbsp;Home to London’s only '
            'Enterprise Zone, the Royal Docks is one of the most significant '
            'regeneration projects in the UK. The team was established in 2017 '
            'to help deliver the cohesive transformation of the Royal Docks into '
            'a vibrant, mixed-use destination with culture and community at its '
            'heart </span>at Wormwood Scrubs.</p>',
    'notes_markdown': '\n'
                    'The Royal Docks Team is a multi-disciplinary team that '
                    'brings together officers from across the Greater London '
                    'Authority, the London Borough of Newham and the London '
                    'Economic Action Partnership.&nbsp;Home to London’s only '
                    'Enterprise Zone, the Royal Docks is one of the most '
                    'significant regeneration projects in the UK. The team was '
                    'established in 2017 to help deliver the cohesive '
                    'transformation of the Royal Docks into a vibrant, '
                    'mixed-use destination with culture and community at its '
                    'heart at Wormwood Scrubs.',
    'num_resources': 4,
    'num_tags': 0,
    'organization': {'approval_status': 'approved',
                    'created': '2023-06-01T10:24:49.126Z',
                    'description': '',
                    'id': '8d12196f-977d-49db-942a-01778010c530',
                    'image_url': 'https://airdrive-images.s3-eu-west-1.amazonaws.com/london/img/publisher/2023-06-01T10%3A24%3A46/_new.png',
                    'is_organization': True,
                    'name': 'violence-reduction-unit',
                    'revision_id': None,
                    'state': 'active',
                    'title': 'Violence Reduction Unit  ',
                    'type': 'organization'},
    'owner_org': '8d12196f-977d-49db-942a-01778010c530',
    'private': False,
    'relationships_as_object': [],
    'relationships_as_subject': [],
    'resources': [{'cache_last_updated': None,
                    'cache_url': None,
                    'created': '2024-01-23T10:53:38.415Z',
                    'description': None,
                    'format': 'spreadsheet',
                    'hash': '99a304b95c2855fb128d44172ec1599e',
                    'id': '50d2c9c5-07b9-4cc8-bcfe-ef01845db8df',
                    'last_modified': None,
                    'mimetype': None,
                    'mimetype_inner': None,
                    'name': 'VRU Q2-Q3 2022-23 Dataset',
                    'package_id': 'e307e8f6-02b8-4e13-95e4-1f5b7499e5f7',
                    'position': 3,
                    'resource_type': None,
                    'revision_id': None,
                    'size': 31578,
                    'state': 'active',
                    'url': 'https://data.london.gov.uk/download/violence-reduction-unit/50d2c9c5-07b9-4cc8-bcfe-ef01845db8df/Q2-Q3%25202022-23%2520Dataset%2520for%2520VRU%2520.xlsx',
                    'url_type': None,
                    'webstore_last_updated': None,
                    'webstore_url': None},
                {'cache_last_updated': None,
                    'cache_url': None,
                    'created': '2024-01-23T10:54:12.357Z',
                    'description': None,
                    'format': 'spreadsheet',
                    'hash': '972adee1759f048ccb7fb07d753cbfc9',
                    'id': '1ef840d0-2c02-499c-ae40-382005b2a0c7',
                    'last_modified': None,
                    'mimetype': None,
                    'mimetype_inner': None,
                    'name': 'VRU Q1 2023-24 Dataset',
                    'package_id': 'e307e8f6-02b8-4e13-95e4-1f5b7499e5f7',
                    'position': 2,
                    'resource_type': None,
                    'revision_id': None,
                    'size': 22989,
                    'state': 'active',
                    'url': 'https://data.london.gov.uk/download/violence-reduction-unit/1ef840d0-2c02-499c-ae40-382005b2a0c7/VRU%2520Dataset%2520Q1%2520April-Nov%25202023.xlsx',
                    'url_type': None,
                    'webstore_last_updated': None,
                    'webstore_url': None},
                {'cache_last_updated': None,
                    'cache_url': None,
                    'created': '2024-05-22T12:19:32.262Z',
                    'description': None,
                    'format': 'spreadsheet',
                    'hash': '20da429e77848b55622188da08674006',
                    'id': '92b2bfec-3ffe-448f-9394-577e9f8cbd81',
                    'last_modified': None,
                    'mimetype': None,
                    'mimetype_inner': None,
                    'name': 'VRU Q4 2023-24 Dataset',
                    'package_id': 'e307e8f6-02b8-4e13-95e4-1f5b7499e5f7',
                    'position': 1,
                    'resource_type': None,
                    'revision_id': None,
                    'size': 18758,
                    'state': 'active',
                    'url': 'https://data.london.gov.uk/download/violence-reduction-unit/92b2bfec-3ffe-448f-9394-577e9f8cbd81/VRU%2520Q4%2520Upload.xlsx',
                    'url_type': None,
                    'webstore_last_updated': None,
                    'webstore_url': None},
                {'cache_last_updated': None,
                    'cache_url': None,
                    'created': '2024-09-04T10:29:05.459Z',
                    'description': None,
                    'format': 'spreadsheet',
                    'hash': 'd8a3515e9107fdefdb77f1afde12778c',
                    'id': '1f91627d-d3fb-4b64-b5f7-1fdfd1069ba7',
                    'last_modified': None,
                    'mimetype': None,
                    'mimetype_inner': None,
                    'name': 'VRU Q1 2024-25 Dataset ',
                    'package_id': 'e307e8f6-02b8-4e13-95e4-1f5b7499e5f7',
                    'position': 0,
                    'resource_type': None,
                    'revision_id': None,
                    'size': 10614,
                    'state': 'active',
                    'url': 'https://data.london.gov.uk/download/violence-reduction-unit/1f91627d-d3fb-4b64-b5f7-1fdfd1069ba7/Q1%2520VRU.xlsx',
                    'url_type': None,
                    'webstore_last_updated': None,
                    'webstore_url': None}],
    'revision_id': None,
    'state': 'active',
    'tags': [],
    'title': 'Violence Reduction Unit',
    'type': 'dataset',
    'url': None,
    'version': None}

    extracted_data = extract_package_show_data(data)
    pprint(extracted_data)
