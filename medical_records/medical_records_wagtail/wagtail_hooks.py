from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_patients_menu_item():
    return MenuItem(
        "Patients",
        "/cms/pages/",
        icon_name="user",
        order=200,
    )
