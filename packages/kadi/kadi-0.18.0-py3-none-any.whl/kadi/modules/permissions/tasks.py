# Copyright 2021 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from .core import apply_role_rule
from kadi.ext.celery import celery
from kadi.ext.db import db
from kadi.lib.tasks.core import launch_task
from kadi.modules.accounts.models import User
from kadi.modules.permissions.models import RoleRule


@celery.task(name="kadi.permissions.apply_role_rules")
def _apply_role_rules_task(user_id, **kwargs):
    user = None

    if user_id is not None:
        user = User.query.get(user_id)

    # Always iterate through the rules in a consistent order (their creation date), in
    # case there are multiple rules for the same resource applying different roles to
    # the same user.
    for role_rule in RoleRule.query.order_by(RoleRule.created_at):
        apply_role_rule(role_rule, user=user)
        db.session.commit()


def start_apply_role_rules_task(user=None):
    """Apply all existing role rules in a background task.

    :param user: (optional) A specific user to apply the role rules to. If not given,
        all users are considered.
    :return: ``True`` if the task was started successfully, ``False`` otherwise.
    """
    user_id = None

    if user is not None:
        user_id = user.id

    return launch_task("kadi.permissions.apply_role_rules", args=(user_id,))
