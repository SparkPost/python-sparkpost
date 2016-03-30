import json

from .base import Resource


class Templates(Resource):
    """
    Templates class used to create, update, delete, list and get templates. For
    detailed request and response formats, see the `Templates API documentation
    <https://www.sparkpost.com/api#/reference/templates>`_.
    """

    key = 'templates'

    def _translate_keys(self, **kwargs):
        model = {
            'content': {},
            'options': {}
        }

        if 'id' in kwargs:
            model['id'] = kwargs.get('id')
        model['name'] = kwargs.get('name')
        model['description'] = kwargs.get('description')
        model['published'] = kwargs.get('published')

        model['options']['open_tracking'] = kwargs.get('track_opens')
        model['options']['click_tracking'] = kwargs.get('track_clicks')
        model['options']['transactional'] = kwargs.get('is_transactional')

        model['content']['html'] = kwargs.get('html')
        model['content']['text'] = kwargs.get('text')
        model['content']['subject'] = kwargs.get('subject')
        model['content']['from'] = kwargs.get('from_email')
        model['content']['reply_to'] = kwargs.get('reply_to')
        model['content']['headers'] = kwargs.get('custom_headers')

        return model

    def create(self, **kwargs):
        """
        Create a template based on the supplied parameters

        :param str id: ID used to reference the template
        :param str name: Editable display name
        :param str description: Detailed description of the template
        :param bool published: Defaults to False. Whether the template is a
            published or draft version

        :param bool track_opens: Defaults to transmission level setting.
            Used to track opens of transmission
        :param bool track_clicks: Defaults to transmission level setting.
            Used to track clicks of transmission
        :param bool is_transactional: Defaults to transmission level setting.
            Distinguishes between transactional and non-transactional messages
            for unsubscribe and suppression purposes

        :param str html: HTML part of template
        :param str text: Text part of template
        :param str subject: Subject of template
        :param str from_email: Friendly from of template, domain must be a
            verified sending domain to your account or template create
            will fail
        :param str reply_to: Reply to of template
        :param dict custom_headers: Used to set any headers associated with
            template

        :returns: a ``dict`` with the ID
        :raises: :exc:`SparkPostAPIException` if template uses an unverified
            sending domain or there's a syntax error in the content
        """
        payload = self._translate_keys(**kwargs)
        results = self.request('POST', self.uri, data=json.dumps(payload))
        return results

    def update(self, template_id, **kwargs):
        """
        Update a template by ID based on the supplied parameters

        :param str template_id: ID of the template you want to retrieve

        :param str name: Editable display name
        :param str description: Detailed description of the template
        :param bool published: Defaults to False. Whether the template is a
            published or draft version

        :param bool track_opens: Defaults to transmission level setting.
            Used to track opens of transmission
        :param bool track_clicks: Defaults to transmission level setting.
            Used to track clicks of transmission
        :param bool is_transactional: Defaults to transmission level setting.
            Distinguishes between transactional and non-transactional messages
            for unsubscribe and suppression purposes

        :param str html: HTML part of template
        :param str text: Text part of template
        :param str subject: Subject of template
        :param str from_email: Friendly from of template, domain must be a
            verified sending domain to your account or template create
            will fail
        :param str reply_to: Reply to of template
        :param dict custom_headers: Used to set any headers associated with
            template

        :returns: TODO
        :raises: :exc:`SparkPostAPIException` if template is not found
        """
        uri = "%s/%s" % (self.uri, template_id)
        payload = self._translate_keys(**kwargs)
        results = self.request('PUT', uri, data=json.dumps(payload))
        return results

    def delete(self, template_id):
        """
        Delete a template by ID

        :param str template_id: ID of the template you want to delete

        :returns: TODO
        :raises: :exc:`SparkPostAPIException` if template is not found or if
            template is in use
        """
        uri = "%s/%s" % (self.uri, template_id)
        results = self.request('DELETE', uri)
        return results

    def get(self, template_id, draft=None):
        """
        Get a template by ID

        :param str template_id: ID of the template you want to retrieve
        :param bool draft: Defaults to None. If True, returns the most
            recent draft template. If False, returns the most recent published
            template. If None, returns the most recent template version
            regardless of draft or published.

        :returns: the requested template if found
        :raises: :exc:`SparkPostAPIException` if template is not found
        """
        uri = "%s/%s" % (self.uri, template_id)
        params = {}
        if draft is not None:
            params['draft'] = str(draft).lower()
        results = self.request('GET', uri, params=params)
        return results

    def list(self):
        """
        Get a list of your templates

        :returns: list of templates
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        results = self.request('GET', self.uri)
        return results

    def preview(self, template_id, substitution_data, draft=None):
        """
        Get a preivew of your template by ID with the
        provided substitution_data

        :param str template_id: ID of the template you want to retrieve
        :param dict substitution_data: data to be substituted in the
            template content
        :param bool draft: Defaults to None. If True, previews the most
            recent draft template. If False, previews the most recent published
            template. If None, previews the most recent template version
            regardless of draft or published.

        :returns: the requested template if found with content expanded using
            substitution data provided
        :raises: :exc:`SparkPostAPIException` if API call fails
        """
        uri = "%s/%s/preview" % (self.uri, template_id)
        params = {}
        if draft is not None:
            params['draft'] = str(draft).lower()
        data = json.dumps({'substitution_data': substitution_data})
        results = self.request('POST',
                               uri,
                               params=params,
                               data=data)
        return results
