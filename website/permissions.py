from flask_login import current_user

role_permissions = {
    "Student": ["manage_instance"],

    "Professor": ["manage_instance",
                  "table_users",
                  "groups_for_current_professor"],

    "Admin": ["manage_instance",
              "table_users",
              "table_groups",
              "change_role",
              "groups_for_current_professor"]
}


def user_has_permission(permission):
    return permission in role_permissions[current_user.role]
