class CoreAttrs:

    def list_display(self):
        return ["id"]
    
    def list_display_links(self):
        return []
    
    def list_editable(self):
        return []
    def list_filter(self):
        return ["id"]
    def list_max_show_all(self):
        return []
    def list_per_page(self):
        return []
    def list_select_related(self):
        return []
    def is_registered(self):
        return True
    def has_action(self):
        return False
    
    def has_dropdown_action(self):
        return False
    
    def form(self):
        try:
            return None
        except:
            pass
    
    def exclude(self):
        return []
    def action(self):
        return []
    def dropdown_action(self):
        return []