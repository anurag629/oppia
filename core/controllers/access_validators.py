# Copyright 2021 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Controllers for validating access."""

from __future__ import annotations

from core import feconf
from core.constants import constants
from core.controllers import acl_decorators
from core.controllers import base
from core.domain import blog_services
from core.domain import classroom_services
from core.domain import config_domain
from core.domain import learner_group_services
from core.domain import user_services

from typing import Dict # isort: skip


# TODO(#13605): Refactor access validation handlers to follow a single handler
# pattern.

class ClassroomAccessValidationHandler(base.BaseHandler):
    """Validates whether request made to /learn route.
    """

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON

    URL_PATH_ARGS_SCHEMAS: Dict[str, str] = {}

    HANDLER_ARGS_SCHEMAS = {
        'GET': {
            'classroom_url_fragment': {
                'schema': {
                    'type': 'basestring'
                }
            }
        }
    }

    @acl_decorators.open_access
    def get(self) -> None:
        # Please use type casting here instead of type ignore[union-attr] once
        # this attribute `normalized_request` has been type annotated in the
        # parent class BaseHandler.
        classroom_url_fragment = self.normalized_request.get( # type: ignore[union-attr]
            'classroom_url_fragment')
        classroom = classroom_services.get_classroom_by_url_fragment( # type: ignore[no-untyped-call]
            classroom_url_fragment)

        if not classroom:
            raise self.PageNotFoundException


class ManageOwnAccountValidationHandler(base.BaseHandler):
    """Validates access to preferences page.
    """

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON

    URL_PATH_ARGS_SCHEMAS: Dict[str, str] = {}

    HANDLER_ARGS_SCHEMAS: Dict[str, Dict[str, str]] = {
        'GET': {}
    }

    @acl_decorators.can_manage_own_account
    def get(self) -> None:
        pass


class ProfileExistsValidationHandler(base.BaseHandler):
    """The world-viewable profile page."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON

    URL_PATH_ARGS_SCHEMAS = {
        'username': {
            'schema': {
                'type': 'basestring'
            }
        }
    }

    HANDLER_ARGS_SCHEMAS: Dict[str, Dict[str, str]] = {
        'GET': {}
    }

    @acl_decorators.open_access
    def get(self, username: str) -> None:
        """Validates access to profile page."""

        user_settings = user_services.get_user_settings_from_username( # type: ignore[no-untyped-call]
            username)

        if not user_settings:
            raise self.PageNotFoundException


class ReleaseCoordinatorAccessValidationHandler(base.BaseHandler):
    """Validates access to release coordinator page."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON

    URL_PATH_ARGS_SCHEMAS: Dict[str, str] = {}

    HANDLER_ARGS_SCHEMAS: Dict[str, Dict[str, str]] = {
        'GET': {}
    }

    @acl_decorators.can_access_release_coordinator_page
    def get(self) -> None:
        """Handles GET requests."""
        pass


class ViewLearnerGroupPageAccessValidationHandler(base.BaseHandler):
    """Validates access to view learner group page."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON

    URL_PATH_ARGS_SCHEMAS = {
        'learner_group_id': {
            'schema': {
                'type': 'basestring',
                'validators': [{
                    'id': 'is_regex_matched',
                    'regex_pattern': constants.LEARNER_GROUP_ID_REGEX
                }]
            }
        }
    }

    HANDLER_ARGS_SCHEMAS: Dict[str, Dict[str, str]] = {
        'GET': {}
    }

    @acl_decorators.can_access_learner_groups
    def get(self, learner_group_id: str) -> None:
        """Handles GET requests."""
        if not config_domain.LEARNER_GROUPS_ARE_ENABLED.value:
            raise self.PageNotFoundException

        is_valid_request = learner_group_services.is_user_learner(
            self.user_id, learner_group_id)

        if not is_valid_request:
            raise self.PageNotFoundException


class BlogHomePageAccessValidationHandler(base.BaseHandler):
    """Validates access to blog home page."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON

    URL_PATH_ARGS_SCHEMAS: Dict[str, str] = {}

    HANDLER_ARGS_SCHEMAS: Dict[str, Dict[str, str]] = {
        'GET': {}
    }

    @acl_decorators.can_access_blog_dashboard
    def get(self) -> None:
        """Validates access to blog home page."""
        pass


class BlogPostPageAccessValidationHandler(base.BaseHandler):
    """Validates whether request made to correct blog post route."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON

    URL_PATH_ARGS_SCHEMAS: Dict[str, str] = {}

    HANDLER_ARGS_SCHEMAS = {
        'GET': {
            'blog_post_url_fragment': {
                'schema': {
                    'type': 'basestring'
                }
            }
        }
    }

    @acl_decorators.can_access_blog_dashboard
    def get(self) -> None:
        # Please use type casting here instead of type ignore[union-attr] once
        # this attribute `normalized_request` has been type annotated in the
        # parent class BaseHandler.
        blog_post_url_fragment = self.normalized_request.get( # type: ignore[union-attr]
            'blog_post_url_fragment')
        blog_post = blog_services.get_blog_post_by_url_fragment( # type: ignore[no-untyped-call]
            blog_post_url_fragment)

        if not blog_post:
            raise self.PageNotFoundException
