"""
This file was generated with the help of Gemini.
"""
from admin_tools.dashboard import modules, Dashboard

class MyDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            title='Applications',
            models=('leads.models.Lead',),
        ))
